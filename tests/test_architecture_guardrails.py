"""
Architecture guardrails for public launch.

Enforces structural invariants established by al-f968, al-18ec, al-58c0:
- No duplicate CLI output helpers (all use core/cli_output.py)
- Command handler modules stay thin (business logic in core/domain modules)
- Hotspot file size thresholds to prevent regression
- Import direction constraints (domain modules do not import from commands)
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest  # type: ignore[import-untyped]

# Project root is 3 levels up from tests/
PROJECT_ROOT = Path(__file__).parent.parent
SRC_ROOT = PROJECT_ROOT / "src" / "agent_loom"
BRANCH_NODES = (
    ast.If,
    ast.For,
    ast.While,
    ast.Try,
    ast.Match,
    ast.BoolOp,
    ast.IfExp,
    ast.With,
    ast.comprehension,
    ast.ExceptHandler,
)


def _max_function_branch_complexity(path: Path) -> tuple[str, int]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    max_name = ""
    max_complexity = 0
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        score = sum(isinstance(sub, BRANCH_NODES) for sub in ast.walk(node))
        if score > max_complexity:
            max_name = node.name
            max_complexity = score
    return max_name, max_complexity


class TestSharedCliOutputContract:
    """Guardrail: All CLIs use shared output helpers from core/cli_output.py."""

    SHARED_MODULE = SRC_ROOT / "core" / "cli_output.py"
    CLI_FILES = [
        SRC_ROOT / "team" / "cli.py",
        SRC_ROOT / "workspace" / "cli.py",
        SRC_ROOT / "ticket" / "cli.py",
        SRC_ROOT / "compound" / "cli.py",
        SRC_ROOT / "pack" / "cli.py",
        SRC_ROOT / "init.py",
    ]

    # Local wrappers are allowed (e.g., team/output.py delegates to core helpers)
    ALLOWED_WRAPPERS = [
        SRC_ROOT / "team" / "output.py",
        SRC_ROOT / "workspace" / "output.py",
        SRC_ROOT / "ticket" / "cli.py",  # local _emit_json wrapper delegates to core helpers
    ]

    def test_shared_output_module_exists(self) -> None:
        """core/cli_output.py must exist and export expected helpers."""
        assert self.SHARED_MODULE.exists(), "core/cli_output.py missing"
        text = self.SHARED_MODULE.read_text(encoding="utf-8")
        assert "normalize_payload" in text
        assert "emit_json" in text
        assert "make_ok_envelope" in text or "ok_envelope" in text

    def test_no_duplicate_output_helpers_in_cli_files(self) -> None:
        """CLI files must not contain duplicate local output helper implementations."""
        # Forbidden patterns: local _payload/_emit_json function definitions
        forbidden_patterns = [
            re.compile(r"^\s*def\s+_payload\s*\(", re.MULTILINE),
            re.compile(r"^\s*def\s+_emit_json\s*\(", re.MULTILINE),
            re.compile(r"^\s*def\s+_normalize\s*\(", re.MULTILINE),
        ]

        for cli_file in self.CLI_FILES:
            if not cli_file.exists():
                continue
            if cli_file in self.ALLOWED_WRAPPERS:
                continue

            text = cli_file.read_text(encoding="utf-8")
            for rx in forbidden_patterns:
                match = rx.search(text)
                assert not match, (
                    f"Duplicate helper {rx.pattern} found in {cli_file.relative_to(PROJECT_ROOT)}. "
                    f"Use core/cli_output.py shared helpers instead."
                )

    def test_wrapper_modules_delegate_to_shared_helpers(self) -> None:
        """Allowed wrapper modules must import from core/cli_output.py."""
        for wrapper in self.ALLOWED_WRAPPERS:
            if not wrapper.exists():
                continue
            text = wrapper.read_text(encoding="utf-8")
            # Must import from core.cli_output
            assert re.search(
                r"from\s+agent_loom\.core\.cli_output\s+import", text
            ) or re.search(r"from\s+\.\.core\.cli_output\s+import", text), (
                f"{wrapper.relative_to(PROJECT_ROOT)} must import from core.cli_output"
            )


class TestCommandHandlerBoundaries:
    """Guardrail: Command handler modules stay thin, delegate to core/domain modules."""

    TEAM_COMMANDS = SRC_ROOT / "team" / "commands"
    WORKSPACE_COMMANDS = SRC_ROOT / "workspace" / "commands"

    # Threshold: command handler files should not exceed 350 lines (allows reasonable complexity)
    MAX_HANDLER_LINES = 350

    def test_team_command_handlers_are_thin(self) -> None:
        """Team command handler modules should not exceed size threshold."""
        if not self.TEAM_COMMANDS.exists():
            pytest.skip("team/commands not found")

        for py_file in self.TEAM_COMMANDS.glob("*.py"):
            if py_file.name == "__init__.py":
                continue
            lines = len(py_file.read_text(encoding="utf-8").splitlines())
            assert lines <= self.MAX_HANDLER_LINES, (
                f"{py_file.relative_to(PROJECT_ROOT)} has {lines} lines (max {self.MAX_HANDLER_LINES}). "
                f"Extract business logic to team/core.py or domain modules."
            )

    def test_workspace_command_handlers_are_thin(self) -> None:
        """Workspace command handler modules should not exceed size threshold."""
        if not self.WORKSPACE_COMMANDS.exists():
            pytest.skip("workspace/commands not found")

        for py_file in self.WORKSPACE_COMMANDS.glob("*.py"):
            if py_file.name == "__init__.py":
                continue
            lines = len(py_file.read_text(encoding="utf-8").splitlines())
            assert lines <= self.MAX_HANDLER_LINES, (
                f"{py_file.relative_to(PROJECT_ROOT)} has {lines} lines (max {self.MAX_HANDLER_LINES}). "
                f"Extract business logic to workspace/core.py or domain modules."
            )


class TestHotspotSizeControl:
    """Guardrail: Known hotspot files must not regrow uncontrolled."""

    HOTSPOTS = {
        # team/core.py is being decomposed; monitor for growth
        SRC_ROOT / "team" / "core.py": {
            "max_lines": 6900,  # Current ~6728
            "description": "team/core.py (decomposition in progress)",
        },
        SRC_ROOT / "memory" / "cli.py": {
            "max_lines": 140,  # Public shim should remain thin.
            "description": "memory/cli.py (public shim)",
        },
        SRC_ROOT / "memory" / "cli_runtime.py": {
            "max_lines": 140,  # Public runtime entrypoint should remain thin.
            "description": "memory/cli_runtime.py (runtime entrypoint)",
        },
        SRC_ROOT / "memory" / "cli_handlers.py": {
            "max_lines": 440,  # Current ~363
            "description": "memory/cli_handlers.py (command dispatch hotspot)",
        },
        SRC_ROOT / "memory" / "cli_parser.py": {
            "max_lines": 1100,  # Current ~994
            "description": "memory/cli_parser.py (parser hotspot)",
        },
        SRC_ROOT / "memory" / "cli_output.py": {
            "max_lines": 260,  # Current ~196
            "description": "memory/cli_output.py (output/payload hotspot)",
        },
        SRC_ROOT / "memory" / "cli_edit_options.py": {
            "max_lines": 280,  # Current ~211
            "description": "memory/cli_edit_options.py (edit option hotspot)",
        },
        SRC_ROOT / "workspace" / "cli_harness.py": {
            "max_lines": 120,  # Public shim should remain thin.
            "description": "workspace/cli_harness.py (public shim)",
        },
        SRC_ROOT / "workspace" / "cli_harness_groups.py": {
            "max_lines": 900,  # Current ~740
            "description": "workspace/cli_harness_groups.py (parser hotspot)",
        },
        SRC_ROOT / "dashboard" / "app.py": {
            "max_lines": 160,  # Public composition root should remain thin.
            "description": "dashboard/app.py (composition root)",
        },
        SRC_ROOT / "dashboard" / "blueprints" / "team.py": {
            "max_lines": 280,  # Current ~229
            "description": "dashboard/blueprints/team.py (team API hotspot)",
        },
        SRC_ROOT / "dashboard" / "blueprints" / "tickets.py": {
            "max_lines": 220,  # Current ~170
            "description": "dashboard/blueprints/tickets.py (tickets API hotspot)",
        },
        SRC_ROOT / "dashboard" / "blueprints" / "workspace.py": {
            "max_lines": 190,  # Current ~137
            "description": "dashboard/blueprints/workspace.py (workspace API hotspot)",
        },
        SRC_ROOT / "workspace" / "render.py": {
            "max_lines": 120,  # Public shim should remain thin.
            "description": "workspace/render.py (public shim)",
        },
        SRC_ROOT / "workspace" / "render_text.py": {
            "max_lines": 760,  # Current ~669
            "description": "workspace/render_text.py (text rendering hotspot)",
        },
        SRC_ROOT / "ticket" / "core.py": {
            "max_lines": 1850,  # Current ~1744
            "description": "ticket/core.py (ticket workflow hotspot)",
        },
        SRC_ROOT / "compound" / "cli.py": {
            "max_lines": 720,  # Current ~658
            "description": "compound/cli.py (command dispatch hotspot)",
        },
    }

    def test_hotspot_files_within_size_threshold(self) -> None:
        """Hotspot files must not exceed documented size thresholds."""
        for path, config in self.HOTSPOTS.items():
            if not path.exists():
                continue

            lines = len(path.read_text(encoding="utf-8").splitlines())
            max_lines = config["max_lines"]
            desc = config["description"]

            assert lines <= max_lines, (
                f"{desc} has {lines} lines (max {max_lines}). "
                f"Extract functionality to domain modules to stay under threshold."
            )


class TestHotspotComplexityControl:
    """Guardrail: hotspot modules must not exceed max function branch complexity."""

    HOTSPOT_COMPLEXITY = {
        SRC_ROOT / "team" / "core.py": {
            "max_function_branch_nodes": 175,  # Current max: tui ~=163
            "description": "team/core.py sidecar lifecycle complexity",
        },
        SRC_ROOT / "memory" / "cli.py": {
            "max_function_branch_nodes": 2,  # Public shim should not branch.
            "description": "memory/cli.py shim complexity",
        },
        SRC_ROOT / "memory" / "cli_runtime.py": {
            "max_function_branch_nodes": 20,  # Current max: main ~=14
            "description": "memory/cli_runtime.py runtime entrypoint complexity",
        },
        SRC_ROOT / "memory" / "cli_handlers.py": {
            "max_function_branch_nodes": 15,  # Current max: _run_add ~=7
            "description": "memory/cli_handlers.py command dispatch complexity",
        },
        SRC_ROOT / "memory" / "cli_parser.py": {
            "max_function_branch_nodes": 35,  # Current max: _normalize_argv ~=30
            "description": "memory/cli_parser.py parser complexity",
        },
        SRC_ROOT / "memory" / "cli_output.py": {
            "max_function_branch_nodes": 40,  # Current max: payload_for ~=35
            "description": "memory/cli_output.py output mapping complexity",
        },
        SRC_ROOT / "memory" / "cli_edit_options.py": {
            "max_function_branch_nodes": 40,  # Current max: _build_edit_options ~=35
            "description": "memory/cli_edit_options.py edit option complexity",
        },
        SRC_ROOT / "workspace" / "cli_harness.py": {
            "max_function_branch_nodes": 2,  # Public shim should not branch.
            "description": "workspace/cli_harness.py shim complexity",
        },
        SRC_ROOT / "workspace" / "cli_harness_groups.py": {
            "max_function_branch_nodes": 12,  # Current max ~=1
            "description": "workspace/cli_harness_groups.py parser complexity",
        },
        SRC_ROOT / "dashboard" / "app.py": {
            "max_function_branch_nodes": 20,  # Current max: create_app ~=10
            "description": "dashboard/app.py composition complexity",
        },
        SRC_ROOT / "dashboard" / "blueprints" / "team.py": {
            "max_function_branch_nodes": 65,  # Current max: create_team_blueprint ~=55
            "description": "dashboard/blueprints/team.py request handling complexity",
        },
        SRC_ROOT / "dashboard" / "blueprints" / "tickets.py": {
            "max_function_branch_nodes": 50,  # Current max: create_tickets_blueprint ~=42
            "description": "dashboard/blueprints/tickets.py request handling complexity",
        },
        SRC_ROOT / "dashboard" / "blueprints" / "workspace.py": {
            "max_function_branch_nodes": 45,  # Current max: create_workspace_blueprint ~=35
            "description": "dashboard/blueprints/workspace.py request handling complexity",
        },
        SRC_ROOT / "workspace" / "render.py": {
            "max_function_branch_nodes": 2,  # Public shim should not branch.
            "description": "workspace/render.py shim complexity",
        },
        SRC_ROOT / "workspace" / "render_text.py": {
            "max_function_branch_nodes": 40,  # Current max: _render_worktree_group_diff ~=17
            "description": "workspace/render_text.py text rendering complexity",
        },
        SRC_ROOT / "ticket" / "core.py": {
            "max_function_branch_nodes": 95,  # Current max: update ~=86
            "description": "ticket/core.py update workflow complexity",
        },
        SRC_ROOT / "compound" / "cli.py": {
            "max_function_branch_nodes": 30,  # Current max: _handle_init ~=14
            "description": "compound/cli.py command routing complexity",
        },
    }

    def test_hotspot_max_function_complexity(self) -> None:
        for path, config in self.HOTSPOT_COMPLEXITY.items():
            if not path.exists():
                continue
            fn_name, score = _max_function_branch_complexity(path)
            max_score = int(config["max_function_branch_nodes"])
            desc = str(config["description"])
            assert score <= max_score, (
                f"{desc} has function `{fn_name}` complexity={score} "
                f"(max {max_score}). Extract branches into dedicated helpers."
            )


class TestImportDirection:
    """Guardrail: Domain modules must not import from command handler modules."""

    TEAM_COMMANDS = SRC_ROOT / "team" / "commands"
    WORKSPACE_COMMANDS = SRC_ROOT / "workspace" / "commands"

    TEAM_CORE_MODULES = [
        SRC_ROOT / "team" / "core.py",
        SRC_ROOT / "team" / "permissions.py",
        SRC_ROOT / "team" / "utilities.py",
        SRC_ROOT / "team" / "inbox.py",
        SRC_ROOT / "team" / "merge_queue.py",
        SRC_ROOT / "team" / "models.py",
        SRC_ROOT / "team" / "output.py",
        SRC_ROOT / "team" / "start_state.py",
    ]

    WORKSPACE_CORE_MODULES = [
        SRC_ROOT / "workspace" / "core.py",
        SRC_ROOT / "workspace" / "models.py",
        SRC_ROOT / "workspace" / "state.py",
        SRC_ROOT / "workspace" / "guards.py",
        SRC_ROOT / "workspace" / "utils.py",
    ]

    def _check_no_command_imports(self, module_path: Path) -> None:
        """Check that a module does not import from commands/ directory."""
        if not module_path.exists():
            return

        text = module_path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(module_path))

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.module and ".commands." in node.module:
                    pytest.fail(
                        f"{module_path.relative_to(PROJECT_ROOT)} imports from command handler module: {node.module}. "
                        f"Import direction violation: domain modules must not import from commands."
                    )

    def test_team_core_modules_do_not_import_from_commands(self) -> None:
        """Team domain modules must not import from team/commands/."""
        for module in self.TEAM_CORE_MODULES:
            self._check_no_command_imports(module)

    def test_workspace_core_modules_do_not_import_from_commands(self) -> None:
        """Workspace domain modules must not import from workspace/commands/."""
        for module in self.WORKSPACE_CORE_MODULES:
            self._check_no_command_imports(module)


class TestTeamDecompositionBoundaries:
    """Guardrails for Team decomposition parity and layering boundaries."""

    TEAM_CORE = SRC_ROOT / "team" / "core.py"
    TEAM_COMMANDS = SRC_ROOT / "team" / "commands"

    @staticmethod
    def _parse_module(path: Path) -> ast.Module:
        return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    @staticmethod
    def _function_call_names(tree: ast.Module, function_name: str) -> set[str]:
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name == function_name:
                names: set[str] = set()
                for sub in ast.walk(node):
                    if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name):
                        names.add(sub.func.id)
                return names
        raise AssertionError(f"Function not found: {function_name}")

    def test_team_core_key_commands_delegate_to_extracted_modules(self) -> None:
        tree = self._parse_module(self.TEAM_CORE)

        expected_calls = {
            "objective_set": {
                "_objective_state_read_text_input",
                "_objective_state_apply_objective_mutation",
            },
            "objective_append": {
                "_objective_state_read_text_input",
                "_objective_state_apply_objective_mutation",
            },
            "spawn": {
                "_max_headcount",
                "_active_spawn_headcount",
                "_agent_for_role",
                "_model_for_role",
            },
            "send": {
                "sender_for_send",
                "resolve_send_target",
                "communication_policy_from_run",
                "route_allows_target",
                "delivery_suggestions",
            },
            "wait": {
                "wait_for_wake",
                "_maybe_manager_checkin_after_wait",
            },
        }

        for function_name, required in expected_calls.items():
            calls = self._function_call_names(tree, function_name)
            missing = sorted(name for name in required if name not in calls)
            assert not missing, (
                f"{self.TEAM_CORE.relative_to(PROJECT_ROOT)}::{function_name} "
                f"missing delegation calls: {missing}"
            )

    def test_team_commands_do_not_import_team_cli_or_other_command_modules(self) -> None:
        for module_path in sorted(self.TEAM_COMMANDS.glob("*.py")):
            if module_path.name == "__init__.py":
                continue

            tree = self._parse_module(module_path)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        name = str(alias.name or "")
                        assert not name.startswith("agent_loom.team.cli"), (
                            f"{module_path.relative_to(PROJECT_ROOT)} imports team.cli; "
                            "command handlers must depend on core/domain modules only."
                        )
                        assert not name.startswith("agent_loom.team.commands."), (
                            f"{module_path.relative_to(PROJECT_ROOT)} imports another command module ({name}); "
                            "no command->command imports allowed."
                        )
                if isinstance(node, ast.ImportFrom):
                    name = str(node.module or "")
                    assert name not in {"agent_loom.team.cli", ".cli"}, (
                        f"{module_path.relative_to(PROJECT_ROOT)} imports team.cli; "
                        "command handlers must depend on core/domain modules only."
                    )
                    assert not name.startswith("agent_loom.team.commands"), (
                        f"{module_path.relative_to(PROJECT_ROOT)} imports another command module ({name}); "
                        "no command->command imports allowed."
                    )


class TestModuleBoundaryDocumentation:
    """Guardrail: Module README architecture sections exist and are non-trivial."""

    READMES = [
        SRC_ROOT / "team" / "README.md",
        SRC_ROOT / "workspace" / "README.md",
    ]

    def test_readmes_contain_architecture_sections(self) -> None:
        """Module READMEs must document architecture boundaries."""
        for readme in self.READMES:
            assert readme.exists(), f"{readme.relative_to(PROJECT_ROOT)} missing"

            text = readme.read_text(encoding="utf-8")

            # Must contain "Module architecture" or "Architecture" section
            assert re.search(
                r"##\s+Module\s+architecture", text, re.IGNORECASE
            ) or re.search(r"##\s+Architecture", text, re.IGNORECASE), (
                f"{readme.relative_to(PROJECT_ROOT)} missing architecture section"
            )

            # Must mention boundaries/guardrails
            assert (
                "boundaries" in text.lower() or "guardrails" in text.lower()
            ), f"{readme.relative_to(PROJECT_ROOT)} must document boundaries or guardrails"

            # Must mention shared output helpers
            assert (
                "cli_output" in text or "shared output" in text.lower()
            ), f"{readme.relative_to(PROJECT_ROOT)} must document shared output contract"
