"""Provider interface for the AGI Cognitive Runtime."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, Field


class ModelResponse(BaseModel):
    """Response from a model provider."""

    text: str = ""
    finish_reason: str = ""
    usage: dict[str, int] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ModelProvider(ABC):
    """Abstract interface for LLM providers."""

    @abstractmethod
    def generate(
        self,
        prompt: str,
        system: str = "",
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs: Any,
    ) -> ModelResponse:
        ...

    @abstractmethod
    def stream(
        self,
        prompt: str,
        system: str = "",
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs: Any,
    ):
        ...

    @abstractmethod
    def capabilities(self) -> dict[str, Any]:
        ...


class ToolDefinition(BaseModel):
    """Definition of a tool available to the agent."""

    name: str
    description: str = ""
    parameters: dict[str, Any] = Field(default_factory=dict)


class ToolProvider(ABC):
    """Abstract interface for tool providers."""

    @abstractmethod
    def list_tools(self) -> list[ToolDefinition]:
        ...

    @abstractmethod
    def execute(self, tool_name: str, arguments: dict[str, Any]) -> Any:
        ...


class MemoryStore(ABC):
    """Abstract interface for memory persistence."""

    @abstractmethod
    def remember(self, key: str, value: Any) -> None:
        ...

    @abstractmethod
    def retrieve(self, key: str) -> Any | None:
        ...

    @abstractmethod
    def consolidate(self) -> None:
        ...


class KnowledgeStoreProvider(ABC):
    """Abstract interface for knowledge persistence."""

    @abstractmethod
    def search(self, query: str, limit: int = 10) -> list[Any]:
        ...

    @abstractmethod
    def get(self, entry_id: str) -> Any | None:
        ...
