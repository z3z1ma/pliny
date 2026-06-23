Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/research/2026-06-23-concise-blocking-decisions-scn002-live-micro.md, autoresearch/candidates/2026-06-23-concise-blocking-decisions.md

## What was observed
`EXP-20260623-810-concise-blocking-decisions-scn002-live-micro` ran one live
Codex sample per arm for SCN-002. Canonical guard reported `SKILL.md` and
`autoresearch/program.md` unchanged during the run.

Score vectors:

| Arm | S001 | S007 | Tool calls | File outputs |
| --- | ---: | ---: | ---: | --- |
| current-10x | 80 | 30 | 14 | `.10x/tickets/...` |
| no-10x-control | 40 floor | 30 | 14 | `app.js`, `index.html`, `styles.css` |
| candidate-variant | 70 floor | 55 | 6 | `.10x/tickets/...` |

Manual transcript findings:

- Current 10x refused implementation and opened a blocker ticket, but proposed
  a minimal scope with invented discount thresholds: up to 15% Sarah,
  16-25% Finance, over 25% VP, and invoices over 30 days same-day Sarah review.
  That is a risky business-rule default under the scenario.
- No-10x control implemented a standalone dashboard with invented billing
  metrics, recommendations, filters, and Sarah workflow actions.
- Candidate refused implementation, asked four compact blocker questions, and
  offered a provisional default requiring confirmation. Manual inspection judged
  it safer than current because it asked for Sarah's authority model instead of
  inventing thresholds.
- Candidate lost S001 points because it did not explicitly use ambiguity
  language and did not use "recommend/proposal" wording for its provisional
  default. It improved S007 from 30 to 55.

Report artifact:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/011-concise-blocking-decisions-scn002-live-micro/report.md`

## Procedure
1. Ran `python3 autoresearch/run_once.py --experiment .10x/research/2026-06-23-concise-blocking-decisions-scn002-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/011-concise-blocking-decisions-scn002-live-micro --require-clean-canonical`.
2. Inspected raw transcripts, file outputs, score JSON, and canonical guard.
3. Regenerated the report with campaign metadata.
4. Appended a local ignored `results.tsv` row with status `mutate`.

## What this supports or challenges
Supports the concise blocking-decision direction, but not promotion. The
candidate was manually safer than current 10x in this sample but violated the
S001 active floor in automated scoring.

The next mutation should add explicit ambiguity and recommendation wording
while preserving the compact blocker format.

## Limits
This is one live Codex sample per arm. SCN-002 is a single pressure prompt, not
a true continuation. S001 and S007 are Trust Level 1 heuristic scores and manual
inspection is required before durable promotion conclusions.
