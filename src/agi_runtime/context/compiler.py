"""Context compiler for the AGI Cognitive Runtime."""

from __future__ import annotations

from pydantic import BaseModel, Field

from agi_runtime.memory.models import Episode, Memory
from agi_runtime.knowledge.store import KnowledgeStore
from agi_runtime.world.model import WorldModel
from agi_runtime.planning.plan import Plan
from agi_runtime.metacognition.state import MetacognitiveState
from agi_runtime.reasoning.hypothesis import HypothesisSpace


class CognitiveContext(BaseModel):
    """Compact context package for the LLM."""

    task_description: str = ""
    active_goal: str = ""
    relevant_concepts: list[str] = Field(default_factory=list)
    relevant_principles: list[str] = Field(default_factory=list)
    active_heuristics: list[str] = Field(default_factory=list)
    current_plan: Plan | None = None
    hypotheses: list[str] = Field(default_factory=list)
    memory_summary: str = ""
    verification_requirements: list[str] = Field(default_factory=list)
    uncertainty: str = ""
    world_model_summary: str = ""
    metacognition: MetacognitiveState | None = None

    def to_prompt(self) -> str:
        parts: list[str] = []
        if self.task_description:
            parts.append(f"TASK: {self.task_description}")
        if self.active_goal:
            parts.append(f"GOAL: {self.active_goal}")
        if self.relevant_concepts:
            parts.append(f"CONCEPTS: {', '.join(self.relevant_concepts)}")
        if self.relevant_principles:
            parts.append(f"PRINCIPLES: {', '.join(self.relevant_principles)}")
        if self.active_heuristics:
            parts.append(f"HEURISTICS: {', '.join(self.active_heuristics)}")
        if self.current_plan:
            ready = self.current_plan.ready_steps()
            parts.append(f"PLAN: {len(self.current_plan.steps)} steps, {len(ready)} ready")
        if self.hypotheses:
            parts.append(f"HYPOTHESES: {', '.join(self.hypotheses)}")
        if self.uncertainty:
            parts.append(f"UNCERTAINTY: {self.uncertainty}")
        if self.metacognition:
            parts.append(f"METACOGNITION: {self.metacognition.summary()}")
        return "\n".join(parts)


class ContextCompiler:
    """Compiles a compact cognitive context from runtime state."""

    def __init__(
        self,
        knowledge: KnowledgeStore | None = None,
        memory: Memory | None = None,
        world_model: WorldModel | None = None,
    ) -> None:
        self.knowledge = knowledge or KnowledgeStore()
        self.memory = memory or Memory()
        self.world_model = world_model or WorldModel()

    def compile(
        self,
        task_description: str,
        plan: Plan | None = None,
        hypotheses: HypothesisSpace | None = None,
        metacognition: MetacognitiveState | None = None,
        retrieved_episodes: list[Episode] | None = None,
        max_concepts: int = 10,
        max_principles: int = 5,
    ) -> CognitiveContext:
        ctx = CognitiveContext(task_description=task_description)

        relevant = self.knowledge.search(task_description, limit=max_concepts)
        ctx.relevant_concepts = [e.name or e.id for e in relevant]
        principles = self.knowledge.by_type("principle")
        ctx.relevant_principles = [e.name or e.id for e in principles[:max_principles]]

        if plan:
            ctx.current_plan = plan
        if hypotheses:
            ctx.hypotheses = [h.statement for h in hypotheses.rank()[:5]]
        if metacognition:
            ctx.metacognition = metacognition

        # Callers that already ran retrieval this turn (e.g. CognitiveRuntime.run,
        # which needs the episodes earlier for its own trace) should pass
        # retrieved_episodes so this doesn't score the whole episode store a
        # second time with a second call. Only retrieve here as a fallback for
        # callers that use the compiler standalone.
        episodes = (
            retrieved_episodes
            if retrieved_episodes is not None
            else self.memory.find_similar_episodes(task_description, limit=3)
        )
        if episodes:
            lessons = [ep.lesson for ep in episodes if ep.lesson]
            ctx.memory_summary = "; ".join(lessons[:3])

        return ctx
