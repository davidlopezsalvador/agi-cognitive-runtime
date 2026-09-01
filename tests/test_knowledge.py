"""Tests for knowledge store."""

from agi_runtime.knowledge.store import KnowledgeEntry, KnowledgeStore


def test_knowledge_entry():
    entry = KnowledgeEntry(
        id="reasoning.abduction.basic",
        type="principle",
        name="Abductive reasoning",
        description="Inferring plausible explanations from observations.",
        domain=["reasoning", "inference"],
    )
    assert entry.id == "reasoning.abduction.basic"
    assert entry.version == 1


def test_knowledge_store_add_and_get():
    store = KnowledgeStore()
    entry = KnowledgeEntry(id="test.1", type="principle", name="Test Principle")
    store.add(entry)

    found = store.get("test.1")
    assert found is not None
    assert found.name == "Test Principle"


def test_knowledge_store_search():
    store = KnowledgeStore()
    store.add(KnowledgeEntry(id="p1", type="principle", name="Abstraction", tags=["reasoning"]))
    store.add(KnowledgeEntry(id="p2", type="principle", name="Verification", tags=["quality"]))
    store.add(KnowledgeEntry(id="p3", type="heuristic", name="Occam's Razor", tags=["reasoning"]))

    results = store.search("reasoning")
    assert len(results) >= 2


def test_knowledge_store_by_domain():
    store = KnowledgeStore()
    store.add(KnowledgeEntry(id="p1", type="principle", domain=["reasoning", "logic"]))
    store.add(KnowledgeEntry(id="p2", type="principle", domain=["networking"]))

    results = store.by_domain("reasoning")
    assert len(results) == 1


def test_knowledge_store_by_type():
    store = KnowledgeStore()
    store.add(KnowledgeEntry(id="p1", type="principle"))
    store.add(KnowledgeEntry(id="p2", type="heuristic"))
    store.add(KnowledgeEntry(id="p3", type="principle"))

    results = store.by_type("principle")
    assert len(results) == 2


def test_knowledge_store_by_trigger():
    store = KnowledgeStore()
    store.add(KnowledgeEntry(id="p1", type="principle", triggers=["debugging", "diagnosis"]))
    store.add(KnowledgeEntry(id="p2", type="principle", triggers=["planning"]))

    results = store.by_trigger("debugging")
    assert len(results) == 1
