"""Knowledge import from YAML files."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from agi_runtime.knowledge.store import KnowledgeEntry, KnowledgeStore


class KnowledgeImporter:
    """Imports knowledge from YAML files into the knowledge store."""

    def __init__(self, store: KnowledgeStore | None = None) -> None:
        self.store = store or KnowledgeStore()

    def import_yaml_file(self, file_path: str | Path) -> int:
        path = Path(file_path)
        if not path.exists():
            return 0

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except (yaml.YAMLError, Exception):
            return 0

        if isinstance(data, dict):
            entries = [data]
        elif isinstance(data, list):
            entries = data
        else:
            return 0

        count = 0
        for entry_data in entries:
            if isinstance(entry_data, dict) and self._validate_entry(entry_data):
                entry = self._dict_to_entry(entry_data)
                self.store.add(entry)
                count += 1

        return count

    def import_yaml_directory(self, dir_path: str | Path, pattern: str = "*.yaml") -> int:
        path = Path(dir_path)
        if not path.exists():
            return 0

        count = 0
        for file_path in sorted(path.rglob(pattern)):
            count += self.import_yaml_file(file_path)

        return count

    def import_knowledge_dir(self, base_path: str | Path = "knowledge") -> int:
        path = Path(base_path)
        if not path.exists():
            return 0

        count = 0
        for subdir in ["principles", "heuristics", "procedures", "concepts", "patterns", "anti_patterns"]:
            dir_path = path / subdir
            if dir_path.exists():
                count += self.import_yaml_directory(dir_path, "*.yaml")

        md_count = self._import_markdown_files(path)
        count += md_count

        return count

    def _import_markdown_files(self, base_path: Path) -> int:
        count = 0
        for subdir in ["principles", "heuristics", "procedures", "concepts", "patterns", "anti_patterns"]:
            dir_path = base_path / subdir
            if not dir_path.exists():
                continue
            for md_file in dir_path.glob("*.md"):
                entry = self._markdown_to_entry(md_file, subdir)
                if entry:
                    self.store.add(entry)
                    count += 1
        return count

    def _validate_entry(self, data: dict[str, Any]) -> bool:
        required = ["id", "type"]
        return all(k in data for k in required)

    def _dict_to_entry(self, data: dict[str, Any]) -> KnowledgeEntry:
        return KnowledgeEntry(
            id=data.get("id", ""),
            version=data.get("version", 1),
            type=data.get("type", "principle"),
            domain=data.get("domain", []),
            name=data.get("name", ""),
            description=data.get("description", ""),
            summary=data.get("summary", ""),
            heuristics=data.get("heuristics", []),
            triggers=data.get("triggers", []),
            procedure=data.get("procedure", []),
            anti_patterns=data.get("anti_patterns", []),
            verification_questions=data.get("verification_questions", []),
            examples=data.get("examples", []),
            source=data.get("source", ""),
            tags=data.get("tags", []),
        )

    def _markdown_to_entry(self, file_path: Path, entry_type: str) -> KnowledgeEntry | None:
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception:
            return None

        lines = content.strip().split("\n")
        if not lines:
            return None

        name = lines[0].lstrip("# ").strip()
        entry_id = f"{entry_type}.{file_path.stem}"

        description = ""
        summary = ""
        domain = []
        triggers = []
        procedure = []
        heuristics = []
        anti_patterns = []

        current_section = None
        for line in lines[1:]:
            line = line.strip()
            if not line:
                continue

            if line.startswith("## "):
                current_section = line[3:].lower()
                continue

            if current_section == "concept":
                if not description:
                    description = line
            elif current_section == "principle":
                if not summary:
                    summary = line
            elif current_section == "domain":
                if line.startswith("- "):
                    domain.append(line[2:])
            elif current_section == "triggers":
                if line.startswith("- "):
                    triggers.append(line[2:])
            elif current_section == "procedure":
                if line.startswith("- ") or line[0].isdigit():
                    procedure.append(line.lstrip("- ").lstrip("0123456789. "))
            elif current_section == "heuristics":
                if line.startswith("- "):
                    heuristics.append(line[2:])
            elif current_section == "anti-patterns":
                if line.startswith("- "):
                    anti_patterns.append(line[2:])

        return KnowledgeEntry(
            id=entry_id,
            type=entry_type.rstrip("s"),
            domain=domain,
            name=name,
            description=description,
            summary=summary,
            heuristics=heuristics,
            triggers=triggers,
            procedure=procedure,
            anti_patterns=anti_patterns,
            source=str(file_path),
        )
