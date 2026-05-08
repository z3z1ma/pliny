# Documentation Sync

Use this reference when documentation surfaces need to mirror Loom owner truth.

## Routing Matrix

| Documentation need | Loom owner to check first |
| --- | --- |
| durable principle, policy, expensive architecture choice, ADR-like precedent | constitution decision |
| intended behavior or API contract | spec |
| accepted architecture/workflow/troubleshooting explanation | wiki |
| investigation, alternatives, rejected options | research |
| live docs task, blocker, follow-up, closure | ticket |
| observed command output or screenshot | evidence |
| release note, changelog draft, PR summary | ship package mirroring owner records |
| support-only retrieval cue | memory |

Docs outside `.loom` can mirror or present owner truth, but they do not silently
own it unless the constitution says so.

## Decision Mentions

When documentation needs to mention a durable decision, link the constitution
decision record or summarize it as a mirror. Do not create a parallel ADR store in
the docs tree.

A safe decision mention includes:

- the decision ID or accepted decision link
- a short current consequence
- supersession or version caveat when relevant
- a pointer back to the owner record for alternatives and rationale

## Inline Comments

Comment the why:

- compatibility constraint
- security boundary
- performance tradeoff
- non-obvious ordering requirement
- link to accepted decision or wiki page for a deeper rationale

Avoid comments that restate the code, commented-out old code, or TODOs that should
be tickets.

## API Documentation

For public or shared APIs, mirror the spec-owned contract for:

- input schema and validation
- output shape
- error codes and semantics
- auth/permission expectations
- pagination/filtering/sorting where relevant
- idempotency and side effects
- examples
- version, deprecation, or migration status

If this information defines intended behavior, it belongs in a spec first.

## README And Setup Docs

Check:

- project purpose in one paragraph
- quick start
- install/setup commands
- environment variables without secrets
- test/lint/build/dev commands
- architecture overview and owner-record links
- contribution/review/release workflow if relevant
- troubleshooting links for recurring issues

Commands that are presented as current should be verified or marked unverified.

## Changelog And Release Notes

Changelog entries should mirror accepted ticket truth:

- Added
- Changed
- Fixed
- Removed
- Deprecated
- Security

Do not announce removal before migration evidence and reference reconciliation are
truthful. Use `loom-ship` for packaging release wording.

## Path-Local Agent Context

Path-local instruction files can help agents retrieve owner records. They should
point at Loom records, not define competing truth.

Safe pattern:

```markdown
This file is a context adapter, not a truth owner.

Read:
- wiki:<accepted-page>
- spec:<behavior-contract>
- decision:<decision-id>
```

## Verification

- link targets and IDs resolve
- commands are fresh or marked stale
- docs mirror owner records
- no secrets or sensitive data are included
- no stale references to removed paths remain
- TODOs became tickets or were removed
