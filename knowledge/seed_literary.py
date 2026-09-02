"""Optional literary-derived reasoning patterns for the AGI Cognitive Runtime.

Kept deliberately OUT of knowledge/seed.py's seed_knowledge() so they're an
explicit, toggleable experimental variable rather than baked into every
runtime by default. See AUDIT.md and benchmarks/literary_tasks.py for the
experiment this supports: does surfacing these patterns change agent
behaviour on adaptation/verification tasks, compared to the same runtime
without them?

Each entry follows the same KnowledgeEntry shape as knowledge/seed.py — a
distilled, structured heuristic with explicit triggers and verification
questions — NOT raw literary prose. The `source` field documents where the
pattern was extracted from; that provenance is doing real work here, since
these two are unvalidated hypotheses about transferable reasoning patterns,
not established principles like the ones in seed.py.
"""

from __future__ import annotations

from agi_runtime.knowledge.store import KnowledgeEntry, KnowledgeStore


def seed_literary_knowledge(store: KnowledgeStore | None = None) -> KnowledgeStore:
    """Adds the literary-derived entries to `store` (or a new one) and
    returns it. Call this IN ADDITION to seed_knowledge() when you want the
    "literary" condition of the experiment; skip it for the baseline
    condition. Never call it unconditionally inside CognitiveRuntime — that
    would remove the ability to A/B test it."""
    if store is None:
        store = KnowledgeStore()

    entries = [
        KnowledgeEntry(
            id="reasoning.adaptation.picaresque",
            type="heuristic",
            name="Picaresque Iterative Adaptation",
            description=(
                "Treat an adversarial or information-scarce environment as the "
                "default condition, not an exception, and extract a narrow, "
                "mechanistic lesson from each failure that compounds into the "
                "next attempt instead of starting over from a blank slate."
            ),
            summary=(
                "Each failed attempt should yield one specific, reusable trick "
                "tied to a concrete trigger condition — not a vague resolution "
                "to 'be more careful' — and later attempts should explicitly "
                "build on earlier ones."
            ),
            domain=["adaptation", "resilience", "learning", "memory"],
            triggers=[
                "repeated failure",
                "adversarial or opaque environment",
                "resource scarcity",
                "multiple similar attempts",
                "unreliable or withholding counterpart",
            ],
            heuristics=[
                "Assume the environment will not volunteer information you need — verify it yourself before relying on it.",
                "When an attempt fails, extract a lesson specific enough to name the exact trigger it applies to, not a general mood ('be careful').",
                "Check episodic memory for a lesson from a structurally similar past failure before generating a fresh strategy from scratch.",
                "Let each new lesson refine, not replace, the previous one when they apply to the same trigger.",
            ],
            procedure=[
                "Attempt the task with the best available strategy.",
                "On failure, identify the exact mechanism that caused it (not just 'it failed').",
                "State the lesson as: when <trigger>, do <specific action> — avoid vague lessons.",
                "Store the lesson in episodic memory tagged with its trigger.",
                "On the next similar attempt, retrieve and apply matching lessons before acting.",
            ],
            anti_patterns=[
                "Treating each new attempt as unrelated to the last one.",
                "Recording a lesson too vague to know when it applies.",
                "Assuming good faith or full information from an opaque or adversarial environment.",
                "Repeating an already-failed strategy because the lesson from it was never made specific enough to retrieve.",
            ],
            verification_questions=[
                "Is this lesson specific enough that I'd know exactly when to apply it next time?",
                "Have I checked memory for a similar past failure before generating a new strategy?",
                "Am I assuming information the environment hasn't actually confirmed?",
            ],
            source=(
                "Structural pattern derived from the picaresque narrative form — "
                "specifically Lazarillo de Tormes, a first-person account of "
                "successive service under a sequence of masters, where each "
                "episode of deprivation or deception yields one concrete, "
                "reusable trick carried into the next. Unvalidated as a "
                "transferable LLM reasoning aid — treat as an experimental "
                "hypothesis, not an established principle."
            ),
            tags=["experimental", "literary-derived"],
        ),
        KnowledgeEntry(
            id="metacognition.verification.quixotic_dialectic",
            type="pattern",
            name="Quixotic-Pragmatic Verification Dialectic",
            description=(
                "Pair an ambitious, interpretive reading of ambiguous evidence "
                "with an explicit, mundane reality-check role that is allowed "
                "to dissent without the goal being abandoned outright."
            ),
            summary=(
                "Confident interpretation and grounded skepticism are two "
                "required roles, not a single voice: propose the ambitious "
                "reading, then explicitly test it against the plainest, least "
                "flattering explanation before acting on it."
            ),
            domain=["metacognition", "verification", "planning"],
            triggers=[
                "high-confidence conclusion from ambiguous evidence",
                "single source of interpretation",
                "no dissenting check performed",
                "decision made under enthusiasm for a plan",
            ],
            heuristics=[
                "After forming a confident interpretation, explicitly generate the plainest, least interesting alternative explanation before acting.",
                "Notice when you are interpreting ambiguous evidence in the direction your goal wants it to point.",
                "Treat a dissenting or deflating counter-read as information to engage with, not an obstacle to the plan.",
                "Revise the plan in light of the pragmatic check rather than either ignoring it or abandoning the goal entirely.",
            ],
            procedure=[
                "State the confident interpretation and what it implies for action.",
                "Generate the plain, unglamorous alternative explanation for the same evidence.",
                "Ask what observation would distinguish between the two.",
                "If the mundane explanation isn't ruled out, revise the plan instead of proceeding on the confident one.",
            ],
            anti_patterns=[
                "Accepting the first coherent interpretation of ambiguous evidence without a grounding check.",
                "Silencing or skipping the pragmatic check to preserve momentum on the plan.",
                "Abandoning the goal entirely at the first pragmatic objection instead of revising it.",
            ],
            verification_questions=[
                "What would the plainest, most unglamorous explanation be?",
                "Am I interpreting this evidence in the direction I want it to point?",
                "What single observation would settle this either way?",
            ],
            source=(
                "Structural pattern derived from the Quijote-Sancho dialectic in "
                "Don Quijote — a goal-driven, idealizing interpreter paired with "
                "a pragmatic, grounding counterpart who voices dissent without "
                "abandoning the shared journey. Unvalidated as a transferable "
                "LLM reasoning aid — treat as an experimental hypothesis, not "
                "an established principle."
            ),
            tags=["experimental", "literary-derived"],
        ),
    ]

    for entry in entries:
        store.add(entry)

    return store
