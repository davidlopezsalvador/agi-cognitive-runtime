# Hypothesis-Driven Debugging

## Concept

Using systematic hypothesis formation and testing to find root causes.

## Principle

Generate multiple competing hypotheses, then design experiments that best distinguish between them.

## Heuristics

- Generate at least 3 hypotheses before testing any.
- Prefer the cheapest experiment that best separates hypotheses.
- Track confidence for each hypothesis explicitly.
- Abandon hypotheses only with evidence, not intuition.

## Triggers

- Intermittent failures
- Unknown root cause
- Complex system behavior
- Performance issues

## Procedure

1. Observe the problem
2. Generate candidate hypotheses
3. Rank by plausibility
4. Design distinguishing experiments
5. Execute experiments
6. Update confidence
7. Identify root cause

## Anti-Patterns

- Jumping to first hypothesis
- Testing everything at once
- Ignoring contradictory evidence
- Confirmation bias
