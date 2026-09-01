"""Tests for world model and task."""

from agi_runtime.world.task import Task, TaskClassification
from agi_runtime.world.goal import Goal, GoalTree
from agi_runtime.world.model import Belief, WorldModel, WorldModelEntry
from agi_runtime.types import CognitiveDepth, EpistemicStatus, GoalStatus


def test_task_creation():
    task = Task(
        objective="Fix the bug",
        desired_outcome="Bug is resolved",
    )
    assert task.objective == "Fix the bug"
    assert task.cognitive_depth == CognitiveDepth.L0_DIRECT


def test_task_with_constraints():
    task = Task(
        objective="Deploy service",
        desired_outcome="Service is live",
        constraints=["Must not downtime", "Must pass tests"],
    )
    assert len(task.constraints) == 2


def test_task_classification():
    cls = TaskClassification(
        depth=CognitiveDepth.L3_INVESTIGATE,
        domain="debugging",
        complexity=0.7,
        uncertainty_level=0.8,
        requires_planning=True,
        requires_hypotheses=True,
    )
    assert cls.depth == CognitiveDepth.L3_INVESTIGATE
    assert cls.requires_hypotheses is True


def test_goal_creation():
    goal = Goal(description="Fix production issue", priority=1)
    assert goal.status == GoalStatus.ACTIVE
    assert goal.priority == 1


def test_goal_tree():
    tree = GoalTree()
    g1 = Goal(description="Parent goal")
    g2 = Goal(description="Child goal", parent_id=g1.id)
    tree.add_goal(g1)
    tree.add_goal(g2)
    assert len(tree.goals) == 2
    assert len(tree.active_goals()) == 2

    tree.complete_goal(g1.id)
    assert len(tree.active_goals()) == 1


def test_world_model_entry():
    entry = WorldModelEntry(entity="API server", state="running")
    assert entry.entity == "API server"
    entry.verify()
    assert entry.last_verified is not None


def test_belief():
    belief = Belief(
        claim="The bug is in the auth module",
        status=EpistemicStatus.HYPOTHESIS,
        confidence=0.6,
    )
    assert belief.status == EpistemicStatus.HYPOTHESIS


def test_world_model():
    wm = WorldModel()
    entry = WorldModelEntry(entity="database", state="connected")
    belief = Belief(claim="DB is healthy", status=EpistemicStatus.FACT)

    wm.add_entry(entry)
    wm.add_belief(belief)

    assert wm.get_entity("database") is not None
    assert len(wm.facts()) == 1
    assert len(wm.hypotheses()) == 0
