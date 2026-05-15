# Loom Driver Rename Packet

ID: packet:20260515T070409Z-loom-driver-rename
Type: Packet
Status: consumed
Created: 2026-05-15 07:04 UTC
Updated: 2026-05-15 07:04 UTC
Target: ticket:20260515-loom-driver-rename
Packet Kind: Ralph
Mode: execution
Context Style: live-reference
Worker: manual handoff
Branch: main
Worktree: /Users/alexanderbutler/code_projects/personal/agent-loom
Risk: high - mechanical rename of a shipped model-visible agent and existing Loom graph records.
Verification Posture: observation-first
Change Class: agent interface rename

## Mission

Rename the inner-loop coordination agent to Loom Driver consistently across filenames, IDs, source text, docs, adapter manifests, and Loom records. Preserve behavior; change terminology and cross-record references only.

## Context Bundle

Records:

- `ticket:20260515-loom-driver-rename` - scope and acceptance for this rename.
- `spec:loom-driver-agent` - expected behavior contract after the rename.
- Existing Driver-related tickets, evidence, audit, and packet records after filename and text migration - must remain cross-linked consistently.

Files:

- `loom-core/agents/loom-driver.md` - canonical prompt after rename.
- `loom-core/codex/agents/loom-driver.toml` - Codex prompt copy after rename.
- `loom-core/loom-core.mjs` - helper names, agent registration, and smoke checks.
- `loom-core/.claude-plugin/plugin.json` and `loom-core/.codex-plugin/plugin.json` - adapter surfaces.
- `INSTALL.md`, `README.md`, `loom-core/README.md`, `ARCHITECTURE.md` - docs that name the agent.

## Read Scope

- Entire workspace except `.git/` and dependency/cache directories, for predecessor-name search and targeted rename.
- `.loom/**` records, including hidden and untracked files.
- `loom-core/**`, `README.md`, `INSTALL.md`, and `ARCHITECTURE.md`.

## Write Scope

Records Or Artifacts:

- `.loom/tickets/**` - rename affected records and update this ticket.
- `.loom/specs/**` - rename affected spec record and terminology only.
- `.loom/evidence/**` - rename affected evidence records and create fresh validation evidence.
- `.loom/audit/**` - rename affected audit records; fresh audit belongs after execution.
- `.loom/packets/ralph/**` - rename affected packets and fill this packet output.

Source Paths:

- `loom-core/agents/**`
- `loom-core/codex/agents/**`
- `loom-core/loom-core.mjs`
- `loom-core/.claude-plugin/plugin.json`
- `loom-core/.codex-plugin/plugin.json`
- `INSTALL.md`
- `README.md`
- `loom-core/README.md`
- `ARCHITECTURE.md`

## Source Snapshot

The workspace already contains the new inner-loop coordination agent work as uncommitted changes and Loom records. This packet intentionally updates those in-progress source and record surfaces so the graph uses the Driver name before the work settles.

## Task

Perform a consistent rename to the Driver agent name and slug. Rename affected files and records, update IDs and prose, update helper/function/object names in source, update adapter manifest entries, update docs, and keep behavior text otherwise unchanged.

Do not add compatibility aliases, shims, redirects, or legacy-name support. Do not change agent behavior except where terminology must change.

## Evidence, Review, Or Verification Expectations

After the last material rename, run and record:

- predecessor-name filename search over the workspace.
- predecessor-name content search over the workspace, including `.loom` records.
- `npm --prefix loom-core run smoke`.
- `npm --prefix loom-core run pack:check`.
- `git diff --check`.
- `claude plugin validate "$PWD/loom-core"`.

Create fresh evidence for this ticket and update this ticket to `review` when implementation evidence is recorded.

## Stop Conditions

- Stop if the rename reveals a need for compatibility aliases or migration policy.
- Stop if any predecessor-name occurrence appears intentionally required.
- Stop if source checks fail after the rename and cannot be corrected within the rename scope.
- Stop if the rename would require changing behavior beyond terminology.

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

- Renamed `loom-core/agents/loom-driver.md` and `loom-core/codex/agents/loom-driver.toml` to the Driver slug.
- Updated `loom-core/loom-core.mjs` helper names, smoke checks, OpenCode registration, permission checks, and smoke output keys for Driver.
- Updated `loom-core/.claude-plugin/plugin.json` and `loom-core/.codex-plugin/plugin.json` for Driver agent references.
- Updated `INSTALL.md`, `README.md`, `loom-core/README.md`, and `ARCHITECTURE.md` for Driver naming.

Records changed:

- Renamed and updated affected specs, tickets, packets, evidence records, and audit records to Driver IDs, filenames, and prose.
- Created `ticket:20260515-loom-driver-rename`.
- Created `evidence:20260515-loom-driver-rename-validation`.
- Updated this packet.

Evidence gathered:

- Workspace filename search found no predecessor-name paths outside VCS metadata.
- Workspace content search found no predecessor-name text outside VCS metadata.
- `npm --prefix loom-core run smoke` passed with Driver agent registration and prompt/TOML parity.
- `npm --prefix loom-core run pack:check` passed and packed Driver Markdown/TOML surfaces.
- `git diff --check` passed with no output.
- `claude plugin validate "$PWD/loom-core"` passed.

What was not verified or reviewed:

- Live runtime invocation was not tested in supported harnesses.
- VCS metadata under `.git/` was not rewritten.
- Fresh Ralph-backed audit is still required before closure.

Blockers, risks, or assumptions discovered:

- No blocker discovered.
- Residual risk remains around live harness invocation and runtime permission enforcement, matching the prior Driver coordination-ticket limits.

Recommended next move:

- Move `ticket:20260515-loom-driver-rename` to review and run a Ralph-backed audit over the rename consistency, source surfaces, docs, validation evidence, and cross-record links.
