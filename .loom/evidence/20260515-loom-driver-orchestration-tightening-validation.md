# Loom Driver Orchestration Tightening Validation

ID: evidence:20260515-loom-driver-orchestration-tightening-validation
Type: Evidence Dossier
Status: recorded
Created: 2026-05-15
Updated: 2026-05-15
Observed: 2026-05-15 06:33 UTC

## Summary

This dossier records validation observations after tightening Loom Driver around packet compilation, worker coordination, output reconciliation, evidence, audit, ticket state, and read-only direction-setting records.

## Observations

- Observation: Core smoke check passed after the prompt, TOML, permission, and spec changes.
  - Procedure/source: Ran `npm --prefix loom-core run smoke` from `/Users/alexanderbutler/code_projects/personal/agent-loom` after the changes.
  - Actual result: Command exited successfully with `ok: true`, agent names `loom-driver` and `loom-weaver`, Driver prompt/TOML parity true, Driver direction-record boundary true, Driver task permission `allow`, and Driver edit permissions denying `*` while allowing `.loom/tickets/**`, `.loom/packets/ralph/**`, `.loom/evidence/**`, and `.loom/audit/**`.

- Observation: Core package dry-run check passed after the changes.
  - Procedure/source: Ran `npm --prefix loom-core run pack:check` from `/Users/alexanderbutler/code_projects/personal/agent-loom` after the changes.
  - Actual result: Command exited successfully. The dry-run tarball contents included `agents/loom-driver.md` and `codex/agents/loom-driver.toml`.

- Observation: Diff whitespace check passed after the changes.
  - Procedure/source: Ran `git diff --check` from `/Users/alexanderbutler/code_projects/personal/agent-loom` after the changes.
  - Actual result: Command exited successfully with no output.

- Observation: Claude Core plugin manifest validation passed in the current source state.
  - Procedure/source: Ran `claude plugin validate "$PWD/loom-core"` from `/Users/alexanderbutler/code_projects/personal/agent-loom` after the changes.
  - Actual result: Command exited successfully and reported validation passed for `loom-core/.claude-plugin/plugin.json`.

- Observation: Prompt inspection found coordination language in both model-visible Driver surfaces.
  - Procedure/source: Searched `loom-core/agents/loom-driver.md` and `loom-core/codex/agents/loom-driver.toml` for coordination, packet, worker, reconcile, evidence, audit, direction-setting, complete, blocked, and escalated.
  - Actual result: Both surfaces contained repeated hits for packet compilation, worker coordination, output reconciliation, evidence, audit, completion, blocker, escalation, and direction-setting record language.

- Observation: Prompt inspection found no direct-edit or contributor-process leakage matches in the Driver surfaces.
  - Procedure/source: Searched `loom-core/agents/loom-driver.md` and `loom-core/codex/agents/loom-driver.toml` for direct edit, directly edit, source edit, edits code, generic coder, You are not, Do not turn, Do not let, self-justification, package smoke, dogfood, repository workflow, and adapter self.
  - Actual result: No matches were returned for either Driver surface.

## Artifacts

- `npm --prefix loom-core run smoke` output - shows Driver prompt/TOML parity and execution-record-only OpenCode edit permissions.
- `npm --prefix loom-core run pack:check` output - shows Core smoke plus dry package contents containing Driver Markdown and TOML files.
- `git diff --check` output - no output, indicating no whitespace errors in the diff.
- `claude plugin validate "$PWD/loom-core"` output - reports Claude plugin validation passed.
- Grep results for Driver behavior and leakage terms - show required coordination terms present and no direct-edit or contributor-process leakage matches.

## What This Shows

- `ticket:20260515-loom-driver-orchestration-tightening#ACC-001` - supports - the amended spec now describes Driver as inner-loop coordination through packets, workers, evidence, audit, and ticket reconciliation, with completion, blocker, and escalation outcomes.
- `ticket:20260515-loom-driver-orchestration-tightening#ACC-002` - supports - the canonical prompt and Codex TOML contain matching coordination behavior and Core smoke reports prompt/TOML parity.
- `ticket:20260515-loom-driver-orchestration-tightening#ACC-003` - supports - Core smoke shows Driver edit permissions deny general edits and allow only execution-record paths while preserving task permission for worker orchestration.
- `ticket:20260515-loom-driver-orchestration-tightening#ACC-004` - supports - updated docs describe Driver as packetized coordination and no longer claim Driver directly edits source.
- `ticket:20260515-loom-driver-orchestration-tightening#ACC-005` - supports - Core smoke, Core pack dry-run, `git diff --check`, and Claude plugin validation passed.

## What This Does Not Show

This evidence does not prove live runtime invocation in OpenCode, Claude Code, Codex, Cursor, or Gemini. It does not prove OpenCode's runtime permission matcher applies glob rules in the same order as represented in smoke output. It does not prove ticket closure because `ticket:20260515-loom-driver-orchestration-tightening#ACC-006` still requires a fresh Ralph-backed audit pass.

## Related Records

- `ticket:20260515-loom-driver-orchestration-tightening` - consuming ticket for these observations.
- `spec:loom-driver-agent` - amended behavior contract these observations support.
- `packet:20260515T062418Z-loom-driver-orchestration-tightening` - implementation packet that requested this validation evidence.
