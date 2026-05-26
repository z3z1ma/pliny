from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class IterationRecord:
    iteration: int
    started_at: str
    ended_at: str
    duration_seconds: float
    exit_code: int | None
    commit_sha: str | None
    files_changed: list[str]
    lines_added: int
    lines_removed: int
    diff_stat: str
    previous_commit_sha: str | None = None


class IterationStore:
    def __init__(self, workspace_root: str | Path, workstation_id: str) -> None:
        self.workspace_root = Path(workspace_root).resolve()
        self.workstation_id = workstation_id

    @property
    def root(self) -> Path:
        return self.workspace_root / ".mill" / "workstations" / self.workstation_id / "iterations"

    def next_iteration(self) -> int:
        records = self.list()
        return (records[-1].iteration + 1) if records else 1

    def list(self) -> list[IterationRecord]:
        if not self.root.exists():
            return []
        records = []
        for path in sorted(self.root.glob("*.json"), key=lambda item: int(item.stem)):
            records.append(self.get(int(path.stem)))
        return records

    def get(self, iteration: int) -> IterationRecord:
        path = self._json_path(iteration)
        data = json.loads(path.read_text(encoding="utf-8"))
        return IterationRecord(**data)

    def diff(self, iteration: int) -> str | None:
        path = self._diff_path(iteration)
        if not path.exists():
            return None
        return path.read_text(encoding="utf-8")

    def save(self, record: IterationRecord, diff: str) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        self._json_path(record.iteration).write_text(json.dumps(asdict(record), indent=2) + "\n", encoding="utf-8")
        self._diff_path(record.iteration).write_text(diff, encoding="utf-8")

    def aggregate_diff(self) -> str:
        diffs = []
        for record in self.list():
            diff = self.diff(record.iteration)
            if diff:
                diffs.append(diff)
        return "\n".join(diffs)

    def _json_path(self, iteration: int) -> Path:
        return self.root / f"{iteration}.json"

    def _diff_path(self, iteration: int) -> Path:
        return self.root / f"{iteration}.diff"
