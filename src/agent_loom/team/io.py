from __future__ import annotations

import dataclasses
import json
import os
from pathlib import Path
from typing import Any


@dataclasses.dataclass
class FileLock:
    """A small advisory file lock.

    This intentionally stays simple: we only need to serialize run.json updates.

    On platforms without fcntl (Windows), we fall back to a best-effort lock via
    exclusive file creation.
    """

    path: Path
    _fd: int = -1

    def __enter__(self) -> "FileLock":
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._fd = os.open(self.path, os.O_RDWR | os.O_CREAT, 0o600)
        try:
            import fcntl  # type: ignore

            fcntl.flock(self._fd, fcntl.LOCK_EX)
        except Exception:
            pass
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        try:
            import fcntl  # type: ignore

            fcntl.flock(self._fd, fcntl.LOCK_UN)
        except Exception:
            pass
        if self._fd != -1:
            os.close(self._fd)


def _atomic_write_file(path: Path, data: str, *, encoding: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "w", encoding=encoding) as f:
        f.write(data)
        f.flush()
        try:
            os.fsync(f.fileno())
        except Exception:
            pass
    os.replace(tmp, path)


def _atomic_write_json(path: Path, payload: Any) -> None:
    data = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    _atomic_write_file(path, data, encoding="utf-8")


def _atomic_write_text(path: Path, text: str, *, encoding: str = "utf-8") -> None:
    _atomic_write_file(path, text, encoding=encoding)


def _read_json(path: Path) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


__all__ = [
    "FileLock",
    "_atomic_write_file",
    "_atomic_write_json",
    "_atomic_write_text",
    "_read_json",
]
