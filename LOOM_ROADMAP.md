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
