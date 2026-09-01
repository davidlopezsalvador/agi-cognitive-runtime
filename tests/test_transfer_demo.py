"""Tests for transfer demo."""

from agi_runtime.transfer.demo import TransferDemonstrator, TransferDemo
from agi_runtime.transfer.engine import TransferEngine
from agi_runtime.memory.models import Memory, Episode
from agi_runtime.knowledge.store import KnowledgeStore


def test_demonstrator_creation():
    demo = TransferDemonstrator()
    assert demo.transfer is not None


def test_populate_and_demonstrate():
    demo = TransferDemonstrator()
    demo.populate_from_seed()

    result = demo.demonstrate(
        "Debug network latency",
        "Investigate slow database queries",
    )
    assert isinstance(result, TransferDemo)
    assert result.confidence >= 0.0


def test_full_transfer_demo():
    demo = TransferDemonstrator()
    demo.populate_from_seed()

    results = demo.full_transfer_demo()
    assert len(results) == 4
    for r in results:
        assert isinstance(r, TransferDemo)
        assert r.shared_abstraction != ""


def test_no_experiences():
    demo = TransferDemonstrator()
    result = demo.demonstrate(
        "Novel problem X",
        "Different problem Y",
    )
    assert isinstance(result, TransferDemo)
    assert result.confidence == 0.0
