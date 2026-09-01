"""World model for the AGI Cognitive Runtime."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field

from agi_runtime.types import BaseSchema, EpistemicStatus


class WorldModelEntry(BaseSchema):
    """Entry in the world model."""

    entity: str = Field(description="What this entry is about")
    state: str = Field(description="Current state of the entity")
    properties: dict[str, Any] = Field(default_factory=dict)
    relationships: list[str] = Field(default_factory=list)
    observations: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    source: str = Field(default="", description="Where this knowledge came from")
    last_verified: datetime | None = None

    def verify(self) -> None:
        """Mark this entry as verified."""
        self.last_verified = datetime.now(timezone.utc)


class Belief(BaseSchema):
    """A belief with explicit epistemic status."""

    claim: str = Field(description="What is believed")
    status: EpistemicStatus = EpistemicStatus.UNKNOWN
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    evidence: list[str] = Field(default_factory=list)
    counter_evidence: list[str] = Field(default_factory=list)
    source: str = Field(default="")
    last_checked: datetime | None = None


class WorldModel(BaseModel):
    """The agent's model of the world."""

    entries: list[WorldModelEntry] = Field(default_factory=list)
    beliefs: list[Belief] = Field(default_factory=list)

    def add_entry(self, entry: WorldModelEntry) -> None:
        self.entries.append(entry)

    def add_belief(self, belief: Belief) -> None:
        self.beliefs.append(belief)

    def get_entity(self, entity: str) -> WorldModelEntry | None:
        for e in self.entries:
            if e.entity == entity:
                return e
        return None

    def update_belief(self, belief_id: str, **kwargs: Any) -> None:
        for b in self.beliefs:
            if b.id == belief_id:
                for k, v in kwargs.items():
                    setattr(b, k, v)
                break

    def facts(self) -> list[Belief]:
        return [b for b in self.beliefs if b.status == EpistemicStatus.FACT]

    def assumptions(self) -> list[Belief]:
        return [b for b in self.beliefs if b.status == EpistemicStatus.ASSUMPTION]

    def hypotheses(self) -> list[Belief]:
        return [b for b in self.beliefs if b.status == EpistemicStatus.HYPOTHESIS]

    def unknowns(self) -> list[Belief]:
        return [b for b in self.beliefs if b.status == EpistemicStatus.UNKNOWN]
