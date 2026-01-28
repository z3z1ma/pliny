from __future__ import annotations


class MemoryError(RuntimeError):
    def __init__(
        self,
        message: str,
        *,
        code: str = "ERROR",
        exit_code: int = 1,
        hint: str = "",
        suggestions: list[str] | None = None,
        details: dict | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.exit_code = exit_code
        self.hint = hint
        self.suggestions = list(suggestions or [])
        self.details = details


__all__ = ["MemoryError"]
