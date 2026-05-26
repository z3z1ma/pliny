from __future__ import annotations

import asyncio
import json
import re
from dataclasses import asdict
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Protocol

from loom_mill.parser import LoomRecord, parse_records
from loom_mill.workstation import FactoryConfig, WorkstationStatus

from .models import ScheduleOverrides, SchedulingDecision, TicketSummary


DEPENDENCY_STATUS_DONE = {"closed", "cancelled", "shipped"}
DEPENDENCY_WORD_RE = re.compile(r"\b(depends on|blocked by|requires)\b", re.IGNORECASE)
TICKET_RE = re.compile(r"\bticket:\d{8}-[A-Za-z0-9][A-Za-z0-9_-]*\b")
PRIORITY_RANK = {"high": 0, "medium": 1, "low": 2}


class LLMAdvisory(Protocol):
    async def recommend_order(
        self,
        candidates: list[TicketSummary],
        recent_completions: list[str],
        model: str | None,
    ) -> list[str]: ...


class NoopAdvisory:
    async def recommend_order(
        self,
        candidates: list[TicketSummary],
        recent_completions: list[str],
        model: str | None,
    ) -> list[str]:
        return []


class SchedulingAgent:
    def __init__(
        self,
        workspace_root: Path,
        manager=None,
        config: FactoryConfig | None = None,
        advisory: LLMAdvisory | None = None,
        advisory_timeout: float = 5.0,
    ) -> None:
        self.workspace_root = workspace_root.resolve()
        self.manager = manager
        self.config = config or (manager.config if manager is not None else FactoryConfig())
        self.advisory = advisory or NoopAdvisory()
        self.advisory_timeout = advisory_timeout

    async def schedule_next(self) -> SchedulingDecision:
        if not self.config.scheduling_enabled:
            decision = SchedulingDecision(None, [], {}, [], "scheduling disabled")
            self._log_decision(decision)
            return decision
        if self._free_slots() <= 0:
            decision = SchedulingDecision(None, [], {}, [], "WIP limit reached")
            self._log_decision(decision)
            return decision

        candidates, filtered = self._ready_candidates()
        considered = [candidate.ticket_id for candidate in candidates]
        if not candidates:
            decision = SchedulingDecision(None, considered, filtered, [], "no ready tickets")
            self._log_decision(decision)
            return decision

        deterministic = sorted(candidates, key=self._priority_key)
        ordered = self._apply_pins(deterministic)
        recommendation = await self._recommend_order(ordered)
        if recommendation:
            by_id = {candidate.ticket_id: candidate for candidate in ordered}
            recommended = [by_id[ticket_id] for ticket_id in recommendation if ticket_id in by_id]
            remainder = [candidate for candidate in ordered if candidate.ticket_id not in recommendation]
            ordered = recommended + remainder

        selected = ordered[0]
        if self.manager is not None:
            await self.manager.start(selected.path, selected.ticket_id)
        decision = SchedulingDecision(
            selected.ticket_id,
            considered,
            filtered,
            recommendation,
            f"selected {selected.ticket_id}",
        )
        self._log_decision(decision)
        return decision

    async def on_workstation_finished(self, workstation_id: str) -> SchedulingDecision:
        if not self.config.scheduling_enabled:
            decision = SchedulingDecision(None, [], {}, [], f"scheduling disabled after {workstation_id}")
            self._log_decision(decision)
            return decision
        last_decision = SchedulingDecision(None, [], {}, [], "no free capacity")
        while self._free_slots() > 0:
            last_decision = await self.schedule_next()
            if last_decision.selected_ticket is None:
                break
        return last_decision

    def queue(self) -> dict:
        candidates, filtered = self._ready_candidates()
        ordered = self._apply_pins(sorted(candidates, key=self._priority_key))
        return {
            "candidates": [self._ticket_payload(candidate) for candidate in ordered],
            "filtered": filtered,
        }

    def load_overrides(self) -> ScheduleOverrides:
        path = self._overrides_path()
        if not path.exists():
            return ScheduleOverrides()
        data = json.loads(path.read_text(encoding="utf-8"))
        return ScheduleOverrides(
            pinned=[self._normalize_ticket_id(value) for value in data.get("pinned", [])],
            excluded=[self._normalize_ticket_id(value) for value in data.get("excluded", [])],
        )

    def save_overrides(self, overrides: ScheduleOverrides) -> ScheduleOverrides:
        normalized = ScheduleOverrides(
            pinned=[self._normalize_ticket_id(value) for value in overrides.pinned if str(value).strip()],
            excluded=[self._normalize_ticket_id(value) for value in overrides.excluded if str(value).strip()],
        )
        path = self._overrides_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(asdict(normalized), indent=2) + "\n", encoding="utf-8")
        return normalized

    def read_log(self, limit: int | None = None) -> list[dict]:
        path = self._log_path()
        if not path.exists():
            return []
        lines = path.read_text(encoding="utf-8").splitlines()
        if limit is not None and limit >= 0:
            lines = lines[-limit:]
        return [json.loads(line) for line in lines if line.strip()]

    def _ready_candidates(self) -> tuple[list[TicketSummary], dict[str, str]]:
        graph = parse_records(self.workspace_root / ".loom" / "tickets")
        tickets = [record for record in graph.records if record.metadata.id and record.metadata.id.startswith("ticket:")]
        status_by_id = {record.metadata.id: (record.metadata.status or "").lower() for record in tickets}
        active_ticket_ids = self._active_ticket_ids()
        overrides = self.load_overrides()
        excluded = set(overrides.excluded)
        candidates: list[TicketSummary] = []
        filtered: dict[str, str] = {}

        for record in tickets:
            ticket_id = record.metadata.id or ""
            status = (record.metadata.status or "").lower()
            if ticket_id in excluded:
                filtered[ticket_id] = "operator excluded"
                continue
            if ticket_id in active_ticket_ids:
                filtered[ticket_id] = "already active"
                continue
            if status not in self.config.ready_ticket_statuses:
                filtered[ticket_id] = f"status {status or 'missing'} not ready"
                continue
            unsatisfied = self._unsatisfied_dependencies(record, status_by_id)
            if unsatisfied:
                filtered[ticket_id] = "unsatisfied dependencies: " + ", ".join(unsatisfied)
                continue
            candidates.append(self._summary(record))
        return candidates, filtered

    def _unsatisfied_dependencies(self, record: LoomRecord, status_by_id: dict[str, str]) -> list[str]:
        ticket_path = self.workspace_root / ".loom" / "tickets" / record.path
        text = ticket_path.read_text(encoding="utf-8") if ticket_path.exists() else ""
        dependency_ids = {ticket_id for ticket_id in record.metadata.depends_on if ticket_id.startswith("ticket:")}
        related = self._section(text, "Related Records")
        for line in related.splitlines():
            if DEPENDENCY_WORD_RE.search(line):
                dependency_ids.update(TICKET_RE.findall(line))
        return sorted(
            ticket_id
            for ticket_id in dependency_ids
            if ticket_id != record.metadata.id and status_by_id.get(ticket_id, "") not in DEPENDENCY_STATUS_DONE
        )

    def _priority_key(self, candidate: TicketSummary) -> tuple[int, int, date, str]:
        priority = (candidate.priority or "").split("-", 1)[0].strip().lower()
        return (
            PRIORITY_RANK.get(priority, len(PRIORITY_RANK)),
            self._plan_order(candidate.ticket_id),
            candidate.created or date.max,
            candidate.ticket_id,
        )

    def _apply_pins(self, candidates: list[TicketSummary]) -> list[TicketSummary]:
        pinned = self.load_overrides().pinned
        if not pinned:
            return candidates
        rank = {ticket_id: index for index, ticket_id in enumerate(pinned)}
        return sorted(candidates, key=lambda candidate: (rank.get(candidate.ticket_id, len(rank)), candidates.index(candidate)))

    async def _recommend_order(self, candidates: list[TicketSummary]) -> list[str]:
        if not candidates:
            return []
        try:
            recommendation = await asyncio.wait_for(
                self.advisory.recommend_order(candidates, self._recent_completions(), self.config.spc_model),
                timeout=self.advisory_timeout,
            )
        except (TimeoutError, OSError, RuntimeError, ValueError):
            return []
        return [self._normalize_ticket_id(ticket_id) for ticket_id in recommendation]

    def _free_slots(self) -> int:
        if self.manager is None:
            return self.config.max_workstations
        active = sum(1 for state in self.manager.list() if state.status in {WorkstationStatus.RUNNING, WorkstationStatus.PAUSED})
        return max(0, self.config.max_workstations - active)

    def _active_ticket_ids(self) -> set[str]:
        if self.manager is None:
            return set()
        return {self._normalize_ticket_id(state.ticket_id) for state in self.manager.list() if state.ticket_id}

    def _plan_order(self, ticket_id: str) -> int:
        plans_dir = self.workspace_root / ".loom" / "plans"
        if not plans_dir.exists():
            return 1_000_000
        best = 1_000_000
        for path in plans_dir.glob("*.md"):
            text = path.read_text(encoding="utf-8")
            index = text.find(ticket_id)
            if index >= 0:
                best = min(best, index)
        return best

    def _summary(self, record: LoomRecord) -> TicketSummary:
        ticket_path = self.workspace_root / ".loom" / "tickets" / record.path
        text = ticket_path.read_text(encoding="utf-8") if ticket_path.exists() else ""
        title = next((heading for level, heading in record.headings if level == 1), record.metadata.id or ticket_path.stem)
        keywords = [word.lower() for word in re.findall(r"[A-Za-z][A-Za-z0-9_-]{2,}", f"{title} {record.metadata.type or ''}")[:8]]
        return TicketSummary(
            ticket_id=record.metadata.id or self._normalize_ticket_id(ticket_path.stem),
            title=title,
            status=record.metadata.status or "",
            path=ticket_path,
            created=record.metadata.created,
            priority=record.metadata.priority,
            type_keywords=keywords,
        )

    def _recent_completions(self) -> list[str]:
        return [entry.get("selected", "") for entry in self.read_log(limit=10) if entry.get("selected")]

    def _log_decision(self, decision: SchedulingDecision) -> None:
        path = self._log_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "selected": decision.selected_ticket,
            "candidates": decision.candidates_considered,
            "filtered": decision.filtered_out,
            "advisory_recommendation": decision.advisory_recommendation,
            "reasoning": decision.reasoning,
        }
        with path.open("a", encoding="utf-8") as log_file:
            log_file.write(json.dumps(payload) + "\n")

    def _overrides_path(self) -> Path:
        return self.workspace_root / ".mill" / "scheduling_overrides.json"

    def _log_path(self) -> Path:
        return self.workspace_root / ".mill" / "scheduling_log.jsonl"

    def _ticket_payload(self, candidate: TicketSummary) -> dict:
        return {
            "ticket_id": candidate.ticket_id,
            "title": candidate.title,
            "status": candidate.status,
            "path": str(candidate.path),
            "created": candidate.created.isoformat() if candidate.created else None,
            "priority": candidate.priority,
            "type_keywords": candidate.type_keywords,
        }

    def _section(self, text: str, title: str) -> str:
        match = re.search(rf"^##\s+{re.escape(title)}\s*$", text, re.MULTILINE)
        if match is None:
            return ""
        start = match.end()
        next_heading = re.search(r"^##\s+", text[start:], re.MULTILINE)
        end = start + next_heading.start() if next_heading else len(text)
        return text[start:end]

    def _normalize_ticket_id(self, value: str) -> str:
        value = str(value).strip()
        return value if value.startswith("ticket:") else f"ticket:{value}"
