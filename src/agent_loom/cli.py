from __future__ import annotations

import sys
from typing import Optional, Sequence

from agent_loom.compound.cli import main as compound_main
from agent_loom.memory.cli import main as memory_main
from agent_loom.dashboard.cli import main as dashboard_main
from agent_loom.team.cli import main as team_main
from agent_loom.ticket.cli import main as ticket_main
from agent_loom.workspace.cli import main as workspace_main


def _print_root_help() -> None:
    sys.stderr.write(
        "\n".join(
            [
                "Usage: loom <command> ...",
                "",
                "Commands:",
                "  init       Initialize all Loom subsystems (workspace/ticket/memory/team/compound)",
                "  ticket     Git-backed ticket system (.loom/ticket)",
                "  memory     Git-backed memory vault (.loom/memory)",
                "  workspace  Workspace + worktree tooling (.loom/workspaces/workspace.json + .loom/workspace/)",
                "  team       tmux-native orchestration (.loom/team)",
                "  compound   OpenCode compound integration (.opencode)",
                "  dashboard  HTTP server for the Loom API (dashboard UI)",
                "",
                "Help:",
                "  loom <command> -h",
                "",
            ]
        )
        + "\n"
    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = list(argv) if argv is not None else sys.argv[1:]

    if not args or args[0] in {"-h", "--help", "help"}:
        _print_root_help()
        return 0 if (args and args[0] in {"-h", "--help", "help"}) else 2

    cmd, rest = args[0], args[1:]

    if cmd == "init":
        from agent_loom.init import main as init_main

        return int(init_main(list(rest)))

    if cmd == "ticket":
        try:
            ticket_main(list(rest))
            return 0
        except SystemExit as e:
            return int(e.code or 0)

    if cmd == "memory":
        return int(memory_main(list(rest)))

    if cmd == "workspace":
        return int(workspace_main(list(rest)))

    if cmd == "team":
        return int(team_main(list(rest)))

    if cmd == "compound":
        return int(compound_main(list(rest)))

    if cmd == "dashboard":
        return int(dashboard_main(list(rest)))

    sys.stderr.write(f"Unknown command: {cmd}\n")
    _print_root_help()
    return 2
