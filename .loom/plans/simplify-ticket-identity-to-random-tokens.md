---
id: plan:simplify-ticket-identity-to-random-tokens
kind: plan
status: active
created_at: 2026-04-08T07:54:09Z
updated_at: 2026-04-22T17:20:00Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  constitution:
    - constitution:main
  ticket:
    - ticket:psh7h282
external_refs: {}
---

# Purpose / Big Picture

Replace Loom's autoincremented ticket identity scheme with short random tokens so
ticket refs and filenames stop depending on global numbering state, repository
prefix heuristics, and renumbering-oriented examples.

This change should simplify the ticket layer end to end: a new ticket should be
created by generating one random 6-8 character token, using that token in the
canonical ticket ref and the filename, and then reusing the same opaque token
everywhere else in links, dependencies, packets, docs, and examples.

# Progress

- 2026-04-08: investigated the current ticket identity surface across shipped
  scripts, rules, skill references, README examples, and canonical `.loom/`
  records.
- Confirmed that only `skills/loom-tickets/scripts/tickets.py` enforces numeric
  ticket refs mechanically today; the rest of the shipped Python surface mostly
  treats ticket refs as opaque strings.
- Confirmed that the repository currently has six ticket records and no
  `.loom/runs/` or `.loom/verification/` records, which keeps migration scope
  bounded.
- 2026-04-08: created `ticket:psh7h282` as the ready execution owner for this
  migration so the strategy now has a linked ticket ledger entry.
- 2026-04-08: landed the fixed-width token contract at 8 lowercase alphanumeric
  characters, rewrote `skills/loom-tickets/scripts/tickets.py`, migrated the six
  canonical ticket records, and reconciled the shipped docs and `.loom/` graph.
- 2026-04-08: revised the filename contract to `YYYYMMDD-<token>-<slug>.md` and
  renamed the canonical ticket files to carry the UTC creation-date prefix.
- 2026-04-08: verified the shipped Python surface with `uvx ruff check` and
  `uvx ruff format --check`, then smoke-tested ticket creation, linking, and
  dependency mutation in a disposable temp workspace.

# Surprises & Discoveries

- The current shipped `tickets.py` already diverges from the written naming
  doctrine and existing ticket files. Before this migration, the script had
  already moved to one numeric filename shape while the docs and canonical
  tickets still described a different repository-prefixed numeric filename
  convention.
- Numeric ticket assumptions are concentrated in one product script but are
  repeated broadly in examples, schema references, rules, README snippets, and
  canonical `.loom/` records.
- Because the current corpus is still small, a one-pass migration is much more
  attractive than carrying a permanent dual numeric/random ticket identity model.

# Decision Log

- 2026-04-08: treat the user's requested simplification as a full ticket
  identity change, not just an example refresh. Both the canonical ticket ref
  and the filename should move away from autoincremented numbers.
- 2026-04-08: prefer one opaque random token reused across the ref and filename
  rather than separate heuristics for numeric ids and repository-derived filename
  prefixes.
- 2026-04-08: choose a fixed-width 8-character lowercase alphanumeric token
  contract for simplicity and grep-friendliness.
- 2026-04-08: standardize ticket filenames as `YYYYMMDD-<token>-<slug>.md` so
  the UTC creation date and opaque token drive the on-disk path while the
  canonical ref stays `ticket:<token>`.
- 2026-04-08: prefer a one-pass corpus migration over indefinite compatibility
  support for both numeric and random ticket refs. The existing persisted ticket
  data is small enough to rewrite directly.
- 2026-04-08: avoid introducing a dedicated migration helper unless the manual
  reconciliation proves too error-prone. The current corpus size argues for
  ordinary edits plus validation instead of new helper surface area.

# Outcomes & Retrospective

The main migration work has landed.

Its value now is as a durable strategy-and-outcome record: it explains why Loom
collapsed its old ticket identity drift into one random-token contract, which
surfaces had to change, and what evidence supported treating the implementation
as substantially complete.

# Context and Orientation

Before this work, Loom ticket identity had already drifted: canonical ticket
refs used autoincremented numbers, written filename doctrine still described
repository-prefixed numeric filenames, and the shipped helper had already moved
to a different numeric filename shape.

That made ticket creation more stateful than necessary and left the bundle
teaching multiple incompatible naming stories at once. The migration collapsed
that drift into one simpler rule: generate one random short token, use it in the
canonical `ticket:<token>` ref, and reuse it in `YYYYMMDD-<token>-<slug>.md`.

# Milestones

1. Finalize the target ticket identity contract.
   Decide the exact token shape inside the requested 6-8 character range and
   choose the single filename pattern that will ship with it.

2. Update the shipped ticket creation and resolution behavior.
   Replace numeric generation and numeric validation in `tickets.py` with random
   token generation, collision checks, and opaque ticket-ref handling.

3. Reconcile the written corpus and canonical records.
   Update rules, skill references, README snippets, and existing `.loom/` ticket
   links so the repository stops teaching numbered ticket identities.

4. Validate and smoke-test the new shape.
   Confirm the script lint pass, creation flow, dependency flow, and graph
   references all work with the random ticket identity format.

# Plan of Work

Start by locking the smallest viable identity contract: one short random token,
one canonical `ticket:<token>` ref, and one filename pattern derived from that
same token. Do not begin by editing examples alone, because the current drift is
partly caused by multiple competing naming rules.

Once the contract is chosen, change `skills/loom-tickets/scripts/tickets.py`
first so the shipped behavior becomes the new source of truth. Then reconcile
the written rules and examples that currently teach numeric tickets. Finally,
migrate the existing canonical ticket records and any references to them across
`.loom/` in one pass so the graph reflects one identity scheme instead of two.

The migration should stay intentionally simple. Because the corpus is still
small, the preferred path is direct record edits and reference reconciliation,
not a new migrator CLI and not a permanent compatibility layer that keeps both
ticket formats alive indefinitely.

# Concrete Steps

1. Inventory every numeric ticket assumption that affects shipped behavior,
   shipped docs, or canonical `.loom/` truth. The initial investigation already
   found the main product script, rules appendices, README snippets, several
   skill references, and the existing `.loom/` plans/specs/initiatives/tickets.
2. Choose the ticket token contract within the requested 6-8 character range.
   A fixed width is likely simpler than a variable width; if no stronger reason
   appears, prefer 8 lowercase alphanumeric characters and collision retry.
3. Rewrite `skills/loom-tickets/scripts/tickets.py` so ticket creation uses a
   random token, filename generation uses that same token, and ticket-target
   resolution accepts opaque `ticket:<token>` refs instead of numeric-only refs.
4. Update ticket skill docs and the shared rules/docs surfaces that currently
   teach numbered ticket refs or numbered ticket filename patterns.
5. Rename existing ticket files and rewrite their frontmatter ids from numeric
   refs to random-token refs.
6. Reconcile every direct reference to those ticket refs or filenames across
   `.loom/`, `rules/`, `skills/`, `README.md`, and `AGENTS.md`.
7. Run structural verification and a behavioral smoke test by creating a new
   ticket and exercising `depends-on`, `link`, and any packet-targeting flows
   against the new random-ticket shape.

# Validation and Acceptance

- `uvx ruff check skills/*/scripts/*.py` should pass after the ticket CLI change.
- The new ticket create flow should emit a random-token ticket ref and filename
  without consulting existing numeric state.
- `scripts/tickets.py depends-on` and `scripts/tickets.py link` should continue
  to resolve and mutate ticket records correctly using the new opaque refs.
- Searches for stale numbered ticket guidance should come back clean on the
  touched product surfaces and canonical `.loom/` records outside explicitly
  historical migration notes.
- Acceptance should not claim completion until the repo stops containing mixed
  active truth about numeric ticket ids versus random ticket ids.

# Idempotence and Recovery

The safest recovery posture is milestone-based rather than half-migrated.

If the code change lands but corpus reconciliation is incomplete, the work
should remain explicitly in progress rather than being treated as done. If the
record migration begins, finish the reference reconciliation in the same slice or
stop and record the partial state honestly; mixed ticket identities will be hard
for future agents to reason about.

Because the ticket corpus is small, recovery should rely on a preserved
old-to-new ticket mapping during the migration pass instead of inventing a long-
lived compatibility mechanism.

# Artifacts and Notes

- Primary behavior surface: `skills/loom-tickets/scripts/tickets.py`
- Primary ticket docs: `skills/loom-tickets/SKILL.md`,
  `skills/loom-tickets/references/schema-tickets.md`,
  `skills/loom-tickets/references/scripts.md`, and
  `skills/loom-tickets/references/examples.md`
- Cross-surface examples already teaching numeric tickets: `README.md`,
  `AGENTS.md`, `rules/loom.md`, `rules/verification-doctrine.md`,
  `rules/appendices/common-schema-conventions.md`,
  `rules/appendices/naming-conventions.md`, and several skill references such as
  `skills/loom-ralph/references/*`, `skills/loom-docs/references/scripts.md`,
  `skills/loom-critique/references/scripts.md`, and
  `skills/loom-plans/references/scripts.md`
- Canonical records already using numeric ticket refs include the current ticket
  set plus linked plans, specs, initiatives, roadmap notes, and research notes
  under `.loom/`
- Current canonical ticket files:
  `.loom/tickets/20260401-14eh8c66-smoke-test-ticket-creation.md`,
  `.loom/tickets/20260401-z8h0g58e-inventory-shared-loom-script-clis.md`,
  `.loom/tickets/20260404-1ypcbj0m-exercise-one-end-to-end-ralph-critique-and-wiki-flow.md`,
  `.loom/tickets/20260404-zomng8h3-evaluate-optional-wrapper-commands-for-core-workflows.md`,
  `.loom/tickets/20260404-vyypge85-harden-packet-scope-and-workspace-structural-validation.md`,
  `.loom/tickets/20260408-psh7h282-migrate-ticket-identity-to-random-tokens.md`

# Interfaces and Dependencies

The main implementation dependency is the ticket CLI because it currently owns:

- id generation
- filename generation
- dependency normalization
- ticket target resolution
- numeric id validation

The main reconciliation dependency is the text graph under `.loom/` and the
shipped docs corpus, because ticket refs are embedded directly in Markdown and
example commands.

Related packet-oriented skills such as Ralph, docs, and critique do not appear to
hard-code numeric ticket validation in Python today, but their written examples
and packet examples do assume numbered ticket refs. Those surfaces need truth
reconciliation even if their scripts need little or no behavioral change.

# Linked Tickets

- `ticket:psh7h282` owns the execution truth for the ticket-identity migration.

# Risks and Open Questions

- whether any packet, docs, or critique records outside the current visible
  corpus will need manual migration later once real run artifacts exist
- whether the corpus should preserve an explicit old-to-new ticket mapping note
  during migration for human traceability

# Revision Notes

- 2026-04-08: created the plan after investigating the current numeric ticket-id
  surface and confirming that the main behavioral change is concentrated in the
  ticket CLI while the broader cost is corpus reconciliation.
- 2026-04-08: recorded the recommendation to migrate the small existing ticket
  corpus in one pass instead of keeping a permanent dual numeric/random identity
  model.
- 2026-04-08: linked `ticket:psh7h282` as the ready execution owner for the plan.
- 2026-04-08: recorded the final contract as 8 lowercase alphanumeric characters
  with `YYYYMMDD-<token>-<slug>.md` filenames and noted that the implementation,
  corpus migration, and verification all landed in the same slice.
