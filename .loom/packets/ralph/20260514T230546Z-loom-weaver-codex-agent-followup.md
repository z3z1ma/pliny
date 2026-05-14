# Loom Weaver Codex Agent Follow-up Packet

ID: packet:20260514T230546Z-loom-weaver-codex-agent-followup
Type: Packet
Status: consumed
Created: 2026-05-14 23:05 UTC
Updated: 2026-05-14 23:14 UTC
Target: ticket:20260514-loom-weaver-agent
Packet Kind: Ralph
Mode: execution
Context Style: live-reference
Worker: manual handoff - current session will execute from this packet
Branch: main
Worktree: /Users/alexanderbutler/code_projects/personal/agent-loom
Iteration: 2
Risk: high - model-visible prompt and cross-harness adapter surfaces
Verification Posture: observation-first
Change Class: Codex support revision and audit finding fix

## Mission

Revise the Loom Weaver implementation to match the operator's latest Codex
direction: do not expose Loom Weaver as a Core skill; instead ship a Codex custom
agent TOML definition and document a manual `curl` step that writes it to
`~/.codex/agents/` as described by Codex subagent docs.

Also address audit `FIND-001` from `packet:20260514T230124Z-loom-weaver-agent-audit`
by updating contributor guidance to include `loom-core/agents/` wherever it names
model-visible product behavior surfaces.

## Context Bundle

Records:

- `ticket:20260514-loom-weaver-agent` - active ticket and acceptance criteria.
- `spec:loom-weaver-agent` - behavior contract and resolved Codex decision to revise.
- `research:20260514-direct-interactive-agent-surfaces` - Codex source-backed support matrix.
- `evidence:20260514-loom-weaver-implementation-validation` - prior validation evidence, now partly stale where it references bundled skill support.
- `packet:20260514T230124Z-loom-weaver-agent-audit` - review packet output found `FIND-001` in `AGENTS.md`.

## Read Scope

- `.loom/tickets/20260514-loom-weaver-agent.md`
- `.loom/specs/loom-weaver-agent.md`
- `.loom/research/20260514-direct-interactive-agent-surfaces.md`
- `.loom/evidence/20260514-loom-weaver-implementation-validation.md`
- `.loom/packets/ralph/20260514T230124Z-loom-weaver-agent-audit.md`
- `AGENTS.md`
- `INSTALL.md`
- `README.md`
- `loom-core/README.md`
- `loom-core/agents/loom-weaver.md`
- `loom-core/skills/loom-weaver/SKILL.md`
- `loom-core/loom-core.mjs`
- `loom-core/package.json`
- `loom-core/.codex-plugin/plugin.json`
- Official Codex docs already cited in research, especially custom agents under `~/.codex/agents/`.

## Write Scope

Records Or Artifacts:

- `.loom/tickets/20260514-loom-weaver-agent.md`
- `.loom/specs/loom-weaver-agent.md`
- `.loom/research/20260514-direct-interactive-agent-surfaces.md`
- `.loom/evidence/20260514-loom-weaver-implementation-validation.md` or a new follow-up evidence record
- `.loom/audit/**` if recording the prior audit result
- this packet

Source Paths:

- `loom-core/skills/loom-weaver/SKILL.md` - remove the skill surface.
- `loom-core/codex/**` - add Codex custom agent TOML.
- `loom-core/loom-core.mjs` - update smoke/inspection away from skill sync and toward Codex TOML presence.
- `loom-core/package.json` - include Codex agent artifact if needed.
- `loom-core/.codex-plugin/plugin.json` - update Codex install-surface prompt.
- `AGENTS.md`, `INSTALL.md`, `README.md`, `loom-core/README.md` - documentation and contributor guidance alignment.

## Task

Implement the follow-up inside write scope:

- Delete the Loom Weaver Core skill surface.
- Add a Codex custom agent TOML file suitable for `~/.codex/agents/loom-weaver.toml` with `name`, `description`, and `developer_instructions` matching the Loom Weaver behavior contract.
- Document a `curl -fsSL https://raw.githubusercontent.com/z3z1ma/agent-loom/main/loom-core/codex/agents/loom-weaver.toml -o ~/.codex/agents/loom-weaver.toml` style install path, with `mkdir -p ~/.codex/agents` first.
- Keep Codex docs honest: this is manual custom-agent installation, natural-language subagent invocation after install, and `/agent` thread management; do not claim `@<agent>` or plugin-shipped profile/custom-agent support.
- Fix `AGENTS.md` dogfooding guidance so it no longer omits `loom-core/agents/`.
- Update records and evidence to reflect the revised Codex route.
- Run fresh validation after edits.

## Evidence, Review, Or Verification Expectations

- Source inspection should show no `loom-core/skills/loom-weaver/SKILL.md` remains.
- Source inspection should show `loom-core/codex/agents/loom-weaver.toml` contains the `.loom/` write boundary and core Loom Weaver behavior.
- Core smoke and pack check should pass, with pack output including the Codex TOML artifact.
- `git diff --check` should pass.
- Claude and Gemini validators should still pass if their surfaces remain changed.
- Evidence should be updated or added to avoid relying on the stale bundled-skill claim.
- A fresh audit/review should run before closure.

## Stop Conditions

- Stop if Codex custom-agent TOML cannot be represented without copying unsafe or stale prompt content.
- Stop if removing the skill breaks activation checks or Core smoke in a way that requires changing broader skill policy.
- Stop if the manual install docs would contradict the operator's new direction or current Codex docs.

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

Outcome: stop.

Files changed:

- `loom-core/skills/loom-weaver/SKILL.md` removed.
- `loom-core/codex/agents/loom-weaver.toml` added.
- `loom-core/loom-core.mjs`
- `loom-core/package.json`
- `loom-core/.codex-plugin/plugin.json`
- `AGENTS.md`
- `INSTALL.md`
- `README.md`
- `loom-core/README.md`

Records changed:

- `.loom/tickets/20260514-loom-weaver-agent.md`
- `.loom/specs/loom-weaver-agent.md`
- `.loom/research/20260514-direct-interactive-agent-surfaces.md`
- `.loom/evidence/20260514-loom-weaver-implementation-validation.md`
- `.loom/evidence/20260514-loom-weaver-codex-agent-followup-validation.md`
- `.loom/audit/20260514-loom-weaver-agent-audit.md`
- `.loom/packets/ralph/20260514T230546Z-loom-weaver-codex-agent-followup.md`

Evidence, review findings, validation output, or observations gathered:

- Created `evidence:20260514-loom-weaver-codex-agent-followup-validation`.
- Removed the Core Loom Weaver skill and replaced the Codex path with `loom-core/codex/agents/loom-weaver.toml`.
- Updated smoke to verify Codex TOML presence, `developer_instructions`, `.loom/` write boundary, and prompt-body match with `loom-core/agents/loom-weaver.md`.
- First revised smoke failed because the TOML multiline parser preserved a leading newline; parser was fixed and smoke then passed.
- `npm --prefix loom-core run pack:check` passed and included `codex/agents/loom-weaver.toml` in the dry-run tarball.
- `git diff --check`, `claude plugin validate "$PWD/loom-core"`, and `gemini extensions validate "$PWD/loom-core"` passed.
- Recorded `audit:20260514-loom-weaver-agent-audit` from the prior review output and fixed its `FIND-001` in `AGENTS.md`.

What was not verified or reviewed:

- No live Codex custom-agent invocation was tested.
- No live OpenCode, Claude Code, Cursor, or Gemini runtime invocation was tested.
- Cursor plugin behavior remains unvalidated by a local validator.
- A fresh final audit over the revised state has not yet run.

Blockers, risks, or assumptions discovered:

- Codex support is now an explicit custom-agent installation step, not plugin-automatic installation.
- The Codex custom-agent TOML duplicates the canonical prompt body, so smoke now checks that the TOML developer instructions match the canonical agent body.

Recommended next move:

- Run a fresh audit/review packet over the final diff, updated evidence, and ticket acceptance criteria before closure.
