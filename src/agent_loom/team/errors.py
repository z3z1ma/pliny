from __future__ import annotations


class TeamError(RuntimeError):
    def __init__(
        self,
        message: str,
        *,
        code: str = "ERROR",
        exit_code: int = 1,
        data: dict | None = None,
        hint: str = "",
        suggestions: list[str] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.exit_code = exit_code
        self.data = data
        self.hint = hint
        self.suggestions = list(suggestions or [])


__all__ = ["TeamError"]
