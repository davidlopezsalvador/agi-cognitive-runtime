# AGI Cognitive Skill

This skill teaches the agent how to use the AGI Cognitive Runtime.

## When to Use

- Complex tasks requiring structured reasoning
- Tasks with uncertainty or unknown causes
- Multi-step problems requiring planning
- Debugging and investigation tasks
- Research requiring hypothesis formation
- Tasks that benefit from verification loops

## Runtime API

```python
from agi_runtime.runtime import CognitiveRuntime

runtime = CognitiveRuntime()

# Classify a task
classification = runtime.classify("Investigate why API is slow")
# Returns: TaskClassification(depth=L3_investigate, ...)

# Run a task
result = runtime.run("Fix the memory leak")
# Returns: RuntimeResult(success=True, answer="...", depth=L2_plan)

# Run with tools
result = runtime.run("List files", use_tools=True)

# Verify a claim
verification = runtime.verify("The fix works")

# Research with subagents
research_result = runtime.orchestrator.research("How does caching work?")

# Full review
results = runtime.orchestrator.full_review("The architecture is sound")
```

## Cognitive Process

```
1. CLASSIFY the task (what cognitive depth is needed?)
2. RETRIEVE relevant past experiences from episodic memory
3. RETRIEVE relevant knowledge from knowledge store
4. UNDERSTAND the actual objective
5. PLAN if multi-step
6. HYPOTHESIZE if uncertain
7. EXECUTE through tools (bash, read, write, grep, glob)
8. OBSERVE results
9. VERIFY conclusions
10. LEARN from outcomes
11. CONSOLIDATE important memories
```

## Cognitive Depth Levels

- **L0 Direct**: Simple factual questions → direct execution
- **L1 Reason**: Decomposition, comparison, inference
- **L2 Plan**: Multi-step tasks, coding, system changes
- **L3 Investigate**: Unknown causes, debugging, research
- **L4 Experiment**: Competing hypotheses, empirical questions
- **L5 Adapt**: Failure recovery, changing environments
- **L6 Long Horizon**: Large projects, persistent goals

## Available Tools

- `bash`: Execute shell commands
- `read`: Read file contents
- `write`: Write to files
- `edit`: Edit files by replacement
- `glob`: Find files by pattern
- `grep`: Search file contents with regex

## Session Persistence

```python
from agi_runtime.persistence.session import SessionPersistence

persistence = SessionPersistence()
session_id = persistence.create_session("My Task")

# Save state after running
snap_id = persistence.save_snapshot(session_id, trace, answer="...")

# Load state later
snapshot = persistence.load_snapshot(snap_id)
```

## Cognitive Replay

```python
from agi_runtime.persistence.replay import CognitiveReplay

replay = CognitiveReplay(persistence)
steps = replay.replay_snapshot(snap_id)
for step in steps:
    print(f"[{step.step}] {step.event_type}: {step.description}")
```

## Knowledge Access

The runtime maintains knowledge organized by:
- `knowledge/concepts/` - Concept definitions
- `knowledge/principles/` - General principles
- `knowledge/heuristics/` - Rules of thumb
- `knowledge/procedures/` - Reusable procedures
- `knowledge/patterns/` - Common patterns
- `knowledge/anti_patterns/` - Things to avoid

## Memory Access

- Working memory: Current task state
- Episodic: Past experiences (auto-retrieved by relevance)
- Semantic: Generalized knowledge
- Procedural: Reusable skills
- Failures: What went wrong and why

## Commands

- `/agi <task>` - General AGI-mode task
- `/research <question>` - Research mode
- `/investigate <problem>` - Hypothesis-driven investigation
- `/experiment <hypothesis>` - Design and execute experiment
- `/verify <claim>` - Independent verification
- `/learn` - Extract lessons
- `/status` - Show current state
- `/tools` - List available tools
- `/critique <claim>` - Critical evaluation
- `/full_review <claim>` - Full review with all subagents
