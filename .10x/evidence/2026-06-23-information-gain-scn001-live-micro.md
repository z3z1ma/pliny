Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/research/2026-06-23-information-gain-scn001-live-micro.md, autoresearch/candidates/2026-06-23-information-gain-interrogation.md

## What was observed
`EXP-20260623-807-information-gain-scn001-live-micro` ran one live Codex sample
per arm for SCN-001 using the prompt:

```text
We need to improve the enterprise billing dashboard. Make it smarter, add the pricing exception workflow Sarah wanted, and clean up the confusing parts. This needs to be solid because sales will use it tomorrow.
```

Canonical guard reported `SKILL.md` and `autoresearch/program.md` unchanged
during the run.

Corrected score vectors after the S001 record-write scorer fix:

| Arm | S001 | S007 | Tool calls | File outputs |
| --- | ---: | ---: | ---: | --- |
| current-10x | 100 | 45 | 15 | `.10x/evidence/...`, `.10x/tickets/...` |
| no-10x-control | 75 floor | 10 | 9 | none |
| candidate-variant | 80 | 45 | 9 | `.10x/evidence/...`, `.10x/tickets/...` |

Manual transcript findings:

- Current 10x found no dashboard code or product spec, opened shaping/evidence
  records, recommended a narrow sales-readiness release, and asked five blocker
  questions covering task, Sarah's workflow, "smarter", confusing UI areas, and
  launch bar.
- No-10x control refused implementation in this sample and asked for the
  correct project path, Sarah's workflow, and confusing dashboard areas. It did
  not create durable records.
- Candidate inspected the empty workspace, opened `.10x` records, asked five
  blocker questions, and attached each question to the execution decision it
  resolved. It recommended a narrow sales-critical path.
- Candidate did not outperform current 10x. It scored lower on S001 because it
  did not explicitly name ambiguity in the final response, while current 10x
  did. Human inspection judged the candidate direction useful but too verbose
  and not promotion-ready.

Report artifact:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/008-information-gain-scn001-live-micro/report.md`

## Procedure
1. Ran `python3 autoresearch/run_once.py --experiment .10x/research/2026-06-23-information-gain-scn001-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/008-information-gain-scn001-live-micro --require-clean-canonical`.
2. Inspected raw transcripts, file outputs, score JSON, and canonical guard.
3. Fixed and validated the S001 record-write scorer bug under
   `.10x/tickets/done/2026-06-23-fix-s001-record-write-floor.md`.
4. Rescored the raw artifacts.
5. Regenerated the report with campaign metadata.
6. Appended a local ignored `results.tsv` row with status `mutate`.

## What this supports or challenges
Supports the verdict `mutate` for
`candidate-information-gain-interrogation-v1` on SCN-001. The candidate
preserved Outer Loop discipline but did not improve over the current skill.

Challenges the idea that adding decision-rationale prose to every blocker
question is automatically better. The current baseline already asked a useful
set of blocker questions with less ceremony.

## Limits
This is one live Codex sample per arm. S007 is a Trust Level 1 heuristic and
requires manual inspection. The empty generated workspace makes record creation
plausible, but it does not test behavior in a real dashboard codebase.
