from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any

from flask import Request

from agent_loom.dashboard.auth import authorize_request
from agent_loom.dashboard.config import ServerConfig
from agent_loom.dashboard.http import err
from agent_loom.dashboard.requests import require_token_default
from agent_loom.dashboard.workspace_read import detect_workspace_mode


def subsystem_versions() -> dict[str, str]:
    versions: dict[str, str] = {}
    for name in ["ticket", "team", "memory", "workspace", "compound"]:
        try:
            mod = importlib.import_module(f"agent_loom.{name}.constants")
            versions[name] = str(getattr(mod, "SUBSYSTEM_VERSION", ""))
        except Exception:
            versions[name] = ""
    return versions


def ensure_writes_enabled(cfg: ServerConfig) -> tuple[bool, dict[str, Any] | None]:
    if cfg.enable_writes:
        return True, None
    return False, err(code="WRITES_DISABLED", message="Writes are disabled")


def require_auth(
    cfg: ServerConfig, req: Request
) -> tuple[bool, dict[str, Any] | None]:
    need = require_token_default(str(req.host.split(":")[0]), cfg.require_token)
    res = authorize_request(req=req, token=cfg.token, require_token=need)
    if res.ok:
        return True, None
    return False, err(code="UNAUTHORIZED", message=res.reason)


def tickets_dir(cfg: ServerConfig) -> Path:
    return (cfg.repo_root / ".loom" / "ticket").resolve()


def detect_ws_mode_root(
    cfg: ServerConfig, *, mode: str, root_arg: str
) -> tuple[str, Path]:
    return detect_workspace_mode(cwd=cfg.repo_root, mode=mode, root_arg=root_arg)
