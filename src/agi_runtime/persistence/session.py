"""Multi-session persistence for the AGI Cognitive Runtime."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from agi_runtime.types import BaseSchema
from agi_runtime.memory.models import Memory, Episode, SemanticEntry, ProceduralSkill, FailureRecord
from agi_runtime.knowledge.store import KnowledgeStore, KnowledgeEntry
from agi_runtime.world.model import WorldModel, Belief, WorldModelEntry
from agi_runtime.world.goal import Goal, GoalTree
from agi_runtime.planning.plan import Plan, PlanStep
from agi_runtime.reasoning.hypothesis import Hypothesis, HypothesisSpace
from agi_runtime.metacognition.state import MetacognitiveState
from agi_runtime.runtime import CognitiveTrace


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class RuntimeSnapshot(BaseSchema):
    """Full snapshot of runtime state."""

    trace: CognitiveTrace = Field(default_factory=CognitiveTrace)
    episodes: list[dict[str, Any]] = Field(default_factory=list)
    semantic: list[dict[str, Any]] = Field(default_factory=list)
    skills: list[dict[str, Any]] = Field(default_factory=list)
    failures: list[dict[str, Any]] = Field(default_factory=list)
    goals: list[dict[str, Any]] = Field(default_factory=list)
    beliefs: list[dict[str, Any]] = Field(default_factory=list)
    hypotheses: list[dict[str, Any]] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class SessionPersistence:
    """Manages persistence of runtime state across sessions."""

    def __init__(self, db_path: str | Path = "memory/sessions.db") -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self._init_tables()

    def _init_tables(self) -> None:
        self.conn.executescript("""
            CREATE TABLE IF NOT EXISTS sessions (
                id TEXT PRIMARY KEY,
                name TEXT DEFAULT '',
                created TEXT NOT NULL,
                updated TEXT NOT NULL,
                metadata TEXT DEFAULT '{}'
            );
            CREATE TABLE IF NOT EXISTS snapshots (
                id TEXT PRIMARY KEY,
                session_id TEXT NOT NULL,
                task TEXT DEFAULT '',
                depth TEXT DEFAULT '',
                answer TEXT DEFAULT '',
                trace TEXT DEFAULT '{}',
                episodes TEXT DEFAULT '[]',
                goals TEXT DEFAULT '[]',
                beliefs TEXT DEFAULT '[]',
                hypotheses TEXT DEFAULT '[]',
                created TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES sessions(id)
            );
            CREATE TABLE IF NOT EXISTS cognitive_traces (
                id TEXT PRIMARY KEY,
                snapshot_id TEXT NOT NULL,
                step INTEGER DEFAULT 0,
                event_type TEXT DEFAULT '',
                data TEXT DEFAULT '{}',
                created TEXT NOT NULL,
                FOREIGN KEY (snapshot_id) REFERENCES snapshots(id)
            );
        """)

    def create_session(self, name: str = "") -> str:
        session_id = f"session_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
        now = _now_iso()
        self.conn.execute(
            "INSERT INTO sessions (id, name, created, updated) VALUES (?, ?, ?, ?)",
            (session_id, name, now, now),
        )
        self.conn.commit()
        return session_id

    def save_snapshot(
        self,
        session_id: str,
        trace: CognitiveTrace,
        answer: str = "",
        depth: str = "",
        episodes: list[Episode] | None = None,
        goals: list[Goal] | None = None,
        beliefs: list[Belief] | None = None,
        hypotheses: list[Hypothesis] | None = None,
    ) -> str:
        snapshot_id = f"snap_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S_%f')}"
        now = _now_iso()

        episodes_data = [ep.model_dump(mode="json") for ep in (episodes or [])]
        goals_data = [g.model_dump(mode="json") for g in (goals or [])]
        beliefs_data = [b.model_dump(mode="json") for b in (beliefs or [])]
        hyps_data = [h.model_dump(mode="json") for h in (hypotheses or [])]

        self.conn.execute(
            """INSERT INTO snapshots (id, session_id, task, depth, answer, trace, episodes, goals, beliefs, hypotheses, created)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                snapshot_id, session_id, trace.task, depth, answer,
                trace.model_dump_json(),
                json.dumps(episodes_data),
                json.dumps(goals_data),
                json.dumps(beliefs_data),
                json.dumps(hyps_data),
                now,
            ),
        )
        self.conn.commit()
        return snapshot_id

    def load_snapshot(self, snapshot_id: str) -> dict[str, Any] | None:
        row = self.conn.execute(
            "SELECT * FROM snapshots WHERE id = ?", (snapshot_id,)
        ).fetchone()
        if not row:
            return None
        return {
            "id": row["id"],
            "session_id": row["session_id"],
            "task": row["task"],
            "depth": row["depth"],
            "answer": row["answer"],
            "trace": json.loads(row["trace"]),
            "episodes": json.loads(row["episodes"]),
            "goals": json.loads(row["goals"]),
            "beliefs": json.loads(row["beliefs"]),
            "hypotheses": json.loads(row["hypotheses"]),
            "created": row["created"],
        }

    def list_sessions(self) -> list[dict[str, str]]:
        rows = self.conn.execute("SELECT id, name, created FROM sessions ORDER BY created DESC").fetchall()
        return [{"id": r["id"], "name": r["name"], "created": r["created"]} for r in rows]

    def list_snapshots(self, session_id: str) -> list[dict[str, str]]:
        rows = self.conn.execute(
            "SELECT id, task, depth, created FROM snapshots WHERE session_id = ? ORDER BY created DESC",
            (session_id,),
        ).fetchall()
        return [{"id": r["id"], "task": r["task"], "depth": r["depth"], "created": r["created"]} for r in rows]

    def restore_memory(self, snapshot_id: str) -> Memory:
        snap = self.load_snapshot(snapshot_id)
        if not snap:
            return Memory()

        mem = Memory()
        for ep_data in snap["episodes"]:
            mem.episodes.append(Episode(**ep_data))
        return mem

    def restore_world_model(self, snapshot_id: str) -> WorldModel:
        snap = self.load_snapshot(snapshot_id)
        if not snap:
            return WorldModel()

        wm = WorldModel()
        for b_data in snap["beliefs"]:
            wm.beliefs.append(Belief(**b_data))
        return wm

    def restore_hypotheses(self, snapshot_id: str) -> HypothesisSpace:
        snap = self.load_snapshot(snapshot_id)
        if not snap:
            return HypothesisSpace()

        space = HypothesisSpace()
        for h_data in snap["hypotheses"]:
            space.hypotheses.append(Hypothesis(**h_data))
        return space

    def save_trace_step(
        self, snapshot_id: str, step: int, event_type: str, data: dict[str, Any]
    ) -> None:
        trace_id = f"trace_{step}_{datetime.now(timezone.utc).strftime('%H%M%S_%f')}"
        self.conn.execute(
            "INSERT INTO cognitive_traces (id, snapshot_id, step, event_type, data, created) VALUES (?, ?, ?, ?, ?, ?)",
            (trace_id, snapshot_id, step, event_type, json.dumps(data), _now_iso()),
        )
        self.conn.commit()

    def load_trace(self, snapshot_id: str) -> list[dict[str, Any]]:
        rows = self.conn.execute(
            "SELECT * FROM cognitive_traces WHERE snapshot_id = ? ORDER BY step",
            (snapshot_id,),
        ).fetchall()
        return [
            {"step": r["step"], "event_type": r["event_type"], "data": json.loads(r["data"])}
            for r in rows
        ]

    def close(self) -> None:
        self.conn.close()
