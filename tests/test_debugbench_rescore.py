"""Tests for benchmarks/debugbench_rescore.py's scoring logic, using small
synthetic Solution classes instead of the external results JSON — so these
run in CI without that file being present, and so the harness itself is
under test, not just trusted blindly."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from benchmarks.debugbench_rescore import ast_normalized, differential_test

ORACLE_BINARY_SEARCH_STYLE = """
class Solution:
    def double_it(self, x: int) -> int:
        return x * 2
"""

FUNCTIONALLY_EQUIVALENT_DIFFERENT_NAMES = """
class Solution:
    def double_it(self, value: int) -> int:
        result = value + value
        return result
"""

ACTUALLY_BUGGY = """
class Solution:
    def double_it(self, x: int) -> int:
        return x * 3
"""

LIST_PROBLEM_ORACLE = """
class Solution:
    def total(self, nums: List[int]) -> int:
        return sum(nums)
"""

LIST_PROBLEM_BUGGY_ON_EMPTY = """
class Solution:
    def total(self, nums: List[int]) -> int:
        if not nums:
            return -1
        return sum(nums)
"""


def test_differential_test_passes_functionally_equivalent_renamed_code():
    result = differential_test(ORACLE_BINARY_SEARCH_STYLE, FUNCTIONALLY_EQUIVALENT_DIFFERENT_NAMES)
    assert result == "pass"


def test_differential_test_fails_genuinely_buggy_code():
    result = differential_test(ORACLE_BINARY_SEARCH_STYLE, ACTUALLY_BUGGY)
    assert result == "fail"


def test_differential_test_catches_empty_list_edge_case():
    # This is exactly the kind of bug exact-string-match AND naive random
    # fuzzing without structured edge cases could both miss.
    result = differential_test(LIST_PROBLEM_ORACLE, LIST_PROBLEM_BUGGY_ON_EMPTY)
    assert result == "fail"


def test_ast_normalized_ignores_variable_names():
    a = ast_normalized(ORACLE_BINARY_SEARCH_STYLE)
    b = ast_normalized(FUNCTIONALLY_EQUIVALENT_DIFFERENT_NAMES.replace("result = value + value\n        return result", "return value * 2"))
    assert a == b


def test_ast_normalized_returns_none_on_syntax_error():
    assert ast_normalized("def broken(:") is None
