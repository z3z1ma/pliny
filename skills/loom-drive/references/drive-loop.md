# Drive Loop

This reference supports the `loom-drive` skill.

The drive loop is a skill-driven parent workflow through existing Loom owner
layers. It starts from a user request and advances only through recorded state and
bounded routes.

## Parent Invariants

- Owner records own durable truth by layer.
- Tickets record live execution state.
- Packets are bounded child contracts, not project truth.
- Subagents are transport and context-management aids, not final authority.
- Scope and write authority fail closed.
- The parent reconciles every child result before dependent continuation.
- Continuation state must be recoverable from owner records, not unrecorded
  conversation context.

## Drive State Machine

The parent should know which state it is in before acting:

```text
intake -> objective-contract -> owner-shaping -> tranche-planning -> ticket-execution -> reconciliation -> reassessment -> continuation | ask-user | stop
```

- `intake`: decide whether the request is actually drive-shaped.
- `objective-contract`: capture outcome, success signals, authority, limits, and
  stop conditions.
- `owner-shaping`: create or refine initiative/research/spec/plan truth.
- `tranche-planning`: slice only the next useful bounded work set.
- `ticket-execution`: advance tickets through local edit, Ralph, critique,
  evidence, wiki, or acceptance routes.
- `reconciliation`: update ticket truth and any owner records affected by the
  result.
- `reassessment`: compare current state against the objective contract.
- `continuation`: create the next tranche or choose the next route.
- `ask-user`: pause for a focused decision the agent cannot safely infer.
- `stop`: objective satisfied, blocked, unsafe, over budget, or outside authority.

Before `ticket-execution`, run the hard preflight gates in
`checkpoint-resume-protocol.md`. A failed gate may route to the owner repair path
that clears it, but it blocks implementation execution, acceptance, and dependent
continuation until repaired.

Do not skip directly from intake to execution for broad objectives. The graph must
first contain enough objective truth to make continuation recoverable.

## Activation Triage

Ask what the user actually requested:

- **High-level objective**: create or refine initiative-level outcome and success
  criteria, then drive through this loop.
- **Existing initiative continuation**: read the initiative/plan/ticket chain,
  identify the next unmet objective gap, and create or advance the next tranche.
- **Single bounded task**: route directly to ticket/local edit/Ralph instead of
  using the full drive loop.
- **Unknown evidence or behavior**: route to research or spec shaping before
  creating execution tickets.

Drive-shaped work has both an outcome and delegated continuation. If the user
only asks for a recommendation, explanation, or one bounded mutation, choose the
owner skill that owns that narrower truth instead.

If scope ownership or workspace trust is unclear, return to `loom-workspace`.

## Focused Objective Questions

Ask as few questions as can safely establish:

1. target outcome in measurable terms
2. success criteria or acceptance signals
3. constraints, non-goals, and risk tolerance
4. delegated autonomy and what requires user approval
5. budget/time limits and stop conditions
6. preferred first tranche when multiple routes are equally plausible

If the user cannot answer everything, record reasonable assumptions only when
they are low risk and explicitly reversible. Otherwise stop and ask.

When the answer becomes durable, convert success criteria into stable objective
criterion IDs in the initiative, such as `OBJ-001`. Tickets, evidence, and
critique can then cite those IDs when judging whether the drive should continue.

## Owner-Layer Routing

- objective, outcome metrics, strategic framing -> initiative
- missing evidence, options, tradeoffs, rejected paths -> research
- intended behavior and reusable acceptance contract -> spec
- sequencing, rollout, and tranche strategy -> plan
- live execution, blockers, next move, closure -> ticket
- bounded child implementation contract -> packet through Ralph
- observed artifacts and validation output -> evidence
- adversarial verdicts and required follow-up -> critique
- accepted explanation or reusable workflow knowledge -> wiki
- support-only recall -> memory

Do not let the plan become the ledger. Do not let a packet, subagent response, or
wiki page redefine acceptance. Move truth into the owning layer before relying on
it.

## Tranche Shape

A tranche is the next small set of work that advances the objective while keeping
review and recovery tractable.

Use `tranche-decision-protocol.md` to choose the tranche. Do not choose from
intuition alone when objective criteria, evidence gaps, or critique state can
determine the route.

A good tranche:

- maps to explicit objective or spec claims
- creates independently legible tickets
- avoids overlapping write scopes unless intentionally sequenced
- names expected evidence and critique posture
- leaves the next reassessment point obvious

A tranche is not ready until it names included objective/spec claims, excluded
claims, dependency order, likely write scopes, evidence/critique gates, and the
reassessment point.

Do not decompose the whole objective merely to look complete. Decompose enough to
make the next safe progress step durable.

## Execution Routing

For each ticket or follow-up:

- use a local edit when the change is tiny, obvious, and safe in the current
  context
- use Ralph when the implementation step benefits from fresh context or explicit
  write boundaries
- use critique when review is required or risk warrants adversarial inspection
- use wiki or retrospective when accepted understanding should persist
- route back to research/spec/plan when execution reveals missing evidence,
  behavior, or sequencing truth

Before launching child work, declare target, read scope, write scope, stop
conditions, verification posture, and output contract. After return, reconcile
before launching dependent work.

When several routes are possible, apply the route decision priority from
`tranche-decision-protocol.md` instead of selecting the most implementation-like
route by habit.

When several child routes can run independently, treat that as route federation:
each child gets a bounded route contract, non-overlapping write scope, output
contract, and parent merge target. Do not rely on a shared chat plan.

## Reassessment Checklist

After each ticket or tranche, the parent checks:

- Which objective criterion IDs are satisfied, partially satisfied, or still open?
- Which objective/spec/ticket claims have evidence?
- Is critique required, complete, deferred with rationale, or blocking?
- Did implementation discover new research, spec, plan, or constitution truth?
- Is the next ticket tranche obvious and within delegated authority?
- Would continuing exceed budget, scope, safety, or context limits?

Record the reassessment where it belongs before continuing:

- initiative status summary for objective-level satisfaction and remaining gaps
- plan strategy snapshot for tranche-level sequencing changes
- ticket journal and acceptance disposition for live execution state
- evidence and critique links for support or blockers

For drives with stable objective IDs, every continuation decision should be
traceable to at least one objective criterion, spec acceptance ID, or ticket-local
claim. If none exists, repair the objective contract before continuing.

The answer determines whether to continue, ask the user, route to review/wiki, or
stop.

## Stop And Escalation Conditions

Stop or ask the user when:

- objective or success metrics remain too fuzzy for safe records
- a tradeoff would invent product direction or accept material risk
- continuation would widen scope beyond delegated authority
- required evidence is absent or contradicted
- critique has unresolved medium/high findings without accepted disposition
- write scopes conflict or shared state makes parallel work unsafe
- a blocker prevents ticket progress
- budget, time, privacy, safety, or context limits are hit
- the next step cannot be represented as a bounded Loom route or owner-record
  update

Stopping is a correct loop outcome when it preserves truth and authority.

## Compaction And Continuity

The loop is resumable only if Loom records tell the truth. Before relying on
conversation context, update or create the owner record that should carry the
fact.

A fresh agent should be able to resume by reading:

1. the initiative and any linked research/spec/plan records
2. active or blocked tickets and their evidence/critique disposition
3. consumed Ralph packets or other bounded child outputs when needed for audit
4. wiki pages only for accepted explanation, not live state

Use `checkpoint-resume-protocol.md` for deterministic resume discovery and the
required checkpoint fields.
