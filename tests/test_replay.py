"""Tests for cognitive replay."""

import tempfile
from pathlib import Path

from agi_runtime.persistence.session import SessionPersistence
from agi_runtime.persistence.replay import CognitiveReplay
from agi_runtime.runtime import CognitiveTrace


def test_replay_snapshot():
    with tempfile.TemporaryDirectory() as tmpdir:
        db = SessionPersistence(Path(tmpdir) / "test.db")
        session_id = db.create_session()
        trace = CognitiveTrace(
            task="Investigate bug",
            cognitive_mode="L3_investigate",
            decisions=["Classified as L3"],
            observations=["Found error logs"],
            actions=["Ran diagnostic"],
            verification="Verified root cause",
            lessons=["Check logs first"],
        )
        snap_id = db.save_snapshot(session_id, trace, answer="Root cause found")

        replay = CognitiveReplay(db)
        steps = replay.replay_snapshot(snap_id)
        assert len(steps) > 0
        event_types = [s.event_type for s in steps]
        assert "task_received" in event_types
        assert "classification" in event_types
        db.close()


def test_replay_summary():
    with tempfile.TemporaryDirectory() as tmpdir:
        db = SessionPersistence(Path(tmpdir) / "test.db")
        session_id = db.create_session()
        trace = CognitiveTrace(task="Test task")
        snap_id = db.save_snapshot(session_id, trace)

        replay = CognitiveReplay(db)
        summary = replay.summary(snap_id)
        assert "total_steps" in summary
        assert "event_types" in summary
        db.close()


def test_replay_session():
    with tempfile.TemporaryDirectory() as tmpdir:
        db = SessionPersistence(Path(tmpdir) / "test.db")
        session_id = db.create_session()

        for i in range(3):
            trace = CognitiveTrace(task=f"Task {i}")
            db.save_snapshot(session_id, trace, answer=f"Answer {i}")

        replay = CognitiveReplay(db)
        all_replays = replay.replay_session(session_id)
        assert len(all_replays) == 3
        db.close()


def test_compare_traces():
    with tempfile.TemporaryDirectory() as tmpdir:
        db = SessionPersistence(Path(tmpdir) / "test.db")
        session_id = db.create_session()

        trace_a = CognitiveTrace(task="Task A", decisions=["Decision A"])
        trace_b = CognitiveTrace(task="Task B", observations=["Observation B"])
        snap_a = db.save_snapshot(session_id, trace_a)
        snap_b = db.save_snapshot(session_id, trace_b)

        replay = CognitiveReplay(db)
        comparison = replay.compare_traces(snap_a, snap_b)
        assert "shared_events" in comparison
        assert "only_in_a" in comparison
        db.close()
