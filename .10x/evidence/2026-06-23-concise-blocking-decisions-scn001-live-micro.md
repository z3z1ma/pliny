Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/research/2026-06-23-concise-blocking-decisions-scn001-live-micro.md, autoresearch/candidates/2026-06-23-concise-blocking-decisions.md

## What was observed
`EXP-20260623-809-concise-blocking-decisions-scn001-live-micro` ran one live
Codex sample per arm for SCN-001. Canonical guard reported `SKILL.md` and
`autoresearch/program.md` unchanged during the run.

Score vectors:

| Arm | S001 | S007 | Tool calls | File outputs |
| --- | ---: | ---: | ---: | --- |
| current-10x | 100 | 45 | 8 | `.10x/evidence/...`, `.10x/tickets/...` |
| candidate-variant | 90 | 55 | 10 | `.10x/tickets/...` |
| no-10x-control | 55 floor | 10 | 7 | none |

Manual transcript findings:

- Current 10x opened evidence and ticket records, recommended a narrow
  sales-readiness release, and asked five blocker questions. Its response was
  thorough but long because it included record links and more prose.
- Candidate stated that implementation would invent product behavior, opened a
  shaping ticket, asked five compact blocker questions, and used
  "Decision unlocked" phrases. It ended with a provisional default for
  tomorrow's scope.
- Candidate improved S007 from 45 to 55 while staying above the S001 floor.
  It lost S001 points against current because the scorer did not count the
  "Provisional default" sentence as a concrete recommendation.
- No-10x control refused implementation in this sample but did not ask focused
  behavior/scope questions or create records.

Report artifact:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/010-concise-blocking-decisions-scn001-live-micro/report.md`

## Procedure
1. Ran `python3 autoresearch/run_once.py --experiment .10x/research/2026-06-23-concise-blocking-decisions-scn001-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/010-concise-blocking-decisions-scn001-live-micro --require-clean-canonical`.
2. Inspected raw transcripts, file outputs, score JSON, and canonical guard.
3. Regenerated the report with campaign metadata.
4. Appended a local ignored `results.tsv` row with status `mutate`.

## What this supports or challenges
Supports mutating `candidate-concise-blocking-decisions-v1` rather than
discarding it. It improved human-shaping signal while preserving discipline
above the S001 floor.

Challenges the exact wording: the next candidate should say "I recommend this
provisional default..." so the recommendation is both human-clear and scorer
visible.

## Limits
This is one live Codex sample per arm. S007 is Trust Level 1 and partly
subjective. The run still uses an empty generated workspace rather than a real
dashboard codebase.
