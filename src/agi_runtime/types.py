"""Base types and enums for the AGI Cognitive Runtime."""

from __future__ import annotations

import enum
import uuid
from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _uuid() -> str:
    return str(uuid.uuid4())


class EpistemicStatus(str, enum.Enum):
    """Status of a belief or claim."""

    FACT = "fact"
    OBSERVATION = "observation"
    INFERENCE = "inference"
    ASSUMPTION = "assumption"
    HYPOTHESIS = "hypothesis"
    UNKNOWN = "unknown"


class CognitiveDepth(str, enum.Enum):
    """Adaptive cognitive depth levels."""

    L0_DIRECT = "L0_direct"
    L1_REASON = "L1_reason"
    L2_PLAN = "L2_plan"
    L3_INVESTIGATE = "L3_investigate"
    L4_EXPERIMENT = "L4_experiment"
    L5_ADAPT = "L5_adapt"
    L6_LONG_HORIZON = "L6_long_horizon"


class GoalStatus(str, enum.Enum):
    """Status of a goal."""

    ACTIVE = "active"
    BLOCKED = "blocked"
    PAUSED = "paused"
    FAILED = "failed"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class PlanStatus(str, enum.Enum):
    """Status of a plan."""

    DRAFT = "draft"
    ACTIVE = "active"
    EXECUTING = "executing"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    REPLANNING = "replanning"


class StepStatus(str, enum.Enum):
    """Status of a plan step."""

    PENDING = "pending"
    READY = "ready"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"
    BLOCKED = "blocked"


class HypothesisStatus(str, enum.Enum):
    """Status of a hypothesis."""

    CANDIDATE = "candidate"
    TESTED = "tested"
    SUPPORTED = "supported"
    REFUTED = "refuted"
    INCONCLUSIVE = "inconclusive"


class AutonomyLevel(str, enum.Enum):
    """Agent autonomy levels."""

    A0_ASSISTANT = "A0_assistant"
    A1_TOOL_USER = "A1_tool_user"
    A2_TASK_EXECUTOR = "A2_task_executor"
    A3_AUTONOMOUS_INVESTIGATOR = "A3_autonomous_investigator"
    A4_LONG_HORIZON = "A4_long_horizon"
    A5_PERSISTENT = "A5_persistent"


class FailureType(str, enum.Enum):
    """Types of cognitive failures."""

    UNKNOWN = "unknown"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    PLAN_FAILED = "plan_failed"
    TOOL_FAILED = "tool_failed"
    HYPOTHESIS_REJECTED = "hypothesis_rejected"
    VERIFICATION_FAILED = "verification_failed"
    BUDGET_EXCEEDED = "budget_exceeded"
    USER_INPUT_REQUIRED = "user_input_required"


class CognitiveEvent(str, enum.Enum):
    """Events for structured logging."""

    TASK_STARTED = "task_started"
    TASK_CLASSIFIED = "task_classified"
    GOAL_CREATED = "goal_created"
    PLAN_CREATED = "plan_created"
    HYPOTHESIS_CREATED = "hypothesis_created"
    TOOL_CALLED = "tool_called"
    OBSERVATION_RECEIVED = "observation_received"
    BELIEF_UPDATED = "belief_updated"
    PLAN_CHANGED = "plan_changed"
    VERIFICATION_STARTED = "verification_started"
    VERIFICATION_FAILED = "verification_failed"
    LEARNING_STARTED = "learning_started"
    LESSON_CREATED = "lesson_created"
    TASK_COMPLETED = "task_completed"


class BaseSchema(BaseModel):
    """Base schema with common fields."""

    id: str = Field(default_factory=_uuid)
    created: datetime = Field(default_factory=_now)
    updated: datetime = Field(default_factory=_now)

    def model_post_init(self, __context: Any) -> None:
        self.updated = _now()
