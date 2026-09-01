"""Tests for multi-agent orchestration."""

from agi_runtime.orchestration.agents import (
    AgentOrchestrator,
    AgentRole,
    SubAgent,
    AgentResult,
)


def test_orchestrator_creation():
    orch = AgentOrchestrator()
    assert len(orch.agents) > 0


def test_get_agent():
    orch = AgentOrchestrator()
    researcher = orch.get_agent(AgentRole.RESEARCHER)
    assert researcher is not None
    assert researcher.role == AgentRole.RESEARCHER


def test_research():
    orch = AgentOrchestrator()
    result = orch.research("What is distributed systems?")
    assert isinstance(result, AgentResult)
    assert result.agent_role == AgentRole.RESEARCHER
    assert len(result.findings) > 0


def test_critique():
    orch = AgentOrchestrator()
    result = orch.critique("Microservices are always better than monoliths")
    assert isinstance(result, AgentResult)
    assert len(result.findings) > 0


def test_verify():
    orch = AgentOrchestrator()
    result = orch.verify("The sky is blue")
    assert isinstance(result, AgentResult)


def test_synthesize():
    orch = AgentOrchestrator()
    result = orch.synthesize(["Finding A", "Finding B"])
    assert isinstance(result, AgentResult)
    assert len(result.findings) > 0


def test_full_review():
    orch = AgentOrchestrator()
    results = orch.full_review("Test claim")
    assert "research" in results
    assert "critique" in results
    assert "verification" in results
    assert "synthesis" in results


def test_subagent_default_prompt():
    agent = SubAgent(role=AgentRole.CRITIC)
    prompt = agent._default_prompt()
    assert "critic" in prompt.lower() or "challenge" in prompt.lower()
