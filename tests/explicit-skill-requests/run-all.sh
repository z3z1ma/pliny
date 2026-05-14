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
