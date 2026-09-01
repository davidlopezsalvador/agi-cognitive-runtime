"""Task model for the AGI Cognitive Runtime."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from agi_runtime.types import BaseSchema, CognitiveDepth


class Task(BaseSchema):
    """Structured task representation."""

    objective: str = Field(description="What the task is trying to achieve")
    desired_outcome: str = Field(description="What success looks like")
    literal_request: str = Field(default="", description="The user's literal request")
    constraints: list[str] = Field(default_factory=list)
    resources: list[str] = Field(default_factory=list)
    environment: str = Field(default="", description="Relevant environment context")
    deadline: str | None = None
    uncertainty: str = Field(default="", description="What is uncertain about this task")
    success_criteria: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    unknowns: list[str] = Field(default_factory=list)
    cognitive_depth: CognitiveDepth = CognitiveDepth.L0_DIRECT
    metadata: dict[str, Any] = Field(default_factory=dict)


class TaskClassification(BaseModel):
    """Classification of a task's cognitive requirements."""

    depth: CognitiveDepth
    domain: str
    complexity: float = Field(ge=0.0, le=1.0, description="0=simple, 1=complex")
    uncertainty_level: float = Field(ge=0.0, le=1.0)
    requires_planning: bool = False
    requires_hypotheses: bool = False
    requires_verification: bool = False
    requires_learning: bool = False
    reasoning: str = Field(default="", description="Why this classification was chosen")
