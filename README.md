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

## Quick Start

```bash
pip install -e ".[dev]"
pytest
agi status
```

## OpenCode Integration

This project integrates natively with OpenCode:

- **Agents**: `.opencode/agents/` - Primary AGI agent and cognitive specialists
- **Skills**: `.opencode/skills/` - Cognitive runtime, deep reasoning, research, etc.
- **Commands**: `.opencode/commands/` - `/agi`, `/research`, `/investigate`, etc.

## Development

```bash
pip install -e ".[all]"
pytest
ruff check src/
mypy src/
```

## License

MIT
