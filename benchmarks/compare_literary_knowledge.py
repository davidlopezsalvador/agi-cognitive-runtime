"""A/B harness: does adding the literary-derived knowledge entries change
runtime behaviour on benchmarks/literary_tasks.py, compared to the same
runtime without them?

IMPORTANT — this script needs a real `ModelProvider` (OpenAI or OpenCode)
to test the thing it claims to test. Without one, `CognitiveRuntime` falls
back to template answers for every task regardless of which knowledge
store it has (see runtime.py's `else: answer = "Cognitive runtime
processed: ..."` branch), so both conditions will score identically —
that would demonstrate nothing about the literary entries and everything
about the fallback path. This script will warn and refuse to claim a
result if no provider is passed, rather than silently printing a
meaningless "both scored 0.0" comparison. This wasn't run against a live
model in this sandbox — it's provided ready to run once a provider is
configured; see providers/factory.py for how to build one.

Usage (with a provider available):

    from agi_runtime.providers.factory import create_provider
    from benchmarks.compare_literary_knowledge import run_comparison

    provider = create_provider(...)
    run_comparison(provider)
"""

from __future__ import annotations

from agi_runtime.providers.base import ModelProvider
from agi_runtime.runtime import CognitiveRuntime
from benchmarks.literary_tasks import LITERARY_BENCHMARKS
from benchmarks.runner import BenchmarkRunner

# knowledge/ lives at the repo root, not under src/agi_runtime — it's an
# experimental add-on, deliberately not part of the installed package.
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from knowledge.seed import seed_knowledge  # noqa: E402
from knowledge.seed_literary import seed_literary_knowledge  # noqa: E402


def run_comparison(provider: ModelProvider | None) -> dict:
    if provider is None:
        print(
            "No model_provider given — refusing to run a comparison that would "
            "just show both conditions falling back to the same template answer. "
            "Configure a provider (see providers/factory.py) and pass it in."
        )
        return {}

    baseline_knowledge = seed_knowledge()
    literary_knowledge = seed_literary_knowledge(seed_knowledge())

    baseline_runtime = CognitiveRuntime(model_provider=provider, knowledge=baseline_knowledge)
    literary_runtime = CognitiveRuntime(model_provider=provider, knowledge=literary_knowledge)

    baseline_suite = BenchmarkRunner(baseline_runtime).run_all(LITERARY_BENCHMARKS)
    literary_suite = BenchmarkRunner(literary_runtime).run_all(LITERARY_BENCHMARKS)

    comparison = {
        "baseline": {
            "pass_rate": baseline_suite.pass_rate(),
            "average_score": baseline_suite.average_score(),
            "results": {r.task_id: r.score for r in baseline_suite.results},
        },
        "literary": {
            "pass_rate": literary_suite.pass_rate(),
            "average_score": literary_suite.average_score(),
            "results": {r.task_id: r.score for r in literary_suite.results},
        },
    }

    print(f"{'task':<20} {'baseline':>10} {'literary':>10}")
    for task in LITERARY_BENCHMARKS:
        b = comparison["baseline"]["results"].get(task.id, 0.0)
        l = comparison["literary"]["results"].get(task.id, 0.0)
        print(f"{task.id:<20} {b:>10.2f} {l:>10.2f}")
    print()
    print(f"{'pass_rate':<20} {comparison['baseline']['pass_rate']:>10.2f} {comparison['literary']['pass_rate']:>10.2f}")
    print(f"{'avg_score':<20} {comparison['baseline']['average_score']:>10.2f} {comparison['literary']['average_score']:>10.2f}")

    return comparison


if __name__ == "__main__":
    run_comparison(None)
