# Architectural audit — 2026-09-02

Findings from reading `src/agi_runtime/runtime.py` end to end against the
subsystems it instantiates, plus the fixes applied. Tests for each fix are
in `tests/test_audit_fixes.py`.

## Fixed in this pass

1. **`classify()` precedence bug.** Depth selection was a fixed
   `if/elif` chain (long_horizon → adapt → experiment → investigate →
   plan), so a single incidental adapt-word match always beat any number
   of planning-word matches. Now the depth with the highest keyword count
   wins; ties fall back to the old severity order.
   Known limitation left as-is: `L1_REASON` is still unreachable, because
   `total_signal > 0` guarantees at least one of the five counters is
   `> 0`. Making it reachable needs its own "reasoning_words" signal —
   a real design decision, not something to guess at here.

2. **Duplicate, diverging episodic-memory scoring.**
   `Memory.find_similar_episodes()` and `EpisodicRetriever.retrieve()`
   were two independently-tuned implementations of the same job. Within a
   single `run()` call, both were invoked with different results.
   `find_similar_episodes()` now delegates to `EpisodicRetriever` (single
   scorer). `ContextCompiler.compile()` takes an optional
   `retrieved_episodes` param so `run()` retrieves once and reuses it,
   instead of scoring the whole episode store twice per task.

3. **`generate_hypotheses()` was string templating, not reasoning.**
   `Hypothesis(statement=f"Hypothesis from: {obs}")` regardless of content.
   Now calls the configured `model_provider` to produce a real, specific
   hypothesis per observation; falls back to the same template when no
   provider is configured (documented, not hidden).

4. **`VerificationEngine.verify_claim()` didn't verify anything.**
   `is_verified` and `confidence` never left their Pydantic defaults;
   `challenge()` returned the same static 9 questions for every claim.
   Both now call the provider (when configured) to actually assess the
   specific claim/evidence and generate claim-specific challenge
   questions. No-provider behaviour is unchanged and documented as a
   fallback, not real verification.

5. **Metacognition was inert.** `MetacognitiveState` was constructed with
   defaults and never updated or read anywhere in `run()` —
   `should_proceed()` / `should_ask_user()` were never called. Verification
   results now update `current_confidence`, `failure_risk`,
   `known_unknowns`, `uncertainty_sources`, `verification_status`, and
   `should_ask_user()` now actually flips `RuntimeResult.success` to
   `False` instead of the method always returning `success=True`.

6. **`CognitiveBudget` was aspirational.** `max_steps` was defined but
   `_step_count` was never incremented; `max_tool_calls` was defined but
   `ToolUseLoop` was constructed with its own hardcoded default of 10.
   `_step_count` now increments at each phase boundary and `run()` stops
   early with `success=False` if the budget is exhausted;
   `ToolUseLoop.max_iterations` is now wired from `budget.max_tool_calls`.

## Explicitly NOT wired in this pass

`TransferEngine`, `AgentOrchestrator`, and `AdaptivePlanner` are
constructed in `CognitiveRuntime.__init__` but no code path in `run()`
calls them — this was true before this audit and is still true now.
Wiring them meaningfully requires product decisions this audit shouldn't
guess at: when does a task warrant multi-agent orchestration vs. a single
pass? What counts as a `ReplanTrigger` in practice? Faking a call to
these just to make the architecture diagram true would be worse than
leaving them honestly unwired.

`plan_task()` still builds a `Plan` with steps (e.g. "Generate
hypotheses", "Design experiments", "Verify results") that `run()` does
not walk step-by-step — `run()` executes a fixed sequence of phases and
records the plan for the trace/context, it doesn't interpret it. Turning
the plan into something that's actually executed step-by-step (with
per-step tool use, verification, and replanning on failure) is a bigger
redesign than this pass, and again needs a decision on what a "step
executor" protocol looks like.

## Suggested next audit target

`plan_task()` → real step-by-step execution, since that's the piece that
would make the hypothesis/verify/replan loop in the README actually
happen instead of being front-loaded into two calls before the answer.
