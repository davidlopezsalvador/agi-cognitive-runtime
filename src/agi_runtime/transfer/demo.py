"""Transfer demo: cross-domain structural similarity."""

from __future__ import annotations

from pydantic import BaseModel, Field

from agi_runtime.types import BaseSchema
from agi_runtime.transfer.engine import TransferEngine
from agi_runtime.memory.models import Memory, Episode
from agi_runtime.memory.retriever import EpisodicRetriever
from agi_runtime.knowledge.store import KnowledgeStore


class TransferDemo(BaseSchema):
    """Demonstrates knowledge transfer across domains."""

    source_domain: str
    target_domain: str
    shared_abstraction: str
    source_experience: str = ""
    target_application: str = ""
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class TransferDemonstrator:
    """Demonstrates cross-domain knowledge transfer."""

    def __init__(
        self,
        transfer_engine: TransferEngine | None = None,
        memory: Memory | None = None,
        knowledge: KnowledgeStore | None = None,
    ) -> None:
        self.transfer = transfer_engine or TransferEngine()
        self.memory = memory or Memory()
        self.knowledge = knowledge or KnowledgeStore()
        self.retriever = EpisodicRetriever(self.memory)

    def demonstrate(self, source_task: str, target_task: str) -> TransferDemo:
        source_similar = self.retriever.find_structurally_similar(source_task, limit=3)
        target_similar = self.retriever.find_structurally_similar(target_task, limit=3)

        source_exp = [r.episode.task for r in source_similar]
        target_exp = [r.episode.task for r in target_similar]

        all_experiences = source_exp + target_exp
        similarities = self.transfer.find_structural_similarities(
            target_task, all_experiences
        )

        shared = ""
        if similarities:
            shared = similarities[0].shared_abstraction

        knowledge_matches = self.knowledge.search(source_task, limit=3)
        principles = [k.name for k in knowledge_matches if k.type == "principle"]

        abstraction = shared
        if not abstraction and principles:
            abstraction = f"Principles: {', '.join(principles[:3])}"

        confidence = 0.0
        if similarities:
            confidence = similarities[0].confidence
        elif principles:
            confidence = 0.4

        return TransferDemo(
            source_domain=source_task[:50],
            target_domain=target_task[:50],
            shared_abstraction=abstraction or "No structural similarity found",
            source_experience=source_task,
            target_application=target_task,
            confidence=confidence,
        )

    def full_transfer_demo(self) -> list[TransferDemo]:
        demos = [
            ("Debug network latency", "Investigate slow database queries"),
            ("Fix memory leak in cache", "Optimize connection pool usage"),
            ("Deploy service with zero downtime", "Migrate database without data loss"),
            ("Debug race condition in Python", "Diagnose intermittent failures in distributed system"),
        ]

        results: list[TransferDemo] = []
        for source, target in demos:
            demo = self.demonstrate(source, target)
            results.append(demo)

        return results

    def populate_from_seed(self) -> None:
        pass

        self.memory.store_episode(Episode(
            task="Debug network latency",
            context="Production system, high traffic",
            actions=["Captured packets", "Analyzed logs", "Found bottleneck"],
            result="Root cause: TCP retransmissions due to firewall timeout",
            lesson="When debugging latency, check network layer first, then application layer",
        ))
        self.memory.store_episode(Episode(
            task="Fix memory leak in Python service",
            context="Long-running service, growing RSS",
            actions=["Profiled memory", "Found circular reference", "Fixed with weakref"],
            result="Memory usage stabilized at 200MB",
            lesson="Circular references in Python can prevent garbage collection",
        ))
        self.memory.store_episode(Episode(
            task="Optimize database query performance",
            context="Slow API responses, high DB CPU",
            actions=["Analyzed query plan", "Added index", "Rewrote query"],
            result="Query time reduced from 2s to 50ms",
            lesson="Always check EXPLAIN plans before optimizing application code",
        ))
