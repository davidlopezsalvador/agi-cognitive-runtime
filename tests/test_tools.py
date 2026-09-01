"""Tests for tool execution."""

from agi_runtime.action.tools import BuiltinTools, ToolResult


def test_list_tools():
    tools = BuiltinTools()
    tool_list = tools.list_tools()
    assert len(tool_list) == 6
    names = [t.name for t in tool_list]
    assert "bash" in names
    assert "read" in names
    assert "write" in names


def test_bash_success():
    tools = BuiltinTools()
    result = tools.execute("bash", {"command": "echo hello"})
    assert result.success
    assert "hello" in result.output


def test_bash_failure():
    tools = BuiltinTools()
    result = tools.execute("bash", {"command": "exit 1"})
    assert not result.success


def test_unknown_tool():
    tools = BuiltinTools()
    result = tools.execute("nonexistent", {})
    assert not result.success
    assert "Unknown tool" in result.error
