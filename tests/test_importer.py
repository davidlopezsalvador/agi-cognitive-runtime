"""Tests for knowledge importer."""

import tempfile
from pathlib import Path

from agi_runtime.knowledge.importer import KnowledgeImporter
from agi_runtime.knowledge.store import KnowledgeStore


def test_import_yaml_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        yaml_content = """
id: test.principle1
type: principle
name: Test Principle
description: A test principle
domain:
  - testing
triggers:
  - test_trigger
procedure:
  - Step 1
  - Step 2
"""
        yaml_path = Path(tmpdir) / "test.yaml"
        yaml_path.write_text(yaml_content)

        store = KnowledgeStore()
        importer = KnowledgeImporter(store)
        count = importer.import_yaml_file(yaml_path)

        assert count == 1
        assert len(store.entries) == 1
        assert store.entries[0].name == "Test Principle"


def test_import_yaml_list():
    with tempfile.TemporaryDirectory() as tmpdir:
        yaml_content = """
- id: test.p1
  type: principle
  name: Principle 1
- id: test.p2
  type: heuristic
  name: Heuristic 1
"""
        yaml_path = Path(tmpdir) / "list.yaml"
        yaml_path.write_text(yaml_content)

        store = KnowledgeStore()
        importer = KnowledgeImporter(store)
        count = importer.import_yaml_file(yaml_path)

        assert count == 2
        assert len(store.entries) == 2


def test_import_directory():
    with tempfile.TemporaryDirectory() as tmpdir:
        principles_dir = Path(tmpdir) / "principles"
        principles_dir.mkdir()

        for i in range(3):
            yaml_content = f"""
id: test.p{i}
type: principle
name: Principle {i}
description: Description {i}
"""
            (principles_dir / f"p{i}.yaml").write_text(yaml_content)

        store = KnowledgeStore()
        importer = KnowledgeImporter(store)
        count = importer.import_yaml_directory(principles_dir)

        assert count == 3
        assert len(store.entries) == 3


def test_import_invalid_yaml():
    with tempfile.TemporaryDirectory() as tmpdir:
        yaml_content = "not: valid: yaml: content"
        yaml_path = Path(tmpdir) / "invalid.yaml"
        yaml_path.write_text(yaml_content)

        store = KnowledgeStore()
        importer = KnowledgeImporter(store)
        count = importer.import_yaml_file(yaml_path)

        assert count == 0


def test_import_missing_file():
    store = KnowledgeStore()
    importer = KnowledgeImporter(store)
    count = importer.import_yaml_file("/nonexistent/file.yaml")
    assert count == 0


def test_import_markdown():
    with tempfile.TemporaryDirectory() as tmpdir:
        principles_dir = Path(tmpdir) / "principles"
        principles_dir.mkdir()

        md_content = """# Test Principle

## Concept
This is a test principle.

## Domain
- testing
- debugging

## Procedure
- Step one
- Step two

## Triggers
- test trigger
"""
        (principles_dir / "test_principle.md").write_text(md_content)

        store = KnowledgeStore()
        importer = KnowledgeImporter(store)
        count = importer.import_knowledge_dir(Path(tmpdir))

        assert count == 1
        assert store.entries[0].name == "Test Principle"
