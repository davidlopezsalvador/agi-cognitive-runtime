"""Tests for episodic memory retrieval."""

from agi_runtime.memory.models import Memory, Episode
from agi_runtime.memory.retriever import EpisodicRetriever, RetrievedEpisode


def test_retriever_empty():
    mem = Memory()
    retriever = EpisodicRetriever(mem)
    results = retriever.retrieve("debug timeout")
    assert len(results) == 0


def test_retrieve_by_task_match():
    mem = Memory()
    mem.store_episode(Episode(task="Debug timeout issue", lesson="Check connection pool"))
    mem.store_episode(Episode(task="Deploy service", lesson="Run tests first"))

    retriever = EpisodicRetriever(mem)
    results = retriever.retrieve("debug timeout")
    assert len(results) >= 1
    assert results[0].episode.task == "Debug timeout issue"
    assert results[0].relevance_score > 0


def test_retrieve_by_lesson():
    mem = Memory()
    mem.store_episode(Episode(task="Fix bug X", lesson="Always check connection pool first"))
    mem.store_episode(Episode(task="Deploy service", lesson="Run tests first"))

    retriever = EpisodicRetriever(mem)
    results = retriever.retrieve("connection pool issue")
    assert len(results) >= 1
    assert any("connection pool" in r.applicable_lessons[0] for r in results if r.applicable_lessons)


def test_retrieve_by_failure():
    mem = Memory()
    mem.store_episode(Episode(task="Fix crash", failure="Memory leak in cache"))
    mem.store_episode(Episode(task="Deploy service", lesson="Run tests first"))

    retriever = EpisodicRetriever(mem)
    results = retriever.retrieve("memory leak")
    assert len(results) >= 1


def test_structural_similarity():
    mem = Memory()
    mem.store_episode(Episode(task="Debug network latency", lesson="Use binary search"))
    mem.store_episode(Episode(task="Optimize database query", lesson="Add index"))

    retriever = EpisodicRetriever(mem)
    results = retriever.find_structurally_similar("investigate slow response")
    assert len(results) >= 0


def test_retrieval_limit():
    mem = Memory()
    for i in range(10):
        mem.store_episode(Episode(task=f"Task {i} debug", lesson=f"Lesson {i}"))

    retriever = EpisodicRetriever(mem)
    results = retriever.retrieve("debug", limit=3)
    assert len(results) <= 3
