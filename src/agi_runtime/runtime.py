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
from agi_runtime.verification.engine import VerificationEngine, VerificationResult
from agi_runtime.transfer.engine import TransferEngine
from agi_runtime.context.compiler import ContextCompiler, CognitiveContext
from agi_runtime.compiler.policy import PolicyCompiler, CognitivePolicy
from agi_runtime.cognition.operators import CognitiveOperator
from agi_runtime.providers.base import ModelProvider, ModelResponse
from agi_runtime.action.tools import BuiltinTools, ToolResult
from agi_runtime.action.loop import ToolUseLoop
from agi_runtime.orchestration.agents import AgentOrchestrator, AgentRole
from agi_runtime.memory.retriever import EpisodicRetriever, RetrievedEpisode
from agi_runtime.logging import CognitiveLogger


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
        enable_logging: bool = True,
    ) -> None:
        self.provider = model_provider
        self.knowledge = knowledge or KnowledgeStore()
        self.memory = memory or Memory()
        self.world_model = world_model or WorldModel()
        self.budget = budget or CognitiveBudget()
        self.enable_logging = enable_logging

        self.goals = GoalTree()
        self.hypotheses = HypothesisSpace()
        self.metacognition = MetacognitiveState()
        self.verification = VerificationEngine(provider=model_provider)
        self.transfer = TransferEngine()
        self.context_compiler = ContextCompiler(self.knowledge, self.memory, self.world_model)
        self.policy_compiler = PolicyCompiler()
        self.trace = CognitiveTrace()
        self.tools = BuiltinTools()
        self.tool_loop = ToolUseLoop(
            self.tools, model_provider, max_iterations=self.budget.max_tool_calls
        )
        self.orchestrator = AgentOrchestrator()
        self.adaptive_planner = AdaptivePlanner()
        self.episodic_retriever = EpisodicRetriever(self.memory)
        self.cog_log: CognitiveLogger | None = None

        # NOT wired into run() yet: self.transfer, self.orchestrator and
        # self.adaptive_planner are constructed but no code path in run()
        # calls them. Wiring them for real needs product decisions (when a
        # task warrants multi-agent orchestration vs. a single pass; what
        # counts as a ReplanTrigger) rather than a cosmetic call just to make
        # the diagram true. See AUDIT.md.
        self._last_verification: VerificationResult | None = None
        self._step_count = 0
        self._tool_calls = 0

    def classify(self, task: str) -> TaskClassification:
        task_lower = task.lower()

        uncertainty_words = ["why", "how", "investigate", "debug", "diagnose", "uncertain", "unknown",
                             "por qué", "por que", "investiga", "depura", "diagnostica", "desconocido"]
        planning_words = ["build", "create", "implement", "deploy", "design", "architecture",
                          "construir", "crear", "implementar", "diseñar", "arquitectura"]
        experiment_words = ["experiment", "hypothesis", "test whether", "compare",
                           "experimento", "hipótesis", "prueba si", "compara"]
        adapt_words = ["recover", "fix", "adapt", "change", "retry",
                      "recuperar", "arreglar", "adaptar", "cambiar", "reintenta"]
        long_words = ["project", "long-term", "persistent", "multi-session",
                     "proyecto", "largo plazo", "permanente", "multi-sesión"]

        uncertainty = sum(1 for w in uncertainty_words if w in task_lower)
        planning = sum(1 for w in planning_words if w in task_lower)
        experiment = sum(1 for w in experiment_words if w in task_lower)
        adapt = sum(1 for w in adapt_words if w in task_lower)
        long_horizon = sum(1 for w in long_words if w in task_lower)

        total_signal = uncertainty + planning + experiment + adapt + long_horizon

        # Depth is chosen by which signal is STRONGEST, not by a fixed
        # precedence order. The previous version picked L5_ADAPT whenever
        # adapt > 0, even if planning had 5x the matches — one incidental
        # "retry" would outrank a task overwhelmingly about building
        # something. Ties fall back to severity order (long-horizon >
        # adapt > experiment > investigate > plan), same order as before.
        #
        # Known limitation kept as-is in this pass: because total_signal
        # is the sum of these same five counters, total_signal > 0 always
        # implies at least one counter > 0, so L1_REASON can never be
        # selected here — it would need its own "reasoning_words" signal
        # to become reachable. Flagging rather than guessing that list.
        if total_signal == 0:
            depth = CognitiveDepth.L0_DIRECT
        else:
            scored_depths = [
                (long_horizon, CognitiveDepth.L6_LONG_HORIZON),
                (adapt, CognitiveDepth.L5_ADAPT),
                (experiment, CognitiveDepth.L4_EXPERIMENT),
                (uncertainty, CognitiveDepth.L3_INVESTIGATE),
                (planning, CognitiveDepth.L2_PLAN),
            ]
            best_score = max(score for score, _ in scored_depths)
            depth = next(d for score, d in scored_depths if score == best_score)

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
        """Without a provider this falls back to templating the observation
        into a statement (f"Hypothesis from: {obs}") — not real hypothesis
        generation, just a placeholder so the rest of the pipeline has
        something to rank. With a provider, each observation is actually
        sent to the model to produce a specific, falsifiable hypothesis."""
        for obs in observations[:count]:
            statement = f"Hypothesis from: {obs}"
            if self.provider:
                response = self.provider.generate(
                    f"Observation: {obs}\n\n"
                    "Propose one specific, falsifiable hypothesis that could explain or "
                    "address this. Respond with only the hypothesis statement, no preamble.",
                    system="You are a rigorous hypothesis-generation module. Prefer specific, "
                    "testable hypotheses over vague ones.",
                    temperature=0.4,
                    max_tokens=200,
                )
                statement = response.text.strip() or statement
            self.hypotheses.add(Hypothesis(statement=statement))
        return self.hypotheses.hypotheses

    def verify(self, claim: str, evidence: list[str] | None = None) -> str:
        result = self.verification.verify_claim(claim, evidence)
        questions = self.verification.challenge(claim)
        self._last_verification = result
        self.trace.verification = result.claim + " | " + "; ".join(questions[:3])
        return self.trace.verification

    def ask_llm(self, prompt: str, system: str = "") -> str:
        if not self.provider:
            return f"[No model provider configured] Prompt was: {prompt[:100]}..."
        response = self.provider.generate(prompt, system=system)
        return response.text

    def _budget_exceeded(self) -> bool:
        return self._step_count >= self.budget.max_steps

    def _budget_exceeded_result(
        self,
        task_description: str,
        classification: TaskClassification,
        plan: Plan | None,
        start: float,
    ) -> RuntimeResult:
        budget_str = f"{self._step_count}/{self.budget.max_steps} steps"
        self.trace.decisions.append(f"Stopped: budget exhausted ({budget_str}).")
        if self.cog_log:
            self.cog_log.log_step("BUDGET_EXCEEDED", budget_str)
        return RuntimeResult(
            success=False,
            answer="",
            goal=task_description,
            plan=plan,
            uncertainty="Stopped before completion: step budget exhausted.",
            trace=self.trace,
            duration_seconds=time.time() - start,
            depth=classification.depth,
        )

    def run(self, task_description: str, **kwargs: Any) -> RuntimeResult:
        start = time.time()
        self._step_count = 0
        self._tool_calls = 0
        self.trace = CognitiveTrace(task=task_description)

        if self.enable_logging:
            self.cog_log = CognitiveLogger()
            self.cog_log.log_step('TASK_RECEIVED', task_description)

        classification = self.classify(task_description)
        self._step_count += 1
        self.trace.cognitive_mode = classification.depth.value

        if self.cog_log:
            self.cog_log.log_classification(
                classification.depth.value,
                classification.complexity,
                classification.reasoning.split(', ')[:5]
            )

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
        self._step_count += 1
        self.trace.decisions.append(f"Selected policy: {classification.depth.value}")

        if self.cog_log:
            self.cog_log.log_plan([s.action for s in plan.steps])

        if self._budget_exceeded():
            return self._budget_exceeded_result(task_description, classification, plan, start)

        # Single retrieval pass, reused below and passed into the context
        # compiler — it used to be recomputed a second time inside
        # ContextCompiler.compile() with a different scoring implementation.
        retrieved = self.episodic_retriever.retrieve(task_description, limit=3)
        retrieved_episodes = [r.episode for r in retrieved]
        if retrieved:
            self.trace.observations.append(f"Found {len(retrieved)} relevant past experiences")
            if self.cog_log:
                self.cog_log.log_memory_search(
                    task_description,
                    len(retrieved),
                    retrieved[0].relevance_score if retrieved else 0
                )
        elif self.cog_log:
            self.cog_log.log_memory_search(task_description, 0, 0)

        if classification.requires_hypotheses:
            hypotheses = self.generate_hypotheses([task_description])
            self._step_count += 1
            if self.cog_log:
                for h in hypotheses:
                    self.cog_log.log_hypothesis(h.statement, h.posterior_confidence)

        knowledge_results = self.knowledge.search(task_description)
        if knowledge_results and self.cog_log:
            self.cog_log.log_knowledge_applied(knowledge_results, 'search')

        ctx = self.context_compiler.compile(
            task_description,
            plan=plan,
            hypotheses=self.hypotheses,
            metacognition=self.metacognition,
            retrieved_episodes=retrieved_episodes,
        )

        if self._budget_exceeded():
            return self._budget_exceeded_result(task_description, classification, plan, start)

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
            if self.cog_log:
                for tc in tool_calls:
                    self.cog_log.log_tool_call(tc.tool_name, tc.arguments, tc.result[:100])
        elif self.provider:
            prompt = ctx.to_prompt()
            prompt += f"\n\nTask: {task_description}\n\nExecute this task now. Do not just describe what you would do — actually do it. Provide the specific details, examples, and concrete outputs as if you were performing the work."
            answer = self.ask_llm(prompt, system="You are the AGI Cognitive Runtime. Think step by step and execute the task directly.")
        else:
            answer = f"Cognitive runtime processed: {task_description} (depth={classification.depth.value})"
        self._step_count += 1

        success = True
        if classification.requires_verification:
            verification_text = self.verify(answer)
            self._step_count += 1
            vr = self._last_verification

            # This is where metacognition used to be inert: current_confidence
            # stayed at its 0.5 default for the whole run and should_proceed()/
            # should_ask_user() were never called, so nothing downstream ever
            # acted on them. Now the verification result actually updates the
            # state, and should_ask_user() actually affects `success` below —
            # with no provider, vr stays at its VerificationResult defaults
            # (confidence 0.5, is_verified False), so should_ask_user() stays
            # False and behaviour is unchanged from before in that case.
            if vr is not None:
                self.metacognition.current_confidence = vr.confidence
                self.metacognition.failure_risk = round(1.0 - vr.confidence, 4)
                self.metacognition.known_unknowns = list(vr.concerns)
                self.metacognition.uncertainty_sources = list(vr.concerns)
                self.metacognition.verification_status = (
                    "verified" if vr.is_verified else "unverified"
                )
                if vr.concerns:
                    self.trace.uncertainty = "; ".join(vr.concerns)

                if self.metacognition.should_ask_user():
                    success = False
                    self.trace.decisions.append(
                        "should_ask_user() == True: low confidence / multiple uncertainty "
                        "sources from verification — not asserting success without review."
                    )
                elif not self.metacognition.should_proceed():
                    self.trace.decisions.append(
                        "should_proceed() == False: confidence below threshold, proceeding "
                        "anyway but flagging it rather than silently reporting success."
                    )

            if self.cog_log:
                self.cog_log.log_verification(
                    'Answer verified',
                    verification_text[:100],
                    'PASS' in verification_text or len(verification_text) == 0
                )

        lesson = f"Completed task with depth {classification.depth.value}"
        self.trace.lessons.append(lesson)
        if self.cog_log:
            self.cog_log.log_lesson(lesson)

        self.memory.store_episode(Episode(
            task=task_description,
            context=f"Depth: {classification.depth.value}",
            actions=[f"Classified as {classification.depth.value}", "Executed plan"],
            result=answer[:500],
            lesson=lesson,
        ))

        self.goals.complete_goal(goal.id)
        self._step_count += 1
        elapsed = time.time() - start

        if self.cog_log:
            self.cog_log.log_metacognition(
                self.metacognition.current_confidence,
                self.metacognition.__dict__
            )
            self.cog_log.summary(elapsed * 1000)

        return RuntimeResult(
            success=success,
            answer=answer,
            goal=task_description,
            plan=plan,
            verification=self.trace.verification,
            uncertainty=self.trace.uncertainty,
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
