from __future__ import annotations

import importlib.resources as resources

from agent_loom.workspace.errors import WorkspaceError
from agent_loom.workspace.models import PrimeResult


def prime() -> PrimeResult:
    try:
        text = (
            resources.files("agent_loom.workspace")
            .joinpath("README.md")
            .read_text(encoding="utf-8")
        )
    except FileNotFoundError as exc:
        raise WorkspaceError(
            "Workspace cookbook not found in package data",
        ) from exc

    return PrimeResult(payload={"ok": True, "markdown": text})
