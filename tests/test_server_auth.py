from __future__ import annotations

import subprocess
from pathlib import Path

from agent_loom.dashboard.app import create_app
from agent_loom.dashboard.config import ServerConfig


def _git_init(repo: Path) -> None:
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)


def test_write_gated_when_disabled(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir(parents=True, exist_ok=True)
    _git_init(repo)
    (repo / ".loom" / "ticket").mkdir(parents=True, exist_ok=True)

    app = create_app(
        cfg=ServerConfig(
            repo_root=repo,
            workspace_mode="repo",
            workspace_root=None,
            enable_writes=False,
            token="",
            require_token=False,
        )
    )
    client = app.test_client()

    res = client.post(
        "/api/v1/tickets",
        json={"title": "X", "type": "task", "priority": 2},
    )
    assert res.status_code == 403
    payload = res.get_json()
    assert payload["ok"] is False
    assert payload["error"]["code"] == "WRITES_DISABLED"


def test_write_requires_token_when_configured(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir(parents=True, exist_ok=True)
    _git_init(repo)
    (repo / ".loom" / "ticket").mkdir(parents=True, exist_ok=True)

    app = create_app(
        cfg=ServerConfig(
            repo_root=repo,
            workspace_mode="repo",
            workspace_root=None,
            enable_writes=True,
            token="secret",
            require_token=True,
        )
    )
    client = app.test_client()

    res = client.post(
        "/api/v1/tickets",
        json={"title": "X", "type": "task", "priority": 2},
    )
    assert res.status_code == 401

    res2 = client.post(
        "/api/v1/tickets",
        headers={"Authorization": "Bearer secret"},
        json={"title": "X", "type": "task", "priority": 2, "assignee": "tester"},
    )
    assert res2.status_code == 201
    payload2 = res2.get_json()
    assert payload2["ok"] is True


def test_write_rejects_non_integer_priority(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir(parents=True, exist_ok=True)
    _git_init(repo)
    (repo / ".loom" / "ticket").mkdir(parents=True, exist_ok=True)

    app = create_app(
        cfg=ServerConfig(
            repo_root=repo,
            workspace_mode="repo",
            workspace_root=None,
            enable_writes=True,
            token="",
            require_token=False,
        )
    )
    client = app.test_client()

    res = client.post(
        "/api/v1/tickets",
        json={"title": "X", "type": "task", "priority": "not-an-int"},
    )
    assert res.status_code == 400
    payload = res.get_json()
    assert payload["ok"] is False
    assert payload["error"]["code"] == "ARG"
    assert payload["error"]["details"]["field"] == "priority"


def test_write_rejects_invalid_json_body(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir(parents=True, exist_ok=True)
    _git_init(repo)
    (repo / ".loom" / "ticket").mkdir(parents=True, exist_ok=True)

    app = create_app(
        cfg=ServerConfig(
            repo_root=repo,
            workspace_mode="repo",
            workspace_root=None,
            enable_writes=True,
            token="",
            require_token=False,
        )
    )
    client = app.test_client()

    res = client.post(
        "/api/v1/tickets",
        data="{not-json",
        headers={"Content-Type": "application/json"},
    )
    assert res.status_code == 400
    payload = res.get_json()
    assert payload["ok"] is False
    assert payload["error"]["code"] == "ARG"


def test_write_internal_error_is_sanitized(tmp_path: Path, monkeypatch):
    repo = tmp_path / "repo"
    repo.mkdir(parents=True, exist_ok=True)
    _git_init(repo)
    (repo / ".loom" / "ticket").mkdir(parents=True, exist_ok=True)

    app = create_app(
        cfg=ServerConfig(
            repo_root=repo,
            workspace_mode="repo",
            workspace_root=None,
            enable_writes=True,
            token="",
            require_token=False,
        )
    )
    client = app.test_client()

    def _boom(**_kwargs):
        raise RuntimeError("secret stack trace text")

    monkeypatch.setattr("agent_loom.ticket.api.create", _boom)
    res = client.post(
        "/api/v1/tickets",
        json={"title": "X", "type": "task", "priority": 2},
    )
    assert res.status_code == 500
    payload = res.get_json()
    assert payload["ok"] is False
    assert payload["error"]["code"] == "CREATE_FAILED"
    assert payload["error"]["message"] == "internal error"
    assert "secret stack trace text" not in payload["error"]["message"]
    assert payload["error"]["details"]["error_id"]
