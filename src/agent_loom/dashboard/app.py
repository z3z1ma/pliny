from __future__ import annotations

import os
from uuid import uuid4
from typing import Any

from flask import Flask, jsonify, render_template

from agent_loom.core.errors import LoomError, coerce_loom_error
from agent_loom.dashboard.blueprints import (
    create_compound_blueprint,
    create_health_blueprint,
    create_memory_blueprint,
    create_team_blueprint,
    create_tickets_blueprint,
    create_workspace_blueprint,
)
from agent_loom.dashboard.config import ServerConfig
from agent_loom.dashboard.http import err
from agent_loom.dashboard.workspace_read import WorkspaceReadError

SERVER_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(SERVER_DIR, "templates")


def _register_error_handlers(app: Flask, *, api_error: Any) -> None:
    @app.errorhandler(404)
    def _not_found(_e: Exception) -> Any:
        return jsonify(err(code="NOT_FOUND", message="not found")), 404

    @app.errorhandler(405)
    def _method_not_allowed(_e: Exception) -> Any:
        return jsonify(err(code="METHOD_NOT_ALLOWED", message="method not allowed")), 405

    @app.errorhandler(Exception)
    def _unhandled(e: Exception) -> Any:
        payload, status = api_error(
            e, default_code="SERVER_ERROR", default_message="server error"
        )
        return jsonify(payload), status


def create_app(*, cfg: ServerConfig) -> Flask:
    app = Flask(__name__, template_folder=TEMPLATE_DIR)
    app.config["LOOM_SERVER_CFG"] = cfg

    def _api_error(
        exc: BaseException,
        *,
        default_code: str,
        default_message: str,
    ) -> tuple[dict[str, Any], int]:
        error_id = uuid4().hex
        default_http_status = 500
        if isinstance(exc, LoomError):
            default_http_status = int(exc.http_status)
        elif isinstance(exc, FileNotFoundError):
            default_http_status = 404
        elif isinstance(exc, PermissionError):
            default_http_status = 403
        elif isinstance(exc, (ValueError, WorkspaceReadError)) or hasattr(exc, "code"):
            default_http_status = 400
        expose_message = isinstance(exc, LoomError) and default_http_status < 500
        typed = coerce_loom_error(
            exc,
            default_code=default_code,
            default_message=(
                default_message if default_http_status < 500 else "internal error"
            ),
            default_http_status=default_http_status,
            default_exit_code=2,
            expose_message=expose_message,
            error_id=error_id,
        )
        if typed.http_status >= 500:
            app.logger.exception("dashboard error id=%s", error_id, exc_info=exc)
        details: dict[str, Any] = dict(typed.details)
        if typed.hint:
            details["hint"] = typed.hint
        if typed.suggestions:
            details["suggestions"] = list(typed.suggestions)
        return err(code=typed.code, message=str(typed), details=details), int(
            typed.http_status
        )

    @app.route("/")
    def dashboard() -> Any:
        return render_template("dashboard.html")

    app.register_blueprint(create_health_blueprint(cfg))
    app.register_blueprint(create_tickets_blueprint(cfg, api_error=_api_error))
    app.register_blueprint(create_team_blueprint(cfg, api_error=_api_error))
    app.register_blueprint(create_memory_blueprint(cfg, api_error=_api_error))
    app.register_blueprint(create_workspace_blueprint(cfg, api_error=_api_error))
    app.register_blueprint(create_compound_blueprint(cfg, api_error=_api_error))
    _register_error_handlers(app, api_error=_api_error)

    return app
