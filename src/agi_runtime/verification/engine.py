"""Verification engine for the AGI Cognitive Runtime."""

from __future__ import annotations

import contextlib

from pydantic import Field

from agi_runtime.providers.base import ModelProvider
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


_STATIC_CHALLENGE_QUESTIONS: list[str] = [
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


class VerificationEngine:
    """Engine for independently verifying conclusions.

    Without a model_provider this degrades to the original behaviour:
    verify_claim() only echoes the claim/evidence back (is_verified and
    confidence stay at their Pydantic defaults) and challenge() returns the
    same static question list for every claim. That's a deliberate,
    documented fallback for tests and offline use — not real verification.
    With a provider, both methods actually ask the model to assess the
    specific claim instead of returning a fixed shape.
    """

    def __init__(self, provider: ModelProvider | None = None) -> None:
        self.provider = provider

    def verify_claim(
        self,
        claim: str,
        evidence: list[str] | None = None,
        provider: ModelProvider | None = None,
    ) -> VerificationResult:
        result = VerificationResult(claim=claim)
        if evidence:
            result.evidence = evidence

        active_provider = provider or self.provider
        if active_provider is None:
            return result

        evidence_block = "\n".join(f"- {e}" for e in (evidence or [])) or "(no evidence provided)"
        response = active_provider.generate(
            f"Claim: {claim}\n\nEvidence:\n{evidence_block}\n\n"
            "Assess strictly whether the evidence actually supports the claim. "
            "Do not assume the claim is true. Respond in exactly this format:\n"
            "VERIFIED: yes or no\n"
            "CONFIDENCE: a number between 0.0 and 1.0\n"
            "CONCERNS: comma-separated concerns, or 'none'",
            system="You are a skeptical, independent verification module. "
            "Your job is to find reasons the claim might be wrong, not to agree with it.",
            temperature=0.2,
            max_tokens=300,
        )
        self._apply_verification_response(result, response.text)
        return result

    def _apply_verification_response(self, result: VerificationResult, text: str) -> None:
        result.summary = text.strip()
        for line in text.splitlines():
            line = line.strip()
            upper = line.upper()
            if upper.startswith("VERIFIED:"):
                result.is_verified = line.split(":", 1)[1].strip().lower().startswith("y")
            elif upper.startswith("CONFIDENCE:"):
                with contextlib.suppress(ValueError):
                    result.confidence = max(0.0, min(1.0, float(line.split(":", 1)[1].strip())))
            elif upper.startswith("CONCERNS:"):
                raw = line.split(":", 1)[1].strip()
                if raw and raw.lower() != "none":
                    result.concerns = [c.strip() for c in raw.split(",") if c.strip()]

    def challenge(
        self,
        conclusion: str,
        assumptions: list[str] | None = None,
        provider: ModelProvider | None = None,
    ) -> list[str]:
        active_provider = provider or self.provider
        if active_provider is None:
            return list(_STATIC_CHALLENGE_QUESTIONS)

        assumptions_block = "; ".join(assumptions) if assumptions else "(none stated)"
        response = active_provider.generate(
            f"Conclusion: {conclusion}\nStated assumptions: {assumptions_block}\n\n"
            "Write 3-5 specific, pointed questions that would help someone find a flaw "
            "in THIS conclusion — not generic verification questions. One per line.",
            system="You are a rigorous, skeptical technical reviewer.",
            temperature=0.5,
            max_tokens=300,
        )
        questions = [q.strip("-•* ").strip() for q in response.text.splitlines() if q.strip()]
        return questions or list(_STATIC_CHALLENGE_QUESTIONS)

    def cross_check(
        self, claim_a: str, claim_b: str, evidence_a: list[str], evidence_b: list[str]
    ) -> str:
        shared = set(evidence_a) & set(evidence_b)
        if shared:
            return f"Claims share {len(shared)} pieces of supporting evidence."
        return "Claims have no shared evidence. Independent verification needed."
