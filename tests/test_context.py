"""Tests for context compiler."""

from agi_runtime.context.compiler import CognitiveContext, ContextCompiler
from agi_runtime.knowledge.store import KnowledgeEntry, KnowledgeStore
from agi_runtime.memory.models import Memory, Episode


def test_cognitive_context_to_prompt():
    ctx = CognitiveContext(
        task_description="Fix the bug",
        active_goal="Resolve production issue",
        relevant_concepts=["timeout", "connection_pool"],
    )
    prompt = ctx.to_prompt()
    assert "TASK: Fix the bug" in prompt
    assert "GOAL: Resolve production issue" in prompt


def test_context_compiler_minimal():
    compiler = ContextCompiler()
    ctx = compiler.compile("Fix the timeout issue")
    assert ctx.task_description == "Fix the timeout issue"


def test_context_compiler_with_knowledge():
    store = KnowledgeStore()
    store.add(KnowledgeEntry(id="k1", type="principle", name="Connection pooling", tags=["timeout"]))
    compiler = ContextCompiler(knowledge=store)
    ctx = compiler.compile("Fix timeout")
    assert len(ctx.relevant_concepts) > 0


def test_context_compiler_with_memory():
    mem = Memory()
    mem.store_episode(Episode(task="Debug timeout", lesson="Check connection pool"))
    compiler = ContextCompiler(memory=mem)
    ctx = compiler.compile("Fix timeout issue")
    assert ctx.memory_summary != ""


def test_context_compiler_max_limits():
    store = KnowledgeStore()
    for i in range(20):
        store.add(KnowledgeEntry(id=f"k{i}", type="principle", name=f"Principle {i}"))
    compiler = ContextCompiler(knowledge=store)
    ctx = compiler.compile("test", max_concepts=5)
    assert len(ctx.relevant_concepts) <= 5
