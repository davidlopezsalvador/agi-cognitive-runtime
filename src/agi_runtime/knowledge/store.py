"""Knowledge store for the AGI Cognitive Runtime."""

from __future__ import annotations

from pydantic import BaseModel, Field

from agi_runtime.types import BaseSchema


class KnowledgeEntry(BaseSchema):
    """A structured knowledge entry."""

    id: str = Field(description="e.g. reasoning.abduction.basic")
    version: int = 1
    type: str = Field(description="principle, heuristic, procedure, concept, pattern, anti_pattern")
    domain: list[str] = Field(default_factory=list)
    name: str = ""
    description: str = ""
    summary: str = ""
    heuristics: list[str] = Field(default_factory=list)
    triggers: list[str] = Field(default_factory=list)
    procedure: list[str] = Field(default_factory=list)
    anti_patterns: list[str] = Field(default_factory=list)
    verification_questions: list[str] = Field(default_factory=list)
    examples: list[str] = Field(default_factory=list)
    source: str = ""
    tags: list[str] = Field(default_factory=list)


class KnowledgeStore(BaseModel):
    """In-memory knowledge store with lexical retrieval."""

    entries: list[KnowledgeEntry] = Field(default_factory=list)

    def add(self, entry: KnowledgeEntry) -> None:
        self.entries.append(entry)

    def get(self, entry_id: str) -> KnowledgeEntry | None:
        for e in self.entries:
            if e.id == entry_id:
                return e
        return None

    def search(self, query: str, limit: int = 10) -> list[KnowledgeEntry]:
        query_lower = query.lower()
        query_terms = set(query_lower.split())
        scored: list[tuple[float, KnowledgeEntry]] = []
        for e in self.entries:
            score = 0.0
            text = f"{e.name} {e.description} {e.summary} {' '.join(e.tags)} {' '.join(e.domain)}".lower()
            for term in query_terms:
                if term in text:
                    score += 1.0
            if query_lower in text:
                score += 2.0
            if score > 0:
                scored.append((score, e))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [e for _, e in scored[:limit]]

    def by_domain(self, domain: str) -> list[KnowledgeEntry]:
        return [e for e in self.entries if domain in e.domain]

    def by_type(self, entry_type: str) -> list[KnowledgeEntry]:
        return [e for e in self.entries if e.type == entry_type]

    def by_trigger(self, trigger: str) -> list[KnowledgeEntry]:
        return [e for e in self.entries if trigger in e.triggers]
