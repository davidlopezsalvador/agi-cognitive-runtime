"""Tool execution system for the AGI Cognitive Runtime."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from agi_runtime.providers.base import ToolDefinition, ToolProvider


class ToolResult(BaseModel):
    """Result of a tool execution."""

    success: bool = True
    output: str = ""
    error: str = ""
    exit_code: int = 0
    metadata: dict[str, Any] = Field(default_factory=dict)


class BuiltinTools(ToolProvider):
    """Built-in tools: bash, read, write, grep, glob, edit."""

    def __init__(self, working_dir: str | Path = ".") -> None:
        self.working_dir = Path(working_dir).resolve()

    def list_tools(self) -> list[ToolDefinition]:
        return [
            ToolDefinition(
                name="bash",
                description="Execute a shell command",
                parameters={"command": {"type": "string", "description": "Command to execute"}},
            ),
            ToolDefinition(
                name="read",
                description="Read a file's contents",
                parameters={"path": {"type": "string", "description": "File path to read"}},
            ),
            ToolDefinition(
                name="write",
                description="Write content to a file",
                parameters={
                    "path": {"type": "string", "description": "File path"},
                    "content": {"type": "string", "description": "Content to write"},
                },
            ),
            ToolDefinition(
                name="edit",
                description="Edit a file by replacing text",
                parameters={
                    "path": {"type": "string"},
                    "old": {"type": "string", "description": "Text to replace"},
                    "new": {"type": "string", "description": "Replacement text"},
                },
            ),
            ToolDefinition(
                name="glob",
                description="Find files matching a pattern",
                parameters={"pattern": {"type": "string", "description": "Glob pattern"}},
            ),
            ToolDefinition(
                name="grep",
                description="Search file contents with regex",
                parameters={
                    "pattern": {"type": "string", "description": "Regex pattern"},
                    "path": {"type": "string", "description": "Directory to search"},
                    "include": {"type": "string", "description": "File pattern to include"},
                },
            ),
        ]

    def execute(self, tool_name: str, arguments: dict[str, Any]) -> ToolResult:
        dispatch = {
            "bash": self._bash,
            "read": self._read,
            "write": self._write,
            "edit": self._edit,
            "glob": self._glob,
            "grep": self._grep,
        }
        handler = dispatch.get(tool_name)
        if not handler:
            return ToolResult(success=False, error=f"Unknown tool: {tool_name}")
        try:
            return handler(**arguments)
        except Exception as e:
            return ToolResult(success=False, error=str(e))

    def _bash(self, command: str, timeout: int = 30) -> ToolResult:
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(self.working_dir),
            )
            return ToolResult(
                success=result.returncode == 0,
                output=result.stdout,
                error=result.stderr,
                exit_code=result.returncode,
            )
        except subprocess.TimeoutExpired:
            return ToolResult(success=False, error=f"Command timed out after {timeout}s")

    def _read(self, path: str) -> ToolResult:
        file_path = self.working_dir / path
        if not file_path.exists():
            return ToolResult(success=False, error=f"File not found: {path}")
        try:
            content = file_path.read_text(encoding="utf-8")
            return ToolResult(output=content)
        except Exception as e:
            return ToolResult(success=False, error=str(e))

    def _write(self, path: str, content: str) -> ToolResult:
        file_path = self.working_dir / path
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")
            return ToolResult(output=f"Written {len(content)} bytes to {path}")
        except Exception as e:
            return ToolResult(success=False, error=str(e))

    def _edit(self, path: str, old: str, new: str) -> ToolResult:
        file_path = self.working_dir / path
        if not file_path.exists():
            return ToolResult(success=False, error=f"File not found: {path}")
        try:
            content = file_path.read_text(encoding="utf-8")
            if old not in content:
                return ToolResult(success=False, error=f"Text not found in {path}")
            new_content = content.replace(old, new, 1)
            file_path.write_text(new_content, encoding="utf-8")
            return ToolResult(output=f"Edited {path}")
        except Exception as e:
            return ToolResult(success=False, error=str(e))

    def _glob(self, pattern: str) -> ToolResult:
        matches = list(self.working_dir.glob(pattern))
        paths = [str(p.relative_to(self.working_dir)) for p in matches[:100]]
        return ToolResult(output="\n".join(paths) if paths else "No matches")

    def _grep(self, pattern: str, path: str = ".", include: str = "*") -> ToolResult:
        import re

        search_dir = self.working_dir / path
        if not search_dir.exists():
            return ToolResult(success=False, error=f"Directory not found: {path}")

        results: list[str] = []
        regex = re.compile(pattern, re.IGNORECASE)
        for file_path in search_dir.rglob(include):
            if not file_path.is_file():
                continue
            try:
                for i, line in enumerate(file_path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                    if regex.search(line):
                        rel = file_path.relative_to(self.working_dir)
                        results.append(f"{rel}:{i}: {line.strip()}")
                        if len(results) >= 50:
                            break
            except Exception:
                continue
            if len(results) >= 50:
                break

        return ToolResult(output="\n".join(results) if results else "No matches")
