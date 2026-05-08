# Critique And Wiki

This is an ordered reference for the `using-loom` skill.

Critique and wiki are not side channels. Critique pressure-tests work before
acceptance; wiki preserves accepted understanding so future agents do not
re-derive it from transcripts.

## Critique As Review

Critique is Loom's adversarial review layer. It looks for mismatches, weak
evidence, hidden assumptions, brittle reasoning, unsafe scope, and user-facing
confusion.

Two common forms exist:

- direct artifact critique reviews a record or support artifact as itself, such
  as a plan, ticket, spec, packet, wiki page, or evidence record
- packetized implementation critique reviews a code or behavior change from a
  critique packet plus the relevant diff, evidence, and owner context

Critique can target code, behavior, records, packets, plans, specs, wiki pages,
or any other reviewable work product. It produces findings and verdicts; it does
not close the ticket.

Ask whether the resulting shape is actually good, whether claims are supported,
which residual risks remain, and what follow-up is required before acceptance.
The answer should be inspectable enough for the ticket to consume.

## Critique Policy And Closure Effects

Use the default policy unless a project records something stricter. Decide by
risk class and change class together.

- Low risk: small link fixes, local wording cleanup, or minor ticket hygiene.
  Critique is optional.
- Medium risk: meaningful workflow changes, non-trivial code changes, important
  packet changes, or behavior clarifications that could mislead operators.
  Critique is recommended.
- High risk: scope model, authority model, completion criteria, architecture,
  security, data-sensitive, or user-impacting changes. Critique is mandatory.

Change classes can tighten this. Protocol authority, code behavior, data
migration, and security-sensitive work usually need named critique profiles even
when the diff is small.

Critique gates affect closure through the ticket-owned acceptance decision:

- mandatory critique blocks `closed` until a final critique record exists with an
  explicit verdict, reviewed evidence, residual risks, and acceptance
  recommendation; deferral, `not_required`, or a draft/stub review does not
  satisfy it
- every open medium/high finding from a required critique needs ticket-owned
  disposition: `resolved`, `accepted_risk`, `superseded`, or
  `converted_to_follow_up`
- withdrawn findings require critique-owned rationale and may be cited for audit,
  but do not block closure merely because of severity
- recommended critique needs ticket-owned disposition before closure:
  `completed`, `deferred`, or `not_required` with rationale
- optional critique does not block closure unless a ticket, spec, plan, or human
  gate made it required

A useful critique record names review target, verdict, findings, severity,
confidence, evidence reviewed, residual risks, and required follow-up. "Looks
good" is not enough when the review should persist.

## Wiki As Accepted Explanation

Wiki is Loom's canonical explanation layer. It stores architecture explanations,
workflow guides, concept pages, operator references, troubleshooting notes, and
syntheses that answer recurring questions. Wiki can use packet discipline, but
wiki packets are owned by the wiki workflow; route by the explanation truth being
changed, not by the presence of a packet.

Promote understanding into wiki when the same question will recur, synthesis
crosses multiple records, an accepted workflow changed, a project concept is now
worth naming, or future agents should read the page before touching nearby work.

Wiki pages must be grounded in inspectable sources: canonical records, accepted
critique outcomes, evidence, and accepted external sources when summarizing
outside knowledge. Eloquence does not make a wiki page authoritative by itself.
Tickets remain the live ledger; wiki explains settled understanding and does not
replace ticket-owned retrospective/promotion disposition. Memory may keep
retrieval cues or wiki pointers, but accepted project explanation belongs in wiki,
not only memory.

Maintain wiki deliberately. When accepted reality changes, update the page, mark
it stale, supersede it, or link forward as appropriate. A strong page should make
future recovery cheaper without outranking the records that supplied its truth.

## Retrospective As Promotion Gate

For non-trivial closure, promotion should happen at a concrete retrospective pass,
not ambiently. Retrospective is a workflow coordinator, not a new record kind, a
new directory, or a second ledger. It assimilates lessons into existing owner
layers, then the ticket or initiative records what was promoted, deferred, not
required, or still blocking.

Route retrospective outputs by owner:

- accepted explanations and workflows -> wiki
- durable investigations, rejected options, and null results -> research
- clarified intended behavior -> spec
- changed sequencing, decomposition, rollout, or waves -> plan
- changed strategic framing -> initiative
- changed principles, constraints, or citable decisions -> constitution
- observed artifacts and validation outputs -> evidence
- support-only continuity -> memory

Every repeated mistake should have one prevention artifact: behavior ambiguity to
spec, evidence gaps to evidence or future ticket/test expectations, bad
architectural choices to constitution decisions, operator confusion to wiki,
implementation pitfalls to research or wiki troubleshooting, repeated local
technique to a local skill, and support-only reminders to memory.

Run retrospective when a non-trivial ticket or initiative closes, critique
surfaces stable lessons, or transcript context has answered the same question
more than once. A retrospective that creates no promotions is honest when nothing
durable should persist; manufacturing artifacts is not.
