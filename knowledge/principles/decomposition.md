# Decomposition

## Concept

Breaking complex problems into simpler, manageable subproblems.

## Principle

A problem that can be decomposed into independent subproblems can be solved more reliably than the original monolithic problem.

## Heuristics

- Decompose along natural boundaries (modules, data flows, time steps).
- Prefer decomposition that creates independently testable units.
- When decomposition creates dependencies, make them explicit.
- Stop decomposing when subproblems are directly solvable.

## Triggers

- Complex task
- Multi-step problem
- System design
- Debugging

## Procedure

1. Identify the whole problem
2. Find natural boundaries
3. Create subproblems
4. Identify dependencies
5. Solve subproblems
6. Integrate solutions

## Anti-Patterns

- Over-decomposition (too many tiny pieces)
- Under-decomposition (keeping it monolithic)
- Ignoring dependencies between subproblems
