# Candidate: Deletion Before Accommodation

Candidate ID: `candidate-deletion-before-accommodation-v1`
Created: 2026-06-24
Canonical target: `SKILL.md`
Status: experimental
Promotion: manual-only

## Target Behavior

When a bug or feature request tempts the agent to add coordination logic,
feature flags, compatibility layers, deduplication state, adapters, or another
guard around duplicate behavior, the agent should first check whether one path
is obsolete. If active records, tests, or source ownership show that a stale
path should not exist, the smallest correct solution is usually deletion, not
accommodation.

## Proposed Instruction Overlay

Add near Operational Minimalism or Execute Only the Ticket's Outcome:

```text
Prefer deletion before accommodation. When requested work is caused by duplicate
paths, legacy compatibility code, obsolete branches, or overlapping ownership,
do not add guards, feature flags, dedup stores, adapters, or coordination state
until you have checked whether one path should be removed.

If active records or current tests establish one canonical path and one retired
or redundant path, implement or ticket removal of the retired path. Name the
active authority and the obsolete path. Do not preserve dead compatibility "just
in case"; that is speculative complexity.

If the user explicitly asks to keep a path that active records say is retired,
treat it as a supersession question before implementing accommodation.
```

## Expected Score Movement

- S005 Minimal Implementation: should improve by steering the agent toward
  deletion instead of extra coordination code.
- S003 Ticket Fitness: should improve if executable tickets name the obsolete
  path rather than adding vague dedup work.
- S007 Human Shaping Quality: should improve by giving a principal-engineer
  recommendation that challenges the tempting but more complex fix.

## Scenario Coverage

Primary scenario:

- SCN-010: duplicate incident notifications where active records establish
  PagerDuty as the only current incident-alert path and the legacy email bridge
  is retired, while the prompt suggests a dedup guard or feature flag.

Secondary scenarios:

- SCN-006: ticket boundary when deletion is the actual scope.
- SCN-005: record economy when no new abstraction is needed.

## Expected Failure Modes

- Null result because current `SKILL.md` already follows the execution ladder
  and deletes the obsolete path.
- Over-deletion when active records do not actually establish that a path is
  retired.
- Supersession miss if the user explicitly asks to keep a path that active
  records reject.

## Promotion Boundary

Promote only if current canonical 10x adds or tickets accommodation logic, keeps
both paths alive without authority, or fails to name deletion as the smallest
correct fix while the candidate removes or scopes removal of the retired path.
Discard if current already deletes or tickets deletion correctly.
