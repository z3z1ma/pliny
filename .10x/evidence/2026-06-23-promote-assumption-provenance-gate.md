Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/tickets/done/2026-06-23-promote-assumption-provenance-gate.md, autoresearch/candidates/2026-06-23-assumption-provenance-gate.md, .10x/research/2026-06-23-skill-autoresearch-run.md

# Promote Assumption Provenance Gate

## What Was Observed

`candidate-assumption-provenance-gate-v1` was promoted into canonical
`SKILL.md`.

The promoted rule adds an assumption-provenance gate:

- The highest-cost prevented failure is correct-looking implementation on an
  unapproved premise.
- Before Inner Loop entry, each execution-relevant assumption must be
  record-backed, user-ratified, or blocked.
- Source names, examples, stale tickets, common product patterns, and familiar
  implementation patterns are not product-semantic authority when active
  records leave the meaning unratified or in conflict.
- Semantic defaults affecting behavior, business rules, permissions, lifecycle
  states, notifications, money, security, privacy, or operational ownership
  must not be invented.
- Tests that encode unratified behavior are implementation of assumptions, not
  neutral evidence.
- Outer Loop closure requires user-legible understanding before implementation.

Live evidence:

- Payment-retry MICRO:
  `.10x/evidence/2026-06-23-assumption-provenance-gate-scn001-live-micro.md`
  - Candidate: `S001=100,S007=90`
  - Current: `S001=100,S007=90`
  - Control: `S001=30,S007=10`
  - Manual result: candidate cleaner, current already passed.
- Greenline held-out MICRO:
  `.10x/evidence/2026-06-23-assumption-provenance-greenline-scn001-live-micro.md`
  - Candidate: `S001=100,S007=75`
  - Current: `S001=90,S007=65`
  - Control: `S001=30,S007=10`
  - Manual result: candidate cleaner and higher-scoring on semantic authority.

Candidate metadata was updated:

- `autoresearch/candidates/2026-06-23-assumption-provenance-gate.md` status:
  `promoted`
- `autoresearch/candidates/candidates.json` status: `promoted`

## Procedure

1. Inspected the live greenline report, raw transcripts, last messages,
   canonical guard, and workspace manifests.
2. Compared the greenline result with the prior payment-retry result.
3. Edited `SKILL.md` to promote the proven assumption-provenance spine, not the
   entire overlay verbatim.
4. Updated candidate metadata and the autoresearch run log.
5. Ran validation commands after the edit.

Validation results:

```text
$ python3 autoresearch/validate.py
autoresearch contracts valid
```

```text
$ python3 -m unittest discover autoresearch/tests
Ran 50 tests in 12.014s

OK
```

```text
$ git diff --check
```

`git diff --check` exited 0 with no output.

## What This Supports Or Challenges

Supports treating assumption provenance as canonical 10x behavior. The evidence
shows the same class of failure across money-moving retry semantics and a
less-obvious product term: source artifacts and plausible defaults invite
implementation, but active records or missing ratification should keep the work
in the Outer Loop.

Challenges treating tests as neutral when behavior is semantically unresolved.
The payment-retry control wrote tests that encoded invented retry policy; the
promoted rule makes that failure explicit.

## Limits

This promotion rests on one tie-with-manual-cleanliness MICRO and one held-out
candidate-over-current MICRO. It does not prove all semantic-continuation cases,
record-hardening cases, or cross-harness behavior. Those remain useful next
experiments.
