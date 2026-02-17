from __future__ import annotations

from agent_loom.dashboard.blueprints.compound import create_compound_blueprint
from agent_loom.dashboard.blueprints.health import create_health_blueprint
from agent_loom.dashboard.blueprints.memory import create_memory_blueprint
from agent_loom.dashboard.blueprints.team import create_team_blueprint
from agent_loom.dashboard.blueprints.tickets import create_tickets_blueprint
from agent_loom.dashboard.blueprints.workspace import create_workspace_blueprint

__all__ = [
    "create_compound_blueprint",
    "create_health_blueprint",
    "create_memory_blueprint",
    "create_team_blueprint",
    "create_tickets_blueprint",
    "create_workspace_blueprint",
]
