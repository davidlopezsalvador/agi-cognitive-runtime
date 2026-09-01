"""Tests for tool-use loop."""

from agi_runtime.action.tools import BuiltinTools
from agi_runtime.action.loop import ToolUseLoop, ToolCall


def test_execute_tool():
    tools = BuiltinTools()
    loop = ToolUseLoop(tools)
    result = loop.execute_tool("bash", {"command": "echo hello"})
    assert result.success
    assert "hello" in result.output
    assert len(loop.call_history) == 1


def test_simple_execute_bash():
    tools = BuiltinTools()
    loop = ToolUseLoop(tools)
    output, tool_result = loop.simple_execute("run echo test")
    assert "test" in output
    assert tool_result is not None


def test_simple_execute_read():
    tools = BuiltinTools()
    loop = ToolUseLoop(tools)
    output, tool_result = loop.simple_execute("read pyproject.toml")
    assert "agi-cognitive-runtime" in output
    assert tool_result is not None


def test_simple_execute_unknown():
    tools = BuiltinTools()
    loop = ToolUseLoop(tools)
    output, tool_result = loop.simple_execute("unknown command")
    assert output == ""
    assert tool_result is None


def test_call_history():
    tools = BuiltinTools()
    loop = ToolUseLoop(tools)
    loop.execute_tool("bash", {"command": "echo a"})
    loop.execute_tool("bash", {"command": "echo b"})
    assert len(loop.call_history) == 2
    assert loop.call_history[0].tool_name == "bash"
