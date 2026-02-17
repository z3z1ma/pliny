from __future__ import annotations

from typing import Any

from flask import Blueprint, jsonify, request

from agent_loom.dashboard.blueprints.common import (
    ensure_writes_enabled,
    require_auth,
    tickets_dir,
)
from agent_loom.dashboard.config import ServerConfig
from agent_loom.dashboard.http import ok
from agent_loom.dashboard.requests import json_body, parse_int_field


def create_tickets_blueprint(cfg: ServerConfig, *, api_error: Any) -> Blueprint:
    bp = Blueprint("dashboard_tickets", __name__, url_prefix="/api/v1/tickets")

    @bp.get("")
    def tickets_list() -> Any:
        from agent_loom.ticket.api import list_tickets

        q = request.args
        res = list_tickets(
            tickets_dir=tickets_dir(cfg),
            status=str(q.get("status", "")),
            type_=str(q.get("type", "")),
            assignee=str(q.get("assignee", "")),
            tag=str(q.get("tag", "")),
            prio_min=int(q["prio_min"]) if q.get("prio_min") else None,
            prio_max=int(q["prio_max"]) if q.get("prio_max") else None,
            include_closed=(str(q.get("include_closed", "1")) != "0"),
            limit=int(q["limit"]) if q.get("limit") else 0,
        )
        return jsonify(ok(data=res))

    @bp.get("/<ticket_id>")
    def tickets_show(ticket_id: str) -> Any:
        from agent_loom.ticket.api import show

        res = show(ticket_id=str(ticket_id), tickets_dir=tickets_dir(cfg))
        return jsonify(ok(data=res))

    @bp.get("/<ticket_id>/view")
    def tickets_view(ticket_id: str) -> Any:
        from agent_loom.ticket.api import view

        res = view(ticket_id=str(ticket_id), tickets_dir=tickets_dir(cfg))
        return jsonify(ok(data=res))

    @bp.get("/<ticket_id>/dep")
    def tickets_dep(ticket_id: str) -> Any:
        from agent_loom.ticket.api import dep

        res = dep(ticket_id=str(ticket_id), tickets_dir=tickets_dir(cfg))
        return jsonify(ok(data=res))

    @bp.get("/swarm")
    def tickets_swarm() -> Any:
        from agent_loom.ticket.api import swarm

        q = request.args
        res = swarm(
            tickets_dir=tickets_dir(cfg),
            active_within=str(q.get("active_within") or "2h"),
        )
        return jsonify(ok(data=res))

    @bp.post("")
    def tickets_create() -> Any:
        allowed, payload = ensure_writes_enabled(cfg)
        if not allowed:
            return jsonify(payload), 403
        allowed, payload = require_auth(cfg, request)
        if not allowed:
            return jsonify(payload), 401

        from agent_loom.ticket.api import create

        try:
            body = json_body(request)
            priority = parse_int_field(body, field="priority", default=2)
            if priority is None:
                priority = 2
            res = create(
                tickets_dir=tickets_dir(cfg),
                title=str(body.get("title") or "").strip(),
                type=str(body.get("type") or "task").strip(),
                priority=priority,
                tags=str(body.get("tags") or ""),
                description=str(body.get("description") or ""),
                assignee=str(body.get("assignee") or "").strip(),
                external_ref=str(body.get("external_ref") or "").strip(),
                parent=str(body.get("parent") or "").strip(),
                design=str(body.get("design") or "").strip(),
                acceptance=str(body.get("acceptance") or "").strip(),
            )
        except Exception as e:
            payload, status = api_error(
                e,
                default_code="CREATE_FAILED",
                default_message="ticket create failed",
            )
            return jsonify(payload), status
        return jsonify(ok(data=res)), 201

    @bp.patch("/<ticket_id>")
    def tickets_update(ticket_id: str) -> Any:
        allowed, payload = ensure_writes_enabled(cfg)
        if not allowed:
            return jsonify(payload), 403
        allowed, payload = require_auth(cfg, request)
        if not allowed:
            return jsonify(payload), 401

        from agent_loom.ticket.api import update

        try:
            body = json_body(request)
            res = update(
                tickets_dir=tickets_dir(cfg),
                ticket_id=str(ticket_id),
                title=body.get("title"),
                status=str(body.get("status") or "").strip(),
                priority=(
                    parse_int_field(body, field="priority", default=None)
                    if "priority" in body
                    else None
                ),
                type_=str(body.get("type") or "").strip(),
                assignee=str(body.get("assignee") or "").strip(),
                tags=(str(body.get("tags")) if "tags" in body else None),
                external_ref=(
                    str(body.get("external_ref") or "")
                    if "external_ref" in body
                    else None
                ),
                parent=(str(body.get("parent") or "") if "parent" in body else None),
                deps=(
                    (
                        ",".join([str(x) for x in (body.get("deps") or [])])
                        if isinstance(body.get("deps"), list)
                        else str(body.get("deps") or "")
                    )
                    if "deps" in body
                    else None
                ),
                links=(
                    (
                        ",".join([str(x) for x in (body.get("links") or [])])
                        if isinstance(body.get("links"), list)
                        else str(body.get("links") or "")
                    )
                    if "links" in body
                    else None
                ),
                body_text=(str(body.get("body")) if "body" in body else None),
                force=bool(body.get("force")),
            )
        except Exception as e:
            payload, status = api_error(
                e,
                default_code="UPDATE_FAILED",
                default_message="ticket update failed",
            )
            return jsonify(payload), status
        return jsonify(ok(data=res))

    return bp
