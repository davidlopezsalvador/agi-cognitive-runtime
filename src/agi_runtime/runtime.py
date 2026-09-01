"""Core cognitive runtime - the heart of the AGI Cognitive Runtime."""

from __future__ import annotations

import time
from typing import Any

from pydantic import BaseModel, Field

from agi_runtime.types import (
    CognitiveDepth,
    EpistemicStatus,
    GoalStatus,
    PlanStatus,
    StepStatus,
)
from agi_runtime.world.task import Task, TaskClassification
from agi_runtime.world.goal import Goal, GoalTree
from agi_runtime.world.model import Belief, WorldModel, WorldModelEntry
from agi_runtime.planning.plan import Plan, PlanStep
from agi_runtime.planning.adaptive import AdaptivePlanner, ReplanTrigger
from agi_runtime.reasoning.hypothesis import Hypothesis, HypothesisSpace
from agi_runtime.memory.models import Memory, Episode
from agi_runtime.knowledge.store import KnowledgeStore
from agi_runtime.metacognition.state import MetacognitiveState
from agi_runtime.verification.engine import VerificationEngine
from agi_runtime.transfer.engine import TransferEngine
from agi_runtime.context.compiler import ContextCompiler, CognitiveContext
from agi_runtime.compiler.policy import PolicyCompiler, CognitivePolicy
from agi_runtime.cognition.operators import CognitiveOperator
from agi_runtime.providers.base import ModelProvider, ModelResponse
from agi_runtime.action.tools import BuiltinTools, ToolResult
from agi_runtime.action.loop import ToolUseLoop
from agi_runtime.orchestration.agents import AgentOrchestrator, AgentRole
from agi_runtime.memory.retriever import EpisodicRetriever, RetrievedEpisode


class CognitiveTrace(BaseModel):
    """Structured trace of the cognitive process."""

    task: str = ""
    goal: str = ""
    cognitive_mode: str = ""
    assumptions: list[str] = Field(default_factory=list)
    hypotheses: list[str] = Field(default_factory=list)
    actions: list[str] = Field(default_factory=list)
    observations: list[str] = Field(default_factory=list)
    decisions: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    verification: str = ""
    uncertainty: str = ""
    result: str = ""
    lessons: list[str] = Field(default_factory=list)


class RuntimeResult(BaseModel):
    """Result of a cognitive runtime run."""

    success: bool = False
    answer: str = ""
    goal: str = ""
    plan: Plan | None = None
    evidence: list[str] = Field(default_factory=list)
    verification: str = ""
    uncertainty: str = ""
    lessons: list[str] = Field(default_factory=list)
    trace: CognitiveTrace = Field(default_factory=CognitiveTrace)
    duration_seconds: float = 0.0
    depth: CognitiveDepth = CognitiveDepth.L0_DIRECT


class CognitiveBudget(BaseModel):
    """Resource budget for a cognitive run."""

    max_steps: int = 50
    max_tool_calls: int = 30
    max_context_tokens: int = 8000
    max_hypotheses: int = 10
    max_experiments: int = 10


class CognitiveRuntime:
    """The main cognitive runtime that orchestrates all components."""

    def __init__(
        self,
        model_provider: ModelProvider | None = None,
        knowledge: KnowledgeStore | None = None,
        memory: Memory | None = None,
        world_model: WorldModel | None = None,
        budget: CognitiveBudget | None = None,
    ) -> None:
        self.provider = model_provider
        self.knowledge = knowledge or KnowledgeStore()
        self.memory = memory or Memory()
        self.world_model = world_model or WorldModel()
        self.budget = budget or CognitiveBudget()

        self.goals = GoalTree()
        self.hypotheses = HypothesisSpace()
        self.metacognition = MetacognitiveState()
        self.verification = VerificationEngine()
        self.transfer = TransferEngine()
        self.context_compiler = ContextCompiler(self.knowledge, self.memory, self.world_model)
        self.policy_compiler = PolicyCompiler()
        self.trace = CognitiveTrace()
        self.tools = BuiltinTools()
        self.tool_loop = ToolUseLoop(self.tools, model_provider)
        self.orchestrator = AgentOrchestrator()
        self.adaptive_planner = AdaptivePlanner()
        self.episodic_retriever = EpisodicRetriever(self.memory)

        self._step_count = 0
        self._tool_calls = 0

    def classify(self, task: str) -> TaskClassification:
        task_lower = task.lower()

        uncertainty_words = ["why", "how", "investigate", "debug", "diagnose", "uncertain", "unknown"]
        planning_words = ["build", "create", "implement", "deploy", "design", "architecture"]
        experiment_words = ["experiment", "hypothesis", "test whether", "compare"]
        adapt_words = ["recover", "fix", "adapt", "change", "retry"]
        long_words = ["project", "long-term", "persistent", "multi-session"]

        uncertainty = sum(1 for w in uncertainty_words if w in task_lower)
        planning = sum(1 for w in planning_words if w in task_lower)
        experiment = sum(1 for w in experiment_words if w in task_lower)
        adapt = sum(1 for w in adapt_words if w in task_lower)
        long_horizon = sum(1 for w in long_words if w in task_lower)

        total_signal = uncertainty + planning + experiment + adapt + long_horizon

        if total_signal == 0:
            depth = CognitiveDepth.L0_DIRECT
        elif long_horizon > 0:
            depth = CognitiveDepth.L6_LONG_HORIZON
        elif adapt > 0:
            depth = CognitiveDepth.L5_ADAPT
        elif experiment > 0:
            depth = CognitiveDepth.L4_EXPERIMENT
        elif uncertainty > planning:
            depth = CognitiveDepth.L3_INVESTIGATE
        elif planning > 0:
            depth = CognitiveDepth.L2_PLAN
        else:
            depth = CognitiveDepth.L1_REASON

        complexity = min(total_signal / 5.0, 1.0)

        return TaskClassification(
            depth=depth,
            domain="general",
            complexity=complexity,
            uncertainty_level=min(uncertainty / 3.0, 1.0),
            requires_planning=planning > 0 or depth in (CognitiveDepth.L2_PLAN, CognitiveDepth.L6_LONG_HORIZON),
            requires_hypotheses=uncertainty > 0 or experiment > 0,
            requires_verification=complexity > 0.3,
            requires_learning=complexity > 0.5,
            reasoning=f"Uncertainty={uncertainty}, Planning={planning}, Experiment={experiment}, Adapt={adapt}, Long={long_horizon}",
        )

    def plan_task(self, task: Task) -> Plan:
        plan = Plan(objective=task.objective)
        plan.assumptions = task.constraints.copy()

        if task.cognitive_depth in (CognitiveDepth.L0_DIRECT, CognitiveDepth.L1_REASON):
            plan.steps.append(PlanStep(action=f"Execute: {task.objective}"))
        else:
            plan.steps.append(PlanStep(action=f"Understand: {task.objective}"))
            plan.steps.append(PlanStep(action="Extract constraints and unknowns"))
            if task.cognitive_depth.value.startswith("L3") or task.cognitive_depth.value.startswith("L4"):
                plan.steps.append(PlanStep(action="Generate hypotheses"))
                plan.steps.append(PlanStep(action="Design experiments"))
                plan.steps.append(PlanStep(action="Execute experiments"))
                plan.steps.append(PlanStep(action="Evaluate evidence"))
            else:
                plan.steps.append(PlanStep(action="Plan approach"))
                plan.steps.append(PlanStep(action="Execute approach"))
            plan.steps.append(PlanStep(action="Verify results"))
            plan.steps.append(PlanStep(action="Extract lessons"))

        plan.status = PlanStatus.ACTIVE
        return plan

    def generate_hypotheses(self, observations: list[str], count: int = 3) -> list[Hypothesis]:
        for obs in observations[:count]:
            h = Hypothesis(statement=f"Hypothesis from: {obs}")
            self.hypotheses.add(h)
        return self.hypotheses.hypotheses

    def verify(self, claim: str, evidence: list[str] | None = None) -> str:
        result = self.verification.verify_claim(claim, evidence)
        questions = self.verification.challenge(claim)
        self.trace.verification = result.claim + " | " + "; ".join(questions[:3])
        return self.trace.verification

    def ask_llm(self, prompt: str, system: str = "") -> str:
        if not self.provider:
            return f"[No model provider configured] Prompt was: {prompt[:100]}..."
        response = self.provider.generate(prompt, system=system)
        return response.text

    def run(self, task_description: str, **kwargs: Any) -> RuntimeResult:
        start = time.time()
        self._step_count = 0
        self._tool_calls = 0
        self.trace = CognitiveTrace(task=task_description)

        classification = self.classify(task_description)
        self.trace.cognitive_mode = classification.depth.value

        task = Task(
            objective=task_description,
            desired_outcome=kwargs.get("desired_outcome", "Task completed successfully"),
            cognitive_depth=classification.depth,
            constraints=kwargs.get("constraints", []),
        )

        goal = Goal(description=task_description, priority=1)
        self.goals.add_goal(goal)
        self.trace.goal = task_description

        plan = self.plan_task(task)
        self.trace.decisions.append(f"Selected policy: {classification.depth.value}")

        retrieved = self.episodic_retriever.retrieve(task_description, limit=3)
        if retrieved:
            self.trace.observations.append(f"Found {len(retrieved)} relevant past experiences")

        if classification.requires_hypotheses:
            self.generate_hypotheses([task_description])

        ctx = self.context_compiler.compile(
            task_description,
            plan=plan,
            hypotheses=self.hypotheses,
            metacognition=self.metacognition,
        )

        if retrieved:
            lessons = []
            for r in retrieved:
                if r.episode.lesson:
                    lessons.append(r.episode.lesson)
            if lessons:
                ctx.memory_summary = "; ".join(lessons[:3])

        use_tools = kwargs.get("use_tools", False)

        if use_tools and self.provider:
            system_prompt = "You are the AGI Cognitive Runtime. Use tools to accomplish tasks."
            answer, tool_calls = self.tool_loop.run_with_tools(
                task_description,
                system_prompt=system_prompt,
                context=ctx.to_prompt(),
            )
            self._tool_calls = len(tool_calls)
            self.trace.actions.extend([f"Tool: {tc.tool_name}" for tc in tool_calls])
        elif self.provider:
            prompt = ctx.to_prompt()
            prompt += f"\n\nTask: {task_description}\n\nProvide a structured response with: objective, approach, result."
            answer = self.ask_llm(prompt, system="You are the AGI Cognitive Runtime. Think step by step.")
        else:
            answer = f"Cognitive runtime processed: {task_description} (depth={classification.depth.value})"

        if classification.requires_verification:
            self.verify(answer)

        lesson = f"Completed task with depth {classification.depth.value}"
        self.trace.lessons.append(lesson)

        self.memory.store_episode(Episode(
            task=task_description,
            context=f"Depth: {classification.depth.value}",
            actions=[f"Classified as {classification.depth.value}", "Executed plan"],
            result=answer[:500],
            lesson=lesson,
        ))

        self.goals.complete_goal(goal.id)
        elapsed = time.time() - start

        return RuntimeResult(
            success=True,
            answer=answer,
            goal=task_description,
            plan=plan,
            verification=self.trace.verification,
            lessons=self.trace.lessons,
            trace=self.trace,
            duration_seconds=elapsed,
            depth=classification.depth,
        )

    def status(self) -> dict[str, Any]:
        return {
            "version": "0.1.0",
            "active_goals": len(self.goals.active_goals()),
            "total_goals": len(self.goals.goals),
            "hypotheses": len(self.hypotheses.hypotheses),
            "episodes": len(self.memory.episodes),
            "semantic_entries": len(self.memory.semantic),
            "skills": len(self.memory.procedural),
            "failures": len(self.memory.failures),
            "world_model_entries": len(self.world_model.entries),
            "beliefs": len(self.world_model.beliefs),
            "knowledge_entries": len(self.knowledge.entries),
            "metacognition": self.metacognition.summary(),
            "steps_used": self._step_count,
            "tool_calls": self._tool_calls,
            "tools_available": [t.name for t in self.tools.list_tools()],
            "agents_available": [a.role.value for a in self.orchestrator.agents],
        }
