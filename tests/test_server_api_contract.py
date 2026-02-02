from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from agent_loom.memory.core import add as memory_add
from agent_loom.memory.core import init as memory_init
from agent_loom.dashboard.app import create_app
from agent_loom.dashboard.config import ServerConfig
from agent_loom.ticket.api import create as ticket_create
from agent_loom.team.constants import DEFAULT_RUNS_DIR


def _git_init(repo: Path) -> None:
    subprocess.run(
        ["git", "init", "-b", "main"], cwd=repo, check=True, capture_output=True
    )
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"], cwd=repo, check=True
    )
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)
    (repo / "README.md").write_text("hello\n", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "-m", "init"], cwd=repo, check=True)


@pytest.fixture()
def app(tmp_path: Path):
    repo = tmp_path / "repo"
    repo.mkdir(parents=True, exist_ok=True)
    _git_init(repo)

    (repo / ".tickets").mkdir(parents=True, exist_ok=True)
    ticket_create(
        tickets_dir=repo / ".tickets",
        title="Test ticket",
        type="task",
        priority=2,
        tags="infra",
        description="",
        assignee="tester",
        external_ref="",
        parent="",
        design="",
        acceptance="",
    )

    memory_init(vault=str(repo / ".memory"))
    memory_add(
        vault=str(repo / ".memory"),
        title="Hello",
        body="World",
        tag=["infra"],
    )

    (repo / ".opencode" / "skills" / "demo-skill").mkdir(parents=True, exist_ok=True)
    (repo / ".opencode" / "skills" / "demo-skill" / "SKILL.md").write_text(
        "# Demo\n\nThis is a demo skill.\n", encoding="utf-8"
    )

    cfg = ServerConfig(
        repo_root=repo,
        workspace_mode="repo",
        workspace_root=None,
        enable_writes=False,
        token="",
        require_token=False,
    )
    return create_app(cfg=cfg)


@pytest.fixture()
def client(app):
    return app.test_client()


def test_health_contract(client):
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["ok"] is True
    assert isinstance(data["data"], dict)
    assert "repo_root" in data["data"]


def test_capabilities_includes_worktree_diff(client):
    res = client.get("/api/v1/capabilities")
    assert res.status_code == 200
    payload = res.get_json()
    assert payload["ok"] is True
    eps = payload["data"].get("endpoints") or []
    assert any(
        e.get("method") == "GET" and e.get("path") == "/api/v1/workspace/worktree/diff"
        for e in eps
        if isinstance(e, dict)
    )


def test_workspace_worktree_diff_endpoint(client):
    # Modify tracked file in the repo root (main worktree)
    # The app fixture repository is embedded in the client; fetch it from health.
    h = client.get("/api/v1/health").get_json()["data"]
    repo_root = Path(h["repo_root"]).resolve()
    (repo_root / "README.md").write_text("hello\nworld\n", encoding="utf-8")

    res = client.get(
        "/api/v1/workspace/worktree/diff",
        query_string={"mode": "repo", "path": str(repo_root)},
    )
    assert res.status_code == 200
    payload = res.get_json()
    assert payload["ok"] is True
    data = payload["data"]
    assert data["worktree"] == str(repo_root)
    files = data.get("files") or []
    assert files
    assert "diff --git a/README.md b/README.md" in (files[0] or {}).get("patch", "")


def test_tickets_list_and_show(client):
    res = client.get("/api/v1/tickets")
    assert res.status_code == 200
    payload = res.get_json()
    assert payload["ok"] is True
    tickets = payload["data"]["tickets"]
    assert tickets
    tid = tickets[0]["id"]

    res2 = client.get(f"/api/v1/tickets/{tid}")
    assert res2.status_code == 200
    payload2 = res2.get_json()
    assert payload2["ok"] is True
    assert payload2["data"]["ticket"]["id"] == tid


def test_memory_recall(client):
    res = client.get("/api/v1/memory/recall?q=World&limit=5")
    assert res.status_code == 200
    payload = res.get_json()
    assert payload["ok"] is True


def test_compound_skills(client):
    res = client.get("/api/v1/compound/skills")
    assert res.status_code == 200
    payload = res.get_json()
    assert payload["ok"] is True
    skills = payload["data"]["skills"]
    assert any(s["name"] == "demo-skill" for s in skills)

    res2 = client.get("/api/v1/compound/skills/demo-skill")
    assert res2.status_code == 200
    payload2 = res2.get_json()
    assert payload2["ok"] is True
    assert "Demo" in payload2["data"]["text"]


def test_introspect_ticket_core(client):
    res = client.get("/api/v1/introspect/ticket")
    assert res.status_code == 200
    payload = res.get_json()
    assert payload["ok"] is True
    assert payload["data"]["module"].endswith("agent_loom.ticket.core")
    assert isinstance(payload["data"]["symbols"], list)


def test_dashboard_template_contract(client):
    res = client.get("/")
    assert res.status_code == 200
    html = res.get_data(as_text=True)
    assert "<!doctype html>" in html
    assert 'id="connText"' in html
    assert 'id="globalSearch"' in html
    assert 'id="content"' in html
    assert 'id="liveBtn"' in html
    assert "const $ =" in html

    # Teams UI anchors (render templates are embedded in JS)
    assert 'id="teamsTable"' in html
    assert "data-team-tabs" in html
    assert "data-team-panel" in html


def test_team_capture_text_endpoint(client):
    h = client.get("/api/v1/health").get_json()["data"]
    repo_root = Path(h["repo_root"]).resolve()

    team = "alpha"
    run_dir = repo_root / DEFAULT_RUNS_DIR / team
    captures_dir = run_dir / "captures"
    captures_dir.mkdir(parents=True, exist_ok=True)

    # Ensure the team exists for list surfaces.
    (run_dir / "run.json").write_text(
        '{"team":"alpha","created_at":"2026-01-01T00:00:00Z","updated_at":"2026-01-01T00:00:00Z","session":"s"}\n',
        encoding="utf-8",
    )

    meta_name = "20260101T000000Z_deadbeefcafe_manager.json"
    txt_name = "20260101T000000Z_deadbeefcafe_manager.txt"

    (captures_dir / meta_name).write_text(
        '{"id":"deadbeefcafe","captured_at":"2026-01-01T00:00:00Z","lines":3,"bytes":12,"output_file":"./dummy.txt"}\n',
        encoding="utf-8",
    )
    (captures_dir / txt_name).write_text("hello capture\n", encoding="utf-8")

    res = client.get(
        f"/api/v1/teams/{team}/captures/text",
        query_string={"meta": meta_name},
    )
    assert res.status_code == 200
    payload = res.get_json()
    assert payload["ok"] is True
    data = payload["data"]
    assert data["meta"] == meta_name
    assert "hello capture" in data["text"]
