from __future__ import annotations

from typing import Any

from flask import Blueprint, jsonify

from agent_loom.dashboard.compound_fs import list_skills, read_instincts, read_skill
from agent_loom.dashboard.config import ServerConfig
from agent_loom.dashboard.http import ok


def create_compound_blueprint(cfg: ServerConfig, *, api_error: Any) -> Blueprint:
    bp = Blueprint("dashboard_compound", __name__, url_prefix="/api/v1/compound")

    @bp.get("/skills")
    def compound_skills() -> Any:
        return jsonify(ok(data={"skills": list_skills(cfg.repo_root)}))

    @bp.get("/skills/<name>")
    def compound_skill(name: str) -> Any:
        try:
            return jsonify(ok(data=read_skill(cfg.repo_root, name=str(name))))
        except Exception as e:
            payload, status = api_error(
                e,
                default_code="NOT_FOUND",
                default_message="skill not found",
            )
            return jsonify(payload), status

    @bp.get("/instincts")
    def compound_instincts() -> Any:
        return jsonify(ok(data=read_instincts(cfg.repo_root)))

    return bp
