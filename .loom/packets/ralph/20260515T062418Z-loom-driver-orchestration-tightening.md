# Loom Driver Orchestration Tightening Packet

ID: packet:20260515T062418Z-loom-driver-orchestration-tightening
Type: Packet
Status: consumed
Created: 2026-05-15 06:24 UTC
Updated: 2026-05-15 06:33 UTC
Target: ticket:20260515-loom-driver-orchestration-tightening
Packet Kind: Ralph
Mode: execution
Context Style: live-reference
Worker: manual handoff
Branch: main
Worktree: /Users/alexanderbutler/code_projects/personal/agent-loom
Risk: high - updates a shipped agent persona and permission boundary.
Verification Posture: observation-first
Change Class: prompt and behavior contract correction

## Mission

Revise Loom Driver so the behavior contract, prompt, Codex TOML, docs, and OpenCode registration present it as an inner-loop coordinator for packets, workers, evidence, audit, and ticket reconciliation, with direct edit permission limited to execution records.

## Context Bundle

Records:

- `ticket:20260515-loom-driver-orchestration-tightening` - scope and acceptance for this follow-up.
- `spec:loom-driver-agent` - behavior contract to amend in place.
- `ticket:20260515-loom-driver-agent` - original implementation and residual risks.
- `evidence:20260515-loom-driver-agent-validation` - prior validation baseline.
- `audit:20260515-loom-driver-agent-audit` and `audit:20260515-loom-driver-final-audit` - prior audit baseline.

Files:

- `loom-core/agents/loom-driver.md` - canonical prompt.
- `loom-core/codex/agents/loom-driver.toml` - Codex TOML copy.
- `loom-core/loom-core.mjs` - OpenCode registration and smoke checks.
- `INSTALL.md`, `README.md`, `loom-core/README.md` - docs that describe Driver.

## Read Scope

- `.loom/specs/loom-driver-agent.md`
- `.loom/tickets/20260515-loom-driver-agent.md`
- `.loom/tickets/20260515-loom-driver-orchestration-tightening.md`
- `loom-core/agents/loom-driver.md`
- `loom-core/codex/agents/loom-driver.toml`
- `loom-core/loom-core.mjs`
- `INSTALL.md`
- `README.md`
- `loom-core/README.md`

## Write Scope

Records Or Artifacts:

- `.loom/specs/loom-driver-agent.md` - update the same product-slice behavior contract.
- `.loom/tickets/20260515-loom-driver-orchestration-tightening.md` - update state and journal.
- `.loom/evidence/20260515-loom-driver-orchestration-tightening-validation.md` - create after validation.
- this packet - fill output and status.

Source Paths:

- `loom-core/agents/loom-driver.md`
- `loom-core/codex/agents/loom-driver.toml`
- `loom-core/loom-core.mjs`
- `INSTALL.md`
- `README.md`
- `loom-core/README.md`

Read-only high-authority records:

- `.loom/constitution/**`, `.loom/plans/**`, `.loom/research/**` - do not mutate.

## Source Snapshot

The current working tree includes the prior uncommitted Driver implementation and closed Loom records. The follow-up starts from the first Driver prompt, which still allowed direct file edits in prompt language and OpenCode permissions. Existing validation and audit records are useful baselines but will become stale for the changed prompt and permissions.

## Task

Update the spec and prompt so Driver is the coordinator that moves shaped graph work through packets, worker launches, output reconciliation, evidence, audit, and ticket state. Emphasize completion through all graph-supported work in the operator's scope, with stopping conditions limited to completion, concrete blockers, stale packets, missing authority, or higher-level ambiguity.

Remove direct source-edit framing from Driver's behavior. Workers launched from packets may change source within their packet scopes; Driver itself should write execution records and coordinate the work.

Keep the prompt free of contributor-facing process, repository workflow, and explanatory self-commentary. Prefer direct operating doctrine over contrastive or defensive prose.

Update OpenCode permissions so Driver can update execution records and launch workers, but cannot directly edit source files or high-authority Loom records.

## Evidence, Review, Or Verification Expectations

After changes, run and record:

- Source inspection or grep showing orchestration, packet compilation, worker coordination, output reconciliation, evidence, audit, completion pressure, and high-authority read-only posture in both Driver model-visible surfaces.
- Core smoke showing prompt/TOML parity and updated Driver permissions.
- `npm --prefix loom-core run pack:check`.
- `git diff --check`.
- Claude validation only if the Claude manifest changes.

Create `.loom/evidence/20260515-loom-driver-orchestration-tightening-validation.md`.

## Stop Conditions

- Stop if the spec amendment reveals a materially different product slice.
- Stop if OpenCode cannot express the intended coordination-only write boundary without misleading smoke output.
- Stop if prompt/TOML parity cannot be preserved.
- Stop if validation cannot be gathered after the last material change.

## Output Contract

The worker must update this packet or return output with:

- outcome: `continue`, `stop`, `blocked`, or `escalate`
- files changed
- records changed
- evidence, review findings, validation output, or observations gathered
- what was not verified or reviewed
- blockers, risks, or assumptions discovered
- recommended next move for the consuming surface

## Worker Output

Outcome: `stop`

Files changed:

- Rewrote `loom-core/agents/loom-driver.md` around packet compilation, worker coordination, output reconciliation, evidence, audit, ticket state, direction-record authority, and graph-supported completion.
- Rewrote `loom-core/codex/agents/loom-driver.toml` with developer instructions matching the canonical prompt.
- Updated `loom-core/loom-core.mjs` so Driver direct edit permissions deny general writes and allow only execution-record paths while preserving task permission for worker orchestration.
- Updated `INSTALL.md`, `README.md`, `loom-core/README.md`, and `loom-core/.codex-plugin/plugin.json` to describe Driver as inner-loop coordination rather than direct implementation.

Records changed:

- Amended `spec:loom-driver-agent` in place for the same product slice.
- Created `ticket:20260515-loom-driver-orchestration-tightening`.
- Created `evidence:20260515-loom-driver-orchestration-tightening-validation`.
- Updated this packet.

Evidence gathered:

- `npm --prefix loom-core run smoke` passed with Driver prompt/TOML parity and execution-record-only edit permissions.
- `npm --prefix loom-core run pack:check` passed and dry-run package contents included Driver Markdown and TOML files.
- `git diff --check` passed with no output.
- `claude plugin validate "$PWD/loom-core"` passed.
- Grep inspection found coordination, packet, worker, reconciliation, evidence, audit, completion, blocker, escalation, and direction-setting record language in both Driver surfaces.
- Grep inspection found no direct-edit or contributor-process leakage matches in the Driver surfaces.

What was not verified or reviewed:

- Live runtime invocation was not tested in supported harnesses.
- OpenCode runtime permission matching was not tested beyond smoke output and source inspection.
- Fresh Ralph-backed audit is still required before closure.

Blockers, risks, or assumptions discovered:

- No blocker discovered. Residual risk remains around runtime permission enforcement and live harness behavior.

Recommended next move:

- Move `ticket:20260515-loom-driver-orchestration-tightening` to review and run a Ralph-backed audit over the amended spec, prompt, TOML, permissions, docs, and validation evidence.
