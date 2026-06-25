Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Target: .10x/research/2026-06-25-skill-authoring-no-native-dir-scn012-live-micro.md
Verdict: concerns

# Skill Authoring No Native Dir Result Review

## Target

`EXP-20260625-989-skill-authoring-no-native-dir-scn012-live-micro`

## Findings

- Pass: Current `SKILL.md` satisfied the no-native-dir control. It created the
  expected `.10x/skills/<slug>/SKILL.md` source skill, updated the parent ticket
  to record the absence of a harness exposure target, and avoided speculative
  mirror directories.
- Significant: The duplicate-current arm wrote
  `.10x/skills/ledger-import-fixture-replay.md` instead of
  `.10x/skills/ledger-import-fixture-replay/SKILL.md`. This failed the manual
  skill source-path floor and suggests the source path shape should be made
  more salient before promotion.
- Minor: Current's S006 score was below floor, but manual inspection shows the
  parent intentionally remained active because residual closure work was outside
  the request. Treat that score as a heuristic false negative.
- Pass: No arm created `.claude`, `.agents`, `.opencode`, or another harness
  mirror directory.

## Verdict

Concerns raised. Current passed the primary no-native-dir arm, but the
duplicate-current source-path failure justifies a targeted candidate experiment
before any `SKILL.md` promotion.

## Residual Risk

A narrow source-path rule could improve skill authoring reliability, but it must
not weaken existing `.claude`, `.opencode`, and `.agents` mirroring behavior or
encourage product changes in this repo's internal `.10x/skills/` directory.
