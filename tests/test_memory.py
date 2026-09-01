"""Tests for memory."""

from agi_runtime.memory.models import (
    Episode,
    FailureRecord,
    Memory,
    ProceduralSkill,
    SemanticEntry,
    WorkingMemory,
)


def test_working_memory():
    wm = WorkingMemory(current_goal="Fix bug")
    assert wm.current_goal == "Fix bug"
    wm.clear()
    assert wm.current_goal == ""


def test_episode():
    ep = Episode(task="Fix login bug", result="Fixed by updating session handler")
    assert ep.task == "Fix login bug"
    assert ep.lesson == ""


def test_procedural_skill():
    skill = ProceduralSkill(name="debug_network", success_count=8, failure_count=2)
    assert skill.success_rate == 0.8


def test_failure_record():
    record = FailureRecord(
        task="Deploy service",
        failure="Build failed",
        cause="Missing dependency",
        reusable_lesson="Always check dependencies before deploy",
    )
    assert record.reusable_lesson != ""


def test_memory_store_and_retrieve():
    mem = Memory()
    ep = Episode(task="Debug timeout", lesson="Check connection pool")
    mem.store_episode(ep)

    found = mem.find_similar_episodes("timeout")
    assert len(found) >= 1


def test_memory_find_skills():
    mem = Memory()
    skill = ProceduralSkill(name="debug_database", purpose="Debug database issues")
    mem.store_skill(skill)

    found = mem.find_relevant_skills("database")
    assert len(found) == 1


def test_memory_find_failures():
    mem = Memory()
    record = FailureRecord(task="Deploy", cause="Missing env var")
    mem.store_failure(record)

    found = mem.find_related_failures("env var")
    assert len(found) == 1


def test_memory_semantic():
    mem = Memory()
    entry = SemanticEntry(
        concept="Connection pooling",
        principle="Reuse connections to reduce overhead",
        domain=["databases", "networking"],
    )
    mem.store_semantic(entry)
    assert len(mem.semantic) == 1
