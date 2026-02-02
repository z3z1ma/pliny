from typing import TYPE_CHECKING, Literal, Optional

if TYPE_CHECKING:
    from agent_loom.ticket.store import AuditLogger

SUBSYSTEM_NAME = "agent-loom-ticket"
SUBSYSTEM_VERSION = "1.0.0"

TICKET_DIRNAME = ".tickets"
LOCKS_DIRNAME = ".locks"
CACHE_DIRNAME = ".cache"
CONFIG_FILENAME = "config.yaml"
AUDIT_DIRNAME = ".audit"

VALID_STATUSES = ("open", "ready", "in_progress", "blocked", "review", "closed")

TERMINAL_STATUSES = ("closed",)
BACKLOG_STATUSES = ("open", "ready")
ACTIVE_STATUSES = ("in_progress", "blocked", "review")
NON_TERMINAL_STATUSES = ("open", "ready", "in_progress", "blocked", "review")

STATUS_ORDER = ("open", "ready", "in_progress", "blocked", "review", "closed")

TICKET_DIR_OVERRIDE: Optional[str] = None

AUDIT_MODE: Literal["all", "writes", "off"] = "all"
AUDIT_LOGGER: Optional["AuditLogger"] = None

__all__ = [
    "SUBSYSTEM_NAME",
    "SUBSYSTEM_VERSION",
    "TICKET_DIRNAME",
    "LOCKS_DIRNAME",
    "CACHE_DIRNAME",
    "CONFIG_FILENAME",
    "AUDIT_DIRNAME",
    "VALID_STATUSES",
    "TERMINAL_STATUSES",
    "BACKLOG_STATUSES",
    "ACTIVE_STATUSES",
    "NON_TERMINAL_STATUSES",
    "STATUS_ORDER",
    "TICKET_DIR_OVERRIDE",
    "AUDIT_MODE",
    "AUDIT_LOGGER",
]
