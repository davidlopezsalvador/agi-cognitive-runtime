"""Tests for transfer engine."""

from agi_runtime.transfer.engine import StructuralSimilarity, TransferEngine


def test_transfer_engine_similarities():
    engine = TransferEngine()
    similarities = engine.find_structural_similarities(
        "debug network latency issue",
        ["debug database latency problem", "fix slow query performance"],
    )
    assert len(similarities) > 0


def test_transfer_engine_no_similarities():
    engine = TransferEngine()
    similarities = engine.find_structural_similarities(
        "quantum physics calculation",
        ["bake a chocolate cake"],
    )
    assert len(similarities) == 0


def test_transfer_engine_abstract():
    engine = TransferEngine()
    principle = engine.abstract_principle(["example1", "example2"])
    assert "2 examples" in principle


def test_transfer_engine_apply():
    engine = TransferEngine()
    result = engine.apply_transfer("hypothesis testing", "software", "hardware")
    assert "software" in result
    assert "hardware" in result
