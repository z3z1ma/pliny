from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ServerConfig:
    repo_root: Path
    workspace_mode: str  # auto|repo|poly
    workspace_root: Path | None
    enable_writes: bool
    token: str
    require_token: bool
