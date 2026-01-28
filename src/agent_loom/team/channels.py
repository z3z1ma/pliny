from __future__ import annotations

from agent_loom.team.constants import DEFAULT_TMUX_SESSION_PREFIX
from agent_loom.team.strings import sanitize


def resolve_team_from_session(session: str) -> str:
    if session.startswith(f"{DEFAULT_TMUX_SESSION_PREFIX}-"):
        return session[len(f"{DEFAULT_TMUX_SESSION_PREFIX}-") :]
    return session


def channel_for(*, run_id: str, to: str) -> str:
    rid = str(run_id or "").strip()
    recipient = sanitize(str(to or "").strip(), allow=r"a-zA-Z0-9._-", max_len=48)
    if not rid or not recipient:
        return ""
    return f"team:{rid[:12]}:to:{recipient}"


__all__ = ["channel_for", "resolve_team_from_session"]
