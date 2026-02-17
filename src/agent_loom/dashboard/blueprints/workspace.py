from __future__ import annotations

from typing import Any

from flask import Blueprint, jsonify, request

from agent_loom.dashboard.blueprints.common import detect_ws_mode_root
from agent_loom.dashboard.config import ServerConfig
from agent_loom.dashboard.http import ok
from agent_loom.dashboard.workspace_read import (
    components_index,
    harness_worktrees,
    repo_worktrees,
    workspace_meta,
    worktree_diff,
)


def create_workspace_blueprint(cfg: ServerConfig, *, api_error: Any) -> Blueprint:
    bp = Blueprint("dashboard_workspace", __name__, url_prefix="/api/v1/workspace")

    @bp.get("/meta")
    def ws_meta() -> Any:
        q = request.args
        try:
            mode, root = detect_ws_mode_root(
                cfg,
                mode=str(q.get("mode") or cfg.workspace_mode),
                root_arg=str(
                    q.get("root") or (str(cfg.workspace_root) if cfg.workspace_root else "")
                ),
            )
            payload = workspace_meta(mode=mode, root=root)
        except Exception as e:
            payload, status = api_error(
                e,
                default_code="WS_ERROR",
                default_message="workspace metadata request failed",
            )
            return jsonify(payload), status
        return jsonify(ok(data=payload))

    @bp.get("/worktrees")
    def ws_worktrees() -> Any:
        q = request.args
        try:
            mode, root = detect_ws_mode_root(
                cfg,
                mode=str(q.get("mode") or cfg.workspace_mode),
                root_arg=str(
                    q.get("root") or (str(cfg.workspace_root) if cfg.workspace_root else "")
                ),
            )
            if mode == "repo":
                payload = repo_worktrees(
                    root=root,
                    q=str(q.get("q") or ""),
                    dirty_only=(str(q.get("dirty") or "0") == "1"),
                )
            else:
                payload = harness_worktrees(
                    root=root,
                    group=str(q.get("group") or ""),
                    repo=str(q.get("repo") or ""),
                    q=str(q.get("q") or ""),
                    dirty_only=(str(q.get("dirty") or "0") == "1"),
                    missing_only=(str(q.get("missing") or "0") == "1"),
                )
        except Exception as e:
            payload, status = api_error(
                e,
                default_code="WS_ERROR",
                default_message="workspace worktrees request failed",
            )
            return jsonify(payload), status
        return jsonify(ok(data=payload))

    @bp.get("/components/index")
    def ws_components_index() -> Any:
        q = request.args
        try:
            mode, root = detect_ws_mode_root(
                cfg,
                mode=str(q.get("mode") or cfg.workspace_mode),
                root_arg=str(
                    q.get("root") or (str(cfg.workspace_root) if cfg.workspace_root else "")
                ),
            )
            if mode != "harness":
                return jsonify(ok(data={"index": None}))
            idx = components_index(root=root)
            return jsonify(ok(data={"index": idx}))
        except Exception as e:
            payload, status = api_error(
                e,
                default_code="WS_ERROR",
                default_message="workspace components index request failed",
            )
            return jsonify(payload), status

    @bp.get("/services/index")
    def ws_services_index() -> Any:
        return ws_components_index()

    @bp.get("/worktree/diff")
    def ws_worktree_diff() -> Any:
        q = request.args
        try:
            mode, root = detect_ws_mode_root(
                cfg,
                mode=str(q.get("mode") or cfg.workspace_mode),
                root_arg=str(
                    q.get("root") or (str(cfg.workspace_root) if cfg.workspace_root else "")
                ),
            )
            payload = worktree_diff(
                mode=mode,
                root=root,
                path=str(q.get("path") or ""),
                diff_mode=str(q.get("diff_mode") or "cumulative"),
                base=str(q.get("base") or ""),
                max_patch_bytes=(
                    int(q.get("max_bytes") or 2_000_000)
                    if str(q.get("max_bytes") or "").strip()
                    else 2_000_000
                ),
            )
        except Exception as e:
            payload, status = api_error(
                e,
                default_code="WS_ERROR",
                default_message="workspace diff request failed",
            )
            return jsonify(payload), status
        return jsonify(ok(data=payload))

    return bp
