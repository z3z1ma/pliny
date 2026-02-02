from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from agent_loom.memory.core import add as memory_add
from agent_loom.memory.core import init as memory_init
from agent_loom.dashboard.app import create_app
from agent_loom.dashboard.config import ServerConfig
from agent_loom.ticket.api import create as ticket_create


def _git_init(repo: Path) -> None:
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)


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
