"""Cognitive operators for the AGI Cognitive Runtime."""

from __future__ import annotations

from enum import Enum
from typing import Any, Callable

from pydantic import BaseModel, Field

from agi_runtime.types import BaseSchema


class OperatorCategory(str, Enum):
    """Categories of cognitive operators."""

    PERCEPTION = "perception"
    UNDERSTANDING = "understanding"
    REASONING = "reasoning"
    HYPOTHESIS = "hypothesis"
    PLANNING = "planning"
    EXECUTION = "execution"
    RECOVERY = "recovery"
    METACOGNITION = "metacognition"
    LEARNING = "learning"


class CognitiveOperator(BaseSchema):
    """A reusable cognitive operator."""

    name: str
    category: OperatorCategory
    purpose: str = ""
    inputs: list[str] = Field(default_factory=list, description="Expected input types")
    outputs: list[str] = Field(default_factory=list, description="Output types produced")
    preconditions: list[str] = Field(default_factory=list)
    procedure: list[str] = Field(default_factory=list)
    failure_modes: list[str] = Field(default_factory=list)
    verification: list[str] = Field(default_factory=list)
    examples: list[list[str]] = Field(default_factory=list)


DEFAULT_OPERATORS: list[CognitiveOperator] = [
    CognitiveOperator(
        name="OBSERVE",
        category=OperatorCategory.PERCEPTION,
        purpose="Gather information from the environment or tools",
        inputs=["task", "environment"],
        outputs=["observations"],
    ),
    CognitiveOperator(
        name="UNDERSTAND",
        category=OperatorCategory.UNDERSTANDING,
        purpose="Comprehend the task, constraints, and objectives",
        inputs=["observations", "task"],
        outputs=["understanding"],
    ),
    CognitiveOperator(
        name="CLASSIFY",
        category=OperatorCategory.UNDERSTANDING,
        purpose="Classify the task and determine cognitive depth",
        inputs=["understanding"],
        outputs=["classification"],
    ),
    CognitiveOperator(
        name="ABSTRACT",
        category=OperatorCategory.REASONING,
        purpose="Extract patterns, concepts, and principles from specifics",
        inputs=["observations", "knowledge"],
        outputs=["abstractions"],
    ),
    CognitiveOperator(
        name="DECOMPOSE",
        category=OperatorCategory.REASONING,
        purpose="Break complex problems into simpler subproblems",
        inputs=["problem"],
        outputs=["subproblems"],
    ),
    CognitiveOperator(
        name="ANALOGIZE",
        category=OperatorCategory.REASONING,
        purpose="Find structural similarities to previously solved problems",
        inputs=["problem", "memory"],
        outputs=["analogies"],
    ),
    CognitiveOperator(
        name="INFER",
        category=OperatorCategory.REASONING,
        purpose="Draw conclusions from available evidence",
        inputs=["evidence", "knowledge"],
        outputs=["inferences"],
    ),
    CognitiveOperator(
        name="HYPOTHESIZE",
        category=OperatorCategory.HYPOTHESIS,
        purpose="Generate candidate explanations for uncertain observations",
        inputs=["observations", "uncertainty"],
        outputs=["hypotheses"],
    ),
    CognitiveOperator(
        name="TEST",
        category=OperatorCategory.HYPOTHESIS,
        purpose="Design and execute tests to distinguish hypotheses",
        inputs=["hypotheses", "tools"],
        outputs=["evidence"],
    ),
    CognitiveOperator(
        name="FALSIFY",
        category=OperatorCategory.HYPOTHESIS,
        purpose="Actively seek evidence that contradicts hypotheses",
        inputs=["hypotheses"],
        outputs=["falsification_evidence"],
    ),
    CognitiveOperator(
        name="PLAN",
        category=OperatorCategory.PLANNING,
        purpose="Construct a sequence of actions to achieve a goal",
        inputs=["goal", "constraints", "knowledge"],
        outputs=["plan"],
    ),
    CognitiveOperator(
        name="EXECUTE",
        category=OperatorCategory.EXECUTION,
        purpose="Carry out a planned action using available tools",
        inputs=["action", "tools"],
        outputs=["result"],
    ),
    CognitiveOperator(
        name="MONITOR",
        category=OperatorCategory.EXECUTION,
        purpose="Track progress against plan and detect deviations",
        inputs=["plan", "observations"],
        outputs=["status"],
    ),
    CognitiveOperator(
        name="BACKTRACK",
        category=OperatorCategory.RECOVERY,
        purpose="Return to a previous state when current path fails",
        inputs=["failure", "plan"],
        outputs=["revised_plan"],
    ),
    CognitiveOperator(
        name="ADAPT",
        category=OperatorCategory.RECOVERY,
        purpose="Modify strategy based on new information or failures",
        inputs=["failure", "world_model"],
        outputs=["adapted_strategy"],
    ),
    CognitiveOperator(
        name="VERIFY",
        category=OperatorCategory.METACOGNITION,
        purpose="Independently check conclusions and actions",
        inputs=["conclusion", "evidence"],
        outputs=["verification_result"],
    ),
    CognitiveOperator(
        name="REFLECT",
        category=OperatorCategory.METACOGNITION,
        purpose="Examine own reasoning process and identify weaknesses",
        inputs=["trace", "metacognition"],
        outputs=["reflection"],
    ),
    CognitiveOperator(
        name="LEARN",
        category=OperatorCategory.LEARNING,
        purpose="Extract reusable lessons from experience",
        inputs=["experience", "result"],
        outputs=["lesson"],
    ),
    CognitiveOperator(
        name="TRANSFER",
        category=OperatorCategory.LEARNING,
        purpose="Apply knowledge from one domain to another",
        inputs=["knowledge", "target_domain"],
        outputs=["transferred_knowledge"],
    ),
    CognitiveOperator(
        name="CONSOLIDATE",
        category=OperatorCategory.LEARNING,
        purpose="Integrate new experience into long-term memory",
        inputs=["experience", "memory"],
        outputs=["consolidated_memory"],
    ),
]


def get_operator(name: str) -> CognitiveOperator | None:
    for op in DEFAULT_OPERATORS:
        if op.name == name:
            return op
    return None
