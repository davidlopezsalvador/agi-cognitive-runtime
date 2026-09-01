"""Tests for policy compiler."""

from agi_runtime.compiler.policy import PolicyCompiler, DEFAULT_POLICIES
from agi_runtime.types import CognitiveDepth


def test_policy_compiler_creation():
    compiler = PolicyCompiler()
    assert len(compiler.policies) > 0


def test_select_direct():
    compiler = PolicyCompiler()
    policy = compiler.select(CognitiveDepth.L0_DIRECT)
    assert policy.id == "direct"
    assert "EXECUTE" in policy.operators


def test_select_investigate():
    compiler = PolicyCompiler()
    policy = compiler.select(CognitiveDepth.L3_INVESTIGATE)
    assert policy.id == "investigate"
    assert "HYPOTHESIZE" in policy.operators


def test_compile_operators():
    compiler = PolicyCompiler()
    operators = compiler.compile(CognitiveDepth.L2_PLAN)
    assert len(operators) >= 3
    names = [op.name for op in operators]
    assert "PLAN" in names
    assert "VERIFY" in names


def test_list_policies():
    compiler = PolicyCompiler()
    policies = compiler.list_policies()
    assert len(policies) > 0
    assert all("id" in p for p in policies)
    assert all("operators" in p for p in policies)


def test_all_depths_have_policy():
    compiler = PolicyCompiler()
    for depth in CognitiveDepth:
        policy = compiler.select(depth)
        assert policy is not None
        assert len(policy.operators) > 0
