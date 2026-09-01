"""Initial benchmark tasks for the AGI Cognitive Runtime."""

from benchmarks import BenchmarkCategory, BenchmarkTask


INITIAL_BENCHMARKS: list[BenchmarkTask] = [
    # Abstraction benchmarks
    BenchmarkTask(
        id="abstract_01",
        category=BenchmarkCategory.ABSTRACTION,
        name="Extract shared principle",
        description=(
            "Given three problems: (A) Python service crashes due to shared global state, "
            "(B) Agent coordination fails due to shared global state, "
            "(C) Database process becomes inconsistent due to shared global state. "
            "Extract the general principle."
        ),
        expected_output="Shared mutable state creates hidden coupling and increases the probability of inconsistent system behavior.",
        success_criteria=["Identifies shared mutable state as the core issue", "States it as a general principle"],
        difficulty=2,
    ),
    # Transfer benchmarks
    BenchmarkTask(
        id="transfer_01",
        category=BenchmarkCategory.TRANSFER,
        name="Transfer diagnostic strategy",
        description=(
            "A software system intermittently loses messages. "
            "The agent successfully diagnoses it using hypothesis-driven debugging. "
            "Now give it: 'An RF system intermittently loses packets.' "
            "Can it transfer the same diagnostic strategy?"
        ),
        expected_output="Uses OBSERVE -> HYPOTHESIZE -> EXPERIMENT -> UPDATE -> VERIFY strategy",
        success_criteria=["Generates hypotheses", "Designs distinguishing experiments", "Does not require RF-specific prompt"],
        difficulty=3,
    ),
    # Adaptation benchmarks
    BenchmarkTask(
        id="adapt_01",
        category=BenchmarkCategory.ADAPTATION,
        name="Recover from wrong model",
        description=(
            "Agent forms hypothesis that a bug is in module A. "
            "Evidence shows module A is not involved. "
            "Measure whether agent detects contradiction, updates belief, and finds actual cause."
        ),
        expected_output="Detects contradiction, abandons module A hypothesis, investigates alternatives",
        success_criteria=["Detects contradiction", "Updates belief", "Creates new hypothesis", "Finds actual cause"],
        difficulty=3,
    ),
    # Verification benchmarks
    BenchmarkTask(
        id="verify_01",
        category=BenchmarkCategory.VERIFICATION,
        name="Detect incorrect solution",
        description=(
            "Agent is given a plausible but incorrect solution to a problem. "
            "Measure whether it independently detects the flaw."
        ),
        expected_output="Identifies the flaw in the provided solution",
        success_criteria=["Challenges the solution", "Identifies specific flaw", "Suggests correction"],
        difficulty=3,
    ),
    # Learning benchmarks
    BenchmarkTask(
        id="learn_01",
        category=BenchmarkCategory.LEARNING,
        name="Experience improves performance",
        description=(
            "Run Task Set A, allow learning, then run Task Set B. "
            "Measure whether performance improves after learning."
        ),
        expected_output="Performance on Set B is better than Set A",
        success_criteria=["Stores lessons", "Retrieves relevant experience", "Performance improves"],
        difficulty=4,
    ),
    # Confidence calibration
    BenchmarkTask(
        id="calibrate_01",
        category=BenchmarkCategory.REASONING,
        name="Confidence calibration",
        description=(
            "Give agent answerable, ambiguous, impossible, and insufficient-information problems. "
            "Measure confidence calibration and appropriate abstention."
        ),
        expected_output="Appropriate confidence levels for each problem type",
        success_criteria=[
            "High confidence for answerable",
            "Lower confidence for ambiguous",
            "Identifies impossible problems",
            "Abstains when information insufficient",
        ],
        difficulty=4,
    ),
    # Long-horizon benchmarks
    BenchmarkTask(
        id="longhorizon_01",
        category=BenchmarkCategory.PLANNING,
        name="Long-horizon goal maintenance",
        description=(
            "100-step engineering task with distractions, partial failures, "
            "new information, and changing constraints. "
            "Measure goal maintenance and completion."
        ),
        expected_output="Maintains original goal, adapts plan, finishes objective",
        success_criteria=["Maintains goal", "Updates plan", "Does not repeat failures", "Completes objective"],
        difficulty=5,
    ),
]
