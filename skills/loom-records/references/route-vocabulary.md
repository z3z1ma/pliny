# Route Vocabulary

This reference owns the shared grammar for Loom route tokens used in checkpoint,
resume, route-readiness, and handoff examples.

Route tokens are not a runtime enum, command router, or new owner layer. They are
grep-friendly Markdown vocabulary for naming the next governed move in existing
owner records.

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
| `continue` | proceed to the next already-governed tranche or route named by owner records |
| `stop` | stop because the objective is satisfied, blocked, unsafe, out of scope, over budget, or awaiting external action |

Workflow coordinator tokens exist only when the coordinator is itself the next
governed move. Use `debugging`, `spike`, `codemap`, or `ship` when the next step
is to run that first-class workflow. If the next truth change is already narrower,
route through the owner token instead: for example, use `research` for a known
investigation write, `evidence` for an observation record, `wiki` for an accepted
atlas page, `ralph` for a bounded implementation packet, `critique` for review,
or `acceptance_review` for ticket closure evaluation.

## Non-Routes

Keep these categories distinct from route tokens:

- **Ticket lifecycle statuses** such as `ready`, `active`, `blocked`,
  `review_required`, `complete_pending_acceptance`, `closed`, and `cancelled`.
  They describe ticket state; they are not `next route:` values.
- **Record lifecycle statuses** such as `draft`, `active`, `accepted`,
  `recorded`, `superseded`, or `abandoned`. They describe a record's lifecycle,
  not the next governed move.
- **Command or adapter names** such as slash commands, harness commands, MCPs, or
  package-specific invocation wrappers. Commands may transport a route, but the
  owner records and workflow skills still own Loom truth.
- **Skill display names** such as Ralph or loom-drive when used as prose. In a
  route-value field, use the token (`ralph`, `debugging`, `spike`, `codemap`,
  `ship`, `continue`, `acceptance_review`, etc.) rather than title case, spaces,
  or hyphens. Do not add a token merely because a skill exists; route tokens name
  governed moves, not the skill inventory.

## Examples

```text
next route: ralph
next route owner: loom-ralph packet contract, then ticket reconciliation

Route: acceptance_review
Route: ask_user
proposed next route: research
```

If multiple routes are plausible, choose the token for the truth that changes
next, then cite the owner record or workflow coordinator that will handle it.
