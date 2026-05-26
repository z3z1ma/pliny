from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


@dataclass(frozen=True)
class HarnessConfig:
    command: str
    args: list[str] = field(default_factory=list)
    env: dict[str, str] | None = None
    cwd: str | None = None

    def command_line(self, ticket_path: Path) -> list[str]:
        rendered_ticket_path = str(ticket_path)
        return [
            self.command,
            *[arg.replace("{ticket_path}", rendered_ticket_path) for arg in self.args],
        ]


@dataclass(frozen=True)
class FactoryConfig:
    max_workstations: int = 1
    harness: HarnessConfig = field(
        default_factory=lambda: HarnessConfig(command="opencode", args=["run", "--model", "gpt-5.5", "{ticket_path}"])
    )
    shipping_mode: Literal["auto-merge", "operator-approved"] = "auto-merge"
    default_target_branch: str = "main"
    cleanup_branch_after_merge: bool = True
    ready_to_ship_statuses: list[str] = field(default_factory=lambda: ["review", "closed"])
    scheduling_enabled: bool = False
    ready_ticket_statuses: list[str] = field(default_factory=lambda: ["open"])
    spc_model: str | None = None
