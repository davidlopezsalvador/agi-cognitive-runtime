"""Hypothesis engine for the AGI Cognitive Runtime."""

from __future__ import annotations

from pydantic import BaseModel, Field

from agi_runtime.types import BaseSchema, HypothesisStatus


class Hypothesis(BaseSchema):
    """A hypothesis for uncertain problems."""

    statement: str = Field(description="What is hypothesized")
    prior_confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    supporting_evidence: list[str] = Field(default_factory=list)
    contradictory_evidence: list[str] = Field(default_factory=list)
    predictions: list[str] = Field(default_factory=list, description="What we expect if true")
    tests: list[str] = Field(default_factory=list, description="How to test this")
    posterior_confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    status: HypothesisStatus = HypothesisStatus.CANDIDATE

    def add_supporting(self, evidence: str) -> None:
        self.supporting_evidence.append(evidence)
        self._update_confidence()

    def add_contradictory(self, evidence: str) -> None:
        self.contradictory_evidence.append(evidence)
        self._update_confidence()

    def _update_confidence(self) -> None:
        total = len(self.supporting_evidence) + len(self.contradictory_evidence)
        if total == 0:
            return
        ratio = len(self.supporting_evidence) / total
        self.posterior_confidence = 0.5 * self.prior_confidence + 0.5 * ratio

    def is_well_supported(self, threshold: float = 0.7) -> bool:
        return self.posterior_confidence >= threshold and len(self.supporting_evidence) >= 2

    def is_refuted(self, threshold: float = 0.2) -> bool:
        return self.posterior_confidence <= threshold or len(self.contradictory_evidence) >= 3


class HypothesisSpace(BaseModel):
    """Collection of hypotheses for a problem."""

    hypotheses: list[Hypothesis] = Field(default_factory=list)
    problem: str = Field(default="")

    def rank(self) -> list[Hypothesis]:
        return sorted(self.hypotheses, key=lambda h: h.posterior_confidence, reverse=True)

    def best(self) -> Hypothesis | None:
        ranked = self.rank()
        return ranked[0] if ranked else None

    def add(self, hypothesis: Hypothesis) -> None:
        self.hypotheses.append(hypothesis)

    def eliminate_refuted(self) -> list[Hypothesis]:
        refuted = [h for h in self.hypotheses if h.is_refuted()]
        self.hypotheses = [h for h in self.hypotheses if not h.is_refuted()]
        return refuted
