from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from uuid import uuid4

from starlette.requests import Request
from starlette.responses import JSONResponse

from loom_mill.shaping import CanvasNode, CanvasNodeType, NodeStatus, ShapingSession, list_sessions
from loom_mill.shaping.commit import CommitFlow
from loom_mill.shaping.engine import ShapingEngine
from loom_mill.shaping.events import ShapingEvent
from loom_mill.shaping.orchestrator import ShapingOrchestrator
from loom_mill.shaping.session import mark_active_recursive, mark_dead_recursive, mark_stale_recursive, utc_now
from loom_mill.workstation.config import HarnessConfig


def _workspace_root(request: Request) -> Path:
    return Path(request.app.state.workspace_root)


async def _json_body(request: Request) -> dict:
    try:
        body = await request.json()
    except json.JSONDecodeError as error:
        raise ValueError("invalid JSON") from error
    if not isinstance(body, dict):
        raise ValueError("JSON body must be an object")
    return body


def _state_payload(session: ShapingSession) -> dict:
    return asdict(session.state)


def _seed_text(state) -> str:
    inputs = [node for node in state.nodes.values() if node.type == CanvasNodeType.INPUT]
    inputs.sort(key=lambda node: node.timestamp)
    if not inputs:
        return ""
    return str(inputs[0].content.get("text") or "")


def _load_session(request: Request) -> ShapingSession:
    return ShapingSession.load(request.path_params["session_id"], _workspace_root(request))


def _harness_config(request: Request) -> HarnessConfig:
    manager = getattr(request.app.state, "workstation_manager", None)
    if manager is not None:
        return manager.config.harness
    return getattr(request.app.state, "harness_config", HarnessConfig(command="echo"))


def _orchestrators(request: Request) -> dict[str, ShapingOrchestrator]:
    if not hasattr(request.app.state, "shaping_orchestrators"):
        request.app.state.shaping_orchestrators = {}
    return request.app.state.shaping_orchestrators


def _orchestrator(request: Request, session: ShapingSession) -> ShapingOrchestrator:
    orchestrators = _orchestrators(request)
    orchestrator = orchestrators.get(session.session_id)
    if orchestrator is None:
        orchestrator = ShapingOrchestrator(
            session,
            request.app.state.store,
            _harness_config(request),
            timeout_seconds=float(getattr(request.app.state, "shaping_timeout_seconds", 120.0)),
        )
        orchestrators[session.session_id] = orchestrator
    else:
        orchestrator.session = session
    return orchestrator


def _session_locks(request: Request) -> dict[str, object]:
    if not hasattr(request.app.state, "shaping_session_locks"):
        request.app.state.shaping_session_locks = {}
    return request.app.state.shaping_session_locks


def _session_lock(request: Request, session_id: str):
    import asyncio

    locks = _session_locks(request)
    lock = locks.get(session_id)
    if lock is None:
        lock = asyncio.Lock()
        locks[session_id] = lock
    return lock


def _unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


async def create_shaping_session(request: Request) -> JSONResponse:
    try:
        body = await _json_body(request)
        initial_input = body["input"]
        if not isinstance(initial_input, str) or not initial_input.strip():
            raise ValueError("input must be a non-empty string")
    except (KeyError, ValueError) as error:
        return JSONResponse({"error": str(error)}, status_code=400)

    session = ShapingSession.create(_workspace_root(request), initial_input)
    root_node = next(iter(session.state.nodes.values()))
    await request.app.state.store.publish(
        ShapingEvent(session_id=session.session_id, event="node_added", data={"node": asdict(root_node)})
    )
    for edge in session.state.edges:
        if edge.target_id == root_node.id:
            await request.app.state.store.publish(
                ShapingEvent(session_id=session.session_id, event="edge_added", data={"edge": asdict(edge)})
            )
    return JSONResponse({"session_id": session.session_id, "state": _state_payload(session)})


async def list_shaping_sessions(request: Request) -> JSONResponse:
    payload = [
        {
            "id": state.id,
            "phase": state.phase,
            "created_at": state.created_at,
            "seed_text": _seed_text(state),
            "node_count": len(state.nodes),
            "staged_count": len(state.staged_records),
            "status": "committed" if state.ended_at is not None else "active",
        }
        for state in list_sessions(_workspace_root(request))
    ]
    payload.sort(key=lambda item: item["created_at"], reverse=True)
    return JSONResponse(payload)


async def get_shaping_session(request: Request) -> JSONResponse:
    try:
        session = _load_session(request)
    except KeyError:
        return JSONResponse({"detail": "Session not found"}, status_code=404)
    return JSONResponse(_state_payload(session))


async def get_shaping_context(request: Request) -> JSONResponse:
    try:
        session = _load_session(request)
    except KeyError:
        return JSONResponse({"detail": "Session not found"}, status_code=404)
    content = session.read_context()
    return JSONResponse({"content": content, "byte_length": len(content.encode("utf-8"))})


async def add_shaping_input(request: Request) -> JSONResponse:
    try:
        session = _load_session(request)
    except KeyError:
        return JSONResponse({"detail": "Session not found"}, status_code=404)
    if session.state.ended_at is not None:
        return JSONResponse({"error": "Session has ended"}, status_code=409)

    try:
        body = await _json_body(request)
        text = body["text"]
        if not isinstance(text, str) or not text.strip():
            raise ValueError("text must be a non-empty string")
        parent_node_id = body.get("parent_node_id")
        if parent_node_id is not None:
            parent_node_id = str(parent_node_id)
            if parent_node_id not in session.state.nodes:
                raise ValueError("parent_node_id must reference an existing node")
        source_option = body.get("source_option")
        if source_option is not None:
            if not isinstance(source_option, str) or not source_option.strip():
                raise ValueError("source_option must be a non-empty string")
            source_option = source_option.strip()
    except (KeyError, ValueError) as error:
        return JSONResponse({"error": str(error)}, status_code=400)

    content = {"text": text}
    if source_option is not None:
        content["source_option"] = source_option

    node = CanvasNode(
        id=str(uuid4()),
        type=CanvasNodeType.INPUT,
        parent_id=parent_node_id,
        status=NodeStatus.ACTIVE,
        content=content,
        position=None,
        timestamp=utc_now(),
    )
    await session.append_context("Operator Input", text)
    edge = session.add_node_with_edge(node)
    await request.app.state.store.publish(
        ShapingEvent(session_id=session.session_id, event="node_added", data={"node": asdict(node)})
    )
    if edge is not None:
        await request.app.state.store.publish(
            ShapingEvent(session_id=session.session_id, event="edge_added", data={"edge": asdict(edge)})
        )
    return JSONResponse({"session_id": session.session_id, "node": asdict(node), "edge": asdict(edge) if edge else None})


async def select_option_node(request: Request) -> JSONResponse:
    try:
        session = _load_session(request)
    except KeyError:
        return JSONResponse({"detail": "Session not found"}, status_code=404)
    if session.state.ended_at is not None:
        return JSONResponse({"error": "Session has ended"}, status_code=409)

    node_id = request.path_params["node_id"]
    node = session.state.nodes.get(node_id)
    if node is None:
        return JSONResponse({"error": "Node not found"}, status_code=404)
    if node.type != CanvasNodeType.OPTION:
        return JSONResponse({"error": "Node must be an option"}, status_code=400)
    if node.status == NodeStatus.DEAD:
        return JSONResponse({"error": "Cannot select a dead option"}, status_code=409)

    changed: list[str] = []
    if not node.selected or node.status != NodeStatus.ACTIVE:
        node.status = NodeStatus.ACTIVE
        node.selected = True
        changed.append(node.id)

    siblings = [
        candidate
        for candidate in session.state.nodes.values()
        if candidate.type == CanvasNodeType.OPTION
        and candidate.id != node.id
        and candidate.option_group_id is not None
        and candidate.option_group_id == node.option_group_id
    ]
    for sibling in siblings:
        changed.extend(mark_dead_recursive(session.state, sibling.id))

    if changed:
        session.state.updated_at = utc_now()
        session._persist_state()
        for changed_node_id in changed:
            await request.app.state.store.publish(
                ShapingEvent(
                    session_id=session.session_id,
                    event="node_updated",
                    data={"node": asdict(session.state.nodes[changed_node_id])},
                )
            )

    return JSONResponse({"session_id": session.session_id, "state": _state_payload(session), "changed_node_ids": changed})


async def edit_node(request: Request) -> JSONResponse:
    session_id = request.path_params["session_id"]
    async with _session_lock(request, session_id):
        try:
            session = _load_session(request)
        except KeyError:
            return JSONResponse({"detail": "Session not found"}, status_code=404)
        if session.state.ended_at is not None:
            return JSONResponse({"error": "Session has ended"}, status_code=409)

        node_id = request.path_params["node_id"]
        try:
            body = await _json_body(request)
            new_content = body["content"]
            if not isinstance(new_content, str):
                raise ValueError("content must be a string")
        except (KeyError, ValueError) as error:
            return JSONResponse({"error": str(error)}, status_code=400)

        node = session.state.nodes.get(node_id)
        if node is None:
            return JSONResponse({"error": "Node not found"}, status_code=404)
        if node.type != CanvasNodeType.INPUT:
            return JSONResponse({"error": "Only input nodes are editable"}, status_code=400)

        node.content["text"] = new_content
        stale_ids = mark_stale_recursive(session.state, node_id)
        session.state.updated_at = utc_now()
        session._persist_state()

        store = request.app.state.store
        await store.publish(
            ShapingEvent(
                session_id=session.session_id,
                event="node_updated",
                data={"node": asdict(node), "node_id": node_id, "changes": {"content": node.content}},
            )
        )
        if stale_ids:
            await store.publish(
                ShapingEvent(session_id=session.session_id, event="node_invalidated", data={"node_ids": stale_ids})
            )

        engine = ShapingEngine(session, _orchestrator(request, session), store)
        await engine.regenerate(node_id, max_depth=3)
        return JSONResponse({"edited": node_id, "stale_ids": stale_ids})


async def reselect_option_node(request: Request) -> JSONResponse:
    session_id = request.path_params["session_id"]
    async with _session_lock(request, session_id):
        try:
            session = _load_session(request)
        except KeyError:
            return JSONResponse({"detail": "Session not found"}, status_code=404)
        if session.state.ended_at is not None:
            return JSONResponse({"error": "Session has ended"}, status_code=409)

        node_id = request.path_params["node_id"]
        node = session.state.nodes.get(node_id)
        if node is None:
            return JSONResponse({"error": "Node not found"}, status_code=404)
        if node.type != CanvasNodeType.OPTION:
            return JSONResponse({"error": "Node must be an option"}, status_code=400)

        siblings = [
            candidate
            for candidate in session.state.nodes.values()
            if candidate.type == CanvasNodeType.OPTION
            and candidate.id != node.id
            and candidate.option_group_id is not None
            and candidate.option_group_id == node.option_group_id
        ]
        changed: list[str] = []
        for sibling in siblings:
            if sibling.selected and sibling.status == NodeStatus.ACTIVE:
                changed.extend(mark_dead_recursive(session.state, sibling.id))

        node.status = NodeStatus.ACTIVE
        node.selected = True
        changed.append(node.id)
        child_ids = [child.id for child in session.state.nodes.values() if child.parent_id == node.id]
        for child_id in child_ids:
            changed.extend(mark_active_recursive(session.state, child_id))
        changed = _unique(changed)

        session.state.updated_at = utc_now()
        session._persist_state()
        store = request.app.state.store
        for changed_node_id in changed:
            await store.publish(
                ShapingEvent(
                    session_id=session.session_id,
                    event="node_updated",
                    data={"node": asdict(session.state.nodes[changed_node_id])},
                )
            )

        if not child_ids:
            engine = ShapingEngine(session, _orchestrator(request, session), store)
            await engine.regenerate(node_id, max_depth=3)

        return JSONResponse({"session_id": session.session_id, "state": _state_payload(session), "changed_node_ids": changed})


async def explore_shaping_session(request: Request) -> JSONResponse:
    try:
        session = _load_session(request)
    except KeyError:
        return JSONResponse({"detail": "Session not found"}, status_code=404)
    if session.state.ended_at is not None:
        return JSONResponse({"error": "Session has ended"}, status_code=409)

    try:
        body = await _json_body(request)
        goal = body["goal"]
        if not isinstance(goal, str) or not goal.strip():
            raise ValueError("goal must be a non-empty string")
    except (KeyError, ValueError) as error:
        return JSONResponse({"error": str(error)}, status_code=400)

    invocation_id = await _orchestrator(request, session).launch(goal.strip())
    return JSONResponse({"session_id": session.session_id, "invocation_id": invocation_id, "goal": goal.strip()})


async def advance_shaping_session(request: Request) -> JSONResponse:
    session_id = request.path_params["session_id"]
    async with _session_lock(request, session_id):
        try:
            session = _load_session(request)
        except KeyError:
            return JSONResponse({"detail": "Session not found"}, status_code=404)
        if session.state.ended_at is not None:
            return JSONResponse({"error": "Session has ended"}, status_code=409)

        await request.app.state.store.publish(ShapingEvent(session_id=session.session_id, event="advance_started", data={}))
        engine = ShapingEngine(session, _orchestrator(request, session), request.app.state.store)
        try:
            nodes = await engine.advance()
            await request.app.state.store.publish(ShapingEvent(session_id=session.session_id, event="advance_completed", data={"node_count": len(nodes)}))
        except Exception as error:
            await request.app.state.store.publish(ShapingEvent(session_id=session.session_id, event="advance_error", data={"error": str(error)}))
            node = CanvasNode(
                id=str(uuid4()),
                type=CanvasNodeType.OBSERVATION,
                parent_id=None,
                status=NodeStatus.ACTIVE,
                content={"message": f"Shaping advance failed: {error}"},
                position=None,
                timestamp=utc_now(),
            )
            session.add_node(node)
            await request.app.state.store.publish(ShapingEvent(session_id=session.session_id, event="node_added", data={"node": asdict(node)}))
            nodes = [node]
        return JSONResponse({"session_id": session.session_id, "nodes": [asdict(node) for node in nodes]})


async def create_staged_record(request: Request) -> JSONResponse:
    try:
        session = _load_session(request)
    except KeyError:
        return JSONResponse({"detail": "Session not found"}, status_code=404)
    if session.state.ended_at is not None:
        return JSONResponse({"error": "Session has ended"}, status_code=409)
    try:
        body = await _json_body(request)
        surface = body["surface"]
        title = body["title"]
        content = body["content"]
        if not isinstance(surface, str) or not surface.strip():
            raise ValueError("surface must be a non-empty string")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("title must be a non-empty string")
        if not isinstance(content, str):
            raise ValueError("content must be a string")
        record = session.staging.propose(surface.strip(), title.strip(), content, session.state.active_branch)
    except (KeyError, ValueError) as error:
        return JSONResponse({"error": str(error)}, status_code=400)
    return JSONResponse({"session_id": session.session_id, "record": asdict(record)})


async def update_staged_record(request: Request) -> JSONResponse:
    try:
        session = _load_session(request)
    except KeyError:
        return JSONResponse({"detail": "Session not found"}, status_code=404)
    if session.state.ended_at is not None:
        return JSONResponse({"error": "Session has ended"}, status_code=409)
    try:
        body = await _json_body(request)
        content = body.get("content")
        title = body.get("title")
        if content is not None and not isinstance(content, str):
            raise ValueError("content must be a string")
        if title is not None and (not isinstance(title, str) or not title.strip()):
            raise ValueError("title must be a non-empty string")
        record = session.staging.update(request.path_params["temp_id"], content=content, title=title.strip() if title else None)
    except ValueError as error:
        return JSONResponse({"error": str(error)}, status_code=400)
    return JSONResponse({"session_id": session.session_id, "record": asdict(record)})


async def delete_staged_record(request: Request) -> JSONResponse:
    try:
        session = _load_session(request)
    except KeyError:
        return JSONResponse({"detail": "Session not found"}, status_code=404)
    if session.state.ended_at is not None:
        return JSONResponse({"error": "Session has ended"}, status_code=409)
    try:
        temp_id = request.path_params["temp_id"]
        session.staging.reject(temp_id)
        rejected_nodes = _mark_record_nodes_rejected(session, temp_id)
    except ValueError as error:
        return JSONResponse({"error": str(error)}, status_code=400)
    for node in rejected_nodes:
        await request.app.state.store.publish(
            ShapingEvent(session_id=session.session_id, event="node_updated", data={"node": asdict(node)})
        )
    return JSONResponse({"session_id": session.session_id, "rejected": temp_id})


def _mark_record_nodes_rejected(session: ShapingSession, temp_id: str) -> list[CanvasNode]:
    rejected: list[CanvasNode] = []
    for node in session.state.nodes.values():
        if node.type == CanvasNodeType.RECORD and node.content.get("temp_id") == temp_id and node.status != NodeStatus.REJECTED:
            node.status = NodeStatus.REJECTED
            rejected.append(node)
    if rejected:
        session.state.updated_at = utc_now()
        session._persist_state()
    return rejected


async def consolidate_staged_records(request: Request) -> JSONResponse:
    try:
        session = _load_session(request)
    except KeyError:
        return JSONResponse({"detail": "Session not found"}, status_code=404)
    if session.state.ended_at is not None:
        return JSONResponse({"error": "Session has ended"}, status_code=409)
    try:
        body = await _json_body(request)
        targets = body["targets"]
        surface = body["surface"]
        title = body["title"]
        content = body["content"]
        if not isinstance(targets, list) or len(targets) < 2:
            raise ValueError("targets must be a list with at least 2 items")
        if not isinstance(surface, str) or not surface.strip():
            raise ValueError("surface must be a non-empty string")
        if not isinstance(title, str) or not title.strip():
            raise ValueError("title must be a non-empty string")
        if not isinstance(content, str):
            raise ValueError("content must be a string")
        session.staging.consolidate([str(t) for t in targets], surface.strip(), title.strip(), content)
    except (KeyError, ValueError) as error:
        return JSONResponse({"error": str(error)}, status_code=400)
    return JSONResponse({"session_id": session.session_id, "staged_records": [asdict(r) for r in session.state.staged_records]})


async def accept_staged_record(request: Request) -> JSONResponse:
    try:
        session = _load_session(request)
    except KeyError:
        return JSONResponse({"detail": "Session not found"}, status_code=404)
    if session.state.ended_at is not None:
        return JSONResponse({"error": "Session has ended"}, status_code=409)
    try:
        record = session.staging.accept(request.path_params["temp_id"])
    except ValueError as error:
        return JSONResponse({"error": str(error)}, status_code=400)
    return JSONResponse({"session_id": session.session_id, "record": asdict(record)})


async def create_shaping_branch(request: Request) -> JSONResponse:
    try:
        session = _load_session(request)
    except KeyError:
        return JSONResponse({"detail": "Session not found"}, status_code=404)
    if session.state.ended_at is not None:
        return JSONResponse({"error": "Session has ended"}, status_code=409)
    try:
        body = await _json_body(request)
        branch_id = body["branch_id"]
        label = body.get("label", branch_id)
        if not isinstance(branch_id, str) or not branch_id.strip():
            raise ValueError("branch_id must be a non-empty string")
        if not isinstance(label, str) or not label.strip():
            raise ValueError("label must be a non-empty string")
        session.staging.create_branch(branch_id.strip(), label.strip())
    except (KeyError, ValueError) as error:
        return JSONResponse({"error": str(error)}, status_code=400)
    return JSONResponse({"session_id": session.session_id, "active_branch": session.state.active_branch, "branches": session.state.branches})


async def switch_shaping_branch(request: Request) -> JSONResponse:
    try:
        session = _load_session(request)
    except KeyError:
        return JSONResponse({"detail": "Session not found"}, status_code=404)
    if session.state.ended_at is not None:
        return JSONResponse({"error": "Session has ended"}, status_code=409)
    try:
        session.staging.switch_branch(request.path_params["branch_id"])
    except ValueError as error:
        return JSONResponse({"error": str(error)}, status_code=400)
    return JSONResponse({"session_id": session.session_id, "active_branch": session.state.active_branch, "branches": session.state.branches})


async def merge_shaping_branch(request: Request) -> JSONResponse:
    try:
        session = _load_session(request)
    except KeyError:
        return JSONResponse({"detail": "Session not found"}, status_code=404)
    if session.state.ended_at is not None:
        return JSONResponse({"error": "Session has ended"}, status_code=409)
    try:
        body = await _json_body(request)
        target = body.get("target", "main")
        if not isinstance(target, str) or not target.strip():
            raise ValueError("target must be a non-empty string")
        session.staging.merge_branch(request.path_params["source"], target.strip())
    except ValueError as error:
        return JSONResponse({"error": str(error)}, status_code=400)
    return JSONResponse({"session_id": session.session_id, "active_branch": session.state.active_branch, "branches": session.state.branches})


async def commit_shaping_session(request: Request) -> JSONResponse:
    try:
        session = _load_session(request)
    except KeyError:
        return JSONResponse({"detail": "Session not found"}, status_code=404)
    if session.state.ended_at is not None:
        return JSONResponse({"error": "Session has ended"}, status_code=409)
    try:
        result = await CommitFlow(session, _workspace_root(request), request.app.state.store).commit()
    except ValueError as error:
        return JSONResponse({"error": str(error)}, status_code=400)
    except RuntimeError as error:
        return JSONResponse({"error": str(error)}, status_code=500)
    return JSONResponse(asdict(result))


async def cancel_shaping_exploration(request: Request) -> JSONResponse:
    try:
        session = _load_session(request)
    except KeyError:
        return JSONResponse({"detail": "Session not found"}, status_code=404)

    invocation_id = request.path_params["invocation_id"]
    cancelled = await _orchestrator(request, session).cancel(invocation_id)
    return JSONResponse({"session_id": session.session_id, "invocation_id": invocation_id, "cancelled": cancelled})


async def list_shaping_explorations(request: Request) -> JSONResponse:
    try:
        session = _load_session(request)
    except KeyError:
        return JSONResponse({"detail": "Session not found"}, status_code=404)

    return JSONResponse(_orchestrator(request, session).list_explorations())


async def delete_shaping_session(request: Request) -> JSONResponse:
    try:
        session = _load_session(request)
    except KeyError:
        return JSONResponse({"detail": "Session not found"}, status_code=404)
    session.end()
    await request.app.state.store.publish(
        ShapingEvent(session_id=session.session_id, event="session_ended", data={"reason": "cancelled"})
    )
    _orchestrators(request).pop(session.session_id, None)
    return JSONResponse({"session_id": session.session_id, "ended_at": session.state.ended_at})
