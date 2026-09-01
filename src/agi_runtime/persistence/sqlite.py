"""SQLite persistence for memory and knowledge."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from agi_runtime.memory.models import (
    Episode,
    FailureRecord,
    Memory,
    ProceduralSkill,
    SemanticEntry,
    WorkingMemory,
)
from agi_runtime.knowledge.store import KnowledgeEntry, KnowledgeStore


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class SQLiteMemoryStore:
    """SQLite-backed persistent memory."""

    def __init__(self, db_path: str | Path = "memory/runtime.db") -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self._init_tables()

    def _init_tables(self) -> None:
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS episodes (
                id TEXT PRIMARY KEY,
                task TEXT NOT NULL,
                context TEXT DEFAULT '',
                actions TEXT DEFAULT '[]',
                result TEXT DEFAULT '',
                failure TEXT DEFAULT '',
                lesson TEXT DEFAULT '',
                tags TEXT DEFAULT '[]',
                created TEXT NOT NULL,
                updated TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS semantic_entries (
                id TEXT PRIMARY KEY,
                concept TEXT NOT NULL,
                principle TEXT DEFAULT '',
                description TEXT DEFAULT '',
                domain TEXT DEFAULT '[]',
                examples TEXT DEFAULT '[]',
                source_episode_ids TEXT DEFAULT '[]',
                created TEXT NOT NULL,
                updated TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS procedural_skills (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                purpose TEXT DEFAULT '',
                preconditions TEXT DEFAULT '[]',
                procedure TEXT DEFAULT '[]',
                expected_outcomes TEXT DEFAULT '[]',
                failure_modes TEXT DEFAULT '[]',
                verification TEXT DEFAULT '[]',
                examples TEXT DEFAULT '[]',
                success_count INTEGER DEFAULT 0,
                failure_count INTEGER DEFAULT 0,
                created TEXT NOT NULL,
                updated TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS failure_records (
                id TEXT PRIMARY KEY,
                task TEXT NOT NULL,
                attempted_strategy TEXT DEFAULT '',
                failure TEXT DEFAULT '',
                cause TEXT DEFAULT '',
                evidence TEXT DEFAULT '[]',
                corrected_strategy TEXT DEFAULT '',
                reusable_lesson TEXT DEFAULT '',
                created TEXT NOT NULL,
                updated TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS knowledge_entries (
                id TEXT PRIMARY KEY,
                version INTEGER DEFAULT 1,
                type TEXT NOT NULL,
                domain TEXT DEFAULT '[]',
                name TEXT DEFAULT '',
                description TEXT DEFAULT '',
                summary TEXT DEFAULT '',
                heuristics TEXT DEFAULT '[]',
                triggers TEXT DEFAULT '[]',
                procedure TEXT DEFAULT '[]',
                anti_patterns TEXT DEFAULT '[]',
                verification_questions TEXT DEFAULT '[]',
                examples TEXT DEFAULT '[]',
                source TEXT DEFAULT '',
                tags TEXT DEFAULT '[]',
                created TEXT NOT NULL,
                updated TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS beliefs (
                id TEXT PRIMARY KEY,
                claim TEXT NOT NULL,
                status TEXT DEFAULT 'unknown',
                confidence REAL DEFAULT 0.5,
                evidence TEXT DEFAULT '[]',
                counter_evidence TEXT DEFAULT '[]',
                source TEXT DEFAULT '',
                last_checked TEXT,
                created TEXT NOT NULL,
                updated TEXT NOT NULL
            );
        """)

    def store_episode(self, ep: Episode) -> None:
        now = _now_iso()
        self.conn.execute(
            "INSERT OR REPLACE INTO episodes (id, task, context, actions, result, failure, lesson, tags, created, updated) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                ep.id, ep.task, ep.context,
                json.dumps(ep.actions), ep.result, ep.failure, ep.lesson,
                json.dumps(ep.tags), ep.created.isoformat(), now,
            ),
        )
        self.conn.commit()

    def store_semantic(self, entry: SemanticEntry) -> None:
        now = _now_iso()
        self.conn.execute(
            "INSERT OR REPLACE INTO semantic_entries (id, concept, principle, description, domain, examples, source_episode_ids, created, updated) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                entry.id, entry.concept, entry.principle, entry.description,
                json.dumps(entry.domain), json.dumps(entry.examples),
                json.dumps(entry.source_episode_ids),
                entry.created.isoformat(), now,
            ),
        )
        self.conn.commit()

    def store_skill(self, skill: ProceduralSkill) -> None:
        now = _now_iso()
        self.conn.execute(
            "INSERT OR REPLACE INTO procedural_skills (id, name, purpose, preconditions, procedure, expected_outcomes, failure_modes, verification, examples, success_count, failure_count, created, updated) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                skill.id, skill.name, skill.purpose,
                json.dumps(skill.preconditions), json.dumps(skill.procedure),
                json.dumps(skill.expected_outcomes), json.dumps(skill.failure_modes),
                json.dumps(skill.verification), json.dumps(skill.examples),
                skill.success_count, skill.failure_count,
                skill.created.isoformat(), now,
            ),
        )
        self.conn.commit()

    def store_failure(self, record: FailureRecord) -> None:
        now = _now_iso()
        self.conn.execute(
            "INSERT OR REPLACE INTO failure_records (id, task, attempted_strategy, failure, cause, evidence, corrected_strategy, reusable_lesson, created, updated) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                record.id, record.task, record.attempted_strategy,
                record.failure, record.cause, json.dumps(record.evidence),
                record.corrected_strategy, record.reusable_lesson,
                record.created.isoformat(), now,
            ),
        )
        self.conn.commit()

    def load_all_episodes(self) -> list[Episode]:
        rows = self.conn.execute("SELECT * FROM episodes").fetchall()
        return [
            Episode(
                id=r["id"], task=r["task"], context=r["context"],
                actions=json.loads(r["actions"]), result=r["result"],
                failure=r["failure"], lesson=r["lesson"],
                tags=json.loads(r["tags"]),
            )
            for r in rows
        ]

    def load_all_semantic(self) -> list[SemanticEntry]:
        rows = self.conn.execute("SELECT * FROM semantic_entries").fetchall()
        return [
            SemanticEntry(
                id=r["id"], concept=r["concept"], principle=r["principle"],
                description=r["description"], domain=json.loads(r["domain"]),
                examples=json.loads(r["examples"]),
                source_episode_ids=json.loads(r["source_episode_ids"]),
            )
            for r in rows
        ]

    def load_all_skills(self) -> list[ProceduralSkill]:
        rows = self.conn.execute("SELECT * FROM procedural_skills").fetchall()
        return [
            ProceduralSkill(
                id=r["id"], name=r["name"], purpose=r["purpose"],
                preconditions=json.loads(r["preconditions"]),
                procedure=json.loads(r["procedure"]),
                expected_outcomes=json.loads(r["expected_outcomes"]),
                failure_modes=json.loads(r["failure_modes"]),
                verification=json.loads(r["verification"]),
                examples=json.loads(r["examples"]),
                success_count=r["success_count"],
                failure_count=r["failure_count"],
            )
            for r in rows
        ]

    def load_all_failures(self) -> list[FailureRecord]:
        rows = self.conn.execute("SELECT * FROM failure_records").fetchall()
        return [
            FailureRecord(
                id=r["id"], task=r["task"],
                attempted_strategy=r["attempted_strategy"],
                failure=r["failure"], cause=r["cause"],
                evidence=json.loads(r["evidence"]),
                corrected_strategy=r["corrected_strategy"],
                reusable_lesson=r["reusable_lesson"],
            )
            for r in rows
        ]

    def load_memory(self) -> Memory:
        mem = Memory()
        mem.episodes = self.load_all_episodes()
        mem.semantic = self.load_all_semantic()
        mem.procedural = self.load_all_skills()
        mem.failures = self.load_all_failures()
        return mem

    def close(self) -> None:
        self.conn.close()


class SQLiteKnowledgeStore:
    """SQLite-backed persistent knowledge store."""

    def __init__(self, db_path: str | Path = "memory/knowledge.db") -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self._init_tables()

    def _init_tables(self) -> None:
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS knowledge_entries (
                id TEXT PRIMARY KEY,
                version INTEGER DEFAULT 1,
                type TEXT NOT NULL,
                domain TEXT DEFAULT '[]',
                name TEXT DEFAULT '',
                description TEXT DEFAULT '',
                summary TEXT DEFAULT '',
                heuristics TEXT DEFAULT '[]',
                triggers TEXT DEFAULT '[]',
                procedure TEXT DEFAULT '[]',
                anti_patterns TEXT DEFAULT '[]',
                verification_questions TEXT DEFAULT '[]',
                examples TEXT DEFAULT '[]',
                source TEXT DEFAULT '',
                tags TEXT DEFAULT '[]',
                created TEXT NOT NULL,
                updated TEXT NOT NULL
            );
        """)

    def store(self, entry: KnowledgeEntry) -> None:
        now = _now_iso()
        self.conn.execute(
            "INSERT OR REPLACE INTO knowledge_entries (id, version, type, domain, name, description, summary, heuristics, triggers, procedure, anti_patterns, verification_questions, examples, source, tags, created, updated) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                entry.id, entry.version, entry.type,
                json.dumps(entry.domain), entry.name, entry.description,
                entry.summary, json.dumps(entry.heuristics),
                json.dumps(entry.triggers), json.dumps(entry.procedure),
                json.dumps(entry.anti_patterns),
                json.dumps(entry.verification_questions),
                json.dumps(entry.examples), entry.source,
                json.dumps(entry.tags),
                entry.created.isoformat(), now,
            ),
        )
        self.conn.commit()

    def get(self, entry_id: str) -> KnowledgeEntry | None:
        row = self.conn.execute("SELECT * FROM knowledge_entries WHERE id = ?", (entry_id,)).fetchone()
        if not row:
            return None
        return self._row_to_entry(row)

    def search(self, query: str, limit: int = 10) -> list[KnowledgeEntry]:
        rows = self.conn.execute("SELECT * FROM knowledge_entries").fetchall()
        query_lower = query.lower()
        query_terms = set(query_lower.split())
        scored: list[tuple[float, sqlite3.Row]] = []
        for r in rows:
            text = f"{r['name']} {r['description']} {r['summary']} {r['tags']} {r['domain']}".lower()
            score = sum(1.0 for t in query_terms if t in text)
            if query_lower in text:
                score += 2.0
            if score > 0:
                scored.append((score, r))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [self._row_to_entry(r) for _, r in scored[:limit]]

    def by_type(self, entry_type: str) -> list[KnowledgeEntry]:
        rows = self.conn.execute("SELECT * FROM knowledge_entries WHERE type = ?", (entry_type,)).fetchall()
        return [self._row_to_entry(r) for r in rows]

    def load_all(self) -> KnowledgeStore:
        store = KnowledgeStore()
        rows = self.conn.execute("SELECT * FROM knowledge_entries").fetchall()
        for r in rows:
            store.add(self._row_to_entry(r))
        return store

    def _row_to_entry(self, row: sqlite3.Row) -> KnowledgeEntry:
        return KnowledgeEntry(
            id=row["id"], version=row["version"], type=row["type"],
            domain=json.loads(row["domain"]), name=row["name"],
            description=row["description"], summary=row["summary"],
            heuristics=json.loads(row["heuristics"]),
            triggers=json.loads(row["triggers"]),
            procedure=json.loads(row["procedure"]),
            anti_patterns=json.loads(row["anti_patterns"]),
            verification_questions=json.loads(row["verification_questions"]),
            examples=json.loads(row["examples"]),
            source=row["source"], tags=json.loads(row["tags"]),
        )

    def close(self) -> None:
        self.conn.close()
