"""CLI entry point for the AGI Cognitive Runtime."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Optional

import typer

app = typer.Typer(
    name="agi",
    help="AGI Cognitive Runtime - A model-agnostic cognitive architecture for AI agents.",
    no_args_is_help=True,
)


def _get_runtime():
    from agi_runtime.runtime import CognitiveRuntime
    from agi_runtime.providers.factory import create_provider
    provider = create_provider()
    runtime = CognitiveRuntime(model_provider=provider)

    from knowledge.seed import seed_knowledge
    seed_knowledge(runtime.knowledge)

    return runtime


@app.command()
def status() -> None:
    """Show current runtime status."""
    runtime = _get_runtime()
    state = runtime.status()
    typer.echo("AGI Cognitive Runtime v0.1.0")
    typer.echo(f"Active goals: {state['active_goals']}")
    typer.echo(f"Total goals: {state['total_goals']}")
    typer.echo(f"Hypotheses: {state['hypotheses']}")
    typer.echo(f"Episodes: {state['episodes']}")
    typer.echo(f"Semantic entries: {state['semantic_entries']}")
    typer.echo(f"Skills: {state['skills']}")
    typer.echo(f"Failures: {state['failures']}")
    typer.echo(f"Knowledge: {state['knowledge_entries']}")
    typer.echo(f"World model: {state['world_model_entries']} entries, {state['beliefs']} beliefs")
    typer.echo(f"Metacognition: {state['metacognition']}")


@app.command()
def init() -> None:
    """Initialize a new AGI runtime workspace."""
    workspace = Path(".")
    dirs = [
        "memory/episodic",
        "memory/semantic",
        "memory/procedural",
        "knowledge/concepts",
        "knowledge/principles",
        "knowledge/heuristics",
        "knowledge/procedures",
    ]
    for d in dirs:
        (workspace / d).mkdir(parents=True, exist_ok=True)
    typer.echo("Workspace initialized.")


@app.command()
def classify(task: str) -> None:
    """Classify a task's cognitive requirements."""
    runtime = _get_runtime()
    cls = runtime.classify(task)
    typer.echo(f"Task: {task}")
    typer.echo(f"Depth: {cls.depth.value}")
    typer.echo(f"Domain: {cls.domain}")
    typer.echo(f"Complexity: {cls.complexity:.2f}")
    typer.echo(f"Uncertainty: {cls.uncertainty_level:.2f}")
    typer.echo(f"Requires planning: {cls.requires_planning}")
    typer.echo(f"Requires hypotheses: {cls.requires_hypotheses}")
    typer.echo(f"Requires verification: {cls.requires_verification}")
    typer.echo(f"Reason: {cls.reasoning}")


@app.command()
def run(
    task: str,
    verbose: bool = typer.Option(False, "--verbose", "-v"),
) -> None:
    """Run a task through the cognitive runtime."""
    runtime = _get_runtime()
    typer.echo(f"Running: {task}")
    result = runtime.run(task)
    typer.echo(f"\n--- Result ---")
    typer.echo(f"Success: {result.success}")
    typer.echo(f"Depth: {result.depth.value}")
    typer.echo(f"Duration: {result.duration_seconds:.2f}s")
    typer.echo(f"\nAnswer:\n{result.answer}")
    if result.verification:
        typer.echo(f"\nVerification: {result.verification}")
    if result.lessons:
        typer.echo(f"\nLessons: {', '.join(result.lessons)}")
    if verbose and result.plan:
        typer.echo(f"\nPlan ({len(result.plan.steps)} steps):")
        for s in result.plan.steps:
            typer.echo(f"  [{s.status.value}] {s.action}")


@app.command()
def plan(task: str) -> None:
    """Generate a plan for a task."""
    runtime = _get_runtime()
    cls = runtime.classify(task)
    task_obj = runtime.plan_task(
        __import__("agi_runtime.world.task", fromlist=["Task"]).Task(
            objective=task,
            desired_outcome="Completed",
            cognitive_depth=cls.depth,
        )
    )
    typer.echo(f"Plan for: {task}")
    typer.echo(f"Depth: {cls.depth.value}")
    typer.echo(f"Steps ({len(task_obj.steps)}):")
    for s in task_obj.steps:
        typer.echo(f"  - {s.action}")


@app.command()
def investigate(problem: str) -> None:
    """Start a hypothesis-driven investigation."""
    runtime = _get_runtime()
    result = runtime.run(problem)
    typer.echo(f"Investigation: {problem}")
    typer.echo(f"Result: {result.answer}")


@app.command()
def verify(claim: str) -> None:
    """Independently verify a claim."""
    runtime = _get_runtime()
    result = runtime.verify(claim)
    typer.echo(f"Claim: {claim}")
    typer.echo(f"Verification: {result}")


@app.command()
def learn() -> None:
    """Extract lessons from the current session."""
    runtime = _get_runtime()
    episodes = runtime.memory.episodes
    lessons = [ep.lesson for ep in episodes if ep.lesson]
    typer.echo(f"Lessons learned ({len(lessons)}):")
    for lesson in lessons:
        typer.echo(f"  - {lesson}")


@app.command()
def memory_stats() -> None:
    """Show memory statistics."""
    runtime = _get_runtime()
    typer.echo("Memory statistics:")
    typer.echo(f"  Episodes: {len(runtime.memory.episodes)}")
    typer.echo(f"  Semantic entries: {len(runtime.memory.semantic)}")
    typer.echo(f"  Procedural skills: {len(runtime.memory.procedural)}")
    typer.echo(f"  Failure records: {len(runtime.memory.failures)}")


@app.command()
def benchmark(run_all: bool = typer.Option(False, "--all", "-a")) -> None:
    """Run benchmarks."""
    from benchmarks.initial_tasks import INITIAL_BENCHMARKS
    from benchmarks.runner import BenchmarkRunner

    runtime = _get_runtime()
    runner = BenchmarkRunner(runtime)

    if run_all:
        tasks = INITIAL_BENCHMARKS
    else:
        tasks = INITIAL_BENCHMARKS[:3]

    typer.echo(f"Running {len(tasks)} benchmarks...")
    suite = runner.run_all(tasks)
    summary = runner.summary(suite)

    typer.echo(f"\n--- Benchmark Results ---")
    typer.echo(f"Total: {summary['total_tasks']}")
    typer.echo(f"Passed: {summary['passed']}")
    typer.echo(f"Pass rate: {summary['pass_rate']:.1%}")
    typer.echo(f"Avg score: {summary['average_score']:.2f}")
    typer.echo(f"Duration: {summary['total_duration']:.2f}s")

    for result in suite.results:
        status = "PASS" if result.passed else "FAIL"
        typer.echo(f"  [{status}] {result.task_id}: score={result.score:.2f}")


@app.command()
def tools() -> None:
    """List available tools."""
    runtime = _get_runtime()
    for tool in runtime.tools.list_tools():
        typer.echo(f"  {tool.name}: {tool.description}")


@app.command()
def research(question: str) -> None:
    """Research mode: gather and synthesize information."""
    runtime = _get_runtime()
    typer.echo(f"Researching: {question}")
    result = runtime.orchestrator.research(question)
    typer.echo(f"\nFindings:")
    for f in result.findings:
        typer.echo(f"  - {f}")
    typer.echo(f"\nConfidence: {result.confidence:.2f}")


@app.command()
def critique(claim: str) -> None:
    """Critically evaluate a claim."""
    runtime = _get_runtime()
    typer.echo(f"Critiquing: {claim}")
    result = runtime.orchestrator.critique(claim)
    typer.echo(f"\nCritique:")
    for f in result.findings:
        typer.echo(f"  - {f}")


@app.command()
def full_review(claim: str) -> None:
    """Full review: research + critique + verify + synthesize."""
    runtime = _get_runtime()
    typer.echo(f"Full review: {claim}")
    results = runtime.orchestrator.full_review(claim)
    for role, result in results.items():
        typer.echo(f"\n--- {role.title()} ---")
        for f in result.findings:
            typer.echo(f"  - {f}")


@app.command()
def inspect(what: str = typer.Argument("status")) -> None:
    """Inspect runtime state."""
    valid = ["status", "task", "plan", "memory", "beliefs", "hypotheses", "trace", "retrieval", "policy"]
    if what not in valid:
        typer.echo(f"Invalid target. Valid: {', '.join(valid)}")
        raise typer.Exit(1)

    runtime = _get_runtime()

    if what == "status":
        state = runtime.status()
        typer.echo(json.dumps(state, indent=2, default=str))
    elif what == "memory":
        typer.echo(f"Episodes: {len(runtime.memory.episodes)}")
        typer.echo(f"Semantic: {len(runtime.memory.semantic)}")
        typer.echo(f"Skills: {len(runtime.memory.procedural)}")
        typer.echo(f"Failures: {len(runtime.memory.failures)}")
    elif what == "beliefs":
        for b in runtime.world_model.beliefs:
            typer.echo(f"  [{b.status.value}] {b.claim} (conf={b.confidence:.2f})")
    elif what == "hypotheses":
        for h in runtime.hypotheses.rank():
            typer.echo(f"  [{h.status.value}] {h.statement} (conf={h.posterior_confidence:.2f})")
    elif what == "policy":
        from agi_runtime.compiler.policy import PolicyCompiler
        pc = PolicyCompiler()
        for p in pc.list_policies():
            typer.echo(f"  {p['id']}: {p['name']} (depth={p['depth']}) ops={p['operators']}")
    else:
        typer.echo(f"Inspecting: {what}")
        typer.echo("Detailed inspection requires runtime integration.")


@app.command()
def session_create(name: str = typer.Option("", "--name", "-n")) -> None:
    """Create a new session."""
    from agi_runtime.persistence.session import SessionPersistence
    persistence = SessionPersistence()
    session_id = persistence.create_session(name)
    typer.echo(f"Session created: {session_id}")
    persistence.close()


@app.command()
def session_list() -> None:
    """List all sessions."""
    from agi_runtime.persistence.session import SessionPersistence
    persistence = SessionPersistence()
    sessions = persistence.list_sessions()
    if not sessions:
        typer.echo("No sessions found.")
    else:
        for s in sessions:
            typer.echo(f"  {s['id']} - {s['name'] or 'Unnamed'} ({s['created']})")
    persistence.close()


@app.command()
def session_save(
    session_id: str,
    task: str = "",
    answer: str = "",
    depth: str = "",
) -> None:
    """Save current runtime state to a session."""
    from agi_runtime.persistence.session import SessionPersistence
    from agi_runtime.runtime import CognitiveTrace

    runtime = _get_runtime()
    persistence = SessionPersistence()

    trace = CognitiveTrace(task=task or "CLI session", cognitive_mode=depth)
    snap_id = persistence.save_snapshot(
        session_id,
        trace,
        answer=answer,
        depth=depth,
        episodes=runtime.memory.episodes,
        beliefs=runtime.world_model.beliefs,
        hypotheses=runtime.hypotheses.hypotheses,
    )
    typer.echo(f"Snapshot saved: {snap_id}")
    persistence.close()


@app.command()
def session_load(snapshot_id: str) -> None:
    """Load a snapshot and display its state."""
    from agi_runtime.persistence.session import SessionPersistence
    persistence = SessionPersistence()

    snap = persistence.load_snapshot(snapshot_id)
    if not snap:
        typer.echo(f"Snapshot not found: {snapshot_id}")
        raise typer.Exit(1)

    typer.echo(f"Task: {snap['task']}")
    typer.echo(f"Depth: {snap['depth']}")
    typer.echo(f"Answer: {snap['answer'][:200]}")
    typer.echo(f"Episodes: {len(snap['episodes'])}")
    typer.echo(f"Beliefs: {len(snap['beliefs'])}")
    typer.echo(f"Hypotheses: {len(snap['hypotheses'])}")
    persistence.close()


@app.command()
def replay(snapshot_id: str) -> None:
    """Replay a cognitive trace."""
    from agi_runtime.persistence.session import SessionPersistence
    from agi_runtime.persistence.replay import CognitiveReplay

    persistence = SessionPersistence()
    replay_engine = CognitiveReplay(persistence)

    steps = replay_engine.replay_snapshot(snapshot_id)
    if not steps:
        typer.echo(f"No trace found for: {snapshot_id}")
        raise typer.Exit(1)

    typer.echo(f"Cognitive Replay ({len(steps)} steps):")
    for s in steps:
        typer.echo(f"  [{s.step:3d}] {s.event_type}: {s.description[:80]}")
    persistence.close()


@app.command()
def import_knowledge(
    path: str = typer.Argument("knowledge"),
    pattern: str = typer.Option("*.yaml", "--pattern", "-p"),
) -> None:
    """Import knowledge from YAML/MD files."""
    from agi_runtime.knowledge.importer import KnowledgeImporter
    from agi_runtime.knowledge.store import KnowledgeStore

    store = KnowledgeStore()
    importer = KnowledgeImporter(store)

    import_path = Path(path)
    if import_path.is_dir():
        count = importer.import_knowledge_dir(import_path)
    elif import_path.is_file():
        count = importer.import_yaml_file(import_path)
    else:
        typer.echo(f"Path not found: {path}")
        raise typer.Exit(1)

    typer.echo(f"Imported {count} knowledge entries from {path}")
    typer.echo(f"Total entries in store: {len(store.entries)}")


@app.command()
def transfer_demo() -> None:
    """Run the transfer demo across domains."""
    from agi_runtime.transfer.demo import TransferDemonstrator

    demo = TransferDemonstrator()
    demo.populate_from_seed()

    results = demo.full_transfer_demo()
    typer.echo("=== Transfer Demo Results ===")
    for r in results:
        typer.echo(f"\nSource: {r.source_domain}")
        typer.echo(f"Target: {r.target_domain}")
        typer.echo(f"Abstraction: {r.shared_abstraction[:80]}")
        typer.echo(f"Confidence: {r.confidence:.2f}")


if __name__ == "__main__":
    app()
