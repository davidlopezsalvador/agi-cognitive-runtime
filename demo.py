"""End-to-end demo of the AGI Cognitive Runtime."""

from __future__ import annotations

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from agi_runtime.runtime import CognitiveRuntime
from agi_runtime.persistence.session import SessionPersistence
from agi_runtime.persistence.replay import CognitiveReplay
from agi_runtime.transfer.demo import TransferDemonstrator
from knowledge.seed import seed_knowledge


def demo_classify():
    print("=" * 60)
    print("DEMO 1: Task Classification")
    print("=" * 60)

    runtime = CognitiveRuntime()
    seed_knowledge(runtime.knowledge)

    tasks = [
        "What is 2 + 2?",
        "Why is the API returning 500 errors?",
        "Build a new authentication service",
        "Debug the intermittent timeout issue",
        "Test whether caching improves performance",
        "Recover from the failed deployment",
        "Create a multi-month migration project",
    ]

    for task in tasks:
        cls = runtime.classify(task)
        print(f"\n  Task: {task}")
        print(f"  Depth: {cls.depth.value}")
        print(f"  Complexity: {cls.complexity:.2f}")
        print(f"  Requires planning: {cls.requires_planning}")
        print(f"  Requires hypotheses: {cls.requires_hypotheses}")


def demo_run():
    print("\n" + "=" * 60)
    print("DEMO 2: Task Execution (without LLM)")
    print("=" * 60)

    runtime = CognitiveRuntime()
    seed_knowledge(runtime.knowledge)

    tasks = [
        "List files in the current directory",
        "Investigate why the system is slow",
        "Build a caching layer for the API",
    ]

    for task in tasks:
        result = runtime.run(task)
        print(f"\n  Task: {task}")
        print(f"  Depth: {result.depth.value}")
        print(f"  Success: {result.success}")
        print(f"  Answer: {result.answer[:100]}...")
        print(f"  Lessons: {len(result.lessons)}")


def demo_memory():
    print("\n" + "=" * 60)
    print("DEMO 3: Episodic Memory Retrieval")
    print("=" * 60)

    runtime = CognitiveRuntime()
    seed_knowledge(runtime.knowledge)

    runtime.run("Debug network latency issue")
    runtime.run("Fix memory leak in Python service")
    runtime.run("Optimize database query performance")

    print(f"\n  Episodes stored: {len(runtime.memory.episodes)}")

    results = runtime.episodic_retriever.retrieve("timeout problem")
    print(f"\n  Retrieving for 'timeout problem':")
    for r in results:
        print(f"    [{r.relevance_score:.2f}] {r.episode.task}")
        if r.applicable_lessons:
            print(f"      Lesson: {r.applicable_lessons[0][:60]}")


def demo_transfer():
    print("\n" + "=" * 60)
    print("DEMO 4: Cross-Domain Transfer")
    print("=" * 60)

    demo = TransferDemonstrator()
    demo.populate_from_seed()

    results = demo.full_transfer_demo()
    for r in results:
        print(f"\n  Source: {r.source_domain}")
        print(f"  Target: {r.target_domain}")
        print(f"  Abstraction: {r.shared_abstraction[:60]}")
        print(f"  Confidence: {r.confidence:.2f}")


def demo_persistence():
    print("\n" + "=" * 60)
    print("DEMO 5: Session Persistence & Replay")
    print("=" * 60)

    persistence = SessionPersistence()
    session_id = persistence.create_session("Demo Session")

    runtime = CognitiveRuntime()
    seed_knowledge(runtime.knowledge)

    result = runtime.run("Investigate API timeouts")

    from agi_runtime.runtime import CognitiveTrace
    trace = CognitiveTrace(
        task="Investigate API timeouts",
        cognitive_mode="L3_investigate",
        decisions=["Classified as L3", "Selected hypothesis policy"],
        observations=["Found timeout errors"],
        actions=["Ran diagnostics"],
        verification="Root cause found",
        lessons=["Check connection pool"],
    )

    snap_id = persistence.save_snapshot(
        session_id,
        trace,
        answer=result.answer,
        depth="L3_investigate",
        episodes=runtime.memory.episodes,
    )

    print(f"\n  Session: {session_id}")
    print(f"  Snapshot: {snap_id}")

    replay = CognitiveReplay(persistence)
    steps = replay.replay_snapshot(snap_id)
    print(f"\n  Replay ({len(steps)} steps):")
    for s in steps:
        print(f"    [{s.step:3d}] {s.event_type}: {s.description[:60]}")

    persistence.close()


def demo_knowledge():
    print("\n" + "=" * 60)
    print("DEMO 6: Knowledge System")
    print("=" * 60)

    runtime = CognitiveRuntime()
    seed_knowledge(runtime.knowledge)

    print(f"\n  Total knowledge entries: {len(runtime.knowledge.entries)}")

    results = runtime.knowledge.search("debugging")
    print(f"\n  Search 'debugging': {len(results)} results")
    for r in results[:3]:
        print(f"    [{r.type}] {r.name}")

    principles = runtime.knowledge.by_type("principle")
    print(f"\n  Principles: {len(principles)}")

    heuristics = runtime.knowledge.by_type("heuristic")
    print(f"  Heuristics: {len(heuristics)}")


def demo_tools():
    print("\n" + "=" * 60)
    print("DEMO 7: Tool Execution")
    print("=" * 60)

    runtime = CognitiveRuntime()

    tools = runtime.tools.list_tools()
    print(f"\n  Available tools: {len(tools)}")
    for t in tools:
        print(f"    - {t.name}: {t.description}")

    result = runtime.tools.execute("bash", {"command": "echo 'Hello from AGI Runtime!'"})
    print(f"\n  bash echo: {result.output.strip()}")

    result = runtime.tools.execute("bash", {"command": "dir" if sys.platform == "win32" else "ls -la"})
    print(f"\n  Directory listing:")
    for line in result.output.strip().split("\n")[:5]:
        print(f"    {line}")


def main():
    print("AGI Cognitive Runtime - End-to-End Demo")
    print("=" * 60)

    demo_classify()
    demo_run()
    demo_memory()
    demo_transfer()
    demo_persistence()
    demo_knowledge()
    demo_tools()

    print("\n" + "=" * 60)
    print("ALL DEMOS COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    main()
