"""Proves the plumbing for the literary-knowledge experiment works:
the entries are well-formed, retrievable when relevant, and NOT retrieved
when irrelevant, and stay opt-in (not part of the default seed).

This does NOT test whether they improve LLM reasoning — that needs a live
provider and benchmarks/compare_literary_knowledge.py. This only proves
the mechanism these entries would act through actually functions.
"""

import sys
from pathlib import Path

# knowledge/ lives at the repo root (like benchmarks/), not under src/ —
# pytest's pythonpath is set to ["src"] only, so add the repo root here too.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from agi_runtime.context.compiler import ContextCompiler
from agi_runtime.memory.models import Memory
from knowledge.seed import seed_knowledge
from knowledge.seed_literary import seed_literary_knowledge


def test_literary_entries_not_in_default_seed():
    store = seed_knowledge()
    ids = {e.id for e in store.entries}
    assert "reasoning.adaptation.picaresque" not in ids
    assert "metacognition.verification.quixotic_dialectic" not in ids


def test_seed_literary_knowledge_adds_both_entries():
    store = seed_literary_knowledge()
    ids = {e.id for e in store.entries}
    assert "reasoning.adaptation.picaresque" in ids
    assert "metacognition.verification.quixotic_dialectic" in ids


def test_seed_literary_knowledge_composes_with_baseline_seed():
    store = seed_literary_knowledge(seed_knowledge())
    assert len(store.entries) == len(seed_knowledge().entries) + 2


def test_picaresque_entry_retrieved_for_adaptation_query():
    store = seed_literary_knowledge()
    results = store.search("repeated failure adversarial resource scarcity adaptation")
    assert any(e.id == "reasoning.adaptation.picaresque" for e in results)


def test_quixotic_entry_retrieved_for_verification_query():
    store = seed_literary_knowledge()
    results = store.search("confident conclusion ambiguous evidence verification dissent")
    assert any(e.id == "metacognition.verification.quixotic_dialectic" for e in results)


def test_literary_entries_not_retrieved_for_unrelated_query():
    store = seed_literary_knowledge()
    results = store.search("kilometers miles arithmetic conversion")
    ids = {e.id for e in results}
    assert "reasoning.adaptation.picaresque" not in ids
    assert "metacognition.verification.quixotic_dialectic" not in ids


def test_context_compiler_surfaces_literary_entry_when_relevant():
    store = seed_literary_knowledge()
    compiler = ContextCompiler(knowledge=store, memory=Memory())
    ctx = compiler.compile(
        "We keep failing with this adversarial vendor and need to adapt our resource-scarce strategy"
    )
    names = {p for p in ctx.relevant_principles}
    assert "Picaresque Iterative Adaptation" in names


def test_relevant_principles_are_actually_relevance_filtered():
    """Regression test for the bug this file's other test exposed: relevant_principles
    used to be `by_type("principle")[:max_principles]` — the first N principles in
    the whole store, regardless of the task. A store with one obviously-relevant
    principle and several irrelevant ones should surface the relevant one first."""
    from agi_runtime.knowledge.store import KnowledgeEntry, KnowledgeStore

    store = KnowledgeStore()
    store.add(KnowledgeEntry(id="p.unrelated_1", type="principle", name="Unrelated One", description="cooking pasta"))
    store.add(KnowledgeEntry(id="p.unrelated_2", type="principle", name="Unrelated Two", description="gardening tips"))
    store.add(
        KnowledgeEntry(
            id="p.relevant",
            type="principle",
            name="Debugging Strategy",
            description="hypothesis driven debugging of intermittent failures",
        )
    )
    compiler = ContextCompiler(knowledge=store, memory=Memory())
    ctx = compiler.compile("debugging an intermittent failure", max_principles=1)
    assert ctx.relevant_principles == ["Debugging Strategy"]
