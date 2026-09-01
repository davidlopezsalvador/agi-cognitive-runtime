"""Plan model for the AGI Cognitive Runtime."""

from __future__ import annotations

from pydantic import BaseModel, Field

from agi_runtime.types import BaseSchema, PlanStatus, StepStatus


class PlanStep(BaseSchema):
    """A single step in a plan."""

    action: str = Field(description="What to do")
    dependencies: list[str] = Field(default_factory=list, description="IDs of prerequisite steps")
    expected_result: str = Field(default="")
    verification: str = Field(default="", description="How to verify this step succeeded")
    rollback: str = Field(default="", description="How to undo if this fails")
    status: StepStatus = StepStatus.PENDING
    result: str = Field(default="")
    error: str = Field(default="")

    def complete(self, result: str = "") -> None:
        self.status = StepStatus.COMPLETED
        self.result = result

    def fail(self, error: str = "") -> None:
        self.status = StepStatus.FAILED
        self.error = error


class Plan(BaseSchema):
    """A plan for achieving a goal."""

    objective: str
    assumptions: list[str] = Field(default_factory=list)
    steps: list[PlanStep] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    stopping_conditions: list[str] = Field(default_factory=list)
    status: PlanStatus = PlanStatus.DRAFT

    def ready_steps(self) -> list[PlanStep]:
        """Steps whose dependencies are all completed."""
        completed_ids = {s.id for s in self.steps if s.status == StepStatus.COMPLETED}
        return [
            s
            for s in self.steps
            if s.status == StepStatus.PENDING
            and all(d in completed_ids for d in s.dependencies)
        ]

    def progress(self) -> float:
        if not self.steps:
            return 0.0
        done = sum(1 for s in self.steps if s.status == StepStatus.COMPLETED)
        return done / len(self.steps)

    def is_complete(self) -> bool:
        return all(s.status in (StepStatus.COMPLETED, StepStatus.SKIPPED) for s in self.steps)

    def has_failures(self) -> bool:
        return any(s.status == StepStatus.FAILED for s in self.steps)
