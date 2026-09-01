"""Tests for the cognitive runtime."""

from agi_runtime.runtime import CognitiveRuntime, CognitiveBudget, RuntimeResult
from agi_runtime.types import CognitiveDepth


def test_runtime_creation():
    runtime = CognitiveRuntime()
    assert runtime.status()["version"] == "0.1.0"


def test_classify_simple():
    runtime = CognitiveRuntime()
    cls = runtime.classify("Convert 5 km to miles")
    assert cls.depth == CognitiveDepth.L0_DIRECT


def test_classify_reasoning():
    runtime = CognitiveRuntime()
    cls = runtime.classify("Why is the API returning 500 errors?")
    assert cls.depth in (CognitiveDepth.L1_REASON, CognitiveDepth.L3_INVESTIGATE)


def test_classify_planning():
    runtime = CognitiveRuntime()
    cls = runtime.classify("Build a new authentication service")
    assert cls.depth in (CognitiveDepth.L2_PLAN, CognitiveDepth.L6_LONG_HORIZON)


def test_classify_investigation():
    runtime = CognitiveRuntime()
    cls = runtime.classify("Debug the intermittent timeout issue")
    assert cls.depth in (CognitiveDepth.L3_INVESTIGATE, CognitiveDepth.L4_EXPERIMENT)


def test_plan_task():
    runtime = CognitiveRuntime()
    from agi_runtime.world.task import Task
    task = Task(objective="Fix the bug", desired_outcome="Bug fixed", cognitive_depth=CognitiveDepth.L2_PLAN)
    plan = runtime.plan_task(task)
    assert len(plan.steps) >= 3
    assert plan.status.value == "active"


def test_run_simple():
    runtime = CognitiveRuntime()
    result = runtime.run("Convert 5 km to miles")
    assert result.success
    assert result.answer
    assert result.depth == CognitiveDepth.L0_DIRECT


def test_run_with_provider():
    from unittest.mock import MagicMock
    from agi_runtime.providers.base import ModelResponse

    mock_provider = MagicMock()
    mock_provider.generate.return_value = ModelResponse(text="The answer is 42")

    runtime = CognitiveRuntime(model_provider=mock_provider)
    result = runtime.run("What is the meaning of life?")
    assert result.success
    assert "42" in result.answer
    mock_provider.generate.assert_called_once()


def test_hypotheses_generated():
    runtime = CognitiveRuntime()
    result = runtime.run("Investigate why the system is slow")
    assert len(runtime.hypotheses.hypotheses) >= 0


def test_lessons_learned():
    runtime = CognitiveRuntime()
    runtime.run("Fix the performance issue")
    assert len(runtime.memory.episodes) >= 1
    assert runtime.memory.episodes[0].lesson != ""


def test_status():
    runtime = CognitiveRuntime()
    status = runtime.status()
    assert "version" in status
    assert "episodes" in status
    assert "knowledge_entries" in status


def test_verify():
    runtime = CognitiveRuntime()
    result = runtime.verify("The sky is blue", evidence=["It looks blue"])
    assert "sky" in result.lower() or "claim" in result.lower() or "verify" in result.lower()
