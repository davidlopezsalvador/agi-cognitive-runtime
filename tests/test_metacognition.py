"""Tests for metacognition."""

from agi_runtime.metacognition.state import MetacognitiveState


def test_metacognition_defaults():
    state = MetacognitiveState()
    assert state.current_confidence == 0.5
    assert state.should_proceed() is False
    assert state.should_investigate() is False
    state.known_unknowns.append("What is the cause?")
    assert state.should_investigate() is True


def test_metacognition_high_confidence():
    state = MetacognitiveState(current_confidence=0.8, failure_risk=0.3)
    assert state.should_proceed() is True
    assert state.should_investigate() is False


def test_metacognition_should_ask_user():
    state = MetacognitiveState(failure_risk=0.8)
    assert state.should_ask_user() is True


def test_metacognition_summary():
    state = MetacognitiveState(
        current_confidence=0.7,
        known_unknowns=["What is the root cause?"],
        alternative_strategies=["Try approach B"],
    )
    summary = state.summary()
    assert "70%" in summary
    assert "Unknowns: 1" in summary
    assert "Alternatives: 1" in summary
