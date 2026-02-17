from __future__ import annotations

import importlib
import platform
from typing import Any

from flask import Blueprint, jsonify

from agent_loom.dashboard.blueprints.common import subsystem_versions
from agent_loom.dashboard.capabilities import CAPABILITY_ENDPOINTS
from agent_loom.dashboard.config import ServerConfig
from agent_loom.dashboard.http import err, ok
from agent_loom.dashboard.introspect import introspect_module
from agent_loom.dashboard.requests import require_token_default


def create_health_blueprint(cfg: ServerConfig) -> Blueprint:
    bp = Blueprint("dashboard_health", __name__, url_prefix="/api/v1")

    @bp.get("/health")
    def health() -> Any:
        return jsonify(
            ok(
                data={
                    "platform": platform.platform(),
                    "python": platform.python_version(),
                    "repo_root": str(cfg.repo_root.resolve()),
                    "workspace_mode": cfg.workspace_mode,
                    "workspace_root": str(cfg.workspace_root.resolve())
                    if cfg.workspace_root is not None
                    else "",
                    "writes_enabled": bool(cfg.enable_writes),
                    "token_required": bool(
                        require_token_default("127.0.0.1", cfg.require_token)
                    ),
                },
                meta={
                    "subsystem_versions": subsystem_versions(),
                },
            )
        )

    @bp.get("/capabilities")
    def capabilities() -> Any:
        return jsonify(
            ok(
                data={
                    "writes": {"enabled": bool(cfg.enable_writes)},
                    "auth": {
                        "supported": ["bearer", "x-loom-token"],
                        "require_token": bool(cfg.require_token),
                    },
                    "endpoints": CAPABILITY_ENDPOINTS,
                },
                meta={"subsystem_versions": subsystem_versions()},
            )
        )

    @bp.get("/introspect/<subsystem>")
    def introspect(subsystem: str) -> Any:
        name = str(subsystem or "").strip().lower()
        mod_name = {
            "ticket": "agent_loom.ticket.core",
            "team": "agent_loom.team.core",
            "memory": "agent_loom.memory.core",
            "workspace": "agent_loom.workspace.core",
            "compound": "agent_loom.compound.sync",
        }.get(name)
        if not mod_name:
            return jsonify(err(code="ARG", message="Unknown subsystem")), 400
        mod = importlib.import_module(mod_name)
        payload = introspect_module(mod)
        return jsonify(ok(data=payload))

    return bp
