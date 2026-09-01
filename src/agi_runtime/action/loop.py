"""Tool-use loop for the AGI Cognitive Runtime."""

from __future__ import annotations

import json
from typing import Any

from pydantic import BaseModel, Field

from agi_runtime.action.tools import BuiltinTools, ToolResult
from agi_runtime.providers.base import ModelProvider


class ToolCall(BaseModel):
    """A tool call made by the agent."""

    tool_name: str
    arguments: dict[str, Any] = Field(default_factory=dict)
    result: ToolResult | None = None
    step: int = 0


class ToolUseLoop:
    """Manages the tool-use interaction loop with the LLM."""

    def __init__(
        self,
        tools: BuiltinTools,
        provider: ModelProvider | None = None,
        max_iterations: int = 10,
    ) -> None:
        self.tools = tools
        self.provider = provider
        self.max_iterations = max_iterations
        self.call_history: list[ToolCall] = []

    def execute_tool(self, tool_name: str, arguments: dict[str, Any]) -> ToolResult:
        call = ToolCall(tool_name=tool_name, arguments=arguments)
        result = self.tools.execute(tool_name, arguments)
        call.result = result
        self.call_history.append(call)
        return result

    def run_with_tools(
        self,
        task: str,
        system_prompt: str = "",
        context: str = "",
    ) -> tuple[str, list[ToolCall]]:
        if not self.provider:
            return f"[No provider] Task: {task}", []

        tool_defs = self.tools.list_tools()
        tools_desc = "\n".join(
            f"- {t.name}: {t.description}" for t in tool_defs
        )

        messages: list[dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        user_msg = f"Task: {task}"
        if context:
            user_msg = f"Context:\n{context}\n\n{user_msg}"
        user_msg += f"\n\nAvailable tools:\n{tools_desc}\n\nTo use a tool, respond with: TOOL:tool_name:{{\"arg\": \"value\"}}\nWhen done, respond with: DONE:your answer"
        messages.append({"role": "user", "content": user_msg})

        self.call_history = []
        iterations = 0

        while iterations < self.max_iterations:
            iterations += 1
            response = self.provider.generate(
                "\n".join(m["content"] for m in messages),
                system=system_prompt,
                temperature=0.3,
                max_tokens=2048,
            )
            text = response.text.strip()

            if text.startswith("TOOL:"):
                parts = text.split(":", 2)
                if len(parts) >= 3:
                    tool_name = parts[1]
                    try:
                        arguments = json.loads(parts[2])
                    except json.JSONDecodeError:
                        arguments = {}

                    result = self.execute_tool(tool_name, arguments)
                    tool_output = result.output if result.success else f"Error: {result.error}"

                    messages.append({"role": "assistant", "content": text})
                    messages.append({
                        "role": "user",
                        "content": f"Tool result:\n{tool_output[:2000]}\n\nContinue with next tool call or respond DONE:your answer",
                    })
                else:
                    return text, self.call_history
            elif text.startswith("DONE:"):
                return text[5:].strip(), self.call_history
            else:
                return text, self.call_history

        return "[Max iterations reached]", self.call_history

    def simple_execute(self, task: str) -> tuple[str, ToolResult | None]:
        task_lower = task.lower()

        if task_lower.startswith("run ") or task_lower.startswith("execute "):
            cmd = task.split(None, 1)[1] if len(task.split(None, 1)) > 1 else task
            result = self.execute_tool("bash", {"command": cmd})
            return result.output if result.success else result.error, result

        if task_lower.startswith("read "):
            path = task.split(None, 1)[1] if len(task.split(None, 1)) > 1 else ""
            result = self.execute_tool("read", {"path": path})
            return result.output if result.success else result.error, result

        if task_lower.startswith("write "):
            parts = task.split(None, 2)
            if len(parts) >= 3:
                path = parts[1]
                content = parts[2]
                result = self.execute_tool("write", {"path": path, "content": content})
                return result.output if result.success else result.error, result

        if task_lower.startswith("grep "):
            pattern = task.split(None, 1)[1] if len(task.split(None, 1)) > 1 else ""
            result = self.execute_tool("grep", {"pattern": pattern})
            return result.output if result.success else result.error, result

        if task_lower.startswith("ls ") or task_lower == "ls":
            result = self.execute_tool("bash", {"command": "dir" if __import__("sys").platform == "win32" else "ls"})
            return result.output if result.success else result.error, result

        return "", None
