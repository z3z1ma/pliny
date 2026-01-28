from __future__ import annotations

import os
import shlex
import shutil
import subprocess
from pathlib import Path
from typing import Mapping, Optional, Sequence

from agent_loom.team.errors import TeamError


def _require_bin(name: str) -> None:
    if not shutil.which(name):
        raise TeamError(
            f"Required executable not found in PATH: {name}",
            code="MISSING_BIN",
            exit_code=127,
        )


def _run(
    argv: Sequence[str],
    *,
    cwd: Optional[Path] = None,
    env: Optional[Mapping[str, str]] = None,
    check: bool = True,
    timeout: Optional[float] = None,
) -> subprocess.CompletedProcess[str]:
    if not argv:
        raise TeamError("empty argv", code="BUG", exit_code=2)

    try:
        p = subprocess.run(
            list(argv),
            cwd=str(cwd) if cwd is not None else None,
            env=({**os.environ, **dict(env)}) if env is not None else None,
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as e:
        raise TeamError(
            f"Command timed out after {timeout}s: {shlex.join(argv)}",
            code="TIMEOUT",
            exit_code=2,
        ) from e
    except FileNotFoundError as e:
        raise TeamError(
            f"Executable not found: {argv[0]}", code="MISSING_BIN", exit_code=127
        ) from e

    if check and p.returncode != 0:
        raise TeamError(
            "Command failed:\n"
            f"  cmd: {shlex.join(argv)}\n"
            f"  cwd: {str(cwd) if cwd else os.getcwd()}\n"
            f"  exit: {p.returncode}\n"
            f"  stdout:\n{p.stdout}\n"
            f"  stderr:\n{p.stderr}\n",
            code="CMD",
            exit_code=p.returncode or 1,
        )
    return p


__all__ = ["_require_bin", "_run"]
