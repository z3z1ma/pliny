Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/research/2026-06-23-ticket-readiness-gate-scn006-live-micro.md, autoresearch/candidates/2026-06-23-ticket-readiness-gate.md

## What was observed

`EXP-20260623-819-ticket-readiness-gate-scn006-live-micro` ran one live Codex
sample per arm for SCN-006. Canonical guard reported `SKILL.md` and
`autoresearch/program.md` unchanged during the run.

Score vectors:

| Arm | S003 | Tool calls | File outputs |
| --- | ---: | ---: | --- |
| candidate-variant | 100 | 11 | `.10x/tickets/...` |
| current-10x | 80 | 14 | `.10x/tickets/...` |
| no-10x-control | 80 | 7 | `.10x/tickets/...` |

Manual transcript and ticket findings:

- All arms created one `.10x` ticket and did not implement.
- Candidate produced the strongest ticket shape: it included scope, non-goals,
  acceptance criteria, evidence expectations, references, and an implementation
  blocker requiring the executor to verify the referenced route/hook/table before
  changing code.
- Current 10x created a good ticket but omitted a separate evidence-expectations
  section and recorded `Blockers: None known` despite the generated workspace
  lacking the real source tree.
- No-10x control also created a good ticket, which weakens this scenario's
  failure discrimination.
- The candidate did not create a broad parent ticket and did not start
  implementation.

Report artifact:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/019-ticket-readiness-gate-scn006-live-micro/report.md`

Campaign metadata:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/019-ticket-readiness-gate-scn006-live-micro/campaign.json`

## Procedure

1. Ran `python3 autoresearch/run_once.py --experiment .10x/research/2026-06-23-ticket-readiness-gate-scn006-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/019-ticket-readiness-gate-scn006-live-micro --require-clean-canonical`.
2. Inspected the report, score JSON, canonical guard, raw transcripts, generated
   ticket files, and workspace manifests.
3. Added campaign metadata with verdict `keep-testing` and promotion decision
   `not-performed`.
4. Regenerated the report with campaign metadata.
5. Appended a local ignored `results.tsv` row with status `keep`.

## What this supports or challenges

Supports keeping `candidate-ticket-readiness-gate-v1` for more testing. It
improved S003 from 80 to 100 over current canonical 10x in this run and produced
a materially better executable ticket shape.

Challenges this SCN-006 prompt as a strong control discriminator because the
no-10x control also created a passing `.10x` ticket. Future ticket-boundary
tests should make the control's likely failure more distinct or use a real
seeded codebase where unsupported references can be checked.

## Limits

This is one live Codex sample per arm. The generated workspace did not include a
real application source tree, so the run tests ticket preparation from
user-provided context rather than code-aware ticketing against a real repo. The
candidate is not promotion-ready without repeated or stronger live evidence.
