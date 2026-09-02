# Picaresque Iterative Adaptation

## Concept

Treating an adversarial or information-scarce environment as the default
condition, and extracting a narrow, mechanistic lesson from each failure
that compounds into the next attempt.

## Principle

A failure is only useful if the lesson drawn from it is specific enough to
know exactly when to apply it again. Vague resolutions ("be more careful")
don't survive retrieval; concrete ones ("when the master counts the loaves,
count them first yourself") do.

## Heuristics

- Assume the environment will not volunteer information you need — verify it yourself before relying on it.
- When an attempt fails, extract a lesson specific enough to name the exact trigger it applies to.
- Check episodic memory for a lesson from a structurally similar past failure before generating a fresh strategy from scratch.
- Let each new lesson refine, not replace, the previous one when they apply to the same trigger.

## Triggers

- Repeated failure
- Adversarial or opaque environment
- Resource scarcity
- Multiple similar attempts
- Unreliable or withholding counterpart

## Procedure

1. Attempt the task with the best available strategy.
2. On failure, identify the exact mechanism that caused it.
3. State the lesson as: when `<trigger>`, do `<specific action>`.
4. Store the lesson in episodic memory tagged with its trigger.
5. On the next similar attempt, retrieve and apply matching lessons before acting.

## Anti-Patterns

- Treating each new attempt as unrelated to the last.
- Recording a lesson too vague to know when it applies.
- Assuming good faith or full information from an opaque environment.

## Verification Questions

- Is this lesson specific enough that I'd know exactly when to apply it next time?
- Have I checked memory for a similar past failure before generating a new strategy?
- Am I assuming information the environment hasn't actually confirmed?

## Source

Structural pattern derived from the picaresque narrative form — specifically
*Lazarillo de Tormes* — not an established, validated principle like the
other entries in `knowledge/principles/`. It's the experimental half of an
A/B comparison; see `benchmarks/literary_tasks.py` and
`benchmarks/compare_literary_knowledge.py`.
