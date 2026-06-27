Status: done
Created: 2026-06-27
Updated: 2026-06-27
Depends-On:

# Current Skill Complex Autoresearch Trials

## Scope

Run two to three richer current-skill autoresearch trials using the active
live-trial scientist workflow.

Included:

- Use the current canonical `SKILL.md` as the only subject instruction arm.
- Register experiments with explicit `scientific_contract`, exact `arms`,
  scenario provenance, and budget.
- Prefer existing `autoresearch/trial-seeds/` scenarios that exercise complex
  10x behavior, not trivial typo edits.
- Run the trials through the active runner/tooling.
- Inspect raw artifacts, reports, command metadata, workspace manifests, and
  changed files.
- Record scientific findings, rubric/scoring judgments, limits, and tooling
  ergonomics observations.

Excluded:

- Mutating canonical `SKILL.md`.
- Adding candidate variants.
- Reintroducing static scoring or calibration-only paths.
- Promoting any instruction change.

## Acceptance Criteria

- AC-001: Two to three current-skill trial definitions are registered and run or
  an explicit evidence-backed blocker explains why fewer completed.
- AC-002: Each completed trial has preserved runner artifacts under
  `.10x/evidence/.storage/`.
- AC-003: The final report records scientific findings, rubric/scoring
  judgments, and limits.
- AC-004: The final report records tooling ergonomics: what was clear, what was
  difficult, confusing, missing, or guess-prone.
- AC-005: The sub-agent preserves evidence paths and does not mutate
  canonical `SKILL.md`.

## Progress and Notes

- 2026-06-27: Opened to own fresh-context sub-agent execution requested by the
  user.
- 2026-06-27: Registered and ran three current-skill MICRO trials:
  `EXP-20260627-101-current-skill-source-record-conflict`,
  `EXP-20260627-102-current-skill-closure-reference-integrity`, and
  `EXP-20260627-103-current-skill-skill-authoring-retrospective`. Durable
  evidence and manual scientist scoring recorded in
  `.10x/evidence/2026-06-27-current-skill-complex-autoresearch-trials.md`.
  All three `canonical_guard.json` reports show `SKILL.md` and
  `autoresearch/program.md` unchanged during each run.

## Blockers

None.
