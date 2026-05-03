# Route Vocabulary

This reference is the canonical shared grammar for Loom route tokens used in
checkpoint, resume, route-readiness, and handoff examples.

Route tokens are not a runtime enum, command router, or new owner layer. They are
grep-friendly Markdown vocabulary for naming the next governed move in existing
owner records.

For lifecycle words that are not route tokens, use
`skills/loom-records/references/status-lifecycle.md`. Ticket execution states
are owned by `skills/loom-tickets/references/state-machine.md`, and Ralph child
outcomes are owned by `skills/loom-ralph/references/packet-contract.md`.

## Token Grammar

Use lowercase `snake_case` tokens when a field or example asks for a route value,
especially after labels such as `next route:`, `Route:`, `proposed next route:`,
or route-priority tables.

Use ordinary prose when explaining a workflow. Do not rewrite every mention of a
skill name, command, or ticket status into a route token.

## Canonical Route Tokens

| Token | Meaning |
| --- | --- |
| `ask_user` | pause for a focused operator decision the agent cannot safely infer |
| `workspace_status` | inspect workspace structure, queues, and owner-chain trust before choosing a narrower route |
| `records_repair` | repair broken, stale, or contradictory Loom graph records before dependent work |
| `constitution` | create or update constitutional identity, principles, hard constraints, roadmap direction, or citable decisions |
| `initiative` | create or update strategic outcome framing, objectives, success metrics, or delegated autonomy boundaries |
| `research` | gather or synthesize evidence, options, tradeoffs, or null results |
| `spec` | clarify intended behavior, requirements, scenarios, or reusable acceptance |
| `plan` | clarify sequencing, dependency order, tranches, or rollout strategy |
| `ticket` | create or update the live execution owner for bounded work |
| `local_edit` | execute a tiny, safe, in-context mutation without a fresh child packet |
| `ralph` | launch or reconcile one Ralph implementation packet for a bounded ticket slice |
| `debugging` | run a reproduce-first debugging or incident workflow before the next fix or prevention route is clear |
| `spike` | run a bounded spike, sketch, prototype, or experiment as a research-shaped workflow |
| `codemap` | map repository or module structure into evidence, research, and accepted wiki atlas knowledge |
| `evidence` | preserve observed artifacts, validation output, reproduction logs, or support/challenge links |
| `critique` | run adversarial review and record findings, verdicts, and risks |
| `wiki` | promote accepted explanation or reusable workflow knowledge |
| `retrospective` | assimilate accepted learning into the correct owner layers before closure |
| `acceptance_review` | evaluate ticket-owned acceptance and closure readiness without implying closure |
| `ship` | package already-truthful work for merge, release, PR, or handoff without owning closure |
| `continue` | route-token use only: proceed to the next already-governed tranche or route named by owner records; do not use this row to interpret a Ralph child outcome named `continue` |
| `stop` | route-token use only: stop because the objective is satisfied, blocked, unsafe, out of scope, over budget, or awaiting external action; recorded stop routes must include a stop reason or condition; do not use this row to interpret a Ralph child outcome named `stop` |

Workflow coordinator tokens exist only when the coordinator is itself the next
governed move. Use `debugging`, `spike`, `codemap`, or `ship` when the next step
is to run that first-class workflow. If the next truth change is already narrower,
route through the owner token instead: for example, use `research` for a known
investigation write, `evidence` for an observation record, `wiki` for an accepted
atlas page, `ralph` for a bounded implementation packet, `critique` for review,
or `acceptance_review` for ticket closure evaluation.

## Non-Routes

Keep these categories distinct from route tokens. Matching words can appear in
more than one category; the field and owner decide what the word means.

| Category | Examples | Boundary rule |
| --- | --- | --- |
| Route tokens | `constitution`, `initiative`, `research`, `ralph`, `critique`, `continue`, `stop` | Use only when a route field asks for the next governed move. Tokens remain Markdown vocabulary, not a runtime enum, schema, validator, command router, skill inventory, or owner layer. |
| Ticket lifecycle states | `proposed`, `ready`, `active`, `blocked`, `review_required`, `complete_pending_acceptance`, `closed`, `cancelled` | Describe live ticket execution state. They are not `next route:` values. |
| Record lifecycle statuses | `draft`, `active`, `accepted`, `recorded`, `superseded`, `abandoned` | Describe a record's lifecycle or support-surface state, not the next governed move. |
| Ralph child outcomes | `continue`, `stop`, `blocked`, `escalate` | A child outcome is not a route token by itself. It becomes routing truth only after the parent reconciles the child output and translates it into the next owner-truth route, such as `ticket`, `research`, `critique`, `ask_user`, `continue`, or `stop`. |
| Critique-owned finding states | `open`, `withdrawn` | Live inside critique records and describe whether the critique still stands behind a finding. They are not ticket states or route tokens. |
| Ticket-owned finding dispositions | `resolved`, `accepted_risk`, `superseded`, `converted_to_follow_up` | Live in the ticket's critique disposition section for qualified findings. They are not critique finding states and do not name the next route. |
| Support-memory surfaces | `memory`, `loom-memory`, retrieval cues, preferences, reminders, hot context | Memory is optional support recall, not canonical project truth. Do not use `memory` as a `next route:` token; route durable truth changes through the owner token that owns them. |
| Commands and adapters | slash commands, harness commands, MCPs, package-specific wrappers | Commands may transport or prompt a route, but owner records and workflow skills still own Loom truth. |
| Skill display names | Ralph, loom-drive, loom-critique | Use ordinary prose for skill names. In a route-value field, use the token (`ralph`, `debugging`, `spike`, `codemap`, `ship`, `continue`, `acceptance_review`, etc.) rather than title case, spaces, or hyphens. Do not add a token merely because a skill exists; route tokens name governed moves, not the skill inventory. |

When the same word appears in multiple rows, the field decides the vocabulary. A
Ralph packet `outcome: continue` is child output for parent reconciliation; a
recorded `next route: continue` is a parent-owned route decision.

## `ask_user` Readiness

Use `ask_user` only when the next safe move requires an operator decision the
agent cannot infer from owner records, delegated authority, or a low-risk
reversible assumption.

An `ask_user` route should record:

- decision needed: the exact focused question or choice;
- unsafe-inference reason: why proceeding would invent product direction, accept
  material risk, exceed authority, or otherwise rely on an unsafe assumption;
- owner record to update after answer: the constitution, initiative, research,
  spec, plan, ticket, or other owner record that will carry the durable result.

Do not use `ask_user` as an approval gate for every downstream step. If the
assumption is low risk, reversible, and inside delegated authority, record the
assumption in the owner record and continue through the appropriate route.

## Examples

```text
next route: ralph
next route owner: loom-ralph packet contract, then ticket reconciliation

next route: constitution
next route owner: loom-constitution

Route: acceptance_review
Route: ask_user
decision needed: Choose whether the accepted constraint should become a constitutional decision.
unsafe-inference reason: The agent cannot safely invent durable project authority.
owner record to update after answer: constitution:main or decision:<slug>

proposed next route: research

next route: stop
stop reason: OBJ-001 and OBJ-002 are satisfied, required evidence is linked, and no owner work remains.

next route: continue
continue reason: ticket:<token> already names the next governed tranche; this is not a Ralph child outcome.
```

If multiple routes are plausible, choose the token for the truth that changes
next, then cite the owner record or workflow coordinator that will handle it.
