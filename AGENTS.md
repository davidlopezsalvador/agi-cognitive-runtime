# AGI Cognitive Runtime - Agent Instructions

## Project Overview

This is the AGI Cognitive Runtime: a model-agnostic cognitive architecture for general-purpose AI agents. The runtime augments LLMs with memory, world models, planning, reasoning operators, hypothesis generation, verification, learning, transfer, and metacognition.

## Architecture

Core components:
- **Task Model**: Structured task representation
- **Goal Management**: Explicit goals with hierarchy
- **World Model**: Agent's beliefs about the environment
- **Cognitive Operators**: Reusable cognitive actions
- **Planning Engine**: Multi-strategy planning
- **Memory**: Working, episodic, semantic, procedural, failure
- **Knowledge Store**: Principles, heuristics, procedures
- **Hypothesis Engine**: Form and test hypotheses
- **Verification Engine**: Independent conclusion checking
- **Transfer Engine**: Cross-domain knowledge application
- **Metacognition**: Self-awareness and confidence tracking
- **Context Compiler**: Compact context for LLM

## Development Rules

- Use Python 3.10+
- Use Pydantic for all models
- Use type hints everywhere
- Write tests for every cognitive operator
- Keep components independent and testable
- Never silently swallow failures
- Always track uncertainty explicitly

## Testing

```bash
pytest
```

## Code Style

- Follow existing patterns
- No comments unless asked
- Prefer explicit over clever
- Observable state over hidden magic
