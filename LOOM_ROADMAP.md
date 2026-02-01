# LOOM_ROADMAP

High-level direction and priorities.

This is an evolving, empirical compass. Keep it short and stable.

<!-- BEGIN:compound:roadmap-backlog -->
- # Tickets (5)
- - `al-2a06` P2 open - Ticket: UX polish + flexible input normalization
- - `al-b110` P2 in_progress - Sprint tag: consistent ticket creation
- - `al-f351` P2 open - Team: audit inbox sprint prefix/meta coverage
- - `al-8a52` P3 open - UI: improve sprint surfacing
- - `al-f4d2` P3 open - Team: sprint lifecycle commands (show/set/clear)
<!-- END:compound:roadmap-backlog -->

<!-- BEGIN:compound:roadmap-ai-notes -->
- Near-term focus: make team runtime deterministic (startup wiring, mounts, prompt rendering, CLI UX) and lock behavior with small contract tests.
- Treat tests under tests/test_team_*.py as public contracts: prefer stable invariants over full-output snapshots unless the full output is the contract.
- When adding new team behavior, add the smallest dedicated test module first, then expand as invariants emerge.
- Keep template mirrors in sync when changing shipped .opencode assets (avoid install drift).
<!-- END:compound:roadmap-ai-notes -->

## Changelog (AI-first)

This log is optimized for *agents*, not humans.
It tracks changes to skills, instincts, and core context files.

It is intentionally bounded. Do not write entries like "no changes".

<!-- BEGIN:compound:changelog-entries -->
- 2026-02-01T18:01:22.323Z Clarify compound-apply-spec: background autolearn outputs JSON only (no compound_apply call).
- 2026-02-01T17:58:07.931Z Reinforce plan-mode read-only and autolearn JSON-only output discipline.
- 2026-02-01T17:23:11.689Z Reinforce workspace CLI output as a deterministic UX contract and re-affirm mirror-sync discipline when updating scaffolded .opencode templates.
- 2026-02-01T17:13:34.786Z Add a dedicated workspace CLI UX contract-testing skill; reinforce the instinct that workspace CLI output is a deterministic contract.
- 2026-02-01T16:37:51.600Z Add explicit UX contract procedures for workspace CLI and loom init CLI; reinforce deterministic output + targeted pytest gates for workspace/init surface changes.
- 2026-02-01T16:03:01.806Z Add a core CLI UX contract-testing heuristic (deterministic output + focused pytest coverage) for changes in src/agent_loom/cli.py.
- 2026-02-01T15:09:49.491Z Reinforce strict Plan Mode read-only discipline (no edits or write-capable commands).
- 2026-02-01T07:19:03.072Z Add workspace contract-testing instincts + skills to lock CLI UX and workspace runtime changes behind deterministic output and targeted uv-based verification gates.
- 2026-02-01T06:09:14.335Z Reinforced Plan Mode read-only discipline by increasing confidence in the existing plan-mode instinct.
- 2026-02-01T06:00:44.368Z Reinforced the team runtime as a deterministic, contract-tested surface: startup/integrator spawning, mounts, prompts, CLI UX, and start/merge config now have focused tests; kept shipped .opencode skill templates mirrored to avoid install drift.
- 2026-02-01T05:50:03.869Z Add mount-contract testing skill; reinforce instincts that team core/CLI/mount behavior changes require deterministic contracts and targeted tests.
- 2026-02-01T04:37:32.939Z Add a focused mounts contract-testing skill and new instincts to keep team mounts and merge queue behavior deterministic and covered by targeted tests.
- 2026-02-01T04:25:41.443Z Tighten Compound install/plugin learnings: add install contract-testing skill and instincts to keep scaffold template in sync and verify with tests/test_compound_install.py.
- 2026-02-01T04:01:40.251Z Reinforce Plan Mode read-only gate as a hard constraint when system reminder appears.
- 2026-02-01T02:50:12.389Z Add repo-standard verification memory: prefer `uv run basedpyright` over `lsp_diagnostics`, then ruff, then targeted pytest.
- 2026-02-01T01:33:16.827Z Reinforced the team CLI UX contract: changes to src/agent_loom/team/cli.py should be deterministic and paired with focused pytest coverage in tests/test_team_cli_ux.py.
- 2026-02-01T00:21:25.104Z Add spawn/integrator contract-testing guidance for team startup changes; reinforce targeted test+ruff expectations for team core expansions.
- 2026-01-31T21:29:50.566Z Reinforce ticket CLI UX as a contract: when src/agent_loom/ticket/cli.py changes, add/adjust deterministic assertions in tests/test_ticket_ux.py to lock output invariants and prevent drift.
- 2026-01-31T20:54:50.424Z Reinforced team prompt/core contract discipline: prompt structure stays deterministic and is locked by section-level tests when src/agent_loom/team/prompts.py or src/agent_loom/team/core.py changes.
- 2026-01-31T20:42:04.026Z Strengthen team prompt stability: treat prompt text as a contract, keep rendering deterministic, and lock invariants with section-level tests in tests/test_team_prompts.py.
- 2026-01-31T19:44:52.941Z Add a team start/merge config contract-testing instinct and wire it into the team feature checklist (tests/test_team_start_merge_config.py as the canonical lock).
- 2026-01-31T16:34:03.962Z Reinforce team CLI UX as a deterministic contract: add a focused skill for tests/test_team_cli_ux.py and bump confidence in the existing CLI-output/test instincts.
- 2026-01-31T07:40:53.142Z Hardened team learning: ship/merge changes now explicitly require ticket-sync contract tests; reinforced existing instincts around prompt tests, deterministic CLI output, and .opencode as the canonical skills location.
- 2026-01-31T07:19:33.754Z Tighten team feature checklist with explicit target-selection contract testing; reinforce instincts around deterministic CLI output and targeted contract tests.
- 2026-01-31T07:09:37.617Z Tighten team feature procedure: treat CLI UX as a first-class contract via tests/test_team_cli_ux.py; reinforce deterministic output + targeted team checks.
- 2026-01-31T07:09:31.570Z Refine team feature checklist to point CLI UX contract tests at tests/test_team_cli_ux.py; reinforce instincts around deterministic CLI output and targeted test coverage for team core/CLI changes.
- 2026-01-31T06:38:59.617Z Codified a team disband testing contract: update team feature checklist and add an instinct to require tests/test_team_disband.py plus targeted uv/ruff runs when disband semantics change.
- 2026-01-31T05:52:03.949Z Reinforce JSON-only discipline for background autolearn CompoundSpec v2 output.
- 2026-01-31T05:23:44.051Z Reinforced strict Plan Mode read-only and autolearn JSON-only output constraints.
- 2026-01-31T05:18:14.107Z Strengthen team runtime checklist to treat src/agent_loom/team/output.py text as a deterministic UX contract and require focused tests alongside LSP+ruff.
- 2026-01-31T05:06:50.012Z Reinforce JSON-only CompoundSpec v2 output and strict Plan Mode read-only discipline.
- 2026-01-31T05:04:10.556Z Reinforced background autolearn invariants: JSON-only output and strict Plan Mode read-only override.
- 2026-01-31T04:49:40.077Z Reinforce ticket runtime discipline: deterministic CLI UX backed by contract tests; add explicit checklist coverage for frontmatter/file-format round-trip testing.
- 2026-01-31T04:34:44.455Z Reinforce autolearn JSON-only + read-only discipline; extend compound-apply-spec with explicit autolearn constraints and limits reminder.
- 2026-01-31T04:25:39.112Z Reinforce plan-mode read-only guardrail and JSON-only autolearn output discipline.
- 2026-01-31T04:15:19.754Z Reinforce team-core + prompt-contract changes as test-driven surfaces; nudge confidence upward for targeted tests, prompt tests, and LSP-first workflow.
- 2026-01-31T03:33:30.180Z Codify ticket UX output contracts: add tests/test_ticket_ux.py focus, reinforce deterministic CLI output, and tighten targeted-test instincts for ticket/team core changes.
- 2026-01-31T03:03:40.761Z Add a UI-change checklist skill and an instinct to run LSP + ruff + targeted pytest after editing src/agent_loom/ui/*.
- 2026-01-31T02:21:32.199Z Add a ticket module checklist skill and an instinct to require LSP+ruff+targeted tests when changing ticket CLI/core/store.
- 2026-01-31T02:08:53.650Z Reinforced the JSON-only CompoundSpec v2 response discipline for background autolearn runs.
- 2026-01-30T21:10:39.730Z Hardened and expanded team runtime surface (core/cli/inbox/models/constants), evolved prompt assembly, and kept prompt behavior covered via tests/test_team_prompts.py; added ticket API/core plumbing and minor team UI tweaks.
- 2026-01-30T20:45:25.169Z Reinforced the JSON-only CompoundSpec v2 autolearn response instinct.
- 2026-01-30T20:09:26.543Z Codify team prompt contract testing; reinforce JSON-only CompoundSpec output discipline.
- 2026-01-30T19:57:14.512Z Align compounding docs with CompoundSpec v2 (schema + apply flow) and add instincts for uv-run, LSP-first hygiene, and prompt-test coupling.
<!-- END:compound:changelog-entries -->
