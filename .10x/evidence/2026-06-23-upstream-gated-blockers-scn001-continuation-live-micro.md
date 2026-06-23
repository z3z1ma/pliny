Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/research/2026-06-23-upstream-gated-blockers-scn001-continuation-live-micro.md, autoresearch/candidates/2026-06-23-upstream-gated-blockers.md

## What was observed
`EXP-20260623-816-upstream-gated-blockers-scn001-continuation-live-micro`
continued from the actual raw artifacts produced by
`EXP-20260623-814-upstream-gated-blockers-scn001-live-micro`. Each arm received
an answer tailored to its actual first-turn questions.

Canonical guard reported `SKILL.md` and `autoresearch/program.md` unchanged
during the run.

Score vectors:

| Arm | S001 | S007 | Tool calls | File outputs |
| --- | ---: | ---: | ---: | --- |
| current-10x | 100 | 35 | 15 | `.10x/evidence/...`, `.10x/specs/...`, `.10x/tickets/...` |
| candidate-variant | 100 | 80 | 11 | `.10x/specs/...`, `.10x/tickets/...` |
| no-10x-control | 40 floor | 20 | 3 | `enterprise-billing-pricing-exceptions-spec-ticket.md` |

Manual transcript findings:

- Candidate preserved implementation blocking, created a draft `.10x` spec, and
  updated the shaping ticket without creating a prototype or implementation
  ticket.
- Candidate made the remaining blockers explicit: missing real dashboard
  codebase/artifact, no implementation authorization, and sales validation still
  required.
- Current 10x also behaved safely, but its final response was longer and scored
  lower on S007.
- No-10x control created a non-`.10x` combined spec/ticket file, triggering the
  S001 floor for file output in this scenario.
- Raw artifacts report `harness_metadata.prior_turn_count=1` for each arm.

Report artifact:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/017-upstream-gated-blockers-scn001-continuation-live-micro/report.md`

## Procedure
1. Registered an experiment with `prior_raw_paths` from
   `EXP-20260623-814-upstream-gated-blockers-scn001-live-micro`.
2. Wrote `prompts_by_arm` by reading each arm's actual first-turn questions.
3. Ran `python3 autoresearch/run_once.py --experiment .10x/research/2026-06-23-upstream-gated-blockers-scn001-continuation-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/017-upstream-gated-blockers-scn001-continuation-live-micro --require-clean-canonical`.
4. Inspected combined transcripts, file outputs, score JSON, and canonical
   guard.
5. Regenerated the report with campaign metadata.
6. Appended a local ignored `results.tsv` row with status `keep`.

## What this supports or challenges
Supports keeping `candidate-upstream-gated-blockers-v1` as the leading
candidate. It preserved the dynamic continuation behavior while improving S007
over current 10x.

## Limits
Continuation scores still use first-turn S001/S007 heuristics and require
manual inspection. The answer intentionally withheld implementation
authorization, so this does not test transition into a fully executable
implementation ticket.
