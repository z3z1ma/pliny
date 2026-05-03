# Status Snapshot

A status snapshot synthesizes current Loom state without mutating records.

It tells the operator what is live, blocked, waiting for critique, waiting for
acceptance, suspicious, or ready for the next bounded move.

## Inputs

- `constitution:main`
- tickets grouped by status
- linked plans, specs, research, critique, wiki, evidence, and packets
- optional `.loom/workspace.md`, `.loom/harness.md`, and `.loom/support/`
  artifacts linked or cited by owner records
- current git status when repository changes matter

## Procedure

1. Confirm the workspace root and `.loom/` tree.
2. Read only enough constitution and owner context to avoid wrong routing.
3. List tickets in `ready`, `active`, `blocked`, `review_required`, and
   `complete_pending_acceptance`.
4. For the target slice, note linked owners and support records.
5. Surface contradictions and drift.
6. Recommend the next owner layer or workflow route. When naming a
   route value, use the shared tokens from
   `skills/loom-records/references/route-vocabulary.md`.

## Cold-Start And Post-Compaction Resume Route

Use this route when entering a Loom workspace without reliable transcript
context, after context compaction, or when asked to recover current work from
files.

1. Load `loom-bootstrap` doctrine, or confirm the harness already preloaded the
   ordered bootstrap references.
2. Confirm the workspace root and `.loom/` tree, then read `constitution:main`.
3. Discover the active ticket queue and other live states from ticket records:

   ```bash
   rg -n '^status: (active|blocked|review_required|complete_pending_acceptance)\b' .loom/tickets --glob '*.md'
   ```

   Add `ready` when the operator asks for available next work rather than work
   already in flight.
4. For each relevant ticket, read its upstream owner chain: initiative, research,
   spec, plan, and any cited packet or support records needed to understand the
   next route. `.loom/workspace.md`, `.loom/harness.md`, and saved
   `.loom/support/` artifacts are optional support context, not canonical owners.
5. Inspect evidence and critique only as needed to evaluate the ticket's current
   acceptance, review, blocker, or next-route disposition.
6. Continue from the owning records. If chat history, transcript memory, memory
   files, generated context, or an external tracker disagrees with the owner
   records, treat the owner records as canonical and route the mismatch to the
   layer that owns the fact.

Normal workspace entry can resume a bounded ticket or status queue without
invoking the full `loom-drive` loop. Use `loom-drive` when the work is a
high-level objective continuation that needs an anchor, tranche coordination, or
checkpoint fields across multiple routes.

## Pre-Compaction Owner Update Check

Before ending a session, compacting context, or handing off after meaningful
work, update the existing owners that make recovery truthful:

- ticket: live status, blocker, progress, scoped acceptance disposition, critique
  disposition, evidence disposition, retrospective / promotion disposition,
  route-specific wiki disposition when applicable, and the next route
- evidence: observed outputs, validation artifacts, reproduction logs, or other
  artifacts that support or challenge claims
- critique: adversarial findings, verdicts, severities, residual risks, and
  required follow-up
- wiki: accepted explanation or workflow knowledge that should persist after the
  owning layers settle it
- memory: optional support-only recall or pointers to owner records; never live
  state, acceptance truth, required resume context, or a replacement for ticket,
  evidence, critique, or wiki updates

Do not create a separate resume ledger, hidden scratchpad, generated context file
requirement, or canonical memory dependency. If a future agent would need the
fact for correctness, put it in the layer that owns that fact before compaction.

## Scratchpad Avoidance

Do not create generic `scratch.md`, `notes.md`, temporary junk-drawer files, or
generated context files to carry truth that already has an owner layer. They are
easy to miss on resume and quickly become shadow ledgers.

Route scratchpad-like material to the smallest correct owner instead:

- live state, blockers, progress, acceptance disposition, and next route -> ticket
- observed command output, validation artifacts, screenshots, or reproduction logs -> evidence
- adversarial findings, verdicts, residual risks, or required follow-up -> critique
- synthesis, tradeoffs, rejected options, and null results -> research
- accepted explanation or reusable workflow knowledge -> wiki
- support-only reminders, retrieval cues, or pointers to owners -> memory
- intended behavior -> spec
- sequencing or rollout strategy -> plan
- principles, constraints, and citable decisions -> constitution

External trackers, pull requests, dashboards, harness artifacts, generated
context files, and package or release surfaces may help navigate or mirror the
work. They still do not replace the owner update needed for a truthful resume.

## Drift Signals

- ticket says `review_required` but no critique path exists
- ticket says `complete_pending_acceptance` but evidence is weak
- coverage IDs are named but not supported by evidence
- non-ticket status is outside the lifecycle grammar
- plan is tracking live execution state
- wiki or memory is carrying owner truth
- `.loom/support/` artifacts are carrying objective state, live ticket state,
  acceptance, evidence sufficiency, critique verdicts, wiki truth, canonical
  truth, or packet lifecycle
- packet remains `compiled` after the child output has returned
- next-route fields use ticket lifecycle statuses such as `review_required` or
  command/adapter names instead of route tokens

## Native Queries

```bash
rg -n '^status:' .loom/tickets --glob '*.md'
rg -n '^status: (active|blocked|review_required|complete_pending_acceptance)\b' .loom/tickets --glob '*.md'
rg -n '^status:' .loom/{constitution,initiatives,research,specs,plans,critique,wiki,evidence,packets} --glob '*.md'
rg -n 'OBJ-[0-9]{3}|REQ-[0-9]{3}|ACC-[0-9]{3}|CLAIM-[0-9]{3}' .loom --glob '*.md'
rg -n '^id: workspace:main|^kind: workspace$|^status:' .loom/workspace.md 2>/dev/null
rg -n '^id: workspace:harness|^kind: workspace-support$|^status:' .loom/harness.md 2>/dev/null
rg -n '^id: support:|^kind: support-artifact$|^support_kind:|^handoff_kind:|^status:' .loom/support --glob '*.md' 2>/dev/null
find .loom/{tickets,critique,wiki,evidence} -type f -name '*.md' | sort
find .loom/support -type f -name '*.md' 2>/dev/null | sort
git status --short
```

## Output Shape

- status snapshot
- active, blocked, review, and acceptance queues
- contradictions or stale state
- best next owner layer or workflow route and why
