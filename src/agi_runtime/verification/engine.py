"""Verification engine for the AGI Cognitive Runtime."""

from __future__ import annotations

from pydantic import BaseModel, Field

from agi_runtime.types import BaseSchema


class VerificationResult(BaseSchema):
    """Result of a verification check."""

    claim: str
    is_verified: bool = False
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)
    evidence: list[str] = Field(default_factory=list)
    concerns: list[str] = Field(default_factory=list)
    questions: list[str] = Field(default_factory=list, description="Unanswered verification questions")
    summary: str = ""


class VerificationEngine:
    """Engine for independently verifying conclusions."""

    def verify_claim(self, claim: str, evidence: list[str] | None = None) -> VerificationResult:
        result = VerificationResult(claim=claim)
        if evidence:
            result.evidence = evidence
        return result

    def challenge(self, conclusion: str, assumptions: list[str] | None = None) -> list[str]:
        return [
            "What could make this wrong?",
            "Which assumption is least certain?",
            "What evidence contradicts this?",
            "Did I solve the requested problem?",
            "Did I introduce side effects?",
            "What edge cases remain?",
            "Can I reproduce the result?",
            "Can I independently verify it?",
            "What would falsify my conclusion?",
        ]

    def cross_check(
        self, claim_a: str, claim_b: str, evidence_a: list[str], evidence_b: list[str]
    ) -> str:
        shared = set(evidence_a) & set(evidence_b)
        if shared:
            return f"Claims share {len(shared)} pieces of supporting evidence."
        return "Claims have no shared evidence. Independent verification needed."
