from __future__ import annotations

import importlib.resources as resources

from agent_loom.team.errors import TeamError
from agent_loom.team.models import PrimeResult


def prime() -> PrimeResult:
    try:
        text = (
            resources.files("agent_loom.team")
            .joinpath("README.md")
            .read_text(encoding="utf-8")
        )
    except FileNotFoundError as exc:
        raise TeamError(
            "Team cookbook not found in package data",
            code="NOT_FOUND",
            exit_code=2,
            hint="Reinstall the package or verify README is bundled.",
        ) from exc

    return PrimeResult(markdown=text)


__all__ = ["prime"]
