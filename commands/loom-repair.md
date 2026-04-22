---
name: loom-repair
description: "Fix graph drift across the Loom workspace: broken references, stale supersessions, status-vs-journal mismatches, orphan packets, owner-layer conflicts, and structural record failures. Apply safe repairs, route the rest."
arguments: "<scope path | record id | blank for whole workspace>"
category: core
suggested_skills:
  - loom-workspace
  - loom-records
  - loom-tickets
  - loom-constitution
  - loom-specs
  - loom-wiki
  - loom-critique
---

# /loom-repair

You are running **Loom Repair**.

Repair scope:
`$ARGUMENTS`

This command is the explicit graph-hygiene surface.
Use it when `/loom-status` has surfaced drift that nothing has fixed, when a scan should walk the tree periodically, or when a specific record or path needs reference reconciliation.

Hydrate only what you need from:
- `loom-workspace`
- `loom-records`
- `loom-tickets`
- `loom-constitution`
- `loom-specs`
- `loom-wiki`
- `loom-critique`

## Scope

- if `$ARGUMENTS` is blank, scan the whole `.loom/` tree
- if `$ARGUMENTS` names a path or record ID, narrow the scan to that slice and its immediate links

Narrow scans are preferred for routine hygiene. Whole-workspace scans are for periodic passes.

## Drift classes

1. **Broken references.** Typed IDs that no longer resolve to an existing record.
2. **Stale supersessions.** Records marked superseded whose forward link is missing, or successors that do not acknowledge the predecessor.
3. **Status-vs-journal mismatches.** `active` tickets with no recent journal activity; `blocked` tickets with no named blocker; `complete_pending_acceptance` without evidence or critique disposition.
4. **Orphan packets.** Packets whose target ticket is closed or deleted, or packets in `compiled` state without a corresponding child output after a long gap.
5. **Owner-layer conflicts.** A plan carrying live execution state. A wiki page carrying behavior-contract authority. Memory carrying canonical facts. A ticket redefining policy.
6. **Structural record failures.** Missing frontmatter fields, filename-vs-ID mismatches, malformed typed IDs.
7. **Dangling follow-up.** Critique findings that required follow-up with no corresponding ticket; tickets referencing deferred critique that never happened.

## Goals

- classify drift per class with inspectable evidence
- apply only the repairs that are genuinely safe
- route everything else to the right owner skill
- leave the repair trail visible, not silent

## Procedure

1. **Walk the scope.**
   - `find .loom -type f -name '*.md' | sort`
   - `rg -n '^(id|kind|status|links|target):' .loom --glob '*.md'`

2. **Collect findings per class.**
   - Keep evidence with each finding: the file path, the line, and what made you classify it.

3. **Classify repair risk.**
   - **Safe**: broken reference with an obvious rename target, superseded-link repair, filename-vs-ID typo, dead reference in a clearly retired record.
   - **Route**: anything that changes owner-layer truth, reopens a closed ticket, amends constitution, rewrites a wiki page, or invalidates a critique verdict.

4. **Apply safe repairs one batch at a time.**
   - Write them out, verify with a second pass (`rg` the fixed refs, read the changed records).
   - Do not bundle unrelated repairs into one opaque edit.

5. **Route everything else.**
   - Owner-layer conflicts → `/loom-spec`, `/loom-decide`, `/loom-wiki`, or `/loom-ticket`, usually disciplined by `/loom-plan`.
   - Status-vs-journal mismatches → `/loom-ticket` or `/loom-accept`.
   - Orphan packets → `/loom-work` to close out, or mark the packet superseded.
   - Constitutional contradictions → `/loom-decide` to amend or supersede precedent explicitly.
   - Dangling critique follow-up → `/loom-ticket` to create the follow-up.

6. **Leave the repair trail.**
   - Note what was fixed, what was routed, and what remains open.
   - If a repair was non-trivial, consider `/loom-review` on the result.

## Native tools to prefer

- `find .loom -type f -name '*.md' | sort`
- `rg -n '^id:' .loom --glob '*.md'`
- `rg -n '<kind>:<id>' .loom --glob '*.md'`
- `rg -n '^status:' .loom/tickets --glob '*.md'`
- `git log --oneline -- .loom/ | head -20`
- `git diff --stat`

## Guardrails

- Fail closed when ownership is ambiguous; surface the conflict and route, do not guess.
- Do not rewrite canonical records silently; safe repairs are for broken-link hygiene, not semantic edits.
- Do not reconcile contradictions by deletion; rename, supersede with forward links, or amend with explicit reasoning.
- Do not treat recency as truth; the owning layer decides.
- Do not widen scope mid-pass; note larger drift and route rather than triggering an unbounded rewrite.

## Required output

- drift findings table (class, record, evidence, proposed action, risk)
- safe repairs applied, with paths and one-line summaries
- routed findings with the recommended next command per finding
- residual drift that cannot be fixed from here and why
- recommended next command
