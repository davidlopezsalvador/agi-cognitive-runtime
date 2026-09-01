"""Transfer learning for the AGI Cognitive Runtime."""

from __future__ import annotations

from pydantic import BaseModel, Field

from agi_runtime.types import BaseSchema


class StructuralSimilarity(BaseSchema):
    """A detected structural similarity between problems."""

    source_domain: str
    target_domain: str
    shared_abstraction: str
    source_example: str = ""
    target_example: str = ""
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    transferable_elements: list[str] = Field(default_factory=list)


class TransferEngine:
    """Engine for cross-domain knowledge transfer."""

    def find_structural_similarities(
        self, problem: str, experiences: list[str]
    ) -> list[StructuralSimilarity]:
        similarities: list[StructuralSimilarity] = []
        problem_lower = problem.lower()
        for exp in experiences:
            exp_lower = exp.lower()
            shared_terms = set(problem_lower.split()) & set(exp_lower.split())
            if len(shared_terms) >= 2:
                similarities.append(
                    StructuralSimilarity(
                        source_domain="experience",
                        target_domain="current",
                        shared_abstraction=" ".join(shared_terms),
                        source_example=exp,
                        target_example=problem,
                        confidence=min(len(shared_terms) / 5.0, 1.0),
                    )
                )
        return sorted(similarities, key=lambda s: s.confidence, reverse=True)

    def abstract_principle(self, examples: list[str]) -> str:
        if not examples:
            return ""
        return f"General principle derived from {len(examples)} examples"

    def apply_transfer(
        self, principle: str, source_domain: str, target_domain: str
    ) -> str:
        return f"Applying '{principle}' from {source_domain} to {target_domain}"
