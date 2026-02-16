import os

import pytest


@pytest.fixture(autouse=True)
def clear_team_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    for key in tuple(os.environ):
        if key.startswith("TEAM_"):
            monkeypatch.delenv(key, raising=False)
