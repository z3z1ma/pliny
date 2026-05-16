#!/usr/bin/env bash
# Test explicit Loom skill requests and fail when non-skill tools run first.
# Usage: bash tests/explicit-skill-requests/run-test.sh <skill-name> <prompt-file> [max-turns]
# Parser probe: bash tests/explicit-skill-requests/run-test.sh <skill-name> --check-log <log-file>

set -euo pipefail

SKILL_NAME="${1:-}"
PROMPT_FILE="${2:-}"
MAX_TURNS="${3:-3}"

if [[ -z "$SKILL_NAME" || -z "$PROMPT_FILE" ]]; then
  echo "Usage: $0 <skill-name> <prompt-file> [max-turns]" >&2
  exit 2
fi

SKILL_TOOL_PATTERN='"tool":"skill"|"name":"skill"|"name":"Skill"'
SKILL_NAME_PATTERN='"skill":"([^"/:]+[/|:])?'"$SKILL_NAME"'"|"name":"'"$SKILL_NAME"'"|\b'"$SKILL_NAME"'\b'

validate_skill_log() {
  local log_file="$1"
  local first_skill_record first_skill_line first_skill_payload premature_tools

  first_skill_record="$(grep -nE "$SKILL_TOOL_PATTERN" "$log_file" | head -1 || true)"

  if [[ -z "$first_skill_record" ]]; then
    echo "FAIL: no skill tool invocation found"
    echo "Full log: $log_file"
    return 1
  fi

  first_skill_line="${first_skill_record%%:*}"
  first_skill_payload="${first_skill_record#*:}"

  premature_tools="$(head -n "$first_skill_line" "$log_file" \
    | grep -E '"tool":"|"name":"' \
    | grep -Ev '"tool":"skill"|"name":"skill"|"name":"Skill"' || true)"
  if [[ -n "$premature_tools" ]]; then
    echo "FAIL: non-skill tools were invoked before the first skill tool call"
    echo "$premature_tools" | head -5
    echo "Full log: $log_file"
    return 1
  fi

  echo "OK: no non-skill tool invocation before first skill tool call"

  if ! printf '%s\n' "$first_skill_payload" | grep -Eq "$SKILL_NAME_PATTERN"; then
    echo "FAIL: first skill tool invocation was not '$SKILL_NAME'"
    echo "First skill payload: $first_skill_payload"
    echo "Skills mentioned in log:"
    grep -Eo '"skill":"[^"]+"|"name":"loom-[^"]+"|"name":"using-loom"' "$log_file" | sort -u || true
    echo "Full log: $log_file"
    return 1
  fi

  echo "PASS: explicit skill '$SKILL_NAME' was triggered first"
}

if [[ "$PROMPT_FILE" == "--check-log" ]]; then
  LOG_FILE="$MAX_TURNS"
  if [[ -z "$LOG_FILE" || ! -f "$LOG_FILE" ]]; then
    echo "Usage: $0 <skill-name> --check-log <log-file>" >&2
    exit 2
  fi
  validate_skill_log "$LOG_FILE"
  exit $?
fi

if ! command -v opencode >/dev/null 2>&1; then
  echo "SKIP: opencode not installed; cannot run Loom explicit skill integration test"
  exit 0
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TIMESTAMP="$(date +%s)"
OUTPUT_DIR="${LOOM_TEST_OUTPUT_DIR:-/tmp/loom-tests}/$TIMESTAMP/explicit-skill-requests/$SKILL_NAME"
PROJECT_DIR="$OUTPUT_DIR/project"
LOG_FILE="$OUTPUT_DIR/opencode-output.json"

mkdir -p "$PROJECT_DIR/.loom/tickets" "$PROJECT_DIR/.loom/evidence" "$PROJECT_DIR/.loom/audit"

cat > "$PROJECT_DIR/opencode.json" <<EOF
{
  "plugin": [
    "file://$REPO_ROOT/loom-core/loom-core.mjs",
    "file://$REPO_ROOT/loom-playbooks/loom-playbooks.mjs"
  ]
}
EOF

cat > "$PROJECT_DIR/.loom/tickets/auth-cleanup.md" <<'EOF'
# Auth Cleanup

ID: ticket:fixture-auth-cleanup
Type: Ticket
Status: open
Created: 2026-05-13
Updated: 2026-05-13
Risk: low - fixture ticket for activation testing.

## Summary

Fixture ticket for explicit skill activation tests.

## Scope

No real source edits are expected.

## Acceptance

- ACC-001: The agent loads the requested skill before acting.
  - Evidence: activation test transcript.
  - Audit: not required for fixture.

## Current State

Ready for activation testing.

## Journal

- 2026-05-13: Created fixture ticket.
EOF

PROMPT="$(<"$PROMPT_FILE")"

echo "=== Loom Explicit Skill Request Test ==="
echo "Skill: $SKILL_NAME"
echo "Prompt: $PROMPT_FILE"
echo "Max turns hint: $MAX_TURNS (OpenCode CLI currently uses timeout for this test)"
echo "Output: $LOG_FILE"

set +e
(
  cd "$PROJECT_DIR"
  timeout 300 opencode run --print-logs --format json --dangerously-skip-permissions "$PROMPT"
) > "$LOG_FILE" 2>&1
EXIT_CODE=$?
set -e

if [[ $EXIT_CODE -eq 124 ]]; then
  echo "FAIL: opencode timed out"
  exit 1
fi

validate_skill_log "$LOG_FILE"
exit $?
