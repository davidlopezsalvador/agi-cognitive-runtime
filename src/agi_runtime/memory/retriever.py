"""Episodic memory retrieval for the AGI Cognitive Runtime."""

from __future__ import annotations

from pydantic import BaseModel, Field

from agi_runtime.memory.models import Episode, Memory
from agi_runtime.types import BaseSchema


class RetrievedEpisode(BaseSchema):
    """An episode retrieved for relevance to a task."""

    episode: Episode
    relevance_score: float = Field(ge=0.0, le=1.0)
    matched_keywords: list[str] = Field(default_factory=list)
    applicable_lessons: list[str] = Field(default_factory=list)


class EpisodicRetriever:
    """Retrieves relevant past experiences from episodic memory."""

    def __init__(self, memory: Memory) -> None:
        self.memory = memory

    def retrieve(self, task: str, limit: int = 5) -> list[RetrievedEpisode]:
        task_lower = task.lower()
        task_terms = set(task_lower.split())
        scored: list[tuple[float, Episode, list[str]]] = []

        for ep in self.memory.episodes:
            score, matched = self._score_episode(ep, task_lower, task_terms)
            if score > 0:
                scored.append((score, ep, matched))

        scored.sort(key=lambda x: x[0], reverse=True)
        results: list[RetrievedEpisode] = []
        for score, ep, matched in scored[:limit]:
            results.append(RetrievedEpisode(
                episode=ep,
                relevance_score=min(score, 1.0),
                matched_keywords=matched,
                applicable_lessons=[ep.lesson] if ep.lesson else [],
            ))
        return results

    def _score_episode(
        self, ep: Episode, task_lower: str, task_terms: set[str]
    ) -> tuple[float, list[str]]:
        score = 0.0
        matched: list[str] = []

        if task_lower in ep.task.lower():
            score += 5.0
            matched.append("task_match")

        ep_terms = set(ep.task.lower().split())
        overlap = task_terms & ep_terms
        score += len(overlap) * 1.0
        matched.extend(overlap)

        if ep.lesson:
            lesson_lower = ep.lesson.lower()
            for term in task_terms:
                if term in lesson_lower:
                    score += 2.0
                    matched.append(f"lesson:{term}")

        if ep.result:
            for term in task_terms:
                if term in ep.result.lower():
                    score += 0.5

        if ep.failure:
            for term in task_terms:
                if term in ep.failure.lower():
                    score += 1.5
                    matched.append(f"failure:{term}")

        return score, matched

    def find_structurally_similar(self, task: str, limit: int = 3) -> list[RetrievedEpisode]:
        task_lower = task.lower()
        structural_keywords = self._extract_structural_keywords(task_lower)

        scored: list[tuple[float, Episode, list[str]]] = []
        for ep in self.memory.episodes:
            ep_structural = self._extract_structural_keywords(ep.task.lower())
            overlap = structural_keywords & ep_structural
            if overlap:
                score = len(overlap) / max(len(structural_keywords), 1)
                scored.append((score, ep, list(overlap)))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [
            RetrievedEpisode(
                episode=ep,
                relevance_score=score,
                matched_keywords=matched,
                applicable_lessons=[ep.lesson] if ep.lesson else [],
            )
            for score, ep, matched in scored[:limit]
        ]

    def _extract_structural_keywords(self, text: str) -> set[str]:
        structural = {
            "debug", "fix", "investigate", "optimize", "refactor", "design",
            "build", "test", "deploy", "monitor", "scale", "migrate",
            "error", "failure", "bug", "performance", "security", "latency",
            "timeout", "crash", "leak", "race", "deadlock", "bottleneck",
        }
        words = set(text.split())
        return words & structural
