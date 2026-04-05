#!/usr/bin/env python3
"""Build the Loom CLI into a self-contained executable zipapp."""

from __future__ import annotations

import shutil
import tempfile
import zipapp
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOOM_PKG = ROOT / "loom"
OUTPUT = ROOT / "skills" / "loom"


def main() -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        shutil.copytree(LOOM_PKG, tmp / "loom")
        zipapp.create_archive(
            str(tmp),
            str(OUTPUT),
            interpreter="/usr/bin/env python3",
            main="loom.__main__:main",
        )
    OUTPUT.chmod(0o755)
    print(f"Built: {OUTPUT}")
    print(f"Size: {OUTPUT.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
