from __future__ import annotations

from .canonical import sha256_hex
from .contracts import build_record
from ._store_types import ConflictError, OperationResult, ValidationError


class SourceCommandsMixin:
    def observe_source(
        self,
        *,
        actor_id: str,
        source_key: str,
        locator: str,
        retrieval_route: str,
        media_type: str,
        custody_mode: str,
        retention_status: str,
        observed_at: str,
        content: bytes | None = None,
        predecessor_record_id: str | None = None,
        record_id: str | None = None,
        created_at: str | None = None,
    ) -> OperationResult:
        if custody_mode not in {"REFERENCE_ONLY", "CAPTURED", "EMBEDDED", "REDACTED", "UNAVAILABLE"}:
            raise ValidationError("Invalid custody mode")
        content_digest = sha256_hex(content) if content is not None else None
        if custody_mode in {"CAPTURED", "EMBEDDED"} and content is None:
            raise ValidationError(f"{custody_mode} custody requires retained bytes")
        if content is not None:
            self.sources_path.mkdir(exist_ok=True)
            blob_path = self.sources_path / content_digest
            if blob_path.exists() and blob_path.read_bytes() != content:
                raise ConflictError("Content-addressed source digest collision")
            blob_path.write_bytes(content)
        record = build_record(
            project_id=self.project_id,
            record_type="SourceSnapshot",
            actor_id=actor_id,
            record_id=record_id,
            created_at=created_at,
            observed_at=observed_at,
            provenance={"source_locator": locator, "retrieval_route": retrieval_route},
            lineage_key=source_key,
            predecessor_record_id=predecessor_record_id,
            payload={
                "source_key": source_key,
                "locator": locator,
                "retrieval_route": retrieval_route,
                "media_type": media_type,
                "custody_mode": custody_mode,
                "retention_status": retention_status,
                "content_sha256": content_digest,
            },
        )
        return self.insert_record(record)
