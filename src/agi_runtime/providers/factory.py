"""Environment-based provider factory."""

from __future__ import annotations

import os
from typing import Any

from agi_runtime.providers.base import ModelProvider


def create_provider(
    provider: str | None = None,
    model: str | None = None,
    base_url: str | None = None,
    api_key: str | None = None,
) -> ModelProvider | None:
    """Create a model provider from environment variables or explicit args.

    Environment variables:
        AGI_PROVIDER: "openai", "ollama", "lmstudio", "opencode", or "none"
        AGI_MODEL: model name
        AGI_BASE_URL: API base URL
        OPENAI_API_KEY: OpenAI API key
        OPENAI_BASE_URL: OpenAI-compatible base URL
        OPENCODE_SERVER_PASSWORD: OpenCode server password
    """
    provider_name = provider or os.environ.get("AGI_PROVIDER", "")
    model_name = model or os.environ.get("AGI_MODEL", "")
    url = base_url or os.environ.get("AGI_BASE_URL") or os.environ.get("OPENAI_BASE_URL", "")
    key = api_key or os.environ.get("OPENAI_API_KEY", "")

    if provider_name == "none":
        return None

    if provider_name == "opencode":
        from agi_runtime.providers.opencode_provider import OpenCodeProvider
        return OpenCodeProvider(
            base_url=url or None,
            password=os.environ.get("OPENCODE_SERVER_PASSWORD", ""),
        )

    if provider_name == "ollama" or (not provider_name and "ollama" in url.lower()):
        from agi_runtime.providers.openai_provider import OpenAIProvider
        return OpenAIProvider(
            api_key="ollama",
            base_url=url or "http://localhost:11434/v1",
            model=model_name or "llama3.1",
        )

    if provider_name == "lmstudio" or (not provider_name and "lmstudio" in url.lower()):
        from agi_runtime.providers.openai_provider import OpenAIProvider
        return OpenAIProvider(
            api_key="lmstudio",
            base_url=url or "http://localhost:1234/v1",
            model=model_name or "default",
        )

    if key or provider_name == "openai":
        from agi_runtime.providers.openai_provider import OpenAIProvider
        return OpenAIProvider(
            api_key=key,
            base_url=url or "https://api.openai.com/v1",
            model=model_name or "gpt-4o",
        )

    if url:
        from agi_runtime.providers.openai_provider import OpenAIProvider
        return OpenAIProvider(
            api_key=key or "no-key",
            base_url=url,
            model=model_name or "default",
        )

    return None
