# Drive Loop

This reference supports the `loom-drive` skill.

The drive loop is a skill-driven parent workflow through existing Loom owner
layers. It starts from a user request and advances only through recorded owner
truth and bounded packets.

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
intake -> objective-contract -> owner-shaping -> tranche-planning -> ticket-execution -> reconciliation -> reassessment -> continuation | ask_user | stop
```

- `intake`: decide whether the request is actually drive-shaped.
- `objective-contract`: capture outcome, success signals,
  `# Delegated Authority / Autonomy Boundaries`, and
  `# Objective-Level Stop Conditions` when delegated drive work is in scope.
- `owner-shaping`: create or refine constitution/initiative/research/spec/plan
  truth.
- `tranche-planning`: slice only the next useful bounded work set.
- `ticket-execution`: advance tickets through local execution, Ralph packets,
  debugging, spikes, codemaps, evidence, critique, wiki, retrospective,
  acceptance review, or ship packaging as the record truth requires.
- `reconciliation`: update ticket truth and any owner records affected by the
  result.
- `reassessment`: compare current state against the objective contract.
- `continuation`: create the next tranche or choose the next owner/workflow step
  by reasoning from the records.
- `ask_user`: pause for a focused decision the agent cannot safely infer.
- `stop`: objective satisfied, blocked, unsafe, over budget, or outside authority.

These are parent reasoning labels only. Do not save `continuation`, `ask_user`,
or `stop` as frontmatter, ticket status, route fields, or workflow tokens; record
the owner truth, blocker, acceptance decision, or focused user question in the
layer that owns it.

Before `ticket-execution`, run the hard preflight gates in
`checkpoint-resume-protocol.md`. A failed gate points to the owner repair that can
clear it and blocks implementation execution, acceptance, `ship`, external
handoff/PR/release packaging, and dependent continuation until repaired.

Do not skip directly from intake to execution for broad objectives. The graph must
first contain enough objective truth to make continuation recoverable.

## Activation Triage

Ask what the user actually requested:

- **High-level objective**: create or refine initiative-level outcome and success
  criteria, then drive through this loop.
- **Existing initiative continuation**: read the initiative/plan/ticket chain,
  identify the next unmet objective gap, and create or advance the next tranche.
- **Single bounded task**: use the ticket owner, local execution, Ralph, debugging,
  spike, or codemap as appropriate instead of using the full drive loop.
- **Unknown evidence or behavior**: use research or spec shaping before
  creating execution tickets.

Drive-shaped work has both an outcome and delegated continuation. If the user
only asks for a recommendation, explanation, or one bounded mutation, choose the
owner skill that owns that narrower truth instead.

If scope ownership or workspace trust is unclear, return to `loom-workspace`.

## Focused Objective Questions

Ask as few questions as can safely establish:

1. target outcome in measurable terms
2. success criteria or acceptance signals
3. the observed baseline, current workaround, or concrete pain when the objective
   depends on a problem claim
4. the smallest valuable shape when the request is a bundled solution rather than
   a crisp outcome
5. constraints, non-goals, and risk tolerance
6. Delegated Authority / Autonomy Boundaries: what the agent may decide, what
   requires user approval, and any budget/time, risk, privacy, safety, or other
   autonomy limits
7. Objective-Level Stop Conditions: when continuation must stop, ask the user,
   or return to shaping before more work proceeds
8. preferred first tranche when multiple routes are equally plausible

For product, behavior, architecture, workflow, or operator-experience objectives,
use the workspace pressure-check lens before committing to the objective contract:
evidence, specificity, counterfactual, attachment, and durability gaps. Ask only
the gaps that would change the owner record or first tranche.

If the user cannot answer everything, record reasonable assumptions only when
they are low risk and explicitly reversible. Otherwise ask the user and record the
decision needed, why the agent cannot infer it safely, and which owner record will
be updated after the answer.

When the answer becomes durable, convert success criteria into stable objective
criterion IDs in the initiative, such as `OBJ-001`. Tickets, evidence, and
critique can then cite those IDs when judging whether the drive should continue.

## Owner-Layer Routing

- project identity, principles, hard constraints, durable roadmap direction, or
  citable decisions -> constitution
- objective, outcome metrics, strategic framing, delegated autonomy boundaries ->
  initiative
- missing evidence, options, tradeoffs, rejected paths -> research
- intended behavior and reusable acceptance contract -> spec
- complex-change planning, decomposition, sequencing, rollout, and tranche strategy -> plan
- live execution, blockers, next move, closure -> ticket
- bounded child implementation contract -> packet through Ralph
- observed artifacts and validation output -> evidence
- adversarial verdicts and required follow-up -> critique
- accepted explanation or reusable workflow knowledge -> wiki
- support-only recall, retrieval cues, preferences, reminders, or hot context ->
  support coordinator `loom-memory`; not project truth

Do not let the plan become the ledger. Do not let a packet, subagent response,
drive snapshot, critique verdict, or wiki page redefine acceptance. Move truth
into the owning ticket before relying on it.

## Tranche Shape

A tranche is the next small set of work that advances the objective while keeping
review and recovery tractable.

Use `tranche-decision-protocol.md` when objective criteria, evidence gaps,
critique state, dependency order, or write-scope conflicts make the next tranche
unclear. If the owner chain already names one bounded ready ticket and the next
safe action is inferable, do not create extra gap or tranche paperwork.

A good tranche:

- maps to explicit objective or spec claims
- creates independently legible tickets
- avoids overlapping write scopes unless intentionally sequenced
- names expected evidence and critique posture
- leaves the next reassessment point obvious

A fuller tranche detail is only needed when those facts are not already clear
from the owner chain. When using one, name included objective/spec claims,
excluded claims, dependency order, likely write scopes, evidence/critique gates,
and the reassessment point.

Do not decompose the whole objective merely to look complete. Decompose enough to
make the next safe progress step durable.

## Execution Routing

For outcome-driven software work, keep the delivery chain visible even when Loom
does not use command pipelines. The normal chain is:

```text
discover/prioritize -> orient/codemap -> shape behavior/sequence -> execute -> clean up -> critique -> validate -> sync explanation/docs -> ship package
```

Translate each gate into Loom owners instead of copying a command runtime:

- discovery and prioritization -> initiative, research, plan, or ticket triage
- orientation and repo intelligence -> codemap, evidence, research, and wiki atlas
- planning and behavior contract -> spec, plan, and ticket readiness
- implementation -> local execution or Ralph under a ticket-owned scope
- cleanup -> local execution plus critique/evidence when AI artifacts, debug traces,
  placeholders, dead code, or over-engineering could distort the result
- review -> critique with pass splitting proportional to risk
- validation -> evidence tied to ticket/spec claims and acceptance criteria
- documentation or explanation sync -> wiki, README/product docs, research, or
  follow-up ticket according to what truth changed
- PR, release, merge, or external handoff -> ship, with ticket acceptance still
  owning closure

Do not require every gate for every ticket. Do require an explicit disposition when
a gate is skipped or left incomplete on non-trivial or high-risk work, using the
vocabulary owned by that gate: critique disposition status, evidence disposition
status, promotion disposition, or ticket-owned finding disposition. Do not use
`converted_to_follow_up` as a generic gate status; it is only a ticket-owned
finding disposition for a qualified critique finding.

For each ticket or follow-up:

- use local execution when the change is tiny, obvious, and safe in the current
  context
- use Ralph when the implementation step benefits from fresh context or explicit
  write boundaries
- use debugging when a failing behavior or incident needs reproduce-first routing
  before the fix path is clear
- use spike when a bounded experiment, prototype, or sketch should produce
  research/evidence before commitment
- use codemap when repository or module structure should be mapped into evidence,
  research, or accepted atlas knowledge
- use critique when review is required or risk warrants adversarial inspection
- use wiki or retrospective when accepted understanding should persist
- use ship when already-truthful work needs PR, merge, release, or handoff
  packaging without closing the ticket
- update constitution/initiative/research/spec/plan when execution reveals missing
  authority, strategic framing, evidence, behavior, or planning truth

Before launching child work, declare target, read scope, write scope, stop
conditions, verification posture, and output contract. After return, reconcile
before launching dependent work.

When several actions are possible, apply the decision priority from
`tranche-decision-protocol.md` instead of selecting the most implementation-like
action by habit.

When several child tasks can run independently, treat that as bounded parallel
work: each child gets a packet or explicit handoff contract, non-overlapping write
scope, output contract, and parent merge target. Do not rely on a shared chat
plan.

## Reassessment Checklist

After each ticket or tranche, the parent checks:

- Which objective criterion IDs are satisfied, partially satisfied, or still open?
- Which objective/spec/ticket claims have evidence?
- What critique policy applies, and is the ticket-owned critique disposition
  `pending`, `blocking`, `completed`, `deferred` with rationale, or
  `not_required` with rationale?
- Did implementation discover new research, spec, plan, or constitution truth?
- Is the next ticket tranche obvious and within delegated authority?
- Would continuing exceed budget, scope, safety, or context limits?

Record the reassessment where it belongs before continuing:

- initiative status summary for objective-level satisfaction and remaining gaps
- plan strategy or execution-unit updates for tranche-level planning changes
- ticket journal, critique disposition, and acceptance decision for live execution
  and closure state
- evidence and critique links for support or blockers

For drives with stable objective IDs, every continuation decision should be
traceable to at least one objective criterion, spec acceptance ID, or ticket-local
claim. If none exists, repair the objective contract before continuing.

The answer determines whether to continue, ask the user, run review/wiki work, or
stop.

## Stop And Escalation Conditions

Stop or ask the user when:

- objective or success metrics remain too fuzzy for safe records
- a tradeoff would invent product direction or accept material risk
- continuation would widen scope beyond delegated authority
- required evidence is absent or contradicted
- critique has unresolved medium/high findings without ticket-owned disposition
- write scopes conflict or shared state makes parallel work unsafe
- a blocker prevents ticket progress
- budget, time, privacy, safety, or context limits are hit
- the next step cannot be represented as a bounded packet or owner-record update

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
