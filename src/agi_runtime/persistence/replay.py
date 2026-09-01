"""Cognitive replay for the AGI Cognitive Runtime."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from agi_runtime.runtime import CognitiveTrace, RuntimeResult
from agi_runtime.persistence.session import SessionPersistence


class ReplayStep(BaseModel):
    """A single step in a cognitive replay."""

    step: int
    event_type: str
    description: str = ""
    data: dict[str, Any] = Field(default_factory=dict)
    timestamp: str = ""


class CognitiveReplay:
    """Reproduces cognitive runs from saved state."""

    def __init__(self, persistence: SessionPersistence | None = None) -> None:
        self.persistence = persistence or SessionPersistence()

    def replay_snapshot(self, snapshot_id: str) -> list[ReplayStep]:
        snap = self.persistence.load_snapshot(snapshot_id)
        if not snap:
            return []

        steps: list[ReplayStep] = []

        steps.append(ReplayStep(
            step=0,
            event_type="task_received",
            description=f"Task: {snap['task']}",
            data={"task": snap["task"], "depth": snap["depth"]},
        ))

        trace_data = snap["trace"]
        if isinstance(trace_data, dict):
            if trace_data.get("cognitive_mode"):
                steps.append(ReplayStep(
                    step=1,
                    event_type="classification",
                    description=f"Classified as {trace_data['cognitive_mode']}",
                    data={"mode": trace_data["cognitive_mode"]},
                ))

            for i, decision in enumerate(trace_data.get("decisions", [])):
                steps.append(ReplayStep(
                    step=2 + i,
                    event_type="decision",
                    description=decision,
                ))

            for i, obs in enumerate(trace_data.get("observations", [])):
                steps.append(ReplayStep(
                    step=10 + i,
                    event_type="observation",
                    description=obs,
                ))

            for i, action in enumerate(trace_data.get("actions", [])):
                steps.append(ReplayStep(
                    step=20 + i,
                    event_type="action",
                    description=action,
                ))

            if trace_data.get("verification"):
                steps.append(ReplayStep(
                    step=30,
                    event_type="verification",
                    description=trace_data["verification"],
                ))

            for i, lesson in enumerate(trace_data.get("lessons", [])):
                steps.append(ReplayStep(
                    step=40 + i,
                    event_type="lesson",
                    description=lesson,
                ))

        steps.append(ReplayStep(
            step=100,
            event_type="task_completed",
            description=f"Answer: {snap['answer'][:200]}",
            data={"answer": snap["answer"]},
        ))

        return steps

    def replay_session(self, session_id: str) -> list[list[ReplayStep]]:
        snapshots = self.persistence.list_snapshots(session_id)
        all_replays: list[list[ReplayStep]] = []
        for snap_info in snapshots:
            steps = self.replay_snapshot(snap_info["id"])
            all_replays.append(steps)
        return all_replays

    def summary(self, snapshot_id: str) -> dict[str, Any]:
        steps = self.replay_snapshot(snapshot_id)
        return {
            "total_steps": len(steps),
            "event_types": list(set(s.event_type for s in steps)),
            "steps": [
                {"step": s.step, "type": s.event_type, "description": s.description[:100]}
                for s in steps
            ],
        }

    def compare_traces(self, snapshot_id_a: str, snapshot_id_b: str) -> dict[str, Any]:
        steps_a = self.replay_snapshot(snapshot_id_a)
        steps_b = self.replay_snapshot(snapshot_id_b)

        types_a = set(s.event_type for s in steps_a)
        types_b = set(s.event_type for s in steps_b)

        return {
            "trace_a_steps": len(steps_a),
            "trace_b_steps": len(steps_b),
            "shared_events": list(types_a & types_b),
            "only_in_a": list(types_a - types_b),
            "only_in_b": list(types_b - types_a),
        }
