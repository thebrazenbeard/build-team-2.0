from __future__ import annotations

import json
import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .canonical import canonical_json_bytes, sha256_hex
from ._store_types import ConflictError, ValidationError


@dataclass(slots=True)
class StagedFileOperation:
    root: Path
    operation_id: str
    stage_dir: Path
    journal_path: Path
    staged: dict[str, Path]
    new_targets: list[Path]

    def promote(self) -> None:
        self.new_targets = []
        for digest, staged_path in sorted(self.staged.items()):
            target = self.root / "sources" / digest
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.exists():
                if sha256_hex(target.read_bytes()) != digest:
                    raise ConflictError(f"Divergent source bytes for digest {digest}")
                staged_path.unlink(missing_ok=True)
                continue
            self.new_targets.append(target)
        self._write_journal()
        for target in self.new_targets:
            staged_path = self.staged[target.name]
            os.replace(staged_path, target)

    def _write_journal(self) -> None:
        payload = {
            "schema": "LANTERN_FILE_OPERATION_V1",
            "operation_id": self.operation_id,
            "stage_dir": str(self.stage_dir.relative_to(self.root)),
            "new_targets": [str(path.relative_to(self.root)) for path in self.new_targets],
        }
        self.journal_path.parent.mkdir(parents=True, exist_ok=True)
        self.journal_path.write_bytes(canonical_json_bytes(payload) + b"\n")

    def cleanup_after_success(self) -> None:
        shutil.rmtree(self.stage_dir, ignore_errors=True)
        self.journal_path.unlink(missing_ok=True)

    def rollback_files(self) -> None:
        for target in self.new_targets:
            target.unlink(missing_ok=True)
        shutil.rmtree(self.stage_dir, ignore_errors=True)
        self.journal_path.unlink(missing_ok=True)


def stage_source_blobs(root: Path, operation_id: str, blobs: dict[str, bytes]) -> StagedFileOperation:
    safe = sha256_hex(operation_id)[:32]
    stage_dir = root / ".lantern-staging" / safe
    journal_path = root / ".lantern-operations" / f"{safe}.json"
    if stage_dir.exists():
        shutil.rmtree(stage_dir)
    stage_dir.mkdir(parents=True, exist_ok=True)
    staged: dict[str, Path] = {}
    for digest, content in sorted(blobs.items()):
        if sha256_hex(content) != digest:
            raise ValidationError(f"Source blob digest mismatch: {digest}")
        path = stage_dir / digest
        path.write_bytes(content)
        staged[digest] = path
    return StagedFileOperation(root, operation_id, stage_dir, journal_path, staged, [])


def recover_file_operations(root: Path, connection) -> None:
    journal_dir = root / ".lantern-operations"
    if not journal_dir.exists():
        return
    for journal_path in sorted(journal_dir.glob("*.json")):
        try:
            payload = json.loads(journal_path.read_text(encoding="utf-8"))
            operation_id = payload["operation_id"]
            row = connection.execute(
                "select status from file_operations where operation_id=?", (operation_id,)
            ).fetchone()
            committed = row is not None and row["status"] == "COMMITTED"
            if not committed:
                for relative in payload.get("new_targets", []):
                    (root / relative).unlink(missing_ok=True)
            stage_dir = root / payload.get("stage_dir", "")
            if stage_dir != root:
                shutil.rmtree(stage_dir, ignore_errors=True)
            journal_path.unlink(missing_ok=True)
        except Exception:
            # Fail closed: leave an unreadable journal for operator inspection.
            continue
