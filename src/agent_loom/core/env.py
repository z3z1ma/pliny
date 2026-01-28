from __future__ import annotations

import contextlib
import os
from collections.abc import Iterator, Mapping
from typing import Optional


@contextlib.contextmanager
def patched_environ(env: Optional[Mapping[str, str]] = None) -> Iterator[None]:
    if not env:
        yield
        return

    before = os.environ.copy()
    os.environ.update({str(k): str(v) for k, v in env.items()})
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(before)
