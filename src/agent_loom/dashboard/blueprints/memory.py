from __future__ import annotations

from pathlib import Path
from typing import Any

from flask import Blueprint, jsonify, request

from agent_loom.dashboard.config import ServerConfig
from agent_loom.dashboard.http import err, ok


def create_memory_blueprint(cfg: ServerConfig, *, api_error: Any) -> Blueprint:
    bp = Blueprint("dashboard_memory", __name__, url_prefix="/api/v1/memory")

    @bp.get("/recall")
    def memory_recall() -> Any:
        from agent_loom.memory.core import recall

        q = request.args
        vault_raw = str(q.get("vault") or "").strip() or ".loom/memory"
        vault_path = Path(vault_raw).expanduser()
        if not vault_path.is_absolute():
            vault_path = (cfg.repo_root / vault_path).resolve()
        vault = str(vault_path)
        res = recall(
            vault=vault,
            query=str(q.get("q") or ""),
            limit=int(q.get("limit") or 8),
            tag=(q.getlist("tag") if hasattr(q, "getlist") else None),
            not_tag=(q.getlist("not_tag") if hasattr(q, "getlist") else None),
            scope=(q.getlist("scope") if hasattr(q, "getlist") else None),
            not_scope=(q.getlist("not_scope") if hasattr(q, "getlist") else None),
            visibility=(q.getlist("visibility") if hasattr(q, "getlist") else None),
            include_deprecated=(str(q.get("include_deprecated") or "0") == "1"),
            expand=int(q.get("expand") or 0),
            context=(str(q.get("context") or "0") == "1"),
            deterministic=(str(q.get("deterministic") or "0") == "1"),
            format=str(q.get("format") or "json"),
            quiet=True,
        )
        return jsonify(ok(data=res))

    @bp.get("/notes/<note_id>")
    def memory_note(note_id: str) -> Any:
        from agent_loom.memory.vault import (
            find_note_path,
            resolve_vault_root,
            try_read_note_from_path,
            vault_paths,
        )

        vault_raw = str(request.args.get("vault") or "").strip() or ".loom/memory"
        vault_path = Path(vault_raw).expanduser()
        if not vault_path.is_absolute():
            vault_path = (cfg.repo_root / vault_path).resolve()
        vp_root = resolve_vault_root(str(vault_path), cwd=cfg.repo_root)
        vp = vault_paths(vp_root)
        try:
            p = find_note_path(vp, str(note_id))
        except Exception as e:
            payload, status = api_error(
                e,
                default_code="NOT_FOUND",
                default_message="memory note not found",
            )
            return jsonify(payload), status
        note, warns = try_read_note_from_path(
            p, default_visibility="shared", repo_root=cfg.repo_root
        )
        if note is None:
            return jsonify(err(code="READ_FAILED", message="failed to read note")), 400
        return jsonify(ok(data={"note": note, "warnings": warns}))

    return bp
