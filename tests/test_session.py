"""Tests for multi-session persistence."""

import tempfile
from pathlib import Path

from agi_runtime.persistence.session import SessionPersistence
from agi_runtime.runtime import CognitiveTrace
from agi_runtime.memory.models import Episode
from agi_runtime.world.model import Belief
from agi_runtime.types import EpistemicStatus


def test_create_session():
    with tempfile.TemporaryDirectory() as tmpdir:
        db = SessionPersistence(Path(tmpdir) / "test.db")
        session_id = db.create_session("Test Session")
        assert session_id.startswith("session_")
        sessions = db.list_sessions()
        assert len(sessions) == 1
        db.close()


def test_save_snapshot():
    with tempfile.TemporaryDirectory() as tmpdir:
        db = SessionPersistence(Path(tmpdir) / "test.db")
        session_id = db.create_session()
        trace = CognitiveTrace(task="Test task", cognitive_mode="L2_plan")

        snap_id = db.save_snapshot(
            session_id,
            trace,
            answer="Test answer",
            depth="L2_plan",
        )
        assert snap_id.startswith("snap_")

        loaded = db.load_snapshot(snap_id)
        assert loaded is not None
        assert loaded["task"] == "Test task"
        assert loaded["answer"] == "Test answer"
        db.close()


def test_save_snapshot_with_episodes():
    with tempfile.TemporaryDirectory() as tmpdir:
        db = SessionPersistence(Path(tmpdir) / "test.db")
        session_id = db.create_session()
        trace = CognitiveTrace(task="Test")

        ep = Episode(task="Past task", lesson="Learned something")
        snap_id = db.save_snapshot(session_id, trace, episodes=[ep])

        loaded = db.load_snapshot(snap_id)
        assert len(loaded["episodes"]) == 1
        assert loaded["episodes"][0]["task"] == "Past task"
        db.close()


def test_restore_memory():
    with tempfile.TemporaryDirectory() as tmpdir:
        db = SessionPersistence(Path(tmpdir) / "test.db")
        session_id = db.create_session()
        trace = CognitiveTrace(task="Test")

        ep1 = Episode(task="Task 1", lesson="Lesson 1")
        ep2 = Episode(task="Task 2", lesson="Lesson 2")
        snap_id = db.save_snapshot(session_id, trace, episodes=[ep1, ep2])

        mem = db.restore_memory(snap_id)
        assert len(mem.episodes) == 2
        db.close()


def test_restore_world_model():
    with tempfile.TemporaryDirectory() as tmpdir:
        db = SessionPersistence(Path(tmpdir) / "test.db")
        session_id = db.create_session()
        trace = CognitiveTrace(task="Test")

        belief = Belief(claim="Test claim", status=EpistemicStatus.FACT, confidence=0.9)
        snap_id = db.save_snapshot(session_id, trace, beliefs=[belief])

        wm = db.restore_world_model(snap_id)
        assert len(wm.beliefs) == 1
        assert wm.beliefs[0].claim == "Test claim"
        db.close()


def test_list_snapshots():
    with tempfile.TemporaryDirectory() as tmpdir:
        db = SessionPersistence(Path(tmpdir) / "test.db")
        session_id = db.create_session()

        for i in range(3):
            trace = CognitiveTrace(task=f"Task {i}")
            db.save_snapshot(session_id, trace)

        snaps = db.list_snapshots(session_id)
        assert len(snaps) == 3
        db.close()


def test_trace_steps():
    with tempfile.TemporaryDirectory() as tmpdir:
        db = SessionPersistence(Path(tmpdir) / "test.db")
        session_id = db.create_session()
        trace = CognitiveTrace(task="Test")
        snap_id = db.save_snapshot(session_id, trace)

        db.save_trace_step(snap_id, 0, "task_received", {"task": "Test"})
        db.save_trace_step(snap_id, 1, "classified", {"depth": "L2_plan"})

        steps = db.load_trace(snap_id)
        assert len(steps) == 2
        assert steps[0]["event_type"] == "task_received"
        db.close()
