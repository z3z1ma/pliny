from __future__ import annotations

import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

from loom_mill.api import shaping
from loom_mill.state import MillStateStore
from loom_mill.workstation.config import HarnessConfig


class Request:
    def __init__(
        self,
        workspace_root: Path,
        store: MillStateStore,
        body: dict | None = None,
        path_params: dict | None = None,
        harness_config: HarnessConfig | None = None,
    ):
        self.app = SimpleNamespace(
            state=SimpleNamespace(
                workspace_root=str(workspace_root),
                store=store,
                harness_config=harness_config or _printf_harness(),
            )
        )
        self._body = body or {}
        self.path_params = path_params or {}

    async def json(self):
        return self._body


def _body(response) -> dict:
    return json.loads(response.body)


def _printf_harness() -> HarnessConfig:
    return HarnessConfig(command="printf", args=['<node type="question">What is the scope?</node>\n'])


def _init_git(path: Path) -> None:
    subprocess.run(["git", "init"], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.email", "loom@example.com"], cwd=path, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Loom Test"], cwd=path, check=True, capture_output=True)


@pytest.mark.asyncio
async def test_full_shaping_session_lifecycle(tmp_path: Path) -> None:
    _init_git(tmp_path)
    store = MillStateStore()
    harness = _printf_harness()

    create = await shaping.create_shaping_session(Request(tmp_path, store, {"input": "Shape a small backend ticket"}, harness_config=harness))
    session_id = _body(create)["session_id"]

    first_advance = await shaping.advance_shaping_session(Request(tmp_path, store, path_params={"session_id": session_id}, harness_config=harness))
    first_nodes = _body(first_advance)["nodes"]
    assert first_nodes
    assert first_nodes[0]["type"] in {"question", "observation", "record"}

    input_response = await shaping.add_shaping_input(
        Request(tmp_path, store, {"text": "Keep scope to a single backend validation fix."}, {"session_id": session_id}, harness)
    )
    assert _body(input_response)["node"]["type"] == "input"

    second_advance = await shaping.advance_shaping_session(Request(tmp_path, store, path_params={"session_id": session_id}, harness_config=harness))
    assert _body(second_advance)["nodes"]

    staged = await shaping.create_staged_record(
        Request(
            tmp_path,
            store,
            {
                "surface": "tickets",
                "title": "Backend Validation Fix",
                "content": "# Backend Validation Fix\n\nID: temp:tickets:backend-validation-fix\nType: Ticket\nStatus: open\n",
            },
            {"session_id": session_id},
            harness,
        )
    )
    assert _body(staged)["record"]["temp_id"] == "temp:tickets:backend-validation-fix"

    commit = await shaping.commit_shaping_session(Request(tmp_path, store, path_params={"session_id": session_id}, harness_config=harness))
    commit_payload = _body(commit)

    assert commit.status_code == 200
    assert commit_payload["records_created"] == 1
    for relative_path in commit_payload["paths"]:
        assert (tmp_path / relative_path).exists()
    assert (tmp_path / ".loom" / "tickets" / "20260526-backend-validation-fix.md").exists()
