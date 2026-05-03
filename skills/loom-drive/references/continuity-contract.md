# Drive Continuity

This reference supports the `loom-drive` skill.

The drive loop is only real when it is recoverable. The parent may use the
conversation to think, but the current drive state must live in existing Loom
owner records before the agent depends on it for continuation.

## Owner Mapping

Use this map before launching tickets or child work.

| Drive fact | Owner |
| --- | --- |
| objective, why it matters, success metrics | initiative |
| `# Delegated Authority / Autonomy Boundaries` and `# Objective-Level Stop Conditions` for delegated drive work | initiative |
| evidence gaps, options, rejected approaches, conclusions | research |
| intended product behavior, reusable acceptance IDs | spec |
| tranche strategy, sequencing, dependencies, execution waves | plan |
| live state, blockers, next route, scoped coverage | ticket |
| evidence disposition, critique disposition, acceptance decision | ticket |
| bounded child context, source snapshot, read/write scope, output contract | packet or bounded handoff |
| observed support or challenge artifacts | evidence |
| adversarial findings, severity, verdict, residual risk | critique |
| accepted reusable explanation | wiki |
| support-only recall, retrieval cues, preferences, reminders, or hot context that does not own project truth | memory |

If no existing record owns a drive fact, either create the correct owner record or
stop and ask the user. Do not invent a hidden state surface.

## Objective Contract Fields

For a high-level drive, the initiative or linked owner chain should make these
fields inspectable in prose:

- objective statement
- measurable success criteria or acceptance signals, preferably with stable
  criterion IDs such as `OBJ-001`
- hard constraints and non-goals
- `# Delegated Authority / Autonomy Boundaries`: what the agent may decide
  without asking, what must come back to the user as a human-decision trigger,
  and any budget, time, risk, privacy, safety, or other limits
- `# Objective-Level Stop Conditions`: when continuation must stop, ask the user,
  or return to shaping before more work proceeds
- current tranche purpose
- known remaining gaps

These do not require new frontmatter keys. The requirement is that a fresh agent
can find the facts in the owner records and continue honestly.

## Continuity Snapshot

Use a continuity snapshot as a prose convention inside existing owner records. It
is a way to place the right facts in the records that already own them, not a new
record kind or ledger.

Recommended locations:

| Owner record | Put the snapshot here |
| --- | --- |
| initiative | `# Status Summary`, plus criterion IDs under `# Success Metrics` |
| plan | `# Strategy Snapshot` and `# Execution Waves` |
| ticket | `# Coverage`, `# Claim Matrix`, `# Next Move / Next Route`, `# Evidence`, `# Critique Disposition`, and `# Journal` |
| packet or handoff | frontmatter/source snapshot plus output contract and parent merge notes |
| evidence | `# Supports Claims` and `# Challenges Claims` |
| critique | findings, verdict, residual risks, and challenged claims |

The snapshot should answer exactly enough for a fresh parent to resume without
making the initiative own live ticket execution:

```text
drive objective: <initiative id and one-sentence objective>
objective criteria: <OBJ-IDs with satisfied | partial | open | blocked>
current tranche: <plan milestone / wave / purpose>
active tickets: <ticket IDs and states>
evidence state: <claim IDs with evidence links or gaps>
critique state: <required | pending | blocking | completed | deferred | not_required, citing ticket truth>
next route: ask_user | workspace_status | records_repair | research | spec | plan | ticket | local_edit | ralph | debugging | spike | codemap | evidence | critique | wiki | retrospective | acceptance_review | ship | continue | stop
next route owner: <which layer must change next>
reason: <why this follows from current owner truth>
```

Do not duplicate this full block everywhere. Put each fact in the owner record
that owns it, and link across records so the snapshot is recoverable by ordinary
search.

### Saved outer-loop handoff metadata

When a parent intentionally saves an outer-loop synthesis handoff, the handoff
may carry support-local `source_snapshot`, `drive_checkpoint`, nested
`drive_checkpoint.gate_status`, and `handoff_write_scope` fields for recovery.
These fields summarize the owner graph at compilation time and any proposal-time
write permission; they do not own objective state, ticket execution state,
acceptance, evidence sufficiency, critique verdicts, wiki truth, canonical truth,
or packet lifecycle.

Use `templates/outer-loop-handoff.md` for the field-level grammar, and reconcile
any accepted handoff output back into the owner records before depending on it.

## Stable Objective Criterion IDs

Use initiative-owned IDs when high-level success criteria need downstream
coverage. Suggested shape:

```text
- OBJ-001: A user can <observable outcome>.
- OBJ-002: The system preserves <constraint or quality bar>.
- OBJ-003: The workflow can be resumed from Loom records in a fresh session.
```

Use spec-owned `ACC-*` IDs for reusable behavior contracts. Use ticket-local
criteria only for local execution details. A ticket may cover both initiative
`OBJ-*` IDs and spec `ACC-*` IDs when the ticket advances both objective and
behavior truth.

## Reassessment Block

After each ticket or tranche, update the owning records enough to answer:

```text
objective status: satisfied | partially_satisfied | open | blocked | out_of_scope
criteria supported: <claims and evidence links>
criteria still open: <claims or gaps>
ticket critique disposition status: pending | blocking | completed | deferred | not_required
finding dispositions: <qualified finding refs with resolved | accepted_risk | superseded | converted_to_follow_up, or none>
next route: ask_user | workspace_status | records_repair | research | spec | plan | ticket | local_edit | ralph | debugging | spike | codemap | evidence | critique | wiki | retrospective | acceptance_review | ship | continue | stop
next tranche: <ticket IDs or plan update, if known>
reason: <why this next route follows from the records>
```

Put the answer in the layer that owns it. For example, objective-level status
belongs in the initiative, live execution and acceptance state belong in the
ticket, critique findings and verdicts belong in critique, and sequencing changes
belong in the plan. Drive snapshots cite those owners; they do not own acceptance.

If the next route is `continue`, the plan or ticket chain should name the next
tranche. If the next route is `ask_user`, record the exact question and why the
agent cannot safely infer the answer.

Use `skills/loom-records/references/route-vocabulary.md` for the canonical route
token grammar. Do not use ticket lifecycle statuses such as `review_required` or
`complete_pending_acceptance` as `next route:` values.

## Checkpoint Before Child Work

Before launching Ralph or an outer-loop synthesis subagent, verify:

- the child has a bounded source snapshot or read scope
- the child write scope cannot silently mutate owner truth outside its authority
- the current ticket or handoff names stop conditions and output contract
- the parent knows which owner records must be reconciled after return
- a fresh agent could understand why this child is being launched

If any answer is unclear, repair the owner records before launching child work.

## Failure Signs

Stop driving and repair continuity when:

- the only place the objective exists is conversation context
- the next tranche is obvious to the current model but not visible in a plan or
  ticket
- success is judged by vibes instead of linked criteria and evidence
- critique state is remembered but not linked from the ticket
- a subagent output is treated as authoritative before parent reconciliation
- a fresh session would lose the reason for the next route
