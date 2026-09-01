"""Tests for planning."""

from agi_runtime.planning.plan import Plan, PlanStep
from agi_runtime.types import PlanStatus, StepStatus


def test_plan_step():
    step = PlanStep(action="Run tests")
    assert step.status == StepStatus.PENDING
    step.complete("All tests passed")
    assert step.status == StepStatus.COMPLETED
    assert step.result == "All tests passed"


def test_plan_step_failure():
    step = PlanStep(action="Deploy")
    step.fail("Build failed")
    assert step.status == StepStatus.FAILED
    assert step.error == "Build failed"


def test_plan_creation():
    plan = Plan(objective="Fix the bug", steps=[PlanStep(action="Analyze"), PlanStep(action="Fix")])
    assert plan.status == PlanStatus.DRAFT
    assert len(plan.steps) == 2


def test_plan_progress():
    s1 = PlanStep(action="Step 1")
    s2 = PlanStep(action="Step 2")
    plan = Plan(objective="Test", steps=[s1, s2])

    assert plan.progress() == 0.0
    s1.complete()
    assert plan.progress() == 0.5
    s2.complete()
    assert plan.progress() == 1.0
    assert plan.is_complete()


def test_plan_ready_steps():
    s1 = PlanStep(action="Step 1")
    s2 = PlanStep(action="Step 2", dependencies=[s1.id])
    s3 = PlanStep(action="Step 3", dependencies=[s2.id])
    plan = Plan(objective="Test", steps=[s1, s2, s3])

    ready = plan.ready_steps()
    assert len(ready) == 1
    assert ready[0].action == "Step 1"

    s1.complete()
    ready = plan.ready_steps()
    assert len(ready) == 1
    assert ready[0].action == "Step 2"


def test_plan_has_failures():
    s1 = PlanStep(action="Step 1")
    plan = Plan(objective="Test", steps=[s1])
    assert not plan.has_failures()

    s1.fail("Error")
    assert plan.has_failures()
