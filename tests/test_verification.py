"""Tests for verification engine."""

from agi_runtime.verification.engine import VerificationEngine, VerificationResult


def test_verify_claim():
    engine = VerificationEngine()
    result = engine.verify_claim("The fix works", evidence=["Tests pass", "No regressions"])
    assert result.claim == "The fix works"
    assert len(result.evidence) == 2


def test_challenge():
    engine = VerificationEngine()
    questions = engine.challenge("The solution is optimal")
    assert len(questions) > 0
    assert "What could make this wrong?" in questions


def test_cross_check_agreement():
    engine = VerificationEngine()
    result = engine.cross_check(
        "A is true",
        "B is true",
        ["evidence1", "evidence2"],
        ["evidence2", "evidence3"],
    )
    assert "1 pieces" in result


def test_cross_check_disagreement():
    engine = VerificationEngine()
    result = engine.cross_check(
        "A is true",
        "B is true",
        ["evidence1"],
        ["evidence2"],
    )
    assert "no shared evidence" in result
