"""Adaptive replanning for the AGI Cognitive Runtime."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from agi_runtime.planning.plan import Plan, PlanStep
from agi_runtime.types import StepStatus, PlanStatus
from agi_runtime.world.model import WorldModel, Belief
from agi_runtime.types import EpistemicStatus


class ReplanTrigger(BaseModel):
    """Reason for replanning."""

    trigger_type: str = ""
    description: str = ""
    severity: float = Field(default=0.5, ge=0.0, le=1.0)
    affected_steps: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class AdaptivePlanner:
    """Plans and adapts based on results."""

    def __init__(self) -> None:
        self.history: list[dict[str, Any]] = []

    def detect_failures(self, plan: Plan) -> list[ReplanTrigger]:
        triggers: list[ReplanTrigger] = []
        for step in plan.steps:
            if step.status == StepStatus.FAILED:
                triggers.append(ReplanTrigger(
                    trigger_type="step_failed",
                    description=f"Step '{step.action}' failed: {step.error}",
                    severity=0.8,
                    affected_steps=[step.id],
                ))
        return triggers

    def detect_assumption_violations(
        self, plan: Plan, world_model: WorldModel
    ) -> list[ReplanTrigger]:
        triggers: list[ReplanTrigger] = []
        for assumption in plan.assumptions:
            assumption_lower = assumption.lower()
            for belief in world_model.beliefs:
                if belief.status == EpistemicStatus.HYPOTHESIS:
                    if any(w in assumption_lower for w in belief.claim.lower().split()):
                        if belief.confidence < 0.3:
                            triggers.append(ReplanTrigger(
                                trigger_type="assumption_violated",
                                description=f"Assumption '{assumption}' contradicted by: {belief.claim}",
                                severity=0.7,
                            ))
        return triggers

    def detect_stalled(self, plan: Plan, max_stale_steps: int = 3) -> list[ReplanTrigger]:
        triggers: list[ReplanTrigger] = []
        executing = [s for s in plan.steps if s.status == StepStatus.EXECUTING]
        if len(executing) > max_stale_steps:
            triggers.append(ReplanTrigger(
                trigger_type="stalled",
                description=f"{len(executing)} steps stuck in executing state",
                severity=0.6,
            ))
        return triggers

    def replan(
        self,
        plan: Plan,
        triggers: list[ReplanTrigger],
        world_model: WorldModel | None = None,
    ) -> Plan:
        self.history.append({
            "plan_id": plan.id,
            "triggers": [t.model_dump() for t in triggers],
        })

        for step in plan.steps:
            if step.status == StepStatus.FAILED:
                if step.rollback:
                    plan.steps.append(PlanStep(
                        action=f"Recovery: {step.rollback}",
                        dependencies=[s.id for s in plan.steps if s.status == StepStatus.COMPLETED],
                    ))

        failed_ids = {s.id for s in plan.steps if s.status == StepStatus.FAILED}
        for step in plan.steps:
            if step.status == StepStatus.PENDING:
                step.dependencies = [d for d in step.dependencies if d not in failed_ids]

        plan.status = PlanStatus.REPLANNING
        plan.steps.append(PlanStep(
            action="Re-evaluate assumptions and verify progress",
        ))
        plan.status = PlanStatus.ACTIVE
        return plan

    def should_stop(self, plan: Plan, budget_remaining: float = 1.0) -> tuple[bool, str]:
        if plan.is_complete():
            return True, "Plan completed successfully"
        if plan.has_failures():
            failed = [s for s in plan.steps if s.status == StepStatus.FAILED]
            return True, f"{len(failed)} steps failed"
        if budget_remaining <= 0:
            return True, "Budget exhausted"
        return False, ""

    def summary(self, plan: Plan) -> dict[str, Any]:
        return {
            "plan_id": plan.id,
            "status": plan.status.value,
            "progress": plan.progress(),
            "total_steps": len(plan.steps),
            "completed": sum(1 for s in plan.steps if s.status == StepStatus.COMPLETED),
            "failed": sum(1 for s in plan.steps if s.status == StepStatus.FAILED),
            "pending": sum(1 for s in plan.steps if s.status == StepStatus.PENDING),
            "replan_count": len(self.history),
        }
