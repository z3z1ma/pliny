from __future__ import annotations

import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, List, Optional, Sequence

from agent_loom.core.io import atomic_write_json as core_atomic_write_json
from agent_loom.core.io import atomic_write_text as core_atomic_write_text
from agent_loom.core.io import read_json as core_read_json
from agent_loom.core.time import now_iso as core_now_iso
from agent_loom.workspace.errors import WorkspaceError


def now_iso() -> str:
    return core_now_iso()


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def parallel_map(fn, items: Sequence[Any], jobs: int) -> List[Any]:
    if jobs <= 1:
        return [fn(x) for x in items]
    with ThreadPoolExecutor(max_workers=jobs) as ex:
        futs = [ex.submit(fn, x) for x in items]
        return [f.result() for f in futs]


def atomic_write_text(path: Path, text: str) -> None:
    core_atomic_write_text(path, text)


def atomic_write_json(path: Path, data: dict) -> None:
    core_atomic_write_json(path, data)


def read_json(path: Path) -> dict:
    return core_read_json(path)


def which(exe: str) -> Optional[str]:
    return shutil.which(exe)


def run(
    cmd: List[str], cwd: Optional[Path] = None, check: bool = True
) -> subprocess.CompletedProcess:
    p = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and p.returncode != 0:
        raise WorkspaceError(
            f"Command failed: {' '.join(cmd)}\n"
            f"cwd: {cwd or Path.cwd()}\n"
            f"stdout:\n{p.stdout}\n"
            f"stderr:\n{p.stderr}"
        )
    return p


def is_git_repo(path: Path) -> bool:
    # normal repo has .git dir; worktree has .git file
    gitp = path / ".git"
    return gitp.is_dir() or gitp.is_file()


def short(s: str, n: int = 10) -> str:
    return s[:n]
