from __future__ import annotations

from typing import Any, Mapping, Sequence


class TicketUserErrorMixin(Exception):
    """A mixin for user-facing exceptions with recovery guidance.

    We implement this as a mixin so exceptions can still be `ValueError`,
    `FileNotFoundError`, etc. This keeps argparse and legacy callers working
    while giving the CLI structured data for agent UX.
    """

    code: str
    error: str
    hint: str
    suggestions: Sequence[str]
    details: Mapping[str, Any]

    def __init__(
        self,
        *,
        code: str,
        error: str,
        hint: str = "",
        suggestions: Sequence[str] | None = None,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(error)
        self.code = str(code)
        self.error = str(error)
        self.hint = str(hint or "")
        self.suggestions = tuple(suggestions or ())
        self.details = dict(details or {})

    def __str__(self) -> str:  # pragma: no cover
        return self.error


class TicketArgError(TicketUserErrorMixin, ValueError):
    pass


class TicketNotFoundError(TicketUserErrorMixin, FileNotFoundError):
    pass


class TicketPermissionError(TicketUserErrorMixin, PermissionError):
    pass


__all__ = [
    "TicketArgError",
    "TicketNotFoundError",
    "TicketPermissionError",
    "TicketUserErrorMixin",
]
