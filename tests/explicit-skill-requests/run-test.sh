#!/usr/bin/env bash
# Test explicit Loom skill requests and warn when non-skill tools run first.
# Usage: bash tests/explicit-skill-requests/run-test.sh <skill-name> <prompt-file> [max-turns]

set -euo pipefail

SKILL_NAME="${1:-}"
PROMPT_FILE="${2:-}"
MAX_TURNS="${3:-3}"

if [[ -z "$SKILL_NAME" || -z "$PROMPT_FILE" ]]; then
  echo "Usage: $0 <skill-name> <prompt-file> [max-turns]" >&2
  exit 2
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

mkdir -p "$PROJECT_DIR/.loom/tickets" "$PROJECT_DIR/.loom/packets/ralph"

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

SKILL_TOOL_PATTERN='"tool":"skill"|"name":"skill"|"name":"Skill"'
SKILL_NAME_PATTERN='"skill":"([^"/:]+[/|:])?'"$SKILL_NAME"'"|"name":"'"$SKILL_NAME"'"|\b'"$SKILL_NAME"'\b'

FIRST_SKILL_LINE="$(grep -nE "$SKILL_TOOL_PATTERN" "$LOG_FILE" | head -1 | cut -d: -f1 || true)"

if [[ -n "$FIRST_SKILL_LINE" ]]; then
  PREMATURE_TOOLS="$(head -n "$FIRST_SKILL_LINE" "$LOG_FILE" \
    | grep -E '"tool":"|"name":"' \
    | grep -Ev '"tool":"skill"|"name":"skill"|"name":"Skill"|"tool":"todowrite"|"name":"todowrite"' || true)"
  if [[ -n "$PREMATURE_TOOLS" ]]; then
    echo "WARNING: non-skill tools were invoked before the first skill tool call"
    echo "$PREMATURE_TOOLS" | head -5
  else
    echo "OK: no non-skill tool invocation before first skill tool call"
  fi
else
  echo "WARNING: no skill tool invocation found"
fi

if grep -Eq "$SKILL_TOOL_PATTERN" "$LOG_FILE" && grep -Eq "$SKILL_NAME_PATTERN" "$LOG_FILE"; then
  echo "PASS: explicit skill '$SKILL_NAME' was triggered"
  exit 0
fi

echo "FAIL: explicit skill '$SKILL_NAME' was not detected"
echo "Skills mentioned in log:"
grep -Eo '"skill":"[^"]+"|"name":"loom-[^"]+"|"name":"using-loom"' "$LOG_FILE" | sort -u || true
echo "Full log: $LOG_FILE"
exit 1
