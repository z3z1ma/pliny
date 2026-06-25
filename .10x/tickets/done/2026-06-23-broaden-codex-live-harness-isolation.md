Status: done
Created: 2026-06-23
Updated: 2026-06-23
Parent: none
Depends-On: .10x/evidence/2026-06-23-codex-live-isolation-smoke.md, .10x/evidence/2026-06-23-codex-home-isolation.md, .10x/research/2026-06-23-first-autoresearch-calibration-campaign.md

# Broaden Codex Live Harness Isolation Validation

## Scope

Validate Codex no-10x control isolation beyond the existing tiny live smoke and
fixture-smoke metadata.

Included:

- Design a small live Codex isolation battery with explicit run limits.
- Exercise generated workspaces without project instruction files.
- Use `--disable plugins`, `--ignore-user-config`, and recorded non-secret env
  policy metadata.
- Capture JSONL, stderr, workspace manifests, token counts, and tool-use events.
- Compare observations against the existing live-isolation and CODEX_HOME
  isolation evidence.

Excluded:

- Large or expensive benchmark campaigns.
- Copying auth files or secrets into fixture workspaces.
- Claiming complete hidden-context absence without evidence.

## Acceptance Criteria

- AC-001: The live isolation battery has a registered experiment or research
  record before execution.
- AC-002: Each live run records command metadata, exit code, JSONL/stdout,
  stderr, workspace manifest, and token/tool-use observations.
- AC-003: The evidence distinguishes project instruction isolation, plugin/skill
  loader suppression, auth inheritance, and remaining hidden-context risk.
- AC-004: Any failure, warning, or contamination signal opens a follow-up ticket
  instead of being lost in chat.

## Progress And Notes

- 2026-06-23: Opened from first calibration campaign because FULL fixture-smoke
  generated no live Codex calls and previous live evidence supports only narrow
  smoke claims.
- 2026-06-23: Added `autoresearch/run_codex_isolation.py` and tests. Ran a
  bounded two-run live battery with `--disable plugins`, `--ignore-user-config`,
  generated workspaces, read-only sandboxing, command metadata, JSONL, stderr,
  token fields, and workspace manifests. Evidence:
  `.10x/evidence/2026-06-23-codex-isolation-battery.md`.

## Blockers

None. Live-run limits are bounded by this ticket and the accepted subscription
budget policy.
