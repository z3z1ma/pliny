from __future__ import annotations

import asyncio
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from loom_mill.api.scheduling import put_scheduling_enabled, put_scheduling_overrides, scheduling_log, scheduling_queue
from loom_mill.scheduling import ScheduleOverrides, SchedulingAgent
from loom_mill.workstation import FactoryConfig, WorkstationState, WorkstationStatus


class FakeManager:
    def __init__(self, config: FactoryConfig) -> None:
        self.config = config
        self.started: list[tuple[Path, str]] = []
        self._states: list[WorkstationState] = []

    def list(self) -> list[WorkstationState]:
        return self._states

    async def start(self, ticket_path: Path, ticket_id: str):
        self.started.append((ticket_path, ticket_id))
        state = WorkstationState(id=f"ws-{len(self.started)}", ticket_id=ticket_id.removeprefix("ticket:"), status=WorkstationStatus.RUNNING)
        self._states.append(state)
        return SimpleNamespace(state=state)

    def update_config(self, config: FactoryConfig) -> None:
        self.config = config


class FakeRequest:
    def __init__(self, app, data: dict | None = None, query_params: dict | None = None) -> None:
        self.app = app
        self._data = data or {}
        self.query_params = query_params or {}

    async def json(self) -> dict:
        return self._data


class FakeAdvisory:
    def __init__(self, recommendation: list[str], delay: float = 0) -> None:
        self.recommendation = recommendation
        self.delay = delay
        self.calls = []

    async def recommend_order(self, candidates, recent_completions, model):
        self.calls.append((candidates, recent_completions, model))
        if self.delay:
            await asyncio.sleep(self.delay)
        return self.recommendation


def write_ticket(root: Path, slug: str, body: str) -> None:
    path = root / ".loom" / "tickets" / f"{slug}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def ticket(slug: str, *, status: str = "open", created: str = "2026-05-25", priority: str | None = None, extra: str = "") -> str:
    priority_line = f"Priority: {priority}\n" if priority else ""
    return f"""# {slug}

ID: ticket:{slug}
Type: Ticket
Status: {status}
Created: {created}
Updated: 2026-05-25
Risk: low - fixture
{priority_line}
## Related Records

{extra}
"""


@pytest.mark.asyncio
async def test_on_workstation_finished_pulls_ready_tickets_until_wip_capacity(tmp_path: Path) -> None:
    write_ticket(tmp_path, "20260525-a", ticket("20260525-a"))
    write_ticket(tmp_path, "20260525-b", ticket("20260525-b"))
    write_ticket(tmp_path, "20260525-c", ticket("20260525-c", status="active"))
    manager = FakeManager(FactoryConfig(max_workstations=2, scheduling_enabled=True))

    decision = await SchedulingAgent(tmp_path, manager).on_workstation_finished("ws-finished")

    assert decision.selected_ticket == "ticket:20260525-b"
    assert [ticket_id for _, ticket_id in manager.started] == ["ticket:20260525-a", "ticket:20260525-b"]


@pytest.mark.asyncio
async def test_filters_statuses_dependencies_and_exclusions(tmp_path: Path) -> None:
    write_ticket(tmp_path, "20260525-dep", ticket("20260525-dep", status="active"))
    write_ticket(
        tmp_path,
        "20260525-blocked",
        ticket("20260525-blocked", extra="- depends on ticket:20260525-dep\n"),
    )
    write_ticket(tmp_path, "20260525-excluded", ticket("20260525-excluded"))
    write_ticket(tmp_path, "20260525-ready", ticket("20260525-ready"))
    manager = FakeManager(FactoryConfig(max_workstations=1, scheduling_enabled=True))
    agent = SchedulingAgent(tmp_path, manager)
    agent.save_overrides(ScheduleOverrides(excluded=["ticket:20260525-excluded"]))

    decision = await agent.schedule_next()

    assert decision.selected_ticket == "ticket:20260525-ready"
    assert decision.filtered_out["ticket:20260525-dep"] == "status active not ready"
    assert "unsatisfied dependencies" in decision.filtered_out["ticket:20260525-blocked"]
    assert decision.filtered_out["ticket:20260525-excluded"] == "operator excluded"


@pytest.mark.asyncio
async def test_priority_uses_pins_explicit_priority_plan_order_then_creation(tmp_path: Path) -> None:
    write_ticket(tmp_path, "20260525-old", ticket("20260525-old", created="2026-05-20"))
    write_ticket(tmp_path, "20260525-high", ticket("20260525-high", created="2026-05-26", priority="high - fixture"))
    write_ticket(tmp_path, "20260525-plan-first", ticket("20260525-plan-first", created="2026-05-28"))
    plan = tmp_path / ".loom" / "plans" / "20260525-plan.md"
    plan.parent.mkdir(parents=True, exist_ok=True)
    plan.write_text("ticket:20260525-plan-first\nticket:20260525-old\n", encoding="utf-8")
    manager = FakeManager(FactoryConfig(max_workstations=1, scheduling_enabled=True))
    agent = SchedulingAgent(tmp_path, manager)
    agent.save_overrides(ScheduleOverrides(pinned=["ticket:20260525-old"]))

    decision = await agent.schedule_next()

    assert decision.selected_ticket == "ticket:20260525-old"

    manager = FakeManager(FactoryConfig(max_workstations=1, scheduling_enabled=True))
    agent = SchedulingAgent(tmp_path, manager)
    agent.save_overrides(ScheduleOverrides())
    decision = await agent.schedule_next()
    assert decision.selected_ticket == "ticket:20260525-high"


@pytest.mark.asyncio
async def test_llm_advisory_reorders_candidates_and_timeout_falls_back(tmp_path: Path) -> None:
    write_ticket(tmp_path, "20260525-a", ticket("20260525-a", priority="high"))
    write_ticket(tmp_path, "20260525-b", ticket("20260525-b", priority="medium"))
    manager = FakeManager(FactoryConfig(max_workstations=1, scheduling_enabled=True, spc_model="test-model"))
    advisory = FakeAdvisory(["ticket:20260525-b", "ticket:20260525-a"])

    decision = await SchedulingAgent(tmp_path, manager, advisory=advisory).schedule_next()

    assert decision.selected_ticket == "ticket:20260525-b"
    assert advisory.calls[0][2] == "test-model"

    manager = FakeManager(FactoryConfig(max_workstations=1, scheduling_enabled=True))
    slow = FakeAdvisory(["ticket:20260525-b"], delay=0.05)
    fallback = await SchedulingAgent(tmp_path, manager, advisory=slow, advisory_timeout=0.01).schedule_next()
    assert fallback.selected_ticket == "ticket:20260525-a"
    assert fallback.advisory_recommendation == []


@pytest.mark.asyncio
async def test_disabled_scheduler_is_noop(tmp_path: Path) -> None:
    write_ticket(tmp_path, "20260525-a", ticket("20260525-a"))
    manager = FakeManager(FactoryConfig(max_workstations=1, scheduling_enabled=False))

    decision = await SchedulingAgent(tmp_path, manager).on_workstation_finished("ws-1")

    assert decision.selected_ticket is None
    assert manager.started == []


@pytest.mark.asyncio
async def test_scheduling_api_queue_overrides_enabled_and_log(tmp_path: Path) -> None:
    write_ticket(tmp_path, "20260525-a", ticket("20260525-a"))
    manager = FakeManager(FactoryConfig(max_workstations=1, scheduling_enabled=True))
    app = SimpleNamespace(state=SimpleNamespace(workspace_root=str(tmp_path), workstation_manager=manager))

    overrides = await put_scheduling_overrides(FakeRequest(app, {"pinned": ["20260525-a"], "excluded": []}))
    assert overrides.status_code == 200
    assert json.loads(overrides.body)["pinned"] == ["ticket:20260525-a"]

    queue = await scheduling_queue(FakeRequest(app))
    assert json.loads(queue.body)["candidates"][0]["ticket_id"] == "ticket:20260525-a"

    enabled = await put_scheduling_enabled(FakeRequest(app, {"enabled": False}))
    assert enabled.status_code == 200
    assert manager.config.scheduling_enabled is False

    SchedulingAgent(tmp_path, manager).read_log()
    log = await scheduling_log(FakeRequest(app, query_params={"limit": "5"}))
    assert log.status_code == 200
