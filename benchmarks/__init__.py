"""Benchmark framework for the AGI Cognitive Runtime."""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class BenchmarkCategory(str, Enum):
    REASONING = "reasoning"
    ABSTRACTION = "abstraction"
    PLANNING = "planning"
    ADAPTATION = "adaptation"
    LEARNING = "learning"
    TRANSFER = "transfer"
    VERIFICATION = "verification"
    CODING = "coding"
    RESEARCH = "research"
    GENERALIZATION = "generalization"


class BenchmarkTask(BaseModel):
    """A benchmark task for evaluation."""

    id: str
    category: BenchmarkCategory
    name: str
    description: str = ""
    input_data: dict[str, Any] = Field(default_factory=dict)
    expected_output: str = ""
    success_criteria: list[str] = Field(default_factory=list)
    difficulty: int = Field(default=1, ge=1, le=5)
    tags: list[str] = Field(default_factory=list)


class BenchmarkResult(BaseModel):
    """Result of running a benchmark task."""

    task_id: str
    passed: bool = False
    score: float = Field(default=0.0, ge=0.0, le=1.0)
    output: str = ""
    metrics: dict[str, Any] = Field(default_factory=dict)
    duration_seconds: float = 0.0
    error: str = ""


class BenchmarkSuite(BaseModel):
    """A collection of benchmark tasks."""

    name: str
    tasks: list[BenchmarkTask] = Field(default_factory=list)
    results: list[BenchmarkResult] = Field(default_factory=list)

    def pass_rate(self) -> float:
        if not self.results:
            return 0.0
        passed = sum(1 for r in self.results if r.passed)
        return passed / len(self.results)

    def average_score(self) -> float:
        if not self.results:
            return 0.0
        return sum(r.score for r in self.results) / len(self.results)

    def by_category(self, category: BenchmarkCategory) -> list[BenchmarkResult]:
        task_ids = {t.id for t in self.tasks if t.category == category}
        return [r for r in self.results if r.task_id in task_ids]
