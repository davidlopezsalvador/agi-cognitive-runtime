# Architectural audit — 2026-09-02

Findings from reading `src/agi_runtime/runtime.py` end to end against the
subsystems it instantiates, plus the fixes applied. Tests for each fix are
in `tests/test_audit_fixes.py`.

## Fixed in this pass

1. **`classify()` precedence bug.** Depth selection was a fixed
   `if/elif` chain (long_horizon → adapt → experiment → investigate →
   plan), so a single incidental adapt-word match always beat any number
   of planning-word matches. Now the depth with the highest keyword count
   wins; ties fall back to the old severity order.
   Known limitation left as-is: `L1_REASON` is still unreachable, because
   `total_signal > 0` guarantees at least one of the five counters is
   `> 0`. Making it reachable needs its own "reasoning_words" signal —
   a real design decision, not something to guess at here.

2. **Duplicate, diverging episodic-memory scoring.**
   `Memory.find_similar_episodes()` and `EpisodicRetriever.retrieve()`
   were two independently-tuned implementations of the same job. Within a
   single `run()` call, both were invoked with different results.
   `find_similar_episodes()` now delegates to `EpisodicRetriever` (single
   scorer). `ContextCompiler.compile()` takes an optional
   `retrieved_episodes` param so `run()` retrieves once and reuses it,
   instead of scoring the whole episode store twice per task.

3. **`generate_hypotheses()` was string templating, not reasoning.**
   `Hypothesis(statement=f"Hypothesis from: {obs}")` regardless of content.
   Now calls the configured `model_provider` to produce a real, specific
   hypothesis per observation; falls back to the same template when no
   provider is configured (documented, not hidden).

4. **`VerificationEngine.verify_claim()` didn't verify anything.**
   `is_verified` and `confidence` never left their Pydantic defaults;
   `challenge()` returned the same static 9 questions for every claim.
   Both now call the provider (when configured) to actually assess the
   specific claim/evidence and generate claim-specific challenge
   questions. No-provider behaviour is unchanged and documented as a
   fallback, not real verification.

5. **Metacognition was inert.** `MetacognitiveState` was constructed with
   defaults and never updated or read anywhere in `run()` —
   `should_proceed()` / `should_ask_user()` were never called. Verification
   results now update `current_confidence`, `failure_risk`,
   `known_unknowns`, `uncertainty_sources`, `verification_status`, and
   `should_ask_user()` now actually flips `RuntimeResult.success` to
   `False` instead of the method always returning `success=True`.

6. **`CognitiveBudget` was aspirational.** `max_steps` was defined but
   `_step_count` was never incremented; `max_tool_calls` was defined but
   `ToolUseLoop` was constructed with its own hardcoded default of 10.
   `_step_count` now increments at each phase boundary and `run()` stops
   early with `success=False` if the budget is exhausted;
   `ToolUseLoop.max_iterations` is now wired from `budget.max_tool_calls`.

## Explicitly NOT wired in this pass

`TransferEngine`, `AgentOrchestrator`, and `AdaptivePlanner` are
constructed in `CognitiveRuntime.__init__` but no code path in `run()`
calls them — this was true before this audit and is still true now.
Wiring them meaningfully requires product decisions this audit shouldn't
guess at: when does a task warrant multi-agent orchestration vs. a single
pass? What counts as a `ReplanTrigger` in practice? Faking a call to
these just to make the architecture diagram true would be worse than
leaving them honestly unwired.

`plan_task()` still builds a `Plan` with steps (e.g. "Generate
hypotheses", "Design experiments", "Verify results") that `run()` does
not walk step-by-step — `run()` executes a fixed sequence of phases and
records the plan for the trace/context, it doesn't interpret it. Turning
the plan into something that's actually executed step-by-step (with
per-step tool use, verification, and replanning on failure) is a bigger
redesign than this pass, and again needs a decision on what a "step
executor" protocol looks like.

## GLM's independent DebugBench results — rescored (this session)

A separate GLM/OpenCode session (David's usual two-agent workflow) ran
its own experiments against `ling-3.0-flash-fin-free` and committed
several results docs (`DEBUGBENCH_HEURISTICS_RESULTS.md`,
`DEBUGBENCH_EXCERPT_RESULTS.md`, `DEBUGBENCH_FULL_BOOK_RESULTS.md`,
`LITERARY_EXPERIMENT_FINAL.md`, `BBH_REASONING_TEST.md`, and the actual
data: `debugbench_8heuristics_results.json` with 15 real DebugBench
problems, `lazarillo_heuristics.py`/`quijote_heuristics.py` with the
actual 8 heuristics used).

**Scoring flaw found and corrected.** `analyze_medium.py` (the only
analysis script present in this upload) scores correctness by exact
string match against `oracle_code` after stripping whitespace — not
execution. That fails any functionally-correct fix that isn't
byte-identical to the oracle (renamed variables, reordered logic, an
extra comment). `benchmarks/debugbench_rescore.py` (new, this session)
re-scores the same 15-problem dataset via differential testing (execute
candidate vs. oracle across random + structured edge-case inputs;
falls back to AST-normalized structural comparison, then plain string
match, reporting which method was used per problem — never silently
mixing rigor levels):

| | Exact string match (original) | Execution-based (corrected) |
|---|---|---|
| No literary | 7/15 (47%) | 12/15 (80%) |
| 8 literary heuristics | 10/15 (67%) | 13/15 (87%) |
| **Delta** | **+20pp** | **+7pp** |

The headline "+20%" in `DEBUGBENCH_HEURISTICS_RESULTS.md` was
substantially a scoring artifact — both conditions' true correctness was
far higher than exact-match showed, and the real delta shrinks to about
a third the size. +7pp on N=15, one run per condition, is still not
distinguishable from noise — this fixes the SCORING bias, not the
SAMPLE-SIZE problem; both need fixing before trusting a number here.

**Known limitation of the rescore harness itself, flagged rather than
hidden:** `binary-search` fails execution-based testing in BOTH
conditions — but that problem's bug (`bug_type: condition error`, in a
`while` loop) assumes a sorted input array, and the harness's random
`List[int]` generator doesn't sort inputs for 2+-parameter signatures
(only single-list-param problems get the structured/sorted edge cases).
That specific "fail" may be a harness artifact (comparing behavior
outside the algorithm's valid domain), not a genuine shared bug. Noted
in the script's own output rather than quietly treated as a clean result.

**Internal contradiction across GLM's own docs, unresolved:**
`DEBUGBENCH_EXCERPT_RESULTS.md` concludes raw literary text consistently
hurts accuracy (-13% to -20% across 500/1000/2000-token excerpts and the
full book) and only distilled heuristics help (+7%). `LITERARY_EXPERIMENT_FINAL.md`
(dated later, 2026-09-03) concludes the opposite — "distilled doesn't
work, raw text passages DO" — but drops the accuracy metric entirely in
favor of response length (~500 vs ~15,000 chars) and a self-reported
confidence score (50% vs 85%, source unstated), on a different,
non-DebugBench, N=1 task. That swap from an objective metric to
length/self-reported-confidence is exactly the two signals most
confounded by "long narrative context in the prompt primes long,
elaborate output" — not established as evidence of better reasoning.
Also flagged: that doc's "session contamination" exclusion criterion
(discarding sessions that didn't show the effect) has no pre-registered
definition, so it can't be distinguished from result-shopping as
documented.

**Not yet done:** wiring GLM's actual heuristics/control into the
three-arm harness (`compare_n_arm.py`) with the corrected scorer and
real repetitions — this session only fixed the scoring bias on the
existing single-run data, which was the most urgent fix given how much
the exact-match method was distorting both conditions. The N=1 problem
is still open.

## Suggested next audit target

`plan_task()` → real step-by-step execution, since that's the piece that
would make the hypothesis/verify/replan loop in the README actually
happen instead of being front-loaded into two calls before the answer.
