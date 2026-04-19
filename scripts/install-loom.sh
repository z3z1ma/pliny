#!/usr/bin/env bash

set -euo pipefail

action="${1:?missing action}"
harness="${2:-all}"
root="${ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
python_bin="${PYTHON_BIN:-python3}"
home_dir="${HOME:?missing HOME}"

case "$action" in
  install|uninstall) ;;
  *)
    printf 'Unsupported action: %s\n' "$action" >&2
    exit 1
    ;;
esac

case "$harness" in
  all|opencode|claude|codex|gemini) ;;
  *)
    printf 'Unsupported harness: %s\n' "$harness" >&2
    printf 'Supported values: all, opencode, claude, codex, gemini\n' >&2
    exit 1
    ;;
esac

copy_rules() {
  local src_dir="$1"
  local dest_dir="$2"
  mkdir -p "$dest_dir"
  local file
  for file in "$src_dir"/*.md; do
    [ -f "$file" ] || continue
    cp "$file" "$dest_dir/${file##*/}"
  done
}

remove_rules() {
  local src_dir="$1"
  local dest_dir="$2"
  local file
  for file in "$src_dir"/*.md; do
    [ -f "$file" ] || continue
    rm -f "$dest_dir/${file##*/}"
  done
  rmdir "$dest_dir" 2>/dev/null || true
}

copy_skill_dirs() {
  local src_dir="$1"
  local dest_dir="$2"
  mkdir -p "$dest_dir"
  local dir name
  for dir in "$src_dir"/*; do
    [ -d "$dir" ] || continue
    name="${dir##*/}"
    rm -rf "$dest_dir/$name"
    cp -R "$dir" "$dest_dir/$name"
  done
}

remove_skill_dirs() {
  local src_dir="$1"
  local dest_dir="$2"
  local dir name
  for dir in "$src_dir"/*; do
    [ -d "$dir" ] || continue
    name="${dir##*/}"
    rm -rf "$dest_dir/$name"
  done
  rmdir "$dest_dir" 2>/dev/null || true
}

copy_command_markdown() {
  local src_dir="$1"
  local dest_dir="$2"
  mkdir -p "$dest_dir"
  local file
  for file in "$src_dir"/*.md; do
    [ -f "$file" ] || continue
    cp "$file" "$dest_dir/${file##*/}"
  done
}

remove_command_markdown() {
  local src_dir="$1"
  local dest_dir="$2"
  local file
  for file in "$src_dir"/*.md; do
    [ -f "$file" ] || continue
    rm -f "$dest_dir/${file##*/}"
  done
  rmdir "$dest_dir" 2>/dev/null || true
}

upsert_managed_block() {
  local file_path="$1"
  local block_name="$2"
  local harness_name="$3"
  local rules_dir="$4"
  local skills_dir="$5"
  local commands_dir="$6"
  local extra_note="$7"
  mkdir -p "$(dirname "$file_path")"
  "$python_bin" - "$file_path" "$block_name" "$harness_name" "$rules_dir" "$skills_dir" "$commands_dir" "$extra_note" <<'PY'
from pathlib import Path
import re
import sys

file_path = Path(sys.argv[1]).expanduser()
block_name = sys.argv[2]
harness_name = sys.argv[3]
rules_dir = Path(sys.argv[4]).expanduser()
skills_dir = Path(sys.argv[5]).expanduser()
commands_dir = Path(sys.argv[6]).expanduser()
extra_note = sys.argv[7].strip()

begin = f"<!-- BEGIN {block_name} -->"
end = f"<!-- END {block_name} -->"

parts = [
    f"## Loom Global Install ({harness_name})",
    "",
    "This block is managed by the Loom bundle's `make install` target.",
    f"Rules directory: `{rules_dir}`.",
    f"Skills directory: `{skills_dir}`.",
    f"Command surface directory: `{commands_dir}`.",
]

if extra_note:
    parts.extend(["", extra_note])

for rule_path in sorted(rules_dir.glob("*.md")):
    parts.extend(["", f"<!-- source: {rule_path.name} -->", "", rule_path.read_text().rstrip()])

block = begin + "\n\n" + "\n".join(parts).rstrip() + "\n\n" + end + "\n"

existing = file_path.read_text() if file_path.exists() else ""
pattern = re.compile(re.escape(begin) + r".*?" + re.escape(end) + r"\n?", re.S)

if pattern.search(existing):
    updated = pattern.sub(block, existing, count=1)
else:
    if existing and not existing.endswith("\n"):
        existing += "\n"
    separator = "\n\n" if existing.strip() else ""
    updated = existing.rstrip() + separator + block

file_path.write_text(updated)
PY
}

remove_managed_block() {
  local file_path="$1"
  local block_name="$2"
  [ -f "$file_path" ] || return 0
  "$python_bin" - "$file_path" "$block_name" <<'PY'
from pathlib import Path
import re
import sys

file_path = Path(sys.argv[1]).expanduser()
block_name = sys.argv[2]
begin = f"<!-- BEGIN {block_name} -->"
end = f"<!-- END {block_name} -->"
pattern = re.compile(r"\n?" + re.escape(begin) + r".*?" + re.escape(end) + r"\n?", re.S)

text = file_path.read_text()
updated = pattern.sub("\n", text).strip()

if updated:
    file_path.write_text(updated + "\n")
else:
    file_path.unlink()
PY
}

adapt_commands() {
  local mode="$1"
  local src_dir="$2"
  local dest_dir="$3"
  mkdir -p "$dest_dir"
  "$python_bin" - "$mode" "$src_dir" "$dest_dir" <<'PY'
from pathlib import Path
import json
import re
import shutil
import sys

mode = sys.argv[1]
src_dir = Path(sys.argv[2]).expanduser()
dest_dir = Path(sys.argv[3]).expanduser()

def parse_command(path: Path):
    text = path.read_text()
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    frontmatter = {}
    body = text
    if match:
        raw_frontmatter, body = match.groups()
        for line in raw_frontmatter.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("-") or ":" not in stripped:
                continue
            key, value = stripped.split(":", 1)
            frontmatter[key.strip()] = value.strip().strip('"').strip("'")
    return {
        "name": frontmatter.get("name", path.stem),
        "description": frontmatter.get("description", path.stem.replace("-", " ")),
        "arguments": frontmatter.get("arguments", ""),
        "body": body.lstrip(),
    }

def codex_command_skill_name(command_name: str) -> str:
    if command_name.startswith("loom-"):
        return "loom-command-" + command_name[len("loom-"):]
    return command_name + "-command"

def yaml_scalar(value: str) -> str:
    return json.dumps(value)

def adapt_codex_command_body(body: str, source_name: str) -> str:
    adapted = body.replace("`$ARGUMENTS`", "`<invocation request>`")
    adapted = adapted.replace("$ARGUMENTS", "the invocation request")
    adapted = re.sub(
        r"/(loom-[a-z0-9-]+)",
        lambda match: "$" + codex_command_skill_name(match.group(1)),
        adapted,
    )
    adapted = re.sub(
        r"^#\s+\$" + re.escape(codex_command_skill_name(source_name)) + r"\s*\n+",
        "",
        adapted,
        count=1,
        flags=re.M,
    )
    return adapted.strip()

for path in sorted(src_dir.glob("*.md")):
    data = parse_command(path)
    name = data["name"]
    description = data["description"]
    arguments = data["arguments"]
    body = data["body"].rstrip() + "\n"

    if mode == "codex-skill":
        skill_name = codex_command_skill_name(name)
        skill_dir = dest_dir / skill_name
        if skill_dir.exists():
            shutil.rmtree(skill_dir)
        (skill_dir / "agents").mkdir(parents=True)

        skill_description = (
            f"Explicit user-invoked Loom command adapter for /{name}. "
            f"Invoke as ${skill_name}; implicit invocation is disabled."
        )
        adapted_body = adapt_codex_command_body(body, name)
        argument_note = arguments or "No formal argument hint was declared."

        skill_content = "\n".join([
            "---",
            f"name: {skill_name}",
            f"description: {yaml_scalar(skill_description)}",
            "metadata:",
            "  loom_command_adapter: true",
            f"  loom_source_command: {yaml_scalar(name)}",
            f"  loom_command_arguments: {yaml_scalar(arguments)}",
            "---",
            "",
            f"# ${skill_name}",
            "",
            f"This skill is the Codex command adapter for `/{name}`.",
            "",
            "Use the user's current request, including any text after the skill mention, as `<invocation request>`.",
            f"Original argument hint: `{argument_note}`",
            "",
            "Run this workflow only when the user explicitly invokes this skill or asks for this exact command adapter.",
            "",
            adapted_body,
            "",
        ])
        (skill_dir / "SKILL.md").write_text(skill_content)

        openai_yaml = "\n".join([
            "interface:",
            f"  display_name: {yaml_scalar('/' + name)}",
            f"  short_description: {yaml_scalar(description)}",
            f"  default_prompt: {yaml_scalar('$' + skill_name + ' ')}",
            "policy:",
            "  allow_implicit_invocation: false",
            "",
        ])
        (skill_dir / "agents" / "openai.yaml").write_text(openai_yaml)
    elif mode == "gemini-command":
        prompt = body.replace("$ARGUMENTS", "{{args}}")
        content = "\n".join([
            f'description = "{description.replace(chr(34), chr(92) + chr(34))}"',
            'prompt = """',
            prompt.rstrip(),
            '"""',
            "",
        ])
        (dest_dir / f"{name}.toml").write_text(content)
    else:
        raise SystemExit(f"Unsupported adapter mode: {mode}")
PY
}

remove_codex_prompts() {
  local src_dir="$1"
  local dest_dir="$2"
  local file name
  for file in "$src_dir"/*.md; do
    [ -f "$file" ] || continue
    name="${file##*/}"
    name="${name%.md}"
    rm -f "$dest_dir/$name.md"
  done
  rmdir "$dest_dir" 2>/dev/null || true
}

remove_codex_command_skills() {
  local src_dir="$1"
  local dest_dir="$2"
  local file name suffix skill_name
  for file in "$src_dir"/*.md; do
    [ -f "$file" ] || continue
    name="${file##*/}"
    name="${name%.md}"
    if [[ "$name" == loom-* ]]; then
      suffix="${name#loom-}"
      skill_name="loom-command-$suffix"
    else
      skill_name="$name-command"
    fi
    rm -rf "$dest_dir/$skill_name"
  done
  rmdir "$dest_dir" 2>/dev/null || true
}

remove_gemini_commands() {
  local src_dir="$1"
  local dest_dir="$2"
  local file name
  for file in "$src_dir"/*.md; do
    [ -f "$file" ] || continue
    name="${file##*/}"
    name="${name%.md}"
    rm -f "$dest_dir/$name.toml"
  done
  rmdir "$dest_dir" 2>/dev/null || true
}

update_opencode_config() {
  local config_path="$1"
  local rules_glob="$2"
  local mode="$3"
  mkdir -p "$(dirname "$config_path")"
  "$python_bin" - "$config_path" "$rules_glob" "$mode" <<'PY'
from pathlib import Path
import json
import re
import sys

config_path = Path(sys.argv[1]).expanduser()
rules_glob = sys.argv[2]
mode = sys.argv[3]

def load_jsonc(path: Path):
    if not path.exists():
        return {}
    raw = path.read_text()
    if not raw.strip():
        return {}
    stripped = re.sub(r"/\*.*?\*/", "", raw, flags=re.S)
    stripped = re.sub(r"^\s*//.*$", "", stripped, flags=re.M)
    return json.loads(stripped)

data = load_jsonc(config_path)
if not isinstance(data, dict):
    raise SystemExit(f"Expected JSON object in {config_path}")

instructions = data.get("instructions", [])
if isinstance(instructions, str):
    instructions = [instructions]
if not isinstance(instructions, list):
    raise SystemExit(f"Expected 'instructions' to be a list in {config_path}")

if mode == "install":
    if rules_glob not in instructions:
        instructions.append(rules_glob)
    data.setdefault("$schema", "https://opencode.ai/config.json")
elif mode == "uninstall":
    instructions = [item for item in instructions if item != rules_glob]
else:
    raise SystemExit(f"Unsupported mode: {mode}")

data["instructions"] = instructions
config_path.write_text(json.dumps(data, indent=2) + "\n")
PY
}

handle_opencode() {
  local base="$home_dir/.config/opencode"
  local rules_dir="$base/loom/rules"
  local skills_dir="$base/skills"
  local commands_dir="$base/commands"
  local rules_glob="$rules_dir/*.md"

  if [ "$action" = "install" ]; then
    copy_rules "$root/rules" "$rules_dir"
    copy_skill_dirs "$root/skills" "$skills_dir"
    copy_command_markdown "$root/commands" "$commands_dir"
    update_opencode_config "$base/opencode.json" "$rules_glob" install
    printf 'Installed Loom for OpenCode in %s\n' "$base"
  else
    remove_command_markdown "$root/commands" "$commands_dir"
    remove_skill_dirs "$root/skills" "$skills_dir"
    remove_rules "$root/rules" "$rules_dir"
    update_opencode_config "$base/opencode.json" "$rules_glob" uninstall
    printf 'Uninstalled Loom from OpenCode in %s\n' "$base"
  fi
}

handle_claude() {
  local base="$home_dir/.claude"
  local rules_dir="$base/rules/loom"
  local skills_dir="$base/skills"
  local commands_dir="$base/commands"

  if [ "$action" = "install" ]; then
    copy_rules "$root/rules" "$rules_dir"
    copy_skill_dirs "$root/skills" "$skills_dir"
    copy_command_markdown "$root/commands" "$commands_dir"
    printf 'Installed Loom for Claude Code in %s\n' "$base"
  else
    remove_command_markdown "$root/commands" "$commands_dir"
    remove_skill_dirs "$root/skills" "$skills_dir"
    remove_rules "$root/rules" "$rules_dir"
    printf 'Uninstalled Loom from Claude Code in %s\n' "$base"
  fi
}

handle_codex() {
  local base="$home_dir/.codex"
  local rules_dir="$base/loom/rules"
  local skills_dir="$home_dir/.agents/skills"
  local prompts_dir="$base/prompts"
  local block_name="LOOM CODEX RULES"

  if [ "$action" = "install" ]; then
    copy_rules "$root/rules" "$rules_dir"
    copy_skill_dirs "$root/skills" "$skills_dir"
    remove_codex_prompts "$root/commands" "$prompts_dir"
    adapt_commands "codex-skill" "$root/commands" "$skills_dir"
    upsert_managed_block "$base/AGENTS.md" "$block_name" "Codex" "$rules_dir" "$skills_dir" "$skills_dir" "Codex loads global instructions from ~/.codex/AGENTS.md and global skills from ~/.agents/skills/. Loom command wrappers are installed as explicit-only command adapter skills under ~/.agents/skills/loom-command-* with Codex implicit invocation disabled via agents/openai.yaml. Loom rules are mirrored into this managed block because Codex's ~/.codex/rules/ surface is for shell execution policy, not Markdown instructions."
    printf 'Installed Loom for Codex in %s and %s\n' "$base" "$skills_dir"
  else
    remove_codex_command_skills "$root/commands" "$skills_dir"
    remove_codex_prompts "$root/commands" "$prompts_dir"
    remove_skill_dirs "$root/skills" "$skills_dir"
    remove_rules "$root/rules" "$rules_dir"
    remove_managed_block "$base/AGENTS.md" "$block_name"
    printf 'Uninstalled Loom from Codex in %s and %s\n' "$base" "$skills_dir"
  fi
}

handle_gemini() {
  local base="$home_dir/.gemini"
  local rules_dir="$base/loom/rules"
  local skills_dir="$base/skills"
  local commands_dir="$base/commands"
  local block_name="LOOM GEMINI RULES"

  if [ "$action" = "install" ]; then
    copy_rules "$root/rules" "$rules_dir"
    copy_skill_dirs "$root/skills" "$skills_dir"
    adapt_commands "gemini-command" "$root/commands" "$commands_dir"
    upsert_managed_block "$base/GEMINI.md" "$block_name" "Gemini CLI" "$rules_dir" "$skills_dir" "$commands_dir" "Gemini CLI loads global instructions from ~/.gemini/GEMINI.md, global skills from ~/.gemini/skills/, and global custom slash commands from ~/.gemini/commands/*.toml."
    printf 'Installed Loom for Gemini CLI in %s\n' "$base"
  else
    remove_gemini_commands "$root/commands" "$commands_dir"
    remove_skill_dirs "$root/skills" "$skills_dir"
    remove_rules "$root/rules" "$rules_dir"
    remove_managed_block "$base/GEMINI.md" "$block_name"
    printf 'Uninstalled Loom from Gemini CLI in %s\n' "$base"
  fi
}

case "$harness" in
  all)
    handle_opencode
    handle_claude
    handle_codex
    handle_gemini
    ;;
  opencode) handle_opencode ;;
  claude) handle_claude ;;
  codex) handle_codex ;;
  gemini) handle_gemini ;;
esac
