"""Tests for SQLite persistence."""

import tempfile
from pathlib import Path

from agi_runtime.persistence.sqlite import SQLiteMemoryStore, SQLiteKnowledgeStore
from agi_runtime.memory.models import Episode, ProceduralSkill
from agi_runtime.knowledge.store import KnowledgeEntry


def test_sqlite_memory_store():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test.db"
        store = SQLiteMemoryStore(db_path)

        ep = Episode(task="Test task", lesson="Test lesson")
        store.store_episode(ep)

        loaded = store.load_all_episodes()
        assert len(loaded) == 1
        assert loaded[0].task == "Test task"

        skill = ProceduralSkill(name="test_skill", success_count=5, failure_count=1)
        store.store_skill(skill)

        mem = store.load_memory()
        assert len(mem.episodes) == 1
        assert len(mem.procedural) == 1

        store.close()


def test_sqlite_knowledge_store():
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "test_knowledge.db"
        store = SQLiteKnowledgeStore(db_path)

        entry = KnowledgeEntry(
            id="test.1",
            type="principle",
            name="Test Principle",
            domain=["testing"],
            tags=["test"],
        )
        store.store(entry)

        loaded = store.get("test.1")
        assert loaded is not None
        assert loaded.name == "Test Principle"

        results = store.search("test")
        assert len(results) >= 1

        results = store.by_type("principle")
        assert len(results) == 1

        full_store = store.load_all()
        assert len(full_store.entries) == 1

        store.close()
