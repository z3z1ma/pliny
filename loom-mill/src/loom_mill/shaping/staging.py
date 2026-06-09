from __future__ import annotations

import re
from dataclasses import replace
from typing import TYPE_CHECKING

from .models import StagedRecord
from .session import utc_now

if TYPE_CHECKING:
    from .session import ShapingSession


def slugify(title: str) -> str:
    slug = title.lower().strip()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s]+", "-", slug)
    slug = slug.strip("-")[:50]
    return slug or "untitled"


class StagingArea:
    def __init__(self, session: ShapingSession):
        self.session = session

    def propose(self, surface: str, title: str, content: str, branch: str = "main") -> StagedRecord:
        if branch not in self.session.state.branches:
            raise ValueError(f"Branch {branch} not found")
        temp_id = f"temp:{surface}:{slugify(title)}"
        record = StagedRecord(
            temp_id=temp_id,
            surface=surface,
            title=title,
            content=content,
            branch=branch,
            status="proposed",
            proposed_at=utc_now(),
        )
        self.session.state.staged_records.append(record)
        self.session.state.updated_at = utc_now()
        self.session._persist_state()
        return record

    def update(self, temp_id: str, content: str | None = None, title: str | None = None) -> StagedRecord:
        record = self._find(temp_id)
        self._ensure_mutable(record)
        if content is not None:
            record.content = content
        if title is not None:
            record.title = title
        record.status = "modified"
        record.modified_at = utc_now()
        self.session.state.updated_at = utc_now()
        self.session._persist_state()
        return record

    def accept(self, temp_id: str) -> StagedRecord:
        record = self._find(temp_id)
        if record.status == "accepted":
            return record
        record.status = "accepted"
        record.modified_at = utc_now()
        self.session.state.updated_at = utc_now()
        self.session._persist_state()
        return record

    def reject(self, temp_id: str) -> None:
        record = self._find(temp_id)
        self._ensure_mutable(record)
        self.session.state.staged_records = [record for record in self.session.state.staged_records if record.temp_id != temp_id]
        self.session.state.updated_at = utc_now()
        self.session._persist_state()

    def consolidate(self, targets: list[str], surface: str, title: str, content: str) -> StagedRecord:
        if len(targets) != len(set(targets)):
            raise ValueError("Consolidation targets must be unique")
        records = [self._find(temp_id) for temp_id in targets]
        for record in records:
            self._ensure_mutable(record, action="consolidate")
        branch = records[0].branch if records else self.session.state.active_branch
        merged_temp_id = f"temp:{surface}:{slugify(title)}"
        target_ids = set(targets)
        if any(record.temp_id == merged_temp_id and record.temp_id not in target_ids for record in self.session.state.staged_records):
            raise ValueError(f"Staged record {merged_temp_id} already exists")
        now = utc_now()
        merged = StagedRecord(
            temp_id=merged_temp_id,
            surface=surface,
            title=title,
            content=content,
            branch=branch,
            status="proposed",
            proposed_at=now,
        )
        self.session.state.staged_records = [record for record in self.session.state.staged_records if record.temp_id not in target_ids]
        self.session.state.staged_records.append(merged)
        self.session.state.updated_at = now
        self.session._persist_state()
        return merged

    def list_branch(self, branch: str = "main") -> list[StagedRecord]:
        return [record for record in self.session.state.staged_records if record.branch == branch]

    def create_branch(self, branch_id: str, label: str) -> None:
        if branch_id in self.session.state.branches:
            raise ValueError(f"Branch {branch_id} already exists")
        for record in self.list_branch(self.session.state.active_branch):
            self._ensure_mutable(record, action="branch")
        self.session.state.branches.append(branch_id)
        for record in self.list_branch(self.session.state.active_branch):
            self.session.state.staged_records.append(
                replace(record, temp_id=f"{record.temp_id}:{branch_id}", branch=branch_id, modified_at=utc_now())
            )
        self.session.state.updated_at = utc_now()
        self.session._persist_state()

    def switch_branch(self, branch_id: str) -> None:
        if branch_id not in self.session.state.branches:
            raise ValueError(f"Branch {branch_id} not found")
        self.session.state.active_branch = branch_id
        self.session.state.updated_at = utc_now()
        self.session._persist_state()

    def merge_branch(self, source: str, target: str = "main") -> None:
        if source not in self.session.state.branches:
            raise ValueError(f"Branch {source} not found")
        if target not in self.session.state.branches:
            raise ValueError(f"Branch {target} not found")
        if source == target:
            raise ValueError("source and target branches must differ")

        source_records = self.list_branch(source)
        for record in source_records:
            self._ensure_mutable(record, action="merge")
        source_keys = {(record.surface, record.title) for record in source_records}
        for record in self.list_branch(target):
            if (record.surface, record.title) in source_keys:
                self._ensure_mutable(record, action="merge")
        self.session.state.staged_records = [
            record
            for record in self.session.state.staged_records
            if record.branch != target or (record.surface, record.title) not in source_keys
        ]
        for record in source_records:
            record.branch = target
            record.modified_at = utc_now()
        self.session.state.branches = [branch for branch in self.session.state.branches if branch != source]
        self.session.state.active_branch = target
        self.session.state.updated_at = utc_now()
        self.session._persist_state()

    def cross_references(self) -> dict[str, list[str]]:
        refs: dict[str, list[str]] = {}
        active_records = self.list_branch(self.session.state.active_branch)
        all_temp_ids = {record.temp_id for record in active_records}
        for record in active_records:
            refs[record.temp_id] = [temp_id for temp_id in all_temp_ids if temp_id != record.temp_id and temp_id in record.content]
        return refs

    def _find(self, temp_id: str) -> StagedRecord:
        for record in self.session.state.staged_records:
            if record.temp_id == temp_id:
                return record
        raise ValueError(f"Staged record {temp_id} not found")

    def _ensure_mutable(self, record: StagedRecord, action: str = "mutate") -> None:
        if record.status == "accepted":
            raise ValueError(f"Cannot {action} accepted record {record.temp_id}")
