"""Tests for provider factory and knowledge store."""

import os
from unittest.mock import patch

from agi_runtime.providers.factory import create_provider
from agi_runtime.knowledge.store import KnowledgeStore, KnowledgeEntry


def test_create_provider_none():
    with patch.dict(os.environ, {"AGI_PROVIDER": "none"}):
        provider = create_provider()
        assert provider is None


def test_create_provider_no_env():
    with patch.dict(os.environ, {}, clear=True):
        provider = create_provider()
        assert provider is None


def test_knowledge_store_empty():
    store = KnowledgeStore()
    assert len(store.entries) == 0


def test_knowledge_store_add():
    store = KnowledgeStore()
    entry = KnowledgeEntry(
        id="test.principle.1",
        type="principle",
        name="Test Principle",
        description="A test principle",
        domain=["testing"],
        summary="Test summary"
    )
    store.add(entry)
    assert len(store.entries) == 1


def test_knowledge_store_search():
    store = KnowledgeStore()
    entry = KnowledgeEntry(
        id="test.heuristic.1",
        type="heuristic",
        name="Debugging Heuristic",
        description="Use binary search for debugging",
        domain=["reasoning"],
        tags=["debugging"],
        summary="Divide and conquer"
    )
    store.add(entry)
    results = store.search("debugging")
    assert len(results) > 0


def test_knowledge_store_by_type():
    store = KnowledgeStore()
    store.add(KnowledgeEntry(id="p1", type="principle", name="P1", domain=["r"]))
    store.add(KnowledgeEntry(id="h1", type="heuristic", name="H1", domain=["r"]))
    principles = store.by_type("principle")
    heuristics = store.by_type("heuristic")
    assert len(principles) == 1
    assert len(heuristics) == 1


def test_knowledge_store_by_domain():
    store = KnowledgeStore()
    store.add(KnowledgeEntry(id="p1", type="principle", name="P1", domain=["reasoning"]))
    store.add(KnowledgeEntry(id="p2", type="principle", name="P2", domain=["planning"]))
    reasoning = store.by_domain("reasoning")
    assert len(reasoning) == 1
