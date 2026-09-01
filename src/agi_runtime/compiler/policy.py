"""Policy compiler for the AGI Cognitive Runtime."""

from __future__ import annotations

from pydantic import BaseModel, Field

from agi_runtime.types import BaseSchema, CognitiveDepth
from agi_runtime.cognition.operators import CognitiveOperator, DEFAULT_OPERATORS, get_operator


class CognitivePolicy(BaseSchema):
    """A policy that determines which operators to apply."""

    id: str
    name: str
    trigger_depth: list[CognitiveDepth] = Field(default_factory=list)
    trigger_domains: list[str] = Field(default_factory=list)
    operators: list[str] = Field(default_factory=list, description="Operator names in order")
    description: str = ""


DEFAULT_POLICIES: list[CognitivePolicy] = [
    CognitivePolicy(
        id="direct",
        name="Direct Execution",
        trigger_depth=[CognitiveDepth.L0_DIRECT],
        operators=["EXECUTE"],
        description="For simple, obvious tasks",
    ),
    CognitivePolicy(
        id="reason",
        name="Reasoning",
        trigger_depth=[CognitiveDepth.L1_REASON],
        operators=["UNDERSTAND", "DECOMPOSE", "INFER", "EXECUTE", "VERIFY"],
        description="For tasks requiring reasoning",
    ),
    CognitivePolicy(
        id="plan",
        name="Planning",
        trigger_depth=[CognitiveDepth.L2_PLAN],
        operators=["UNDERSTAND", "DECOMPOSE", "PLAN", "EXECUTE", "MONITOR", "VERIFY"],
        description="For multi-step tasks",
    ),
    CognitivePolicy(
        id="investigate",
        name="Investigation",
        trigger_depth=[CognitiveDepth.L3_INVESTIGATE],
        operators=["OBSERVE", "UNDERSTAND", "HYPOTHESIZE", "PLAN", "EXECUTE", "OBSERVE", "UPDATE", "VERIFY"],
        description="For unknown causes and debugging",
    ),
    CognitivePolicy(
        id="experiment",
        name="Experimentation",
        trigger_depth=[CognitiveDepth.L4_EXPERIMENT],
        operators=["OBSERVE", "HYPOTHESIZE", "TEST", "OBSERVE", "UPDATE", "FALSIFY", "VERIFY"],
        description="For uncertain hypotheses",
    ),
    CognitivePolicy(
        id="adapt",
        name="Adaptation",
        trigger_depth=[CognitiveDepth.L5_ADAPT],
        operators=["OBSERVE", "UNDERSTAND", "BACKTRACK", "ADAPT", "PLAN", "EXECUTE", "VERIFY"],
        description="For failure recovery",
    ),
    CognitivePolicy(
        id="long_horizon",
        name="Long Horizon",
        trigger_depth=[CognitiveDepth.L6_LONG_HORIZON],
        operators=["UNDERSTAND", "ABSTRACT", "PLAN", "EXECUTE", "MONITOR", "ADAPT", "LEARN", "CONSOLIDATE"],
        description="For large, persistent tasks",
    ),
]


class PolicyCompiler:
    """Selects and compiles cognitive policies based on task classification."""

    def __init__(self, policies: list[CognitivePolicy] | None = None) -> None:
        self.policies = policies or DEFAULT_POLICIES

    def select(self, depth: CognitiveDepth, domain: str = "") -> CognitivePolicy:
        for policy in self.policies:
            if depth in policy.trigger_depth:
                if not policy.trigger_domains or domain in policy.trigger_domains:
                    return policy
        return self.policies[0]

    def get_operators(self, policy: CognitivePolicy) -> list[CognitiveOperator]:
        operators: list[CognitiveOperator] = []
        for name in policy.operators:
            op = get_operator(name)
            if op:
                operators.append(op)
        return operators

    def compile(self, depth: CognitiveDepth, domain: str = "") -> list[CognitiveOperator]:
        policy = self.select(depth, domain)
        return self.get_operators(policy)

    def list_policies(self) -> list[dict[str, str]]:
        return [
            {"id": p.id, "name": p.name, "depth": d.value, "operators": ", ".join(p.operators)}
            for p in self.policies
            for d in p.trigger_depth
        ]
