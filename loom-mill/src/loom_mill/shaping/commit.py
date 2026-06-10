from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import TYPE_CHECKING

from loom_mill.state.store import MillStateStore

from .events import ShapingEvent
from .models import StagedRecord
from .session import utc_now
from .staging import slugify

if TYPE_CHECKING:
    from .session import ShapingSession


SURFACE_SINGULAR = {
    "tickets": "ticket",
    "specs": "spec",
    "plans": "plan",
    "research": "research",
    "evidence": "evidence",
    "knowledge": "knowledge",
}


@dataclass
class CommitResult:
    records_created: int
    paths: list[str]
    commit_message: str
    session_record_path: str


class CommitFlow:
    def __init__(self, session: ShapingSession, workspace_root: Path, store: MillStateStore):
        self.session = session
        self.workspace_root = Path(workspace_root)
        self.store = store

    async def commit(self) -> CommitResult:
        records = [record for record in self.session.staging.list_branch(self.session.state.active_branch) if record.status == "accepted"]
        if not records:
            raise ValueError("Nothing to commit")

        id_map = {record.temp_id: generate_real_id(record.surface, record.title) for record in records}
        resolved_records = resolve_references(records, id_map)
        path_map = {record.temp_id: self._record_path(record) for record in resolved_records}
        session_record = self._session_record(resolved_records, id_map)
        path_map[session_record.temp_id] = self.workspace_root / ".loom" / "knowledge" / f"{session_record.temp_id.split(':', 2)[2]}.md"

        written_paths = await atomic_write_all([*resolved_records, session_record], path_map, self.workspace_root)
        relative_paths = [str(path.relative_to(self.workspace_root)) for path in written_paths]
        commit_message = self._generate_commit_message(records)
        try:
            self._run_git(["add", *relative_paths])
            self._run_git(["commit", "-m", commit_message])
        except Exception as error:
            self._reset_index(relative_paths)
            for path in written_paths:
                path.unlink(missing_ok=True)
            raise RuntimeError(f"Failed to commit shaped records; rolled back written files: {error}") from error

        self.session.end()
        await self.store.publish(
            ShapingEvent(
                session_id=self.session.session_id,
                event="session_ended",
                data={"reason": "committed", "records_created": len(records)},
            )
        )
        return CommitResult(
            records_created=len(records),
            paths=relative_paths,
            commit_message=commit_message,
            session_record_path=str(path_map[session_record.temp_id].relative_to(self.workspace_root)),
        )

    def _record_path(self, record: StagedRecord) -> Path:
        real_id = generate_real_id(record.surface, record.title)
        stem = real_id.split(":", 1)[1]
        return self.workspace_root / ".loom" / record.surface / f"{stem}.md"

    def _session_record(self, records: list[StagedRecord], id_map: dict[str, str]) -> StagedRecord:
        today = _utc_date().isoformat()
        slug = f"{today.replace('-', '')}-shaping-session-{self.session.session_id[:8]}"
        refs = "\n".join(f"- `{id_map[record.temp_id]}` - {record.title}" for record in records)
        content = f"""# Shaping Session Record

ID: knowledge:{slug}
Type: Knowledge
Status: active
Created: {today}
Updated: {today}

## Summary

Shaping session `{self.session.session_id}` produced {len(records)} staged records and committed them atomically.

## Records Created

{refs}

## Session Context

The full session context document is available at `.mill/shaping-sessions/{self.session.session_id}/context.md`.
"""
        return StagedRecord(
            temp_id=f"temp:knowledge:{slug}",
            surface="knowledge",
            title="Shaping Session Record",
            content=content,
            branch=self.session.state.active_branch,
            status="accepted",
            proposed_at=utc_now(),
        )

    def _generate_commit_message(self, records: list[StagedRecord]) -> str:
        counts: dict[str, int] = {}
        for record in records:
            counts[record.surface] = counts.get(record.surface, 0) + 1
        summary = ", ".join(f"{count} {surface}" for surface, count in counts.items())
        titles = "\n".join(f"- {record.title}" for record in records)
        return f"shape: {summary}\n\nShaped records:\n{titles}"

    def _run_git(self, args: list[str]) -> None:
        result = subprocess.run(["git", *args], cwd=self.workspace_root, capture_output=True, text=True)
        if result.returncode != 0:
            message = result.stderr.strip() or result.stdout.strip() or f"git {' '.join(args)} failed"
            raise RuntimeError(message)

    def _reset_index(self, relative_paths: list[str]) -> None:
        if not relative_paths:
            return
        subprocess.run(["git", "reset", "HEAD", "--", *relative_paths], cwd=self.workspace_root, capture_output=True, text=True)


def generate_real_id(surface: str, title: str) -> str:
    today = _utc_date().strftime("%Y%m%d")
    surface_singular = SURFACE_SINGULAR.get(surface, surface.rstrip("s"))
    return f"{surface_singular}:{today}-{slugify(title)}"


def _utc_date():
    return datetime.now(timezone.utc).date()


def resolve_references(records: list[StagedRecord], id_map: dict[str, str]) -> list[StagedRecord]:
    resolved: list[StagedRecord] = []
    for record in records:
        content = record.content
        for temp_id, real_id in id_map.items():
            content = content.replace(temp_id, real_id)
        real_id = id_map[record.temp_id]
        if re.search(r"^ID:\s*.*$", content, flags=re.MULTILINE):
            content = re.sub(r"^ID:\s*.*$", f"ID: {real_id}", content, count=1, flags=re.MULTILINE)
        else:
            content = content.rstrip() + f"\n\nID: {real_id}\n"
        resolved.append(replace(record, content=content))
    return resolved


async def atomic_write_all(records: list[StagedRecord], path_map: dict[str, Path], workspace_root: Path) -> list[Path]:
    written: list[Path] = []
    tmp_paths: list[Path] = []
    try:
        for record in records:
            path = path_map[record.temp_id]
            path.parent.mkdir(parents=True, exist_ok=True)
            tmp = path.with_suffix(f"{path.suffix}.tmp")
            tmp.write_text(record.content, encoding="utf-8")
            tmp_paths.append(tmp)
            os.replace(tmp, path)
            written.append(path)
        return written
    except Exception:
        for tmp in tmp_paths:
            tmp.unlink(missing_ok=True)
        for path in written:
            path.unlink(missing_ok=True)
        raise
