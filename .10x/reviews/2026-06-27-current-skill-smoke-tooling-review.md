Status: recorded
Created: 2026-06-27
Updated: 2026-06-27
Target: .10x/evidence/2026-06-27-current-skill-smoke-trial.md
Verdict: concerns
Relates-To: .10x/decisions/autoresearch-live-trial-scientist-inspection.md, .10x/specs/10x-autoresearch-loop.md

# Review: Current Skill Smoke Trial Tooling

## Verdict

Concerns.

The happy path is functional and the run artifacts are rich enough to inspect
the result. The ergonomics are not yet completely self-explanatory for a fresh
scientist.

## Findings

Significant: one-arm current-skill regression mode depends on the undocumented
`evaluation_only` field. The user intent was one trial of current `SKILL.md`,
but the documented experiment shape defaults to three arms, and the code only
allows arbitrary arm sets when `evaluation_only: true` is present. This required
code inspection and inference.

Significant: the active autoresearch spec still contains older numeric scorer,
score-vector, scorer-trust, and top-line-index requirements. The newer active
decision and current tooling correctly use live trial artifacts plus scientist
inspection, but the active spec can still steer a reader back toward removed
scorer semantics.

Minor: the JSON runner definition is too thin to be a self-contained scientific
registration. The smoke experiment definition captured arm, scenario, seed,
prompt, and budget, but not the hypothesis, expected pass behavior, inspection
checks, quality floor, or verdict destination. Those lived in the scientist's
head and the post-run evidence record.

Minor: the report faithfully shows the subject's last message, including a link
to the temporary execution workspace. That temp path is not the durable archived
workspace path, so the report can appear to cite an artifact that no longer
exists.

Minor: the happy path still requires hand-selecting the experiment definition
path, output root, run tag, and seed path. This is acceptable for careful
research, but a smoke/regression command shape or documented recipe would reduce
mechanical error.

## Strengths

- `run_once.py` executed exactly one live trial and wrote plan, summary, report,
  raw, command, prompt, and archived workspace artifacts.
- `canonical_guard.json` confirmed `SKILL.md` and `autoresearch/program.md` were
  unchanged during the run.
- The workspace manifest made pass/fail inspection easy: one changed file,
  no timeout, no suppressed instruction contamination, one completed turn.
- The raw artifact preserved transcript, tool events, command metadata, token
  usage, workspace references, and the seed path.
- The renamed `autoresearch/trial-seeds/` path worked end to end.

## Residual Risk

The current tooling is good enough for careful use by a scientist who is willing
to inspect code and artifacts. It is not yet "obvious mode" for a cold-start
scientist who only reads the active program, README, template, and spec.
