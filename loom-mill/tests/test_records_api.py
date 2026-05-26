from pathlib import Path
import json
from types import SimpleNamespace

import pytest

from loom_mill.app import create_app
from loom_mill.api.records import get_record_content
from loom_mill.parser import parse_record
from loom_mill.state import MillStateStore


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _request(store: MillStateStore, workspace_root: Path, record_id: str):
    return SimpleNamespace(
        path_params={"record_id": record_id},
        app=SimpleNamespace(state=SimpleNamespace(store=store, workspace_root=str(workspace_root))),
    )


def test_record_content_route_is_registered():
    assert any(route.path == "/records/{record_id:path}/content" for route in create_app().routes)


@pytest.mark.asyncio
async def test_record_content_endpoint_returns_raw_markdown(tmp_path):
    content = """# Example Ticket

ID: ticket:20260526-example
Type: Ticket
Status: open
Created: 2026-05-26
Updated: 2026-05-26

## Acceptance

- ACC-001: Return raw Markdown.
"""
    loom = tmp_path / ".loom"
    record_path = loom / "tickets" / "20260526-example.md"
    _write(record_path, content)
    record = parse_record(record_path, root=loom)
    store = MillStateStore()
    await store.replace_all_records((record,))

    response = await get_record_content(_request(store, tmp_path, "ticket:20260526-example"))

    assert response.status_code == 200
    assert json.loads(response.body) == {
        "id": "ticket:20260526-example",
        "path": "tickets/20260526-example.md",
        "content": content,
    }


@pytest.mark.asyncio
async def test_record_content_endpoint_returns_404_for_unknown_record(tmp_path):
    (tmp_path / ".loom").mkdir()
    store = MillStateStore()

    response = await get_record_content(_request(store, tmp_path, "ticket:20260526-missing"))

    assert response.status_code == 404
    assert json.loads(response.body) == {"detail": "Record not found"}
