"""Tests for provider factory and knowledge seeding."""

import os
from unittest.mock import patch

from agi_runtime.providers.factory import create_provider
from knowledge.seed import seed_knowledge
from agi_runtime.knowledge.store import KnowledgeStore


def test_create_provider_none():
    with patch.dict(os.environ, {"AGI_PROVIDER": "none"}):
        provider = create_provider()
        assert provider is None


def test_create_provider_no_env():
    with patch.dict(os.environ, {}, clear=True):
        provider = create_provider()
        assert provider is None


def test_seed_knowledge():
    store = seed_knowledge()
    assert len(store.entries) > 20


def test_seed_knowledge_search():
    store = seed_knowledge()
    results = store.search("debugging")
    assert len(results) > 0


def test_seed_knowledge_by_type():
    store = seed_knowledge()
    principles = store.by_type("principle")
    heuristics = store.by_type("heuristic")
    assert len(principles) > 10
    assert len(heuristics) > 0


def test_seed_knowledge_by_domain():
    store = seed_knowledge()
    reasoning = store.by_domain("reasoning")
    assert len(reasoning) > 0
