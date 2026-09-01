"""Tests for cognitive operators."""

from agi_runtime.cognition.operators import DEFAULT_OPERATORS, CognitiveOperator, OperatorCategory, get_operator


def test_default_operators_exist():
    assert len(DEFAULT_OPERATORS) > 0


def test_operator_categories():
    categories = {op.category for op in DEFAULT_OPERATORS}
    assert OperatorCategory.PERCEPTION in categories
    assert OperatorCategory.REASONING in categories
    assert OperatorCategory.PLANNING in categories
    assert OperatorCategory.LEARNING in categories


def test_get_operator():
    op = get_operator("OBSERVE")
    assert op is not None
    assert op.name == "OBSERVE"
    assert op.category == OperatorCategory.PERCEPTION


def test_get_nonexistent_operator():
    op = get_operator("NONEXISTENT")
    assert op is None


def test_operator_has_required_fields():
    for op in DEFAULT_OPERATORS:
        assert op.name
        assert op.category
        assert op.purpose or op.inputs or op.outputs
