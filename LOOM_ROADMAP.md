# LOOM_ROADMAP

High-level direction and priorities.

This is an evolving, empirical compass. Keep it short and stable.

<!-- BEGIN:compound:roadmap-backlog -->
- # Tickets (1)
- - `al-768c` P1 in_progress - Sprint prep: Documentation Foundation
<!-- END:compound:roadmap-backlog -->

<!-- BEGIN:compound:roadmap-ai-notes -->
- Keep ticket runtime minimal: fewer concepts, clearer state transitions, stable rendered UX.
- Replace procedural cookbooks with executable contracts (focused pytest modules) to prevent drift.
- Maintain install determinism: keep `.opencode/` sources and `src/agent_loom/compound/opencode/.opencode/` mirrors in sync.
<!-- END:compound:roadmap-ai-notes -->

## Changelog (AI-first)

This log is optimized for *agents*, not humans.
It tracks changes to skills, instincts, and core context files.

It is intentionally bounded. Do not write entries like "no changes".

<!-- BEGIN:compound:changelog-entries -->
- 2026-02-03T06:27:19.025Z Codified a practice: simplify ticket runtime while locking deterministic UX via focused contract tests; added an instinct to replace deleted cookbooks with tests; reinforced template-mirror determinism.
- 2026-02-03T06:23:48.841Z Reinforced ticket UX contract habit: boosted related instinct confidence and expanded the standard verification gate examples to include ticket UX contract tests.
- 2026-02-03T06:17:16.103Z Reinforced the repo-wide verification posture: `uv run` for all Python commands and `basedpyright` over LSP diagnostics.
- 2026-02-03T01:37:15.816Z Reinforce team core + prompt contract instincts; keep docs in sync.
- 2026-02-03T01:00:59.243Z Reinforce team-core + prompt-contract discipline (determinism + targeted prompt tests) in instincts and always-on context.
- 2026-02-03T00:55:39.333Z Reinforce that team core/prompt changes must be locked with targeted prompt contract tests.
- 2026-02-03T00:51:54.512Z Reinforced instincts that team prompt/core changes must be locked by focused prompt contract tests.
- 2026-02-03T00:47:29.598Z Add a focused checklist skill for prompt assembly changes in src/agent_loom/team/core.py, emphasizing deterministic prompts and contract tests.
- 2026-02-03T00:28:13.735Z Add contract memory for deterministic team init agents (new instinct + skill) and reinforce docs around team boot determinism and focused tests.
- 2026-02-03T00:16:55.004Z Reinforced instincts to always couple team core/prompt changes with deterministic prompt contract tests.
- 2026-02-02T23:45:29.308Z Reinforce dashboard template + server API contract test coupling via instinct confidence bumps; no new skills needed because existing dashboard anchor/contract skill already covers this workflow.
- 2026-02-02T23:18:30.672Z Reinforced the dashboard template anchor/contract instinct based on a real template edit.
- 2026-02-02T23:14:26.285Z Reinforce determinism-as-contract for dashboard HTML and workspace diff/read outputs; add a focused skill + instinct for workspace diff ops testing.
- 2026-02-02T22:25:58.047Z Reinforce dashboard/workspace UX contracts: clarify dashboard template source-of-truth, strengthen anchor-based HTML contract guidance, and bump related instinct confidence.
- 2026-02-02T21:40:49.317Z Reinforced the dashboard CLI output-as-contract instinct based on recent dashboard CLI edits.
- 2026-02-02T21:37:28.324Z Tighten dashboard template contract memory: treat both dashboard.html locations as anchor-and-test gated surfaces.
- 2026-02-02T21:34:30.030Z Add dashboard CLI UX contract testing skill and instinct to keep src/agent_loom/dashboard/cli.py output deterministic and tested.
- 2026-02-02T21:24:36.942Z Reinforce JSON-only and read-only discipline for background autolearn/plan-mode contexts.
- 2026-02-02T21:09:16.406Z Add a checklist + instinct for clean removal of entire CLI command surfaces; deprecate loom-init UX skill while init module is absent.
- 2026-02-02T20:59:17.409Z Reinforce dashboard template anchor + contract testing discipline; bump confidence on server HTML contract instincts.
- 2026-02-02T20:55:37.931Z Add instinct to lock ticket runtime/UX changes behind deterministic output + tests/test_ticket_ux.py gate.
- 2026-02-02T20:31:09.235Z Reinforce server template contract discipline: stable data-* anchors + request-level invariants; slightly increase confidence on related instincts.
- 2026-02-02T20:26:40.303Z Reinforce server template contract instincts (dashboard invariants, deterministic markers) based on recent dashboard.html edits.
- 2026-02-02T20:19:32.304Z Reinforce dashboard/server HTML contract instincts: deterministic template output, diff hygiene, and server API contract tests on dashboard.html changes.
- 2026-02-02T20:11:49.701Z Reinforce dashboard HTML as a deterministic, anchor-driven contract; add an instinct to avoid drift when touching the instincts store.
- 2026-02-02T20:07:39.211Z Reinforce server-rendered dashboard HTML as a deterministic contract; add a focused skill for stable data-* anchors + contract testing when editing dashboard.html.
- 2026-02-02T20:02:22.241Z Reinforce instincts: dashboard/server templates are contract surfaces; pair template edits with deterministic invariants and server API contract tests.
- 2026-02-02T19:44:50.423Z Strengthen confidence in server HTML contract instincts (dashboard/template changes paired with request-level tests; keep scaffold mirrors in sync).
- 2026-02-02T19:37:33.385Z Reinforce server HTML contract instincts and add always-on reminder to keep shipped .opencode template mirrors in sync under src/agent_loom/compound/opencode/.opencode/.
- 2026-02-02T19:32:14.197Z Reinforce instincts around dashboard/server HTML contract testing, diff hygiene for template refactors, and keeping Compound scaffold mirrors in sync.
- 2026-02-02T19:27:44.980Z Codified diff hygiene for large server template refactors; strengthened server HTML contract guidance and tests-first invariants.
- 2026-02-02T19:21:47.052Z Reinforce JSON-only autolearn output and plan-mode read-only discipline; no skill/doc content changes.
- 2026-02-02T18:09:51.586Z Reinforce server-rendered HTML as a deterministic UX contract; add a refactor hygiene skill focused on anchors, meaningful diffs, and request-level contract tests.
- 2026-02-02T18:02:26.339Z Reinforce dashboard/server HTML contract: boost relevant instincts, and tighten server-api-contract-testing guidance for large template refactors + resilient request-level invariants.
- 2026-02-02T17:53:42.145Z Codified that large dashboard.html refactors must be paired with resilient server HTML contract tests asserting stable markers/ordering (not whitespace snapshots).
- 2026-02-02T17:37:43.176Z Reinforced server template determinism and request-level HTML contract testing after dashboard template refactor.
- 2026-02-02T17:11:59.402Z Codified a tighter heuristic and skill: server-rendered HTML changes should be guarded by request-level API contract tests (prefer tests/test_server_api_contract.py) using stable markers and deterministic ordering.
- 2026-02-02T17:02:29.943Z Reinforce deterministic server template UX contracts and strict Plan Mode read-only discipline.
- 2026-02-02T16:51:48.922Z Add instinct to treat server templates as deterministic UX contracts; reinforce always-on guidance to test large dashboard.html refactors with focused invariants.
- 2026-02-02T16:44:53.996Z Add an instinct + skill to treat server-rendered templates (dashboard.html) as deterministic UX contracts with focused pytest coverage.
- 2026-02-02T15:47:25.765Z Reinforced JSON-only discipline for Compound background autolearn responses.
- 2026-02-02T05:46:51.173Z Reinforce plan-mode read-only discipline during autolearn/idle sessions; no new durable procedures identified from README-only edits.
- 2026-02-02T04:29:15.307Z Reinforced strict JSON-only learning output and plan-mode read-only discipline via instinct confidence bumps.
- 2026-02-02T04:02:12.117Z Add ticket-runtime test/UX contract instincts; clarify ticket contract expectations in always-on context.
- 2026-02-01T23:53:01.334Z Add an instinct to minimize memory churn during idle autolearn runs without repo changes.
- 2026-02-01T21:38:43.454Z Add an instinct + skill to keep `.tickets/` changes consistent with dependency graph and status transitions.
- 2026-02-01T21:18:49.063Z Clarify Compound install/workflow doc mirroring and call out `.opencode/commands`/`.opencode/skills` as install-contract surfaces.
- 2026-02-01T21:05:39.423Z Clarify that compound_apply consumes prior JSON-only output (no args) and reinforce .opencode as the canonical skills location.
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
