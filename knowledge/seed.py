"""Seed the knowledge corpus with initial principles, heuristics, and procedures."""

from __future__ import annotations

from pathlib import Path

from agi_runtime.knowledge.store import KnowledgeEntry, KnowledgeStore


def seed_knowledge(store: KnowledgeStore | None = None) -> KnowledgeStore:
    """Populate the knowledge store with initial entries."""
    if store is None:
        store = KnowledgeStore()

    entries = [
        # Reasoning
        KnowledgeEntry(
            id="reasoning.abduction.basic",
            type="principle",
            name="Abductive Reasoning",
            description="Inferring plausible explanations from observations.",
            summary="Prefer explanations that account for available evidence while minimizing unnecessary assumptions.",
            domain=["reasoning", "inference"],
            triggers=["debugging", "diagnosis", "investigation"],
            procedure=[
                "Collect observations",
                "Generate candidate explanations",
                "Compare explanatory power",
                "Identify missing evidence",
                "Test candidates",
            ],
            anti_patterns=["premature_conclusion", "single_hypothesis_lock_in"],
            verification_questions=[
                "What alternative explanation exists?",
                "What evidence would falsify this explanation?",
            ],
        ),
        KnowledgeEntry(
            id="reasoning.deduction.basic",
            type="principle",
            name="Deductive Reasoning",
            description="Drawing conclusions that necessarily follow from premises.",
            summary="If premises are true and logic is valid, conclusion must be true.",
            domain=["reasoning", "logic"],
            triggers=["formal_reasoning", "verification", "proof"],
            procedure=[
                "State premises clearly",
                "Apply logical rules",
                "Derive conclusion",
                "Verify validity",
            ],
        ),
        KnowledgeEntry(
            id="reasoning.induction.basic",
            type="principle",
            name="Inductive Reasoning",
            description="Generalizing from specific observations to broader principles.",
            summary="Patterns observed in specific cases may hold generally, but certainty is never guaranteed.",
            domain=["reasoning", "science"],
            triggers=["pattern_detection", "generalization", "hypothesis_formation"],
            procedure=[
                "Observe multiple instances",
                "Identify common patterns",
                "Form general hypothesis",
                "Test against new instances",
                "Refine generalization",
            ],
        ),
        KnowledgeEntry(
            id="reasoning.analogy.basic",
            type="principle",
            name="Analogical Reasoning",
            description="Transfer reasoning from a familiar domain to an unfamiliar one.",
            summary="Structural similarities between domains can transfer solutions.",
            domain=["reasoning", "transfer"],
            triggers=["novel_problem", "cross_domain", "transfer"],
            procedure=[
                "Identify source domain",
                "Map structural elements",
                "Transfer relations",
                "Verify alignment",
                "Adapt to target",
            ],
        ),

        # Problem solving
        KnowledgeEntry(
            id="problem.decomposition.basic",
            type="principle",
            name="Decomposition",
            description="Break complex problems into simpler subproblems.",
            summary="A decomposed problem is easier to solve than a monolithic one.",
            domain=["problem_solving", "engineering"],
            triggers=["complex_task", "multi_step", "design"],
            procedure=[
                "Identify the whole problem",
                "Find natural boundaries",
                "Create subproblems",
                "Identify dependencies",
                "Solve subproblems",
                "Integrate solutions",
            ],
        ),
        KnowledgeEntry(
            id="problem.first_principles",
            type="principle",
            name="First Principles Thinking",
            description="Break down problems to fundamental truths and reason up from there.",
            summary="Start from the most basic, undeniable facts and build reasoning from there.",
            domain=["problem_solving", "reasoning"],
            triggers=["complex_system", "confusion", "innovation"],
            procedure=[
                "Identify assumptions",
                "Break down to fundamentals",
                "Reason from basics",
                "Rebuild understanding",
            ],
        ),
        KnowledgeEntry(
            id="problem.binary_search",
            type="heuristic",
            name="Binary Search Debugging",
            description="Halve the search space to find problems efficiently.",
            summary="When searching for a cause, eliminate half the possibilities at each step.",
            domain=["debugging", "investigation"],
            triggers=["debugging", "search", "diagnosis"],
            procedure=[
                "Identify search space",
                "Pick midpoint",
                "Test which half contains the problem",
                "Repeat until found",
            ],
        ),

        # Systems
        KnowledgeEntry(
            id="systems.shared_state",
            type="anti_pattern",
            name="Shared Mutable State",
            description="Shared mutable state creates hidden coupling and inconsistency.",
            summary="Avoid shared mutable state. Prefer immutable data or explicit synchronization.",
            domain=["systems", "concurrency"],
            triggers=["race_condition", "inconsistent_state", "concurrency_bug"],
            procedure=[
                "Identify shared state",
                "Determine mutation patterns",
                "Apply synchronization or make immutable",
            ],
        ),
        KnowledgeEntry(
            id="systems.failure_isolation",
            type="principle",
            name="Failure Isolation",
            description="Failures should be contained, not propagated.",
            summary="Design systems so failures in one component don't cascade.",
            domain=["systems", "reliability"],
            triggers=["system_design", "reliability", "fault_tolerance"],
            procedure=[
                "Identify failure modes",
                "Design containment boundaries",
                "Implement circuit breakers",
                "Add health checks",
            ],
        ),
        KnowledgeEntry(
            id="systems.observable_state",
            type="principle",
            name="Observable State",
            description="Systems should expose their internal state for debugging.",
            summary="If you can't see it, you can't fix it.",
            domain=["systems", "observability"],
            triggers=["debugging", "monitoring", "system_health"],
            procedure=[
                "Add structured logging",
                "Expose health endpoints",
                "Track key metrics",
                "Enable distributed tracing",
            ],
        ),

        # Debugging
        KnowledgeEntry(
            id="debugging.reproduce_first",
            type="procedure",
            name="Reproduce First",
            description="Always reproduce the bug before attempting to fix it.",
            summary="A bug you can't reproduce is a bug you can't verify fixing.",
            domain=["debugging"],
            triggers=["bug_fix", "investigation"],
            procedure=[
                "Gather all information about the bug",
                "Create minimal reproduction steps",
                "Verify reproduction",
                "Only then attempt fix",
            ],
        ),
        KnowledgeEntry(
            id="debugging.binary_search_debug",
            type="procedure",
            name="Binary Search Debugging",
            description="Use git bisect or similar to narrow down when a bug was introduced.",
            summary="When did it last work? When does it fail? The answer is between those points.",
            domain=["debugging"],
            triggers=["regression", "git", "version_control"],
            procedure=[
                "Find a passing version",
                "Find a failing version",
                "Bisect between them",
                "Identify the introducing commit",
            ],
        ),
        KnowledgeEntry(
            id="debugging.rubber_duck",
            type="heuristic",
            name="Rubber Duck Debugging",
            description="Explain the problem aloud to find the solution.",
            summary="The act of articulating a problem often reveals the answer.",
            domain=["debugging"],
            triggers=["stuck", "confusion", "complex_bug"],
            procedure=[
                "Explain what you expected",
                "Explain what actually happened",
                "Explain each step of the code",
                "Find where expectation diverges from reality",
            ],
        ),

        # Software engineering
        KnowledgeEntry(
            id="se.yagni",
            type="heuristic",
            name="YAGNI",
            description="You Ain't Gonna Need It. Don't build what you don't need yet.",
            summary="Premature optimization is the root of all evil.",
            domain=["software_engineering", "design"],
            triggers=["design", "architecture", "feature_request"],
            procedure=[
                "Identify the simplest solution that works",
                "Implement it",
                "Refactor when needed",
            ],
        ),
        KnowledgeEntry(
            id="se.kiss",
            type="heuristic",
            name="KISS Principle",
            description="Keep It Simple, Stupid.",
            summary="Simplicity is the ultimate sophistication.",
            domain=["software_engineering", "design"],
            triggers=["design", "complexity", "refactoring"],
            procedure=[
                "Choose the simplest approach",
                "Avoid unnecessary abstractions",
                "Prefer readable over clever",
            ],
        ),
        KnowledgeEntry(
            id="se.single_responsibility",
            type="principle",
            name="Single Responsibility Principle",
            description="A module should have one, and only one, reason to change.",
            summary="Each component should do one thing well.",
            domain=["software_engineering", "design"],
            triggers=["design", "refactoring", "modularity"],
            procedure=[
                "Identify what the component does",
                "Check if it does more than one thing",
                "Split if needed",
            ],
        ),

        # Planning
        KnowledgeEntry(
            id="planning.iterative",
            type="procedure",
            name="Iterative Planning",
            description="Plan at a high level, execute a step, then refine the plan.",
            summary="Plans are hypotheses about how to achieve goals. Revise as you learn.",
            domain=["planning", "project_management"],
            triggers=["complex_project", "uncertainty", "long_horizon"],
            procedure=[
                "Create high-level plan",
                "Execute first step",
                "Observe result",
                "Update plan based on learning",
                "Repeat",
            ],
        ),
        KnowledgeEntry(
            id="planning.stopping_rules",
            type="heuristic",
            name="Stopping Rules",
            description="Define when to stop iterating before you start.",
            summary="Without stopping rules, you'll iterate forever.",
            domain=["planning", "decision_making"],
            triggers=["iteration", "optimization", "decision"],
            procedure=[
                "Define success criteria",
                "Set time/resource budget",
                "Define diminishing returns threshold",
                "Stop when any rule triggers",
            ],
        ),

        # Decision making
        KnowledgeEntry(
            id="decision.reversible_irreversible",
            type="heuristic",
            name="One-Way vs Two-Way Doors",
            description="Distinguish reversible from irreversible decisions.",
            summary="Two-way doors can be changed easily. One-way doors require careful deliberation.",
            domain=["decision_making", "management"],
            triggers=["decision", "architecture", "strategy"],
            procedure=[
                "Classify the decision type",
                "For two-way doors: decide quickly",
                "For one-way doors: deliberate carefully",
            ],
        ),
        KnowledgeEntry(
            id="decision.regret_minimization",
            type="heuristic",
            name="Regret Minimization",
            description="Choose the option you'll least regret in 10 years.",
            summary="Long-term thinking clarifies short-term decisions.",
            domain=["decision_making"],
            triggers=["major_decision", "tradeoff", "career"],
            procedure=[
                "Project forward 10 years",
                "Consider regret for each option",
                "Choose the least regrettable",
            ],
        ),

        # Metacognition
        KnowledgeEntry(
            id="metacognition.calibration",
            type="principle",
            name="Confidence Calibration",
            description="Your confidence should match your actual accuracy.",
            summary="Overconfidence is more dangerous than underconfidence.",
            domain=["metacognition", "reasoning"],
            triggers=["uncertainty", "judgment", "prediction"],
            procedure=[
                "Track predictions and confidence",
                "Compare predicted vs actual accuracy",
                "Adjust confidence levels",
                "Seek disconfirming evidence",
            ],
        ),
        KnowledgeEntry(
            id="metacognition.bias_awareness",
            type="principle",
            name="Cognitive Bias Awareness",
            description="Be aware of systematic biases in your reasoning.",
            summary="Confirmation bias, anchoring, and availability heuristic distort judgment.",
            domain=["metacognition", "reasoning"],
            triggers=["judgment", "decision", "analysis"],
            procedure=[
                "Consider what you might be biased toward",
                "Seek disconfirming evidence",
                "Consider the opposite",
                "Use structured decision processes",
            ],
        ),

        # Transfer
        KnowledgeEntry(
            id="transfer.structural_similarity",
            type="principle",
            name="Structural Similarity",
            description="Transfer knowledge based on structural similarity, not surface features.",
            summary="Problems with the same deep structure can use the same solution strategy.",
            domain=["transfer", "learning"],
            triggers=["novel_problem", "cross_domain", "reuse"],
            procedure=[
                "Abstract the problem to its structure",
                "Search for structurally similar past problems",
                "Identify transferable elements",
                "Adapt to new domain",
            ],
        ),
    ]

    for entry in entries:
        store.add(entry)

    return store
