"""Metacognition models for the AGI Cognitive Runtime."""

from __future__ import annotations

from pydantic import BaseModel, Field


class MetacognitiveState(BaseModel):
    """Dedicated metacognitive state."""

    current_confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    strongest_assumption: str = ""
    weakest_assumption: str = ""
    known_unknowns: list[str] = Field(default_factory=list)
    uncertainty_sources: list[str] = Field(default_factory=list)
    possible_biases: list[str] = Field(default_factory=list)
    alternative_strategies: list[str] = Field(default_factory=list)
    failure_risk: float = Field(default=0.5, ge=0.0, le=1.0)
    verification_status: str = ""

    def should_proceed(self) -> bool:
        return self.current_confidence >= 0.6 and self.failure_risk <= 0.5

    def should_investigate(self) -> bool:
        return len(self.known_unknowns) > 0 or self.current_confidence < 0.4

    def should_ask_user(self) -> bool:
        return self.failure_risk >= 0.7 or len(self.uncertainty_sources) > 3

    def summary(self) -> str:
        parts = [f"Confidence: {self.current_confidence:.0%}"]
        if self.known_unknowns:
            parts.append(f"Unknowns: {len(self.known_unknowns)}")
        if self.alternative_strategies:
            parts.append(f"Alternatives: {len(self.alternative_strategies)}")
        return " | ".join(parts)
