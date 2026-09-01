"""OpenCode API provider - communicates with local OpenCode server."""

from __future__ import annotations

import json
import os
import re
from typing import Any, Iterator

import httpx

from agi_runtime.providers.base import ModelProvider, ModelResponse


def _detect_opencode_credentials() -> tuple[str, str]:
    """Detect OpenCode port and password from logs."""
    log_dir = os.path.join(os.environ.get("APPDATA", ""), "ai.opencode.desktop", "logs")
    if not os.path.exists(log_dir):
        return "", ""

    try:
        entries = sorted(
            [e for e in os.listdir(log_dir) if os.path.isdir(os.path.join(log_dir, e))],
            key=lambda e: os.path.getmtime(os.path.join(log_dir, e)),
            reverse=True,
        )
        if not entries:
            return "", ""

        main_log = os.path.join(log_dir, entries[0], "main.log")
        if not os.path.exists(main_log):
            return "", ""

        with open(main_log, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        port_match = re.search(r"server ready.*url: 'http://127\.0\.0\.1:(\d+)'", content)
        port = port_match.group(1) if port_match else ""

        password = os.environ.get("OPENCODE_SERVER_PASSWORD", "")

        return port, password
    except Exception:
        return "", ""


class OpenCodeProvider(ModelProvider):
    """Provider that uses the local OpenCode API server."""

    def __init__(
        self,
        base_url: str | None = None,
        username: str = "opencode",
        password: str | None = None,
        session_id: str | None = None,
    ) -> None:
        if base_url:
            self.base_url = base_url
        else:
            port, detected_password = _detect_opencode_credentials()
            if port:
                self.base_url = f"http://127.0.0.1:{port}"
            else:
                self.base_url = "http://127.0.0.1:3000"

        self.username = username
        self.password = password or os.environ.get("OPENCODE_SERVER_PASSWORD", "")
        self.session_id = session_id
        self._client = httpx.Client(timeout=120.0)

    def _auth(self) -> httpx.BasicAuth:
        return httpx.BasicAuth(self.username, self.password)

    def generate(
        self,
        prompt: str,
        system: str = "",
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs: Any,
    ) -> ModelResponse:
        parts = []
        if system:
            parts.append(system)
        parts.append(prompt)
        full_message = "\n\n".join(parts)

        payload = {
            "parts": [{"type": "text", "text": full_message}],
            "noReply": False,
        }

        tmp_path = os.path.join(os.environ.get("TEMP", "/tmp"), "opencode_payload.json")
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(payload, f)

        session_id = self.session_id or self._get_or_create_session()

        try:
            with open(tmp_path, "rb") as f:
                resp = self._client.post(
                    f"{self.base_url}/session/{session_id}/message",
                    auth=self._auth(),
                    content=f.read(),
                    headers={"Content-Type": "application/json"},
                )
            resp.raise_for_status()
            data = resp.json()

            text = ""
            if isinstance(data, dict):
                text = data.get("text", "") or data.get("content", "") or json.dumps(data)
            elif isinstance(data, str):
                text = data
            else:
                text = str(data)

            return ModelResponse(
                text=text,
                finish_reason="stop",
                usage={"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
                metadata={"provider": "opencode", "session_id": session_id},
            )
        except Exception as e:
            return ModelResponse(
                text=f"[OpenCode provider error: {e}]",
                finish_reason="error",
                metadata={"error": str(e)},
            )

    def stream(
        self,
        prompt: str,
        system: str = "",
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs: Any,
    ) -> Iterator[str]:
        result = self.generate(prompt, system, temperature, max_tokens, **kwargs)
        yield result.text

    def capabilities(self) -> dict[str, Any]:
        return {
            "provider": "opencode",
            "base_url": self.base_url,
            "streaming": False,
            "session_id": self.session_id,
        }

    def list_sessions(self) -> list[dict[str, Any]]:
        try:
            resp = self._client.get(
                f"{self.base_url}/session",
                auth=self._auth(),
            )
            resp.raise_for_status()
            return resp.json()
        except Exception:
            return []

    def _get_or_create_session(self) -> str:
        sessions = self.list_sessions()
        if sessions and isinstance(sessions, list):
            for s in sessions:
                if isinstance(s, dict) and "id" in s:
                    return s["id"]
        return "default"

    def close(self) -> None:
        self._client.close()
