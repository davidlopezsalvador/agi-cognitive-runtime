"""Re-scores debugbench_8heuristics_results.json using differential
execution testing against oracle_code, instead of analyze_medium.py's
exact whitespace-stripped string match.

Why: exact string match fails any functionally-correct fix that isn't
byte-identical to the oracle (different variable names, reordered
branches, extra whitespace it didn't strip, a helper variable). That's
not a hypothetical concern — DEBUGBENCH_HEURISTICS_RESULTS.md and
LITERARY_EXPERIMENT_FINAL.md are in tension partly because "correct" was
defined so narrowly in one of them. This script asks a better question:
does the candidate function produce the SAME OUTPUT as the oracle across
many random inputs? That's standard differential testing, and it accepts
any functionally-equivalent fix, not just a textually-identical one.

Method, per problem:
  1. Extract the ```python code block from response_lit / response_no_lit
     (same JSON parts-walking as analyze_medium.py).
  2. exec() the oracle code and the candidate code in separate namespaces.
  3. Introspect the Solution method's type hints to generate N random
     inputs (falls back to a fixed small set of structured cases — empty,
     single-element, negative — alongside the random ones, since edge
     cases are where LeetCode-style bugs usually live).
  4. Call both with the same inputs; candidate is "correct" only if it
     matches the oracle's output on every trial.
  5. If the candidate code doesn't parse/exec, or the signature isn't one
     of the supported simple types, falls back to AST-normalized
     comparison (structure-equivalent ignoring variable names/whitespace/
     comments) — strictly more permissive than raw string match, strictly
     less rigorous than execution. Reports which method was used for each
     problem so the two rigor levels are never silently mixed.

This runs candidate code with exec() and calls it with generated inputs.
It's running LeetCode-style pure functions from a controlled dataset in
this sandbox, not arbitrary untrusted code from the internet — reasonable
here, would want stronger isolation (subprocess + resource limits) before
running on anything less controlled.
"""

from __future__ import annotations

import ast
import json
import random
import sys
import typing

RESULTS_FILE = "debugbench_8heuristics_results.json"


def extract_code(response_str: str) -> str | None:
    try:
        response = json.loads(response_str)
        for part in response.get("parts", []):
            if part.get("type") == "text":
                text = part.get("text", "")
                if "```python" in text:
                    return text.split("```python")[1].split("```")[0].strip()
        return None
    except Exception:
        return None


def ast_normalized(code: str) -> str | None:
    """Structure-equivalent comparison: parses the code, strips docstrings/
    comments (already gone post-parse) and renames all Name/arg nodes to
    positional placeholders in order of first appearance, so variable
    renaming doesn't cause a mismatch the way raw string comparison does."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return None

    counter = {"n": 0}
    rename: dict[str, str] = {}

    def norm_name(name: str) -> str:
        if name not in rename:
            rename[name] = f"_v{counter['n']}"
            counter["n"] += 1
        return rename[name]

    class Renamer(ast.NodeTransformer):
        def visit_Name(self, node):
            node.id = norm_name(node.id)
            return node

        def visit_arg(self, node):
            node.arg = norm_name(node.arg)
            return node

        def visit_FunctionDef(self, node):
            node.name = norm_name(node.name)
            self.generic_visit(node)
            return node

        def visit_ClassDef(self, node):
            node.name = norm_name(node.name)
            self.generic_visit(node)
            return node

    renamed = Renamer().visit(tree)
    return ast.dump(renamed, annotate_fields=False)


def _random_value(hint) -> object:
    origin = typing.get_origin(hint)
    if hint in (int, "int"):
        return random.randint(-50, 50)
    if hint in (float, "float"):
        return round(random.uniform(-50, 50), 2)
    if hint in (bool, "bool"):
        return random.choice([True, False])
    if hint in (str, "str"):
        return "".join(random.choice("abcxyz") for _ in range(random.randint(0, 6)))
    if origin in (list, typing.List):
        (inner,) = typing.get_args(hint) or (int,)
        return [_random_value(inner) for _ in range(random.randint(0, 8))]
    return None  # unsupported type -> caller falls back to AST comparison


STRUCTURED_INT_LIST_CASES = [[], [0], [1], [-1, -1], list(range(-5, 6))]


def _find_solution_method(namespace: dict):
    sol_cls = namespace.get("Solution")
    if sol_cls is None:
        return None, None
    for name, member in vars(sol_cls).items():
        if callable(member) and not name.startswith("_"):
            return sol_cls, name
    return None, None


def differential_test(oracle_code: str, candidate_code: str, trials: int = 25) -> str:
    """Returns 'pass', 'fail', or 'unsupported' (falls back to AST check)."""
    base_ns = {name: getattr(typing, name) for name in dir(typing) if not name.startswith("_")}
    oracle_ns: dict = dict(base_ns)
    cand_ns: dict = dict(base_ns)
    try:
        exec(compile(oracle_code, "<oracle>", "exec"), oracle_ns)
        exec(compile(candidate_code, "<candidate>", "exec"), cand_ns)
    except Exception:
        return "unsupported"

    oracle_cls, method_name = _find_solution_method(oracle_ns)
    cand_cls, _ = _find_solution_method(cand_ns)
    if oracle_cls is None or cand_cls is None:
        return "unsupported"

    try:
        hints = typing.get_type_hints(getattr(oracle_cls, method_name), globalns=base_ns)
    except Exception:
        return "unsupported"
    hints.pop("return", None)
    if not hints or any(_random_value(h) is None and h not in (int, float, bool, str) for h in hints.values()):
        # At least one unsupported param type — don't silently under-test.
        for h in hints.values():
            if _random_value(h) is None:
                return "unsupported"

    param_names = list(hints.keys())
    try:
        oracle_inst, cand_inst = oracle_cls(), cand_cls()
        oracle_fn, cand_fn = getattr(oracle_inst, method_name), getattr(cand_inst, method_name)
    except Exception:
        return "unsupported"

    single_int_list_param = len(param_names) == 1 and typing.get_origin(hints[param_names[0]]) in (list, typing.List)

    def run_case(args: list) -> tuple:
        try:
            o = oracle_fn(*args)
        except Exception as e:
            o = ("__EXC__", type(e).__name__)
        try:
            c = cand_fn(*args)
        except Exception as e:
            c = ("__EXC__", type(e).__name__)
        return o, c

    cases: list[list] = []
    if single_int_list_param:
        cases.extend([case] for case in STRUCTURED_INT_LIST_CASES)
    for _ in range(trials):
        cases.append([_random_value(hints[p]) for p in param_names])

    for args in cases:
        o, c = run_case(args)
        if o != c:
            return "fail"
    return "pass"


def score_condition(entries: list[dict], key: str) -> dict:
    exact_match = 0
    exec_pass = 0
    exec_unsupported = 0
    ast_match = 0
    per_problem = []

    for e in entries:
        oracle = e["oracle_code"]
        candidate = extract_code(e[key])
        if candidate is None:
            per_problem.append((e["slug"], "no_code_extracted"))
            continue

        oracle_norm = oracle.strip().replace("\n", "").replace(" ", "").replace("\t", "")
        cand_norm = candidate.strip().replace("\n", "").replace(" ", "").replace("\t", "")
        exact = oracle_norm == cand_norm
        if exact:
            exact_match += 1

        exec_result = differential_test(oracle, candidate)
        if exec_result == "pass":
            exec_pass += 1
            per_problem.append((e["slug"], "exec_pass"))
        elif exec_result == "fail":
            per_problem.append((e["slug"], "exec_fail"))
        else:
            exec_unsupported += 1
            ast_ok = ast_normalized(oracle) == ast_normalized(candidate)
            if ast_ok:
                ast_match += 1
            per_problem.append((e["slug"], "ast_pass" if ast_ok else "ast_fail (unsupported for exec)"))

    n = len(entries)
    return {
        "n": n,
        "exact_match": exact_match,
        "exec_pass": exec_pass,
        "exec_unsupported": exec_unsupported,
        "ast_match_of_unsupported": ast_match,
        "per_problem": per_problem,
    }


def main(path: str = RESULTS_FILE) -> None:
    with open(path, encoding="latin-1") as f:
        entries = json.load(f)

    for key, label in [("response_no_lit", "NO LITERARY"), ("response_lit", "WITH LITERARY (8 heuristics)")]:
        print(f"=== {label} ===")
        result = score_condition(entries, key)
        n = result["n"]
        print(f"  Exact string match (original method):  {result['exact_match']}/{n} ({result['exact_match']/n*100:.0f}%)")
        print(f"  Execution-based pass (this script):    {result['exec_pass']}/{n} ({result['exec_pass']/n*100:.0f}%)")
        print(f"  Execution unsupported (fell back to AST): {result['exec_unsupported']}/{n}")
        if result["exec_unsupported"]:
            print(f"    of those, AST-structure-equivalent to oracle: {result['ast_match_of_unsupported']}/{result['exec_unsupported']}")
        for slug, verdict in result["per_problem"]:
            print(f"    {slug:<55} {verdict}")
        print()


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else RESULTS_FILE)
