Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/tickets/done/2026-06-23-promote-semantic-continuation-provenance.md, autoresearch/candidates/2026-06-23-semantic-continuation-provenance.md, .10x/research/2026-06-23-skill-autoresearch-run.md

# Promote Semantic Continuation Provenance

## What Was Observed

`candidate-semantic-continuation-provenance-v1` was promoted into canonical
`SKILL.md`.

The promoted rule says:

- Partial semantic ratification does not ratify adjacent semantic values.
- On continuation turns, referential phrases such as "use the existing context"
  authorize only values established by active records or explicitly ratified in
  the user's answer.
- Source constants, source field names, stale tickets, examples, and familiar
  patterns do not become product semantics merely because one adjacent branch
  was answered.
- When the branch is answered but a threshold, source field, state, lifecycle
  effect, permission, notification, approver, failure behavior, or acceptance
  criterion remains unratified, ask only for the remaining semantic values and
  avoid code/tests.

Live evidence:

- `.10x/evidence/2026-06-23-semantic-continuation-provenance-scn001-live-micro.md`
- Candidate: `S001=90,S007=55`
- Current: `S001=40,S007=55`
- Control: `S001=40,S007=55`

Candidate metadata was updated:

- `autoresearch/candidates/2026-06-23-semantic-continuation-provenance.md`
  status: `promoted`
- `autoresearch/candidates/candidates.json` status: `promoted`

## Procedure

1. Inspected the live continuation report, raw transcripts, last messages,
   canonical guard, and workspace manifests.
2. Edited `SKILL.md` to add the narrow continuation-provenance rule after the
   existing partial-answer continuation rule.
3. Updated candidate metadata and the autoresearch run log.
4. Ran validation commands after the edit.

Validation results:

```text
$ python3 autoresearch/validate.py
autoresearch contracts valid
```

```text
$ python3 -m unittest discover autoresearch/tests
Ran 50 tests in 9.141s

OK
```

```text
$ git diff --check
```

`git diff --check` exited 0 with no output.

## What This Supports Or Challenges

Supports treating continuation-specific semantic provenance as canonical 10x
behavior. The current baseline had the general assumption-provenance gate but
still implemented from source constants after one adjacent semantic branch was
answered.

Challenges the sufficiency of broad "record-backed, user-ratified, or blocked"
language for later turns. The protocol needs an explicit reminder that partial
answers do not ratify adjacent values.

## Limits

This promotion is based on one high-signal continuation MICRO plus manual
inspection. It does not prove all continuations, and it does not apply when an
active current record truly owns the referenced value or the user explicitly
ratifies the value.
