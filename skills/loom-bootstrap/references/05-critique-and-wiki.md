# Critique And Wiki

This is an ordered bootstrap reference for the `loom-bootstrap` skill.

Critique and Wiki are not side quests.
They are how Loom pressure-tests work and how Loom compounds understanding.

## Critique As Review

Critique is Loom's adversarial review layer.

It has two common shapes:

- direct artifact critique
- packetized implementation critique

Direct artifact critique reviews a Loom record or support artifact as itself:
a plan, ticket, spec, packet, wiki page, evidence record, or external summary.
This usually does not need a packet. Read the target, read enough owner context,
and leave findings when the review should persist.

Packetized implementation critique reviews a code or behavior change. It is
the Ralph-like form. The parent compiles a critique packet from the ticket,
parent plan or initiative, relevant spec/research/evidence, prior packet
output, and the git diff. The reviewer consumes that packet plus the diff and
returns findings, verdict, risks, and follow-up.

Critique asks:

- is the resulting shape actually good
- are the claims supported
- what residual risks remain
- what follow-up work is required before acceptance

Critique can target code changes, behavior changes, Loom records, packets,
plans, specs, wiki pages, or any other reviewable work product.

A critique pass should feel adversarial in the healthy sense.
It should search for mismatches, hidden assumptions, weak evidence, brittle reasoning, and user-facing confusion.

## Default Critique Policy

Use this as the default until a project records something stricter.

Risk class says how dangerous the change is. Change class says what kind of
mutation it is. Use both when deciding whether critique is optional,
recommended, or mandatory.

### Low risk

Examples:

- small link fixes
- local wording cleanup
- minor ticket hygiene

Default: critique optional.

### Medium risk

Examples:

- meaningful workflow changes
- non-trivial code changes
- important packet changes
- behavior clarifications that could mislead operators

Default: critique recommended.

### High risk

Examples:

- scope model changes
- authority model changes
- changes to how completion is judged
- security-sensitive, data-sensitive, or user-impacting code changes
- architecture changes with broad downstream impact

Default: critique mandatory.

Change classes can tighten these defaults. Code behavior, protocol authority,
data migration, and security-sensitive changes usually need named critique
profiles even when the diff looks small.

### Closure effects

Critique policy affects ticket closure through the ticket's acceptance gate:

- mandatory critique blocks `closed` until the required review exists and every
  open medium/high finding has a ticket-owned disposition of `resolved`,
  `accepted_risk`, `superseded`, or `converted_to_follow_up`
- withdrawn findings require critique-owned rationale. They may be cited by the
  ticket for audit history, but do not require ticket-owned finding disposition
  and do not block closure merely because of severity.
- recommended critique requires a recorded ticket-owned disposition status before
  closure: `completed`, `deferred`, or `not_required` with rationale
- optional critique does not block closure unless a ticket, spec, plan, or human
  gate made it required for that work

Critique itself does not close work. It produces findings and verdicts; the
ticket owns the live state and acceptance decision.

## What Good Critique Produces

A good critique record makes these explicit:

- review target
- verdict
- findings
- severity
- confidence
- evidence reviewed
- residual risks
- required follow-up

A good critique does not merely say "looks good".
It leaves a durable review surface another agent can inspect later.

## Wiki Can Use Packet Discipline

Wiki work can be a packetized knowledge-compilation pass.

It happens after enough truth is accepted that the understanding should persist as a page instead of a chat answer.

The wiki workflow owns wiki packets. Ralph's packet discipline may be reused,
but a wiki pass is routed by the explanation truth it changes, not by the fact
that it uses a bounded handoff.

Wiki is where Loom stores:

- architecture explanations
- workflow guides
- concept pages
- operator references
- troubleshooting notes
- synthesis pages that answer recurring questions

## What Makes Wiki Different From Old Docs

Wiki is not a dumping ground for prose.

Wiki is:

- interlinked
- maintained over time
- grounded in accepted owner truth
- designed for future retrieval and reuse
- allowed to grow page by page as understanding compounds

A strong wiki page should reduce the chance that a future agent needs to re-derive the same explanation from scratch.

## Promotion Rule

Promote something into the wiki when one or more of these are true:

- the same question will likely come up again
- the answer requires synthesis across multiple records
- the accepted workflow changed materially
- the project now has a concept or pattern worth naming explicitly
- another agent would benefit from reading the page before touching nearby work

Retrospective is the default promotion gate for non-trivial completed work.
The ticket should record the broader retrospective / promotion disposition for
closure; wiki disposition records only the route-specific wiki outcome when wiki
is one selected promotion route. Direct wiki work is allowed when the ticket is
explicitly a wiki/explanation task or when the parent records why retrospective
is unnecessary.

## Wiki Source Rule

A wiki page should be grounded in:

- canonical records
- accepted critique outcomes
- evidence
- accepted external sources when the page is summarizing outside knowledge

Do not let a wiki page become authoritative by eloquence alone.
Its sources should be inspectable.

## Relationship To Tickets

Tickets remain the live execution ledger.
Wiki does not replace them, and wiki disposition does not replace the broader
ticket-owned retrospective / promotion disposition.

The relationship is:

- tickets say what is happening and whether closure follow-through is completed,
  deferred, not required, or blocking
- critique says what is risky or weak
- wiki says what is now understood and worth preserving

## Relationship To Memory

Memory is optional support recall.
Wiki is canonical explanation.

Memory is useful for retrieval cues, preferences, entities, reminders, and hot
context that may decay or be pruned. Wiki is where accepted explanation becomes
safe for future operators to rely on.

If a concept matters to the project as a whole, it belongs in the wiki rather
than only in memory. Memory may keep a short pointer to the wiki page when that
helps retrieval.

## Maintenance Rule

Wiki pages should age deliberately.

When accepted reality changes:

- update the page if it still describes the same concept
- mark it stale if the concept remains but the page is out of date
- supersede it if a better page replaces it
- link forward from the old page when practical

Good wiki maintenance makes the knowledge base compound instead of rot.

## Retrospective As The Compounding Trigger

Promotion is not supposed to be ambient. For non-trivial closure it should happen at a concrete moment: the **retrospective** pass.

A retrospective is a named workflow — not a new record kind and not a new directory. It assimilates what was learned during a ticket, initiative, or recent work slice into the existing owner layers, then the owning ticket or initiative records what was promoted, deferred, not required, or still blocking:

- accepted explanations and workflows → wiki
- durable investigation results, rejected options, null results → research
- clarified intended behavior → spec
- changed sequencing → plan
- changed strategic framing → initiative
- changed principles, constraints, or citable decisions → constitution (including decision records)
- observed artifacts, challenged observations, or validation artifacts → evidence
- support-only continuity → memory

Every repeated mistake should be promoted into exactly one prevention artifact:

- behavior ambiguity → spec
- missed test case or evidence gap → evidence when an observed artifact exists, or
  a ticket/test expectation when the gap is future work
- bad architectural choice → constitution decision
- recurring operator confusion → wiki workflow or reference page
- repeated implementation pitfall → research null result or wiki troubleshooting page
- repeated project-local technique → project-local skill
- support-only reminder → memory

Run a retrospective when:

- a non-trivial ticket is closing
- an initiative is closing
- a critique surfaced stable lessons
- the same question has been answered from transcript context more than once

Use the retrospective workflow when available. It is a coordinator over existing
owner layers, not a new record kind and not a second execution ledger.

A retrospective that produces no promotions is honest if there was nothing durable to promote. Do not manufacture artifacts to look productive, and do not let retrospective become a second ledger.

The retrospective pass is Loom's compounding mechanism. Without it, wiki and memory drift — pages stay stale, questions keep getting re-derived, and the knowledge base rots instead of growing.
