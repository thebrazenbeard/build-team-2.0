from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "training" / "ROLE_TRAINING_REGISTRY.json"
README = ROOT / "README.md"

SHA1_RE = re.compile(r"^[0-9a-f]{40}$")

REQUIRED = (
    "README.md",
    "STATUS.md",
    "docs/PROTOCOL_EXECUTION_PRECEDENCE_V2.md",
    "training/PROTOCOL_V2_REGRESSION_SUITE.md",
    "training/ROLE_TRAINING_REGISTRY.json",
    "training/FRESH_CHAT_STARTUP.md",
)

STALE_RUNTIME_TOKENS = (
    "uv sync --extra dev",
    "cp .env.example .env",
    'uv run build-team roster',
    'uv run build-team run',
)


def _exists(relative: str) -> bool:
    return (ROOT / relative).exists()


def _git_commit_exists(sha: str) -> bool:
    completed = subprocess.run(
        ["git", "cat-file", "-e", f"{sha}^{{commit}}"],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return completed.returncode == 0


def validate() -> list[str]:
    errors: list[str] = []

    for relative in REQUIRED:
        if not _exists(relative):
            errors.append(f"missing required repository file: {relative}")

    for path in ROOT.rglob("*.json"):
        if ".git" in path.parts:
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"invalid JSON: {path.relative_to(ROOT)}: {exc}")

    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    overlay = registry.get("current_governance_overlay", {})
    if overlay.get("authoritative_ref") != "main":
        errors.append("current governance overlay must bind authoritative_ref=main")

    for key in ("precedence_path", "regression_path"):
        relative = overlay.get(key)
        if not isinstance(relative, str) or not _exists(relative):
            errors.append(f"missing current governance overlay path: {key}={relative!r}")

    roles = registry.get("roles", {})
    if not isinstance(roles, dict) or not roles:
        errors.append("training registry has no roles")
    else:
        for role_key, role in roles.items():
            for field in (
                "package_path",
                "manifest_path",
                "bootstrap_path",
            ):
                relative = role.get(field)
                if not isinstance(relative, str) or not _exists(relative):
                    errors.append(f"{role_key}: missing {field}: {relative!r}")

            for field in (
                "fresh_chat_startup_path",
                "checkpoint_protocol_path",
                "checkpoint_schema_path",
                "checkpoint_tool_path",
            ):
                relative = role.get(field)
                if relative is not None and (
                    not isinstance(relative, str) or not _exists(relative)
                ):
                    errors.append(f"{role_key}: missing {field}: {relative!r}")

            commit = role.get("immutable_source_commit")
            if not isinstance(commit, str) or not SHA1_RE.fullmatch(commit):
                errors.append(f"{role_key}: invalid immutable_source_commit")
            elif not _git_commit_exists(commit):
                errors.append(f"{role_key}: immutable source commit not present: {commit}")

    precedence = overlay.get("precedence_path")
    regression = overlay.get("regression_path")
    for path in sorted((ROOT / "training").glob("*FRESH_CHAT_STARTUP.md")):
        text = path.read_text(encoding="utf-8")
        for relative in (precedence, regression):
            if isinstance(relative, str) and relative not in text:
                errors.append(
                    f"{path.relative_to(ROOT)} does not load governance overlay {relative}"
                )
        if "before operational work" not in text.lower():
            errors.append(
                f"{path.relative_to(ROOT)} lacks before-operational-work boundary"
            )

    readme = README.read_text(encoding="utf-8")
    for token in STALE_RUNTIME_TOKENS:
        if token in readme:
            errors.append(f"README still advertises absent runtime setup: {token}")

    if "thebrazenbeard/bt2" not in readme:
        errors.append("README does not identify canonical BT2 repository")

    return errors


if __name__ == "__main__":
    failures = validate()
    if failures:
        for failure in failures:
            print(f"ERROR: {failure}")
        raise SystemExit(1)
    print("Build Team 2.0 repository validation: PASS")
