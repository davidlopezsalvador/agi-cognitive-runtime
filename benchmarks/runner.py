"""Benchmark runner for the AGI Cognitive Runtime."""

from __future__ import annotations

import time
from typing import Any

from benchmarks import BenchmarkCategory, BenchmarkResult, BenchmarkSuite, BenchmarkTask
from agi_runtime.runtime import CognitiveRuntime, RuntimeResult


class BenchmarkRunner:
    """Runs benchmarks against the cognitive runtime."""

    def __init__(self, runtime: CognitiveRuntime) -> None:
        self.runtime = runtime

    def run_task(self, task: BenchmarkTask) -> BenchmarkResult:
        start = time.time()

        try:
            result = self.runtime.run(
                task.description,
                desired_outcome=task.expected_output,
            )

            passed = self._evaluate(task, result)
            score = self._score(task, result)

            return BenchmarkResult(
                task_id=task.id,
                passed=passed,
                score=score,
                output=result.answer[:1000],
                metrics={
                    "depth": result.depth.value,
                    "duration": result.duration_seconds,
                    "steps": len(result.plan.steps) if result.plan else 0,
                    "has_verification": bool(result.verification),
                    "lesson_count": len(result.lessons),
                },
                duration_seconds=time.time() - start,
            )
        except Exception as e:
            return BenchmarkResult(
                task_id=task.id,
                passed=False,
                score=0.0,
                error=str(e),
                duration_seconds=time.time() - start,
            )

    def run_suite(self, suite: BenchmarkSuite) -> BenchmarkSuite:
        for task in suite.tasks:
            result = self.run_task(task)
            suite.results.append(result)
        return suite

    def run_all(self, tasks: list[BenchmarkTask]) -> BenchmarkSuite:
        suite = BenchmarkSuite(name="Full Benchmark Run", tasks=tasks)
        return self.run_suite(suite)

    def _evaluate(self, task: BenchmarkTask, result: RuntimeResult) -> bool:
        if not result.success:
            return False

        output_lower = result.answer.lower()
        criteria_met = 0
        for criterion in task.success_criteria:
            criterion_lower = criterion.lower()
            keywords = [w for w in criterion_lower.split() if len(w) > 3]
            if any(kw in output_lower for kw in keywords):
                criteria_met += 1

        return criteria_met >= len(task.success_criteria) * 0.5

    def _score(self, task: BenchmarkTask, result: RuntimeResult) -> float:
        if not result.success:
            return 0.0

        score = 0.0
        output_lower = result.answer.lower()

        for criterion in task.success_criteria:
            criterion_lower = criterion.lower()
            keywords = [w for w in criterion_lower.split() if len(w) > 3]
            if any(kw in output_lower for kw in keywords):
                score += 1.0

        if result.verification:
            score += 0.5
        if result.lessons:
            score += 0.5
        if result.plan and result.plan.steps:
            score += 0.5

        max_score = len(task.success_criteria) + 1.5
        return min(score / max_score, 1.0) if max_score > 0 else 0.0

    def summary(self, suite: BenchmarkSuite) -> dict[str, Any]:
        return {
            "total_tasks": len(suite.tasks),
            "completed": len(suite.results),
            "passed": sum(1 for r in suite.results if r.passed),
            "pass_rate": suite.pass_rate(),
            "average_score": suite.average_score(),
            "total_duration": sum(r.duration_seconds for r in suite.results),
            "by_category": {
                cat.value: len(suite.by_category(cat))
                for cat in BenchmarkCategory
            },
        }
