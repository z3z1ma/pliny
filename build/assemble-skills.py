#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parent.parent
SHARED_PACKAGE = WORKSPACE / "build/shared/_loom_lib"
SHARED_SCRIPTS = WORKSPACE / "build/shared/scripts"

MANAGED_SHARED_SCRIPT_NAMES = {
    "rebuild_memory_link_index.py",
    "rebuild_memory_glacier_index.py",
    "scan_memory_l0.py",
    "check_links.py",
    "compile_packet.py",
    "create_verification.py",
    "diagnose_workspace.py",
    "link_records.py",
    "list_records.py",
    "resolve_scope.py",
    "show_status.py",
    "validate_memory_module.py",
    "validate_record.py",
}

LEGACY_SHARED_SCRIPT_NAMES = {
    "doctor.py",
    "init_workspace.py",
    "link_refs.py",
    "new_verification.py",
    "scope_scan.py",
    "status.py",
}

SKILL_SCRIPTS = {
    "loom-constitution": [
        "link_records.py",
        "validate_record.py",
    ],
    "loom-research": [
        "link_records.py",
        "validate_record.py",
    ],
    "loom-initiatives": [
        "link_records.py",
        "validate_record.py",
    ],
    "loom-specs": [
        "link_records.py",
        "validate_record.py",
    ],
    "loom-plans": [
        "link_records.py",
        "validate_record.py",
    ],
    "loom-tickets": [
        "link_records.py",
        "create_verification.py",
        "validate_record.py",
        "check_links.py",
        "resolve_scope.py",
    ],
    "loom-ralph": [
        "compile_packet.py",
        "create_verification.py",
        "validate_record.py",
        "check_links.py",
        "resolve_scope.py",
    ],
    "loom-critique": [
        "compile_packet.py",
        "link_records.py",
        "create_verification.py",
        "validate_record.py",
        "check_links.py",
        "resolve_scope.py",
    ],
    "loom-docs": [
        "compile_packet.py",
        "link_records.py",
        "create_verification.py",
        "validate_record.py",
        "check_links.py",
        "resolve_scope.py",
    ],
    "loom-workspace": [
        "show_status.py",
        "diagnose_workspace.py",
        "list_records.py",
        "validate_record.py",
        "check_links.py",
        "resolve_scope.py",
    ],
    "loom-memory-context": [
        "scan_memory_l0.py",
        "validate_memory_module.py",
    ],
    "loom-memory-reflect": [
        "scan_memory_l0.py",
        "validate_memory_module.py",
    ],
    "loom-memory-housekeeping": [
        "rebuild_memory_glacier_index.py",
        "rebuild_memory_link_index.py",
        "scan_memory_l0.py",
        "validate_memory_module.py",
    ],
}


def utc_now() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def validate_skill_frontmatter(skill_dir: Path) -> dict:
    text = (skill_dir / "SKILL.md").read_text()
    lines = text.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        raise SystemExit(f"{skill_dir.name} SKILL.md missing YAML frontmatter")
    closing = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            closing = index
            break
    if closing is None:
        raise SystemExit(f"{skill_dir.name} SKILL.md missing closing frontmatter fence")

    top_level: dict[str, str] = {}
    for line in lines[1:closing]:
        if not line or line.startswith(" ") or line.startswith("\t"):
            continue
        match = re.match(r"^([a-z0-9-]+):\s*(.*)$", line)
        if match:
            top_level[match.group(1)] = match.group(2).strip()

    name = top_level.get("name")
    description = top_level.get("description")
    if not name:
        raise SystemExit(
            f"{skill_dir.name} SKILL.md missing required frontmatter field: name"
        )
    if name != skill_dir.name:
        raise SystemExit(f"{skill_dir.name} SKILL.md name must match directory name")
    if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", name):
        raise SystemExit(f"{skill_dir.name} SKILL.md has invalid skill name format")
    if not description:
        raise SystemExit(
            f"{skill_dir.name} SKILL.md missing required frontmatter field: description"
        )
    if len(description) > 1024:
        raise SystemExit(
            f"{skill_dir.name} SKILL.md description exceeds 1024 characters"
        )
    if "Use when" not in description:
        raise SystemExit(
            f"{skill_dir.name} SKILL.md description must include 'Use when' guidance"
        )
    if "Not for" not in description:
        raise SystemExit(
            f"{skill_dir.name} SKILL.md description must include 'Not for' guidance"
        )
    return {"name": name, "description": description}


def copy_scripts(skill_dir: Path, script_names: list[str]) -> None:
    scripts_dir = skill_dir / "scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    managed_paths = []
    local_scripts = list(scripts_dir.glob("*.py"))
    if script_names or local_scripts:
        shutil.rmtree(scripts_dir / "loom_helpers", ignore_errors=True)
        destination_pkg = scripts_dir / "_loom_lib"
        shutil.copytree(SHARED_PACKAGE, destination_pkg, dirs_exist_ok=True)
        managed_paths.append(destination_pkg)
        for stale_name in MANAGED_SHARED_SCRIPT_NAMES | LEGACY_SHARED_SCRIPT_NAMES:
            stale_path = scripts_dir / stale_name
            if stale_path.exists():
                stale_path.unlink()
    for script_name in script_names:
        source = SHARED_SCRIPTS / script_name
        if not source.exists():
            raise SystemExit(f"Missing shared script source: {source}")
        destination = scripts_dir / script_name
        shutil.copy2(source, destination)
        destination.chmod(0o755)
        managed_paths.append(destination)


def build_manifest() -> dict:
    skills_root = WORKSPACE / "src/skills"
    manifest = {
        "built_at": utc_now(),
        "workspace": str(WORKSPACE),
        "skills": {},
    }
    for skill_name, scripts in SKILL_SCRIPTS.items():
        skill_dir = skills_root / skill_name
        if not skill_dir.exists():
            raise SystemExit(f"Missing skill directory: {skill_dir}")
        if not (skill_dir / "SKILL.md").exists():
            raise SystemExit(f"Missing SKILL.md for {skill_name}")
        frontmatter = validate_skill_frontmatter(skill_dir)
        references = sorted(
            str(path.relative_to(skill_dir))
            for path in (skill_dir / "references").rglob("*.md")
        )
        copy_scripts(skill_dir, scripts)
        scripts = sorted(path.name for path in (skill_dir / "scripts").glob("*.py"))
        manifest["skills"][skill_name] = {
            "description": frontmatter["description"],
            "references": references,
            "scripts": scripts,
        }
    return manifest


def main() -> int:
    manifest = build_manifest()
    output = WORKSPACE / "build/manifest.json"
    output.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(output.relative_to(WORKSPACE))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
