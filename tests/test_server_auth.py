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
    (repo / ".tickets").mkdir(parents=True, exist_ok=True)

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
    (repo / ".tickets").mkdir(parents=True, exist_ok=True)

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
