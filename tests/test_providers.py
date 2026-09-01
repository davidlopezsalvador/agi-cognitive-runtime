"""Tests for provider interface."""

from agi_runtime.providers.base import (
    MemoryStore,
    ModelProvider,
    ModelResponse,
    KnowledgeStoreProvider,
    ToolDefinition,
    ToolProvider,
)


def test_model_response():
    resp = ModelResponse(text="Hello", finish_reason="stop", usage={"tokens": 10})
    assert resp.text == "Hello"
    assert resp.usage["tokens"] == 10


def test_tool_definition():
    tool = ToolDefinition(name="search", description="Search the web")
    assert tool.name == "search"


def test_model_provider_is_abstract():
    import inspect
    assert inspect.isabstract(ModelProvider)


def test_tool_provider_is_abstract():
    import inspect
    assert inspect.isabstract(ToolProvider)


def test_memory_store_is_abstract():
    import inspect
    assert inspect.isabstract(MemoryStore)


def test_knowledge_store_provider_is_abstract():
    import inspect
    assert inspect.isabstract(KnowledgeStoreProvider)
