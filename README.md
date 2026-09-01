# AGI Cognitive Runtime

> A model-agnostic cognitive architecture for general-purpose AI agents.

## What This Is

An open-source cognitive runtime that augments LLMs with architectural mechanisms required for increasingly general intelligence: memory, world models, planning, reasoning operators, hypothesis generation, verification, learning, transfer, and metacognition.

## What This Is NOT

- A prompt library
- A RAG system
- A collection of books
- A coding assistant
- A collection of agent personas
- A chain-of-thought extraction system
- A fixed workflow for one domain

## Architecture

```
USER / ENVIRONMENT
        |
        v
   PERCEPTION
        |
        v
   UNDERSTANDING & WORLD MODEL
        |
   +----+----+----+
   |         |         |
   v         v         v
 MEMORY  KNOWLEDGE  EXPERIENCE
   |         |         |
   +----+----+----+
        |
        v
   COGNITIVE ENGINE
   (abstraction, reasoning, analogy, causality,
    hypothesis generation, planning, decision,
    creativity, metacognition)
        |
        v
   ACTION / TOOLS
        |
        v
   OBSERVATION
        |
        v
   VERIFICATION
        |
   SUCCESS -> CONSOLIDATE
   FAILURE -> LEARN / ADAPT -> REPLAN
```

## Cognitive Loop

```
OBSERVE -> UNDERSTAND -> MODEL -> FORMULATE -> PLAN
    -> ACT -> OBSERVE RESULT -> VERIFY -> LEARN
    -> UPDATE MODEL -> REPLAN / FINISH
```

## How It Works

### Task Classification

Every task is automatically classified into one of 7 cognitive depth levels:

| Level | Name | When |
|-------|------|------|
| L0 | Direct | Simple factual questions |
| L1 | Reason | Requires logical reasoning |
| L2 | Plan | Requires building/creating |
| L3 | Investigate | Requires debugging/hypotheses |
| L4 | Experiment | Requires testing/comparing |
| L5 | Adapt | Requires recovery/fixing |
| L6 | Long-horizon | Multi-session projects |

The classifier uses keyword analysis with magnitude-based precedence (the signal with the most matches wins, not a fixed order).

### Cognitive Execution Flow

When you call `runtime.run("your task")`, the runtime:

1. **Classifies** the task depth (L0-L6)
2. **Generates plan** based on depth requirements
3. **Retrieves memory** - searches for similar past experiences
4. **Searches knowledge** - applies relevant principles and heuristics
5. **Generates hypotheses** (if L3+) - uses LLM to create specific, testable hypotheses
6. **Compiles context** - packages everything for the LLM
7. **Executes** - runs the task (with tools if configured)
8. **Verifies** (if complexity > 0.3) - uses skeptical LLM prompt to assess the answer
9. **Updates metacognition** - confidence, failure risk, uncertainties
10. **Learns** - stores episode with lessons for future use

### Key Components

#### Memory System
- **Episodic**: Stores past experiences with tasks, actions, results, and lessons
- **Semantic**: Generalized knowledge entries
- **Procedural**: Reusable skills with success/failure tracking
- **Failure**: Records of failures for learning

#### Hypothesis Engine
- Generates specific, falsifiable hypotheses using LLM
- Tracks confidence with Bayesian updates
- Supports supporting/contradictory evidence

#### Verification Engine
- Independent assessment using skeptical LLM prompts
- Parses structured responses (VERIFIED/CONFIDENCE/CONCERNS)
- Generates claim-specific challenge questions
- Falls back to static questions without LLM provider

#### Metacognition
- Tracks current confidence and failure risk
- `should_ask_user()` gates success when confidence is low
- `should_proceed()` determines if execution should continue
- Records uncertainty sources and known unknowns

#### Knowledge Store
- **Principles**: Fundamental rules (e.g., "Hypothesis-Driven Debugging")
- **Heuristics**: Shortcuts (e.g., "Binary Search Debugging")
- **Procedures**: Step-by-step processes
- **Anti-patterns**: Things to avoid

#### Cognitive Budget
- Enforces resource limits (max steps, tool calls, hypotheses)
- Prevents runaway execution
- Reports failure when budget exhausted

## Quick Start

```bash
pip install -e ".[dev]"
pytest
agi status
```

## Usage

### CLI

```bash
# Classify a task
agi classify "Investigate why the API is slow"

# Run a task
agi run "Fix the memory leak in the cache service"

# Generate a plan
agi plan "Build a microservice with Redis"

# Start investigation
agi investigate "Why does the database timeout?"

# Verify a claim
agi verify "The new architecture handles 10x traffic"

# Research with subagents
agi research "Best practices for zero-downtime deployments"

# Full review (research + critique + verify + synth)
agi full_review "Microservices are better than monoliths"

# View cognitive logs
agi logs
agi logs <task_id>
agi logs --json <task_id>

# Session persistence
agi session-create --name "Debug Session"
agi session-save <session_id> --task "Debug API"
agi session-list
agi replay <snapshot_id>

# Knowledge management
agi import-knowledge knowledge/

# Transfer demo
agi transfer-demo
```

### Python API

```python
from agi_runtime.runtime import CognitiveRuntime

# Basic usage (no LLM)
runtime = CognitiveRuntime()
result = runtime.run("Investigate why the API is slow")
print(result.answer)
print(result.depth)  # L3_investigate
print(result.lessons)

# With LLM provider
from agi_runtime.providers.factory import create_provider

provider = create_provider()  # Auto-detect from env
runtime = CognitiveRuntime(model_provider=provider)
result = runtime.run("Fix the memory leak", use_tools=True)

# With custom budget
from agi_runtime.runtime import CognitiveBudget

budget = CognitiveBudget(max_steps=20, max_tool_calls=10)
runtime = CognitiveRuntime(budget=budget)

# Access memory
episodes = runtime.memory.episodes
knowledge = runtime.knowledge.search("debugging")

# Access metacognition
print(runtime.metacognition.current_confidence)
print(runtime.metacognition.should_ask_user())
```

### Provider Configuration

```bash
# OpenAI
OPENAI_API_KEY=sk-... agi run "Research caching"

# Ollama (local)
AGI_PROVIDER=ollama AGI_MODEL=llama3.1 agi run "Debug the bug"

# OpenCode (local server)
AGI_PROVIDER=opencode agi run "Investigate the issue"
```

## Logging

Every cognitive execution generates detailed logs:

```
logs/
├── cognitive_20260901_233112.json  # Structured JSON
├── cognitive_20260901_233112.log   # Human-readable
```

### Log Structure

```json
{
  "task_id": "20260901_233112",
  "total_steps": 7,
  "metrics": {
    "hypotheses_generated": 1,
    "memory_queries": 1,
    "knowledge_applied": 10,
    "tool_calls": 0,
    "verification_checks": 1,
    "lessons_learned": 1,
    "duration_ms": 12.46
  },
  "steps": [
    {"step": 0, "type": "TASK_RECEIVED", "description": "..."},
    {"step": 1, "type": "CLASSIFY", "description": "Depth=L3_investigate"},
    {"step": 2, "type": "PLAN", "description": "Generated 8 steps"},
    {"step": 3, "type": "MEMORY", "description": "Results=2 TopRelevance=1.00"},
    {"step": 4, "type": "KNOWLEDGE", "description": "Applied 10 entries"},
    {"step": 5, "type": "LEARN", "description": "Completed task"},
    {"step": 6, "type": "METACOG", "description": "Confidence=0.50"}
  ]
}
```

## Components

### Core (`src/agi_runtime/`)

| Module | Purpose |
|--------|---------|
| `runtime.py` | Main orchestrator - `CognitiveRuntime.run()` |
| `types.py` | Enums: CognitiveDepth, GoalStatus, PlanStatus, etc. |
| `cognition/operators.py` | 20 cognitive operators (OBSERVE, UNDERSTAND, etc.) |
| `compiler/policy.py` | 7 policies (L0-L6) mapping depth to operators |

### Memory (`src/agi_runtime/memory/`)

| Module | Purpose |
|--------|---------|
| `models.py` | Episode, SemanticEntry, ProceduralSkill, FailureRecord |
| `retriever.py` | EpisodicRetriever with structural similarity |

### Reasoning (`src/agi_runtime/reasoning/`)

| Module | Purpose |
|--------|---------|
| `hypothesis.py` | Hypothesis, HypothesisSpace with Bayesian confidence |

### Planning (`src/agi_runtime/planning/`)

| Module | Purpose |
|--------|---------|
| `plan.py` | Plan, PlanStep with dependency resolution |
| `adaptive.py` | AdaptivePlanner with failure detection |

### Knowledge (`src/agi_runtime/knowledge/`)

| Module | Purpose |
|--------|---------|
| `store.py` | In-memory KnowledgeStore with lexical search |
| `importer.py` | YAML/MD knowledge importer |

### Verification (`src/agi_runtime/verification/`)

| Module | Purpose |
|--------|---------|
| `engine.py` | VerificationEngine with LLM-based assessment |

### Action (`src/agi_runtime/action/`)

| Module | Purpose |
|--------|---------|
| `tools.py` | 6 builtin tools (bash, read, write, edit, glob, grep) |
| `loop.py` | ToolUseLoop for LLM-tool interaction |

### Orchestration (`src/agi_runtime/orchestration/`)

| Module | Purpose |
|--------|---------|
| `agents.py` | SubAgent, AgentOrchestrator (researcher, critic, verifier, synthesizer) |

### Persistence (`src/agi_runtime/persistence/`)

| Module | Purpose |
|--------|---------|
| `sqlite.py` | SQLiteMemoryStore, SQLiteKnowledgeStore |
| `session.py` | SessionPersistence, RuntimeSnapshot |
| `replay.py` | CognitiveReplay from saved state |

### Providers (`src/agi_runtime/providers/`)

| Module | Purpose |
|--------|---------|
| `base.py` | Abstract ModelProvider interface |
| `openai_provider.py` | OpenAI-compatible HTTP provider |
| `opencode_provider.py` | OpenCode local API provider |
| `factory.py` | Auto-detect provider from env vars |

### Metacognition (`src/agi_runtime/metacognition/`)

| Module | Purpose |
|--------|---------|
| `state.py` | MetacognitiveState with confidence tracking |

### Context (`src/agi_runtime/context/`)

| Module | Purpose |
|--------|---------|
| `compiler.py` | ContextCompiler, CognitiveContext for LLM |

### CLI (`src/agi_runtime/cli/`)

| Module | Purpose |
|--------|---------|
| `app.py` | 24 Typer commands |

## Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_runtime.py

# Run audit-specific tests
pytest tests/test_audit_fixes.py
```

### Test Coverage

- 167 tests across 27 test files
- Unit tests for every module
- Integration tests for the runtime pipeline
- Audit tests verifying specific bug fixes

## Development

```bash
pip install -e ".[all]"
pytest
ruff check src/
```

## Project Structure

```
agi-cognitive-runtime/
├── src/agi_runtime/           # Source code
│   ├── runtime.py             # Main runtime
│   ├── types.py               # Enums and schemas
│   ├── cognition/             # Cognitive operators
│   ├── compiler/              # Policy compiler
│   ├── context/               # Context compiler
│   ├── knowledge/             # Knowledge store
│   ├── logging/               # Cognitive logging
│   ├── memory/                # Memory models + retriever
│   ├── metacognition/         # Self-awareness
│   ├── orchestration/         # Multi-agent
│   ├── persistence/           # SQLite + sessions
│   ├── planning/              # Plan + adaptive
│   ├── providers/             # LLM providers
│   ├── reasoning/             # Hypothesis engine
│   ├── transfer/              # Cross-domain
│   ├── verification/          # Independent checking
│   ├── world/                 # Task, Goal, WorldModel
│   ├── action/                # Tools + loop
│   └── cli/                   # CLI commands
├── tests/                     # 167 tests
├── benchmarks/                # 7 benchmark tasks
├── knowledge/                 # 23 seeded entries
├── .opencode/                 # OpenCode integration
├── AUDIT.md                   # Architectural audit log
├── AGENT_TASK.md              # Full spec (95 sections)
├── demo.py                    # End-to-end demo
└── pyproject.toml             # Build config
```

## OpenCode Integration

This project integrates natively with OpenCode:

- **Agents**: `.opencode/agents/` - Primary AGI agent and cognitive specialists
- **Skills**: `.opencode/skills/` - Cognitive runtime, deep reasoning, research, etc.
- **Commands**: `.opencode/commands/` - `/agi`, `/research`, `/investigate`, etc.

## License

MIT
