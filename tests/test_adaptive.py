"""Tests for adaptive replanning."""

from agi_runtime.planning.adaptive import AdaptivePlanner, ReplanTrigger
from agi_runtime.planning.plan import Plan, PlanStep
from agi_runtime.types import StepStatus


def test_detect_failures():
    planner = AdaptivePlanner()
    step = PlanStep(action="Do something")
    step.fail("It broke")
    plan = Plan(objective="Test", steps=[step])

    triggers = planner.detect_failures(plan)
    assert len(triggers) == 1
    assert triggers[0].trigger_type == "step_failed"


def test_no_failures():
    planner = AdaptivePlanner()
    step = PlanStep(action="Do something")
    step.complete("Done")
    plan = Plan(objective="Test", steps=[step])

    triggers = planner.detect_failures(plan)
    assert len(triggers) == 0


def test_replan():
    planner = AdaptivePlanner()
    step1 = PlanStep(action="Step 1")
    step1.complete("Done")
    step2 = PlanStep(action="Step 2")
    step2.fail("Error")
    plan = Plan(objective="Test", steps=[step1, step2])

    triggers = planner.detect_failures(plan)
    new_plan = planner.replan(plan, triggers)

    assert len(new_plan.steps) > 2
    assert new_plan.status.value == "active"


def test_should_stop_complete():
    planner = AdaptivePlanner()
    step = PlanStep(action="Step 1")
    step.complete("Done")
    plan = Plan(objective="Test", steps=[step])

    should, reason = planner.should_stop(plan)
    assert should
    assert "completed" in reason.lower()


def test_should_stop_failed():
    planner = AdaptivePlanner()
    step = PlanStep(action="Step 1")
    step.fail("Error")
    plan = Plan(objective="Test", steps=[step])

    should, reason = planner.should_stop(plan)
    assert should
    assert "failed" in reason.lower()


def test_summary():
    planner = AdaptivePlanner()
    step = PlanStep(action="Step 1")
    plan = Plan(objective="Test", steps=[step])
    summary = planner.summary(plan)

    assert "progress" in summary
    assert "total_steps" in summary
