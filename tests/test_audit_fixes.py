"""Tests for the fixes made during the architectural audit (see AUDIT.md).

Each test targets one specific defect that was found by reading the code,
not by running it — so each one asserts the *old* buggy behaviour would
have failed, to prove the fix actually changes something observable.
"""

from unittest.mock import MagicMock

from agi_runtime.context.compiler import ContextCompiler
from agi_runtime.memory.models import Episode, Memory
from agi_runtime.memory.retriever import EpisodicRetriever
from agi_runtime.providers.base import ModelResponse
from agi_runtime.runtime import CognitiveBudget, CognitiveRuntime
from agi_runtime.types import CognitiveDepth
from agi_runtime.verification.engine import VerificationEngine


# --- classify(): magnitude beats precedence -------------------------------


def test_classify_planning_outweighs_incidental_adapt_word():
    """Before the fix: any adapt-word match (even 1) always won over
    planning, regardless of how many planning words were present, because
    the branch order was `elif adapt > 0: L5_ADAPT` checked before planning.
    Five planning-signal words vs. one incidental 'retry' should resolve to
    planning, not adapt."""
    runtime = CognitiveRuntime()
    task = "Build, create, implement, design and architecture a new service; retry if it fails"
    cls = runtime.classify(task)
    assert cls.depth == CognitiveDepth.L2_PLAN


def test_classify_adapt_still_wins_when_it_actually_dominates():
    runtime = CognitiveRuntime()
    cls = runtime.classify("Recover, adapt, retry and change strategy, then build")
    assert cls.depth == CognitiveDepth.L5_ADAPT


# --- memory retrieval: single scorer, not two divergent ones --------------


def test_find_similar_episodes_matches_episodic_retriever():
    """Memory.find_similar_episodes used to run its own, differently-weighted
    scoring logic than EpisodicRetriever. They should now return the same
    episodes in the same order, because one delegates to the other."""
    mem = Memory()
    mem.store_episode(Episode(task="Debug timeout in payment service", lesson="Check pool size"))
    mem.store_episode(Episode(task="Unrelated task about UI colors"))

    via_memory = mem.find_similar_episodes("timeout payment", limit=5)
    via_retriever = [r.episode for r in EpisodicRetriever(mem).retrieve("timeout payment", limit=5)]

    assert [e.task for e in via_memory] == [e.task for e in via_retriever]


def test_context_compiler_reuses_passed_episodes_without_rescoring():
    """When retrieved_episodes is passed explicitly, compile() must not call
    memory.find_similar_episodes again — that's the double-retrieval bug."""
    mem = MagicMock(spec=Memory)
    mem.entries = []
    compiler = ContextCompiler(memory=mem)
    pre_retrieved = [Episode(task="x", lesson="reuse me")]

    ctx = compiler.compile("some task", retrieved_episodes=pre_retrieved)

    mem.find_similar_episodes.assert_not_called()
    assert ctx.memory_summary == "reuse me"


# --- hypothesis generation: real LLM call, not string templating ----------


def test_generate_hypotheses_uses_provider_output_not_template():
    mock_provider = MagicMock()
    mock_provider.generate.return_value = ModelResponse(
        text="The cache eviction policy is too aggressive under load."
    )
    runtime = CognitiveRuntime(model_provider=mock_provider)

    hyps = runtime.generate_hypotheses(["Requests are slow under load"], count=1)

    assert hyps[0].statement == "The cache eviction policy is too aggressive under load."
    assert not hyps[0].statement.startswith("Hypothesis from:")
    mock_provider.generate.assert_called_once()


def test_generate_hypotheses_falls_back_to_template_without_provider():
    runtime = CognitiveRuntime()
    hyps = runtime.generate_hypotheses(["Requests are slow under load"], count=1)
    assert hyps[0].statement == "Hypothesis from: Requests are slow under load"


# --- verification engine: real assessment, not an echo --------------------


def test_verify_claim_parses_provider_assessment():
    mock_provider = MagicMock()
    mock_provider.generate.return_value = ModelResponse(
        text="VERIFIED: no\nCONFIDENCE: 0.3\nCONCERNS: no regression tests, unclear rollback plan"
    )
    engine = VerificationEngine(provider=mock_provider)

    result = engine.verify_claim("The deploy is safe", evidence=["It compiled"])

    assert result.is_verified is False
    assert result.confidence == 0.3
    assert result.concerns == ["no regression tests", "unclear rollback plan"]


def test_verify_claim_without_provider_keeps_old_echo_behaviour():
    engine = VerificationEngine()
    result = engine.verify_claim("The deploy is safe", evidence=["It compiled"])
    assert result.is_verified is False
    assert result.confidence == 0.5
    assert result.concerns == []


# --- metacognition: should_ask_user() now actually gates `success` --------


def test_low_confidence_verification_flips_run_success_to_false():
    mock_provider = MagicMock()
    mock_provider.generate.side_effect = [
        ModelResponse(text="Hypothesis: caching evicts too early"),  # generate_hypotheses
        ModelResponse(text="Some answer to the task"),  # main answer
        ModelResponse(
            text="VERIFIED: no\nCONFIDENCE: 0.1\n"
            "CONCERNS: untested, unclear requirements, no rollback, conflicting evidence"
        ),  # verify_claim
        ModelResponse(text="What if the caching layer isn't the bottleneck at all?"),  # challenge
    ]
    runtime = CognitiveRuntime(model_provider=mock_provider)

    # Needs complexity > 0.3 (requires_verification) — an experiment-heavy
    # task pushes total_signal high enough; the same signal also sets
    # requires_hypotheses, hence three provider calls above.
    result = runtime.run("Design an experiment to test whether the hypothesis about caching holds")

    assert result.success is False
    assert runtime.metacognition.should_ask_user() is True


def test_verification_updates_metacognition_state():
    mock_provider = MagicMock()
    mock_provider.generate.side_effect = [
        ModelResponse(text="Hypothesis: caching evicts too early"),  # generate_hypotheses
        ModelResponse(text="An answer"),  # main answer
        ModelResponse(text="VERIFIED: yes\nCONFIDENCE: 0.9\nCONCERNS: none"),  # verify_claim
        ModelResponse(text="Is the sample size large enough?"),  # challenge
    ]
    runtime = CognitiveRuntime(model_provider=mock_provider)
    runtime.run("Design an experiment to test whether the hypothesis about caching holds")

    assert runtime.metacognition.current_confidence == 0.9
    assert runtime.metacognition.verification_status == "verified"


# --- budget: max_steps is now enforced, not aspirational -------------------


def test_budget_exceeded_stops_run_and_reports_failure():
    tiny_budget = CognitiveBudget(max_steps=1)
    runtime = CognitiveRuntime(budget=tiny_budget, enable_logging=False)

    result = runtime.run("Convert 5 km to miles")

    assert result.success is False
    assert "budget" in result.uncertainty.lower()


def test_budget_not_exceeded_with_default_budget():
    runtime = CognitiveRuntime(enable_logging=False)
    result = runtime.run("Convert 5 km to miles")
    assert result.success is True


def test_tool_loop_max_iterations_follows_budget():
    budget = CognitiveBudget(max_tool_calls=3)
    runtime = CognitiveRuntime(budget=budget, enable_logging=False)
    assert runtime.tool_loop.max_iterations == 3
