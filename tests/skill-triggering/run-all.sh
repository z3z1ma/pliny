#!/usr/bin/env bash
# Run natural-prompt Loom skill triggering tests.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROMPTS_DIR="$SCRIPT_DIR/prompts"

TESTS=(
  "loom-idea-refine:$PROMPTS_DIR/loom-idea-refine.txt"
  "loom-debugging-and-error-recovery:$PROMPTS_DIR/loom-debugging-and-error-recovery.txt"
  "loom-tickets:$PROMPTS_DIR/loom-tickets.txt"
  "loom-ralph:$PROMPTS_DIR/loom-ralph.txt"
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
  echo "FAIL: $FAILED skill triggering test(s) failed"
  exit 1
fi

echo "PASS: all skill triggering tests passed"
