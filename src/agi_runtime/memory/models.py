"""Memory models for the AGI Cognitive Runtime."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from agi_runtime.types import BaseSchema


class WorkingMemory(BaseModel):
    """Temporary state for the current reasoning process."""

    current_goal: str = ""
    active_constraints: list[str] = Field(default_factory=list)
    current_plan_id: str | None = None
    active_hypothesis_ids: list[str] = Field(default_factory=list)
    recent_observations: list[str] = Field(default_factory=list)
    unresolved_questions: list[str] = Field(default_factory=list)
    context: dict[str, Any] = Field(default_factory=dict)

    def clear(self) -> None:
        self.current_goal = ""
        self.active_constraints.clear()
        self.current_plan_id = None
        self.active_hypothesis_ids.clear()
        self.recent_observations.clear()
        self.unresolved_questions.clear()
        self.context.clear()


class Episode(BaseSchema):
    """An experience stored in episodic memory."""

    task: str = Field(description="What was the task")
    context: str = Field(default="", description="Relevant context")
    actions: list[str] = Field(default_factory=list, description="What was done")
    result: str = Field(default="", description="What happened")
    failure: str = Field(default="", description="What went wrong, if anything")
    lesson: str = Field(default="", description="What was learned")
    tags: list[str] = Field(default_factory=list)


class SemanticEntry(BaseSchema):
    """A generalized knowledge entry in semantic memory."""

    concept: str
    principle: str = ""
    description: str = ""
    domain: list[str] = Field(default_factory=list)
    examples: list[str] = Field(default_factory=list)
    source_episode_ids: list[str] = Field(default_factory=list)


class ProceduralSkill(BaseSchema):
    """A reusable skill in procedural memory."""

    name: str
    purpose: str = ""
    preconditions: list[str] = Field(default_factory=list)
    procedure: list[str] = Field(default_factory=list)
    expected_outcomes: list[str] = Field(default_factory=list)
    failure_modes: list[str] = Field(default_factory=list)
    verification: list[str] = Field(default_factory=list)
    examples: list[str] = Field(default_factory=list)
    success_count: int = 0
    failure_count: int = 0

    @property
    def success_rate(self) -> float:
        total = self.success_count + self.failure_count
        return self.success_count / total if total > 0 else 0.0


class FailureRecord(BaseSchema):
    """A record of a failure for learning."""

    task: str
    attempted_strategy: str = ""
    failure: str = ""
    cause: str = ""
    evidence: list[str] = Field(default_factory=list)
    corrected_strategy: str = ""
    reusable_lesson: str = ""


class Memory(BaseModel):
    """Unified memory interface."""

    working: WorkingMemory = Field(default_factory=WorkingMemory)
    episodes: list[Episode] = Field(default_factory=list)
    semantic: list[SemanticEntry] = Field(default_factory=list)
    procedural: list[ProceduralSkill] = Field(default_factory=list)
    failures: list[FailureRecord] = Field(default_factory=list)

    def store_episode(self, episode: Episode) -> None:
        self.episodes.append(episode)

    def store_semantic(self, entry: SemanticEntry) -> None:
        self.semantic.append(entry)

    def store_skill(self, skill: ProceduralSkill) -> None:
        self.procedural.append(skill)

    def store_failure(self, record: FailureRecord) -> None:
        self.failures.append(record)

    def find_similar_episodes(self, task: str, limit: int = 5) -> list[Episode]:
        task_lower = task.lower()
        scored = []
        for ep in self.episodes:
            score = 0
            if task_lower in ep.task.lower():
                score += 3
            if task_lower in ep.context.lower():
                score += 1
            if ep.lesson:
                score += 1
            scored.append((score, ep))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [ep for _, ep in scored[:limit]]

    def find_relevant_skills(self, task: str) -> list[ProceduralSkill]:
        task_lower = task.lower()
        return [
            s
            for s in self.procedural
            if task_lower in s.name.lower() or task_lower in s.purpose.lower()
        ]

    def find_related_failures(self, task: str) -> list[FailureRecord]:
        task_lower = task.lower()
        return [
            f
            for f in self.failures
            if task_lower in f.task.lower() or task_lower in f.cause.lower()
        ]
