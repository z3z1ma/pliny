from __future__ import annotations

import dataclasses
import datetime as dt
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from agent_loom.compound.install import install_opencode
from agent_loom.core.git import git_repo_root
from agent_loom.memory.core import init as memory_init
from agent_loom.team.core import init_agents
from agent_loom.ticket.core import init as ticket_init
from agent_loom.workspace.poly_ops import poly_init
from agent_loom.workspace.repo_ops import repo_init


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def as_dict(obj: object) -> object:
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return dataclasses.asdict(obj)
    return obj


@dataclass(frozen=True)
class LoomInitSelection:
    workspace: bool
    ticket: bool
    memory: bool
    compound: bool
    team: bool


@dataclass(frozen=True)
class LoomInitOptions:
    root: Path
    git_root: Optional[Path]
    workspace_mode: str  # repo|poly
    selection: LoomInitSelection
    memory_vault: str
    compound_force: bool


@dataclass(frozen=True)
class LoomInitResult:
    ok: bool
    root: str
    git: Dict[str, Any]
    selected: Dict[str, bool]
    results: Dict[str, Any]
    warnings: list[str]
    error: str
    meta: Dict[str, Any]


def detect_git_root(cwd: Path) -> Optional[Path]:
    return git_repo_root(cwd)


def resolve_root_for_init(cwd: Path) -> tuple[Path, Optional[Path]]:
    gr = detect_git_root(cwd)
    if gr is not None:
        return gr.resolve(), gr.resolve()
    return cwd.resolve(), None


def run_init(opts: LoomInitOptions) -> LoomInitResult:
    warnings: list[str] = []
    results: Dict[str, Any] = {}
    ok = True
    err = ""

    git_payload: Dict[str, Any] = {
        "ok": opts.git_root is not None,
        "repo_root": str(opts.git_root) if opts.git_root is not None else "",
    }

    ws_mode = str(opts.workspace_mode or "").strip().lower()
    if opts.selection.workspace and ws_mode not in {"repo", "poly"}:
        raise ValueError("workspace_mode must be 'repo' or 'poly'")

    # Execute in deterministic order.
    try:
        if opts.selection.workspace:
            if ws_mode == "repo":
                if opts.git_root is None:
                    raise ValueError("workspace repo init requires a git repository")
                results["workspace"] = as_dict(repo_init(root=opts.git_root))
            elif ws_mode == "poly":
                results["workspace"] = as_dict(poly_init(root=opts.root))
            else:
                raise ValueError("workspace_mode must be 'repo' or 'poly'")
        else:
            results["workspace"] = {"skipped": True}

        if opts.selection.ticket:
            results["ticket"] = as_dict(ticket_init())
        else:
            results["ticket"] = {"skipped": True}

        if opts.selection.memory:
            results["memory"] = as_dict(memory_init(vault=str(opts.memory_vault)))
        else:
            results["memory"] = {"skipped": True}

        if opts.selection.compound:
            res = install_opencode(
                dest=opts.root,
                dry_run=False,
                force=bool(opts.compound_force),
            )
            results["compound"] = {
                "dest": res.dest,
                "dry_run": res.dry_run,
                "wrote": sorted(list(res.wrote or [])),
                "skipped": sorted(list(res.skipped or [])),
                "warnings": sorted(list(res.warnings or [])),
                "force": bool(opts.compound_force),
            }
        else:
            results["compound"] = {"skipped": True}

        if opts.selection.team:
            if opts.git_root is None:
                results["team"] = {
                    "skipped": True,
                    "reason": "requires git repo",
                }
            else:
                results["team"] = as_dict(
                    init_agents(repo=opts.git_root, create_missing=True)
                )
        else:
            results["team"] = {"skipped": True}
    except Exception as e:
        ok = False
        err = str(e)

    selected = {
        "workspace": bool(opts.selection.workspace),
        "ticket": bool(opts.selection.ticket),
        "memory": bool(opts.selection.memory),
        "compound": bool(opts.selection.compound),
        "team": bool(opts.selection.team),
    }

    if isinstance(results.get("compound"), dict):
        cw = list((results.get("compound") or {}).get("warnings") or [])
        warnings.extend([str(w) for w in cw if str(w)])

    warnings = sorted({w for w in warnings if w})
    return LoomInitResult(
        ok=bool(ok),
        root=str(opts.root),
        git=git_payload,
        selected=selected,
        results=results,
        warnings=warnings,
        error=err,
        meta={"generated_at": now_iso(), "workspace_mode": ws_mode},
    )
