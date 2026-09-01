"""Tests for hypothesis engine."""

from agi_runtime.reasoning.hypothesis import Hypothesis, HypothesisSpace
from agi_runtime.types import HypothesisStatus


def test_hypothesis_creation():
    h = Hypothesis(statement="The issue is a race condition")
    assert h.status == HypothesisStatus.CANDIDATE
    assert h.prior_confidence == 0.5


def test_hypothesis_support():
    h = Hypothesis(statement="Race condition", prior_confidence=0.5)
    h.add_supporting("Log shows concurrent access")
    h.add_supporting("Timing matches race window")
    assert len(h.supporting_evidence) == 2
    assert h.posterior_confidence > 0.5


def test_hypothesis_contradiction():
    h = Hypothesis(statement="Race condition", prior_confidence=0.7)
    h.add_supporting("Evidence A")
    h.add_contradictory("Evidence B")
    h.add_contradictory("Evidence C")
    assert len(h.contradictory_evidence) == 2
    assert h.posterior_confidence < 0.7


def test_hypothesis_well_supported():
    h = Hypothesis(statement="X", prior_confidence=0.5)
    for _ in range(5):
        h.add_supporting("evidence")
    assert h.is_well_supported(threshold=0.6)


def test_hypothesis_refuted():
    h = Hypothesis(statement="X", prior_confidence=0.5)
    for _ in range(5):
        h.add_contradictory("evidence")
    assert h.is_refuted(threshold=0.3)


def test_hypothesis_space():
    space = HypothesisSpace(problem="Why is it slow?")
    h1 = Hypothesis(statement="Network issue", prior_confidence=0.6)
    h2 = Hypothesis(statement="CPU issue", prior_confidence=0.4)
    h1.add_supporting("evidence")
    h1.add_supporting("more evidence")
    h2.add_supporting("some evidence")

    space.add(h1)
    space.add(h2)

    ranked = space.rank()
    assert ranked[0].statement == "Network issue"
    assert space.best() is not None


def test_hypothesis_elimination():
    space = HypothesisSpace()
    h1 = Hypothesis(statement="A")
    h2 = Hypothesis(statement="B")
    for _ in range(5):
        h1.add_contradictory("x")
    space.add(h1)
    space.add(h2)

    refuted = space.eliminate_refuted()
    assert len(refuted) == 1
    assert len(space.hypotheses) == 1
