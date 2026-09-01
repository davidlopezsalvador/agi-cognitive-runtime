# Shared Mutable State Anti-Pattern

## Concept

Shared mutable state creates hidden coupling and increases the probability of inconsistent system behavior.

## Principle

Avoid shared mutable state. Prefer immutable data, message passing, or explicit synchronization.

## Heuristics

- If multiple components can modify the same data, expect concurrency bugs.
- Prefer copy-on-read over shared references.
- When sharing is necessary, use explicit locks or atomic operations.
- Design for immutability by default.

## Triggers

- Race conditions
- Inconsistent state
- Hard-to-reproduce bugs
- Distributed systems

## Examples

- Python global state causing test pollution
- Database connections shared without pooling
- Cache invalidation races
- Distributed consensus failures

## Verification Questions

- Can any two components modify this data concurrently?
- Is the mutation visible to all readers immediately?
- What happens if one reader sees partially updated state?
