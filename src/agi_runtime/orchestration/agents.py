"""Multi-agent orchestration for the AGI Cognitive Runtime."""

from __future__ import annotations

import time
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field

from agi_runtime.types import BaseSchema


class AgentRole(str, Enum):
    """Roles for specialized agents."""

    MASTER = "master"
    RESEARCHER = "researcher"
    PLANNER = "planner"
    IMPLEMENTER = "implementer"
    CRITIC = "critic"
    VERIFIER = "verifier"
    EXPERIMENTER = "experimenter"
    SYNTHESIZER = "synthesizer"


class AgentMessage(BaseSchema):
    """Message between agents."""

    sender: str = ""
    recipient: str = ""
    role: AgentRole = AgentRole.MASTER
    content: str = ""
    message_type: str = "request"
    metadata: dict[str, Any] = Field(default_factory=dict)


class AgentResult(BaseSchema):
    """Result from a subagent."""

    agent_role: AgentRole
    findings: list[str] = Field(default_factory=list)
    evidence: list[str] = Field(default_factory=list)
    hypotheses: list[str] = Field(default_factory=list)
    uncertainties: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)
    artifacts: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    summary: str = ""


class SubAgent(BaseModel):
    """A specialized subagent."""

    role: AgentRole
    name: str = ""
    description: str = ""
    system_prompt: str = ""

    def __init__(self, role: AgentRole, **kwargs: Any) -> None:
        super().__init__(role=role, **kwargs)
        if not self.name:
            self.name = role.value.title()
        if not self.system_prompt:
            self.system_prompt = self._default_prompt()

    def _default_prompt(self) -> str:
        prompts = {
            AgentRole.RESEARCHER: (
                "You are a research specialist. Gather information, evaluate sources, "
                "and provide evidence-based findings. Track uncertainty explicitly."
            ),
            AgentRole.PLANNER: (
                "You are a planning specialist. Break down complex tasks into manageable steps, "
                "identify dependencies, and create actionable plans."
            ),
            AgentRole.IMPLEMENTER: (
                "You are an implementation specialist. Execute plans, write code, "
                "and produce concrete artifacts. Focus on correctness and completeness."
            ),
            AgentRole.CRITIC: (
                "You are a critic. Challenge assumptions, identify weaknesses, "
                "find counter-evidence, and stress-test conclusions. Be constructive."
            ),
            AgentRole.VERIFIER: (
                "You are a verification specialist. Independently check claims, "
                "validate results, and ensure correctness. Never assume the generator is right."
            ),
            AgentRole.EXPERIMENTER: (
                "You are an experimentation specialist. Design experiments that distinguish "
                "between hypotheses, prioritize information gain, and track results."
            ),
            AgentRole.SYNTHESIZER: (
                "You are a synthesis specialist. Combine findings from multiple sources, "
                "resolve conflicts, and produce coherent conclusions."
            ),
        }
        return prompts.get(self.role, "You are a helpful AI assistant.")

    def process(self, task: str, context: str = "") -> AgentResult:
        prompt = task
        if context:
            prompt = f"Context:\n{context}\n\nTask:\n{task}"

        return AgentResult(
            agent_role=self.role,
            summary=f"[{self.name}] Processed: {task[:100]}",
            findings=[f"Analysis from {self.name} perspective"],
            confidence=0.5,
        )


class AgentOrchestrator(BaseModel):
    """Orchestrates multiple specialized agents."""

    agents: list[SubAgent] = Field(default_factory=list)
    results: list[AgentResult] = Field(default_factory=list)

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        if not self.agents:
            self.agents = [
                SubAgent(role=AgentRole.RESEARCHER),
                SubAgent(role=AgentRole.CRITIC),
                SubAgent(role=AgentRole.VERIFIER),
                SubAgent(role=AgentRole.SYNTHESIZER),
            ]

    def get_agent(self, role: AgentRole) -> SubAgent | None:
        for a in self.agents:
            if a.role == role:
                return a
        return None

    def research(self, question: str) -> AgentResult:
        agent = self.get_agent(AgentRole.RESEARCHER)
        if not agent:
            return AgentResult(agent_role=AgentRole.RESEARCHER, summary="No researcher available")
        result = agent.process(question)
        self.results.append(result)
        return result

    def critique(self, claim: str) -> AgentResult:
        agent = self.get_agent(AgentRole.CRITIC)
        if not agent:
            return AgentResult(agent_role=AgentRole.CRITIC, summary="No critic available")
        result = agent.process(f"Critically evaluate: {claim}")
        self.results.append(result)
        return result

    def verify(self, claim: str) -> AgentResult:
        agent = self.get_agent(AgentRole.VERIFIER)
        if not agent:
            return AgentResult(agent_role=AgentRole.VERIFIER, summary="No verifier available")
        result = agent.process(f"Independently verify: {claim}")
        self.results.append(result)
        return result

    def synthesize(self, findings: list[str]) -> AgentResult:
        agent = self.get_agent(AgentRole.SYNTHESIZER)
        if not agent:
            return AgentResult(agent_role=AgentRole.SYNTHESIZER, summary="No synthesizer available")
        context = "\n".join(f"- {f}" for f in findings)
        result = agent.process("Synthesize these findings into a coherent conclusion", context)
        self.results.append(result)
        return result

    def full_review(self, claim: str) -> dict[str, AgentResult]:
        research = self.research(claim)
        criticism = self.critique(claim)
        verification = self.verify(claim)
        all_findings = research.findings + criticism.findings + verification.findings
        synthesis = self.synthesize(all_findings)

        return {
            "research": research,
            "critique": criticism,
            "verification": verification,
            "synthesis": synthesis,
        }
