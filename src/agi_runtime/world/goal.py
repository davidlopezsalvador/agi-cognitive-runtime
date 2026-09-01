"""Goal management for the AGI Cognitive Runtime."""

from __future__ import annotations

from pydantic import BaseModel, Field

from agi_runtime.types import BaseSchema, GoalStatus


class Goal(BaseSchema):
    """Explicit goal object."""

    description: str
    priority: int = Field(default=5, ge=1, le=10, description="1=highest, 10=lowest")
    parent_id: str | None = None
    status: GoalStatus = GoalStatus.ACTIVE
    success_conditions: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    deadline: str | None = None
    progress: float = Field(default=0.0, ge=0.0, le=1.0)
    dependencies: list[str] = Field(default_factory=list, description="IDs of dependent goals")


class GoalTree(BaseModel):
    """Tree of goals and subgoals."""

    goals: list[Goal] = Field(default_factory=list)

    def active_goals(self) -> list[Goal]:
        return [g for g in self.goals if g.status == GoalStatus.ACTIVE]

    def add_goal(self, goal: Goal) -> None:
        self.goals.append(goal)

    def complete_goal(self, goal_id: str) -> None:
        for g in self.goals:
            if g.id == goal_id:
                g.status = GoalStatus.COMPLETED
                g.progress = 1.0
                break
