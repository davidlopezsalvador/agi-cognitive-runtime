"""Benchmark tasks designed to make the literary-knowledge experiment
measurable (see knowledge/seed_literary.py, AUDIT.md).

CAVEAT (read before trusting a pass/fail from these): BenchmarkRunner._evaluate
and ._score do keyword-overlap matching against task.answer text, plus flat
bonuses for having verification/lessons/plan-steps — it does NOT judge
reasoning quality. A run that mentions the right words without actually
reasoning that way would still "pass" here; a run that reasons well but
phrases it differently would not. Treat a pass/fail from these tasks as a
weak, cheap signal to run repeatedly across many trials, not proof that the
literary heuristic worked. success_criteria below are phrased with the
keywords the desired behaviour would plausibly use, specifically so they
have a chance under that evaluator — that's a concession to the harness,
not a claim that word-matching is a good judge of reasoning.

Also note: CognitiveRuntime.run() now sets RuntimeResult.success = False
when MetacognitiveState.should_ask_user() fires (see AUDIT.md #5). Since
_evaluate() requires result.success first, a run that appropriately flags
low confidence on an ambiguous task — arguably the CORRECT behaviour for
adapt_lazarillo_01 / verify_quixote_01 — will register as a benchmark
failure. Read a "fail" on these two tasks with that in mind; it may mean
"handled the uncertainty honestly" rather than "got it wrong".
"""

from benchmarks import BenchmarkCategory, BenchmarkTask

LITERARY_BENCHMARKS: list[BenchmarkTask] = [
    BenchmarkTask(
        id="adapt_lazarillo_01",
        category=BenchmarkCategory.ADAPTATION,
        name="Compounding lessons across an adversarial, information-scarce task",
        description=(
            "You are negotiating API rate limits with three different third-party "
            "vendors, one after another, for the same integration. The first vendor "
            "gives you a rate limit that turns out to be far lower than documented "
            "once you hit it in practice, and support is slow to confirm the real "
            "number. Describe how you would approach the second and third vendor "
            "negotiations differently as a result of what happened with the first — "
            "be specific about what you'd verify up front and why, rather than just "
            "resolving to 'be more careful'."
        ),
        expected_output=(
            "Names a specific verification step to take before trusting documented "
            "limits (e.g. testing empirically before committing), states it as a "
            "rule tied to the trigger condition (undocumented or unconfirmed limits), "
            "and explicitly carries the lesson from vendor 1 into how vendor 2 and 3 "
            "are approached rather than starting fresh each time."
        ),
        success_criteria=[
            "States a specific verification step, not a vague intention",
            "Ties the lesson to a concrete trigger condition",
            "Explicitly builds on the previous vendor's experience for the next one",
            "Treats the vendor relationship as not fully trustworthy by default",
        ],
        difficulty=3,
        tags=["experimental", "literary-derived", "picaresque"],
    ),
    BenchmarkTask(
        id="verify_quixote_01",
        category=BenchmarkCategory.VERIFICATION,
        name="Checking a confident interpretation against the mundane explanation",
        description=(
            "A production error rate spiked right after your team's deploy. You are "
            "confident the deploy caused it — the timing lines up perfectly and your "
            "team is under pressure to prove the new feature is stable. Before you "
            "report the root cause, walk through how you would check that conclusion, "
            "including what the plainest, least dramatic alternative explanation "
            "might be and how you'd rule it in or out."
        ),
        expected_output=(
            "Explicitly generates at least one plain, unglamorous alternative "
            "explanation (e.g. unrelated infra issue, coincidental timing, a "
            "dependency's own incident) before accepting the deploy-caused theory, "
            "names a concrete check that would distinguish the two, and does not "
            "treat confidence under pressure as sufficient evidence on its own."
        ),
        success_criteria=[
            "Explicitly considers a plain alternative explanation, not just the deploy theory",
            "Names a concrete check or observation that would distinguish the theories",
            "Notes that confidence under pressure to confirm a theory is not itself evidence",
        ],
        difficulty=3,
        tags=["experimental", "literary-derived", "quixotic"],
    ),
]
