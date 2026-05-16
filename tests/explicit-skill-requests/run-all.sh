#!/usr/bin/env bash
# Run explicit Loom skill request activation tests.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROMPTS_DIR="$SCRIPT_DIR/prompts"

TESTS=(
  "loom-tickets:$PROMPTS_DIR/use-loom-tickets.txt"
  "loom-ralph:$PROMPTS_DIR/use-loom-ralph.txt"
  "loom-evidence:$PROMPTS_DIR/use-loom-evidence.txt"
  "loom-audit:$PROMPTS_DIR/use-loom-audit.txt"
)

FAILED=0

PROBE_OUTPUT="$(mktemp "${TMPDIR:-/tmp}/loom-explicit-skill-probe.XXXXXX")"
set +e
bash "$SCRIPT_DIR/run-test.sh" "loom-audit" --check-log "$SCRIPT_DIR/wrong-skill-first-requested-later.jsonl" > "$PROBE_OUTPUT" 2>&1
PROBE_STATUS=$?
set -e

if [[ $PROBE_STATUS -eq 0 ]]; then
  echo "FAIL: parser probe passed when wrong skill appeared before requested skill"
  FAILED=$((FAILED + 1))
elif [[ $PROBE_STATUS -ne 1 ]]; then
  echo "FAIL: parser probe exited $PROBE_STATUS instead of intended wrong-skill failure"
  cat "$PROBE_OUTPUT"
  FAILED=$((FAILED + 1))
elif ! grep -Fq "FAIL: first skill tool invocation was not 'loom-audit'" "$PROBE_OUTPUT"; then
  echo "FAIL: parser probe failed for an unexpected reason"
  cat "$PROBE_OUTPUT"
  FAILED=$((FAILED + 1))
else
  echo "PASS: parser probe failed wrong-skill-first/requested-skill-later log"
fi
rm -f "$PROBE_OUTPUT"

for item in "${TESTS[@]}"; do
  skill="${item%%:*}"
  prompt="${item#*:}"
  if ! bash "$SCRIPT_DIR/run-test.sh" "$skill" "$prompt" 3; then
    FAILED=$((FAILED + 1))
  fi
done

if [[ $FAILED -gt 0 ]]; then
  echo "FAIL: $FAILED explicit skill request test(s) failed"
  exit 1
fi

echo "PASS: all explicit skill request tests passed"
