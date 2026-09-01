"""Tests for core types."""

from agi_runtime.types import (
    AutonomyLevel,
    CognitiveDepth,
    CognitiveEvent,
    EpistemicStatus,
    FailureType,
    GoalStatus,
    HypothesisStatus,
    PlanStatus,
    StepStatus,
)


def test_epistemic_status_values():
    assert EpistemicStatus.FACT == "fact"
    assert EpistemicStatus.HYPOTHESIS == "hypothesis"


def test_cognitive_depth_values():
    assert CognitiveDepth.L0_DIRECT == "L0_direct"
    assert CognitiveDepth.L6_LONG_HORIZON == "L6_long_horizon"


def test_goal_status_values():
    assert GoalStatus.ACTIVE == "active"
    assert GoalStatus.COMPLETED == "completed"


def test_plan_status_values():
    assert PlanStatus.DRAFT == "draft"
    assert PlanStatus.EXECUTING == "executing"


def test_step_status_values():
    assert StepStatus.PENDING == "pending"
    assert StepStatus.COMPLETED == "completed"


def test_hypothesis_status_values():
    assert HypothesisStatus.CANDIDATE == "candidate"
    assert HypothesisStatus.REFUTED == "refuted"


def test_autonomy_level_values():
    assert AutonomyLevel.A0_ASSISTANT == "A0_assistant"
    assert AutonomyLevel.A5_PERSISTENT == "A5_persistent"


def test_failure_type_values():
    assert FailureType.UNKNOWN == "unknown"
    assert FailureType.BUDGET_EXCEEDED == "budget_exceeded"


def test_cognitive_event_values():
    assert CognitiveEvent.TASK_STARTED == "task_started"
    assert CognitiveEvent.TASK_COMPLETED == "task_completed"
