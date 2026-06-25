Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Target: .10x/research/2026-06-25-skill-source-path-shape-scn012-live-micro.md
Verdict: concerns

# Skill Source Path Shape Result Review

## Target

`EXP-20260625-990-skill-source-path-shape-scn012-live-micro` and
`candidate-skill-source-path-shape-v1`.

## Findings

- Significant: Candidate improved source path shape on the target MICRO. It
  produced directory-shaped `SKILL.md` source skills in both repetitions, while
  current produced one flat `.10x/skills/<slug>.md` source skill.
- Significant: Candidate is not ready for promotion. It used
  `.10x/skills/replay-ledger-import-fixtures/SKILL.md` in one repetition, which
  satisfies the directory-shaped source-path hypothesis but not the experiment's
  exact slug expectation.
- Significant: Harness-native mirror regressions remain untested with this
  candidate. Promotion would be premature until `.claude`, `.opencode`, and
  `.agents` mirror behavior still passes.
- Pass: No arm created speculative mirror directories in the no-native-dir
  workspace.
- Minor: S006 stayed below floor for current and candidate because the parent
  stayed active for residual closure work. Manual inspection treats this as a
  scorer mismatch for this narrow path-shape target.

## Verdict

Concerns raised. Keep the candidate active for targeted mirror regressions; do
not promote yet.

## Residual Risk

The eventual promoted wording may need to pair source path shape with slug
stability when a governing skill, ticket, prompt, or existing record names a
specific slug. Do not broaden this candidate until the mirror regressions show
the narrow path rule is safe.
