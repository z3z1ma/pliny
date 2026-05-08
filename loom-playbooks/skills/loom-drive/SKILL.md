---
name: loom-drive
description: "Drive delegated objectives through Loom owner layers. Use when the user asks to build, improve, modernize, clean up, migrate, or continue a multi-step outcome that needs shaping, tickets, execution, evidence, critique, and continuation."
compatibility: Markdown-native, script-free Loom protocol.
metadata:
  skill_kind: workflow-coordinator
---

# loom-drive

`loom-drive` is the objective-driven parent-loop coordinator.

It gives the current agent a procedure for turning a broad user objective into
owner records, bounded ticket tranches, Ralph or local execution, reconciliation,
and continuation decisions.

## Core Dependency

This playbook requires `loom-core`. If `using-loom` and the core owner-layer
skills are not installed or preloaded, stop and load/install `loom-core` instead
of treating this playbook as a substitute for Loom doctrine or record grammar.

## Essence

The essence of `loom-drive` is sustained parent judgment.

The user should be able to say what outcome they want, not manually operate every
Loom phase. The parent agent then keeps asking the same governing question:

> What is the next owner-truth mutation or bounded execution step that most
> directly advances the objective without inventing authority?

`loom-drive` is successful when the agent can keep moving between shaping and
execution while the filesystem graph remains the recoverable source of truth. It
is a failure if the real plan lives in chat, if the agent keeps asking for
approval on every obvious next ticket, or if autonomy becomes an excuse to widen
scope without owner records.

## Drive Contract

When this skill activates, the parent accepts a drive contract:

- make the objective measurable enough to judge continuation
- preserve all durable truth in the correct Loom owner layer
- decompose only the next useful tranche, not the whole imagined future
- advance the objective only through the owner layer, workflow, or packet contract
  that the recorded facts justify
- reconcile every child result before depending on it
- continue without waiting for unnecessary user prompts while work remains within
  delegated authority
- stop and ask when the next choice would invent product direction, accept
  material risk, or exceed scope, safety, time, or budget limits

The contract is suspended when the objective can no longer be advanced safely
from the recorded truth.

## Drive Continuity

The loop remains recoverable across sessions only when the current drive state is
recorded in owner artifacts. Before executing downstream work, establish a drive
checkpoint from existing layers:

- initiative owns the objective, measurable success criteria,
  `# Delegated Authority / Autonomy Boundaries`, and
  `# Objective-Level Stop Conditions` for delegated drive work
- initiative success criteria should use stable objective criterion IDs such as
  `OBJ-001` when downstream tickets, evidence, or critique need to cite them
- research owns unresolved evidence, options, rejected paths, and conclusions
- spec owns intended behavior and reusable acceptance criteria
- plan owns high-level complex-change planning, decomposition, tranche strategy,
  sequencing, dependencies, rollout, and execution waves
- tickets own live execution state, blockers, scoped coverage, evidence
  disposition, critique disposition, acceptance decisions, and journals
- packets own bounded child contracts; saved drive handoffs are support artifacts
  that may carry child context, source snapshot, support-local
  `handoff_write_scope`, stop conditions, and output contract without owning
  canonical truth
- evidence, critique, and wiki own observed support, adversarial verdicts, and
  accepted explanation

If a fresh agent could not resume from those records, stop driving and repair the
checkpoint before launching more work.

Use `references/continuity-contract.md` for the continuity convention: objective
status, current tranche, active tickets, blockers, evidence, critique, and journal
history live in existing owner-record sections instead of a new ledger.

Use `references/checkpoint-resume-protocol.md` before stopping, compacting,
launching child work, or handing control to another route. If the checkpoint
cannot be found or updated in owner records, stop driving. Before any child
launch, the checkpoint must already be current; "can update later" is not enough.

## What This Skill Owns

- activation and routing for high-level objective requests
- focused objective-shaping questions before downstream execution
- the repeated parent loop across existing Loom owner layers
- tranche planning and ticket creation posture
- delegation boundaries for owner-layer updates, workflow coordination, packet
  launches, local execution, and optional subagents
- continuation, human-escalation, and stop-condition decisions

## What This Skill Does Not Own

- project truth that belongs in initiative, research, spec, plan, ticket,
  evidence, critique, wiki, or constitution records
- support recall that belongs in memory records
- live execution state; use tickets for execution status, blockers, and closure
- bounded child contracts; Ralph packets own implementation handoff contracts
- critique verdicts or wiki explanation truth
- external scheduling or persistent agent identity

Workflow coordination is not truth ownership. When this skill creates or changes
durable claims, route them into the layer that owns that kind of truth.

## Use This Skill When

- the user asks for a broad outcome, product change, project improvement, or
  multi-step objective rather than one known bounded edit
- an existing initiative or plan should continue without the user manually
  prompting each next ticket
- the work requires moving between objective framing, planning, tickets,
  Ralph execution, debugging, spike, codemap, evidence, critique, wiki, ship
  handoff, spec refinement, implementation slicing, TDD, evidence validation,
  source grounding, context engineering, code review, CI/CD, documentation,
  architecture, product discovery, UI/browser, security, performance, migration,
  simplification, agent orchestration, and reassessment
- context pressure suggests a bounded outer-loop synthesis handoff would make the
  parent more reliable

## Do Not Use This Skill When

Direct owner reasoning wins over drive. If the safe action is already one bounded
owner update or workflow pass, use that owner skill directly and let the ticket,
record, or workflow that owns the truth carry the work.

- the request is already one clear local execution step or one Ralph-ready ticket
- the work is one ticket-sized implementation slice with a clear ticket owner or
  Ralph packet need
- the next truth change belongs entirely to one owner-layer skill
- a single canonical owner record needs a narrow update and no objective-level
  continuation decision is needed
- the user is asking a question that should stay in research, spec shaping, or
  ordinary explanation
- the request depends on capabilities outside the recorded Loom workflow
- scope, budget, authority, or risk is too ambiguous to proceed after focused
  questions

## Activation Triggers

Activate `loom-drive` for chat requests shaped like:

- "build/implement/improve X" where X implies multiple owner records or tickets
- "take this objective and keep going until it is done"
- "continue this initiative/plan" when the next ticket tranche is not yet obvious
- "drive this project toward <outcome>" with delegated autonomy

Before activating, route through `loom-workspace` if the workspace, owner chain,
or repository scope is not trustworthy enough to drive.

Do not activate merely because a task is large. Activate when the user is
delegating outcome advancement across phases. A large but already ticket-ready
implementation still belongs directly to `loom-tickets` or `loom-ralph`; clear
local execution still belongs under the owning ticket or owner skill; and one
single-owner record mutation still belongs to that owner skill.

## User Questioning Posture

Ask only enough focused questions to make the first durable objective safe to
record. Prefer a small batch of questions over repeated approval gates.

Before recording an objective or first tranche, pressure-check the request when it
would shape product behavior, architecture, workflow, or operator experience. Look
for missing evidence that the problem matters, vague beneficiaries, absent current
workarounds, attachment to one solution shape before value is clear, and durability
risks that could make the direction wrong. Ask only the gaps that matter; do not
make the user approve every reversible assumption.

Clarify these before downstream tickets depend on them:

- measurable objective and success criteria
- current baseline, pain, workaround, or observed need when the objective depends
  on a problem claim
- the smallest valuable shape when the request arrives as a large solution or
  bundled feature set
- hard constraints, non-goals, and risk tolerance
- Delegated Authority / Autonomy Boundaries: what the agent may decide without
  returning to the user, what requires user approval, and any budget, time, risk,
  privacy, safety, or other limits
- Objective-Level Stop Conditions: when continuation must stop, ask the user, or
  return to shaping before more work proceeds
- first tranche priority when several owner/workflow choices are plausible

Once those are clear enough, proceed through Loom records without asking for
approval before every ticket. Stop and ask again only at explicit escalation
boundaries.

If the request is still a raw idea, desired feature, or vague product direction
after the pressure check, route to `loom-product-discovery` before drive creates a
tranche. If the request is clearly a specialized workflow, route to that playbook
instead of letting drive become an omnibus engineering manual.

## Default Drive Loop

0. **Accept or refuse the drive contract** — decide whether enough authority,
   objective clarity, and workspace trust exist to drive rather than merely plan
   or ask questions.
1. **Shape the objective** — decide which owner truth is missing and which skill
   can move it without inventing authority.
2. **Record owner truth** — update constitution only when principles,
   constraints, roadmap direction, or citable decisions must change; create or
   refine the initiative for outcome and metrics; add research, spec, or plan
   records only when those layers own missing evidence, behavior, or sequencing
   truth.
3. **Check continuity** — confirm objective, autonomy, current tranche, coverage,
   evidence, critique, blockers, acceptance state, and material journal entries
   live in owner records rather than unrecorded conversation context.
4. **Plan the next tranche** — decompose only enough work to produce bounded,
   independently legible tickets for the next useful step. Use
   `references/tranche-decision-protocol.md` when objective gaps or sequencing
   ambiguity require an optional gap summary or fuller tranche detail before the
   next bounded ticket or workflow pass is safe.
5. **Create or refine tickets** — tickets own live execution state, blockers,
   critique disposition, acceptance decisions, evidence disposition, journal, and
   closure.
6. **Run preflight gates** — distinguish missing owner truth from execution work.
   Failed gates require the owner repair that can clear them; they block local
   edits, Ralph, acceptance review, ship, external handoff/PR/release packaging,
   and dependent continuation until repaired.
7. **Execute bounded work** — use the owner skill when truth must be shaped before
   implementation; use local execution for tiny safe changes, Ralph for fresh-context
   implementation packets, and domain workflows such as debugging, spike, codemap,
   spec refinement, plan/ticket shaping, incremental implementation, TDD,
   evidence validation,
   source grounding, context engineering, code review, CI/CD, documentation,
   architecture, product discovery, UI/browser, security, performance, migration,
   simplification, agent orchestration, critique, wiki, retrospective, acceptance
   review, or ship when their specialized route fits. Durable truth still routes
   to core owner layers. Declare read/write scope and stop conditions before child
   work. `ship` packages or hands off already truthful work; it does not own ticket
   closure.
8. **Reconcile results** — inspect child output, update ticket truth, route
   observations into evidence, findings into critique, accepted explanation into
   wiki, and changed strategy or behavior into the owner layers.
9. **Reassess objective state** — compare current evidence, critique disposition,
   acceptance coverage, and remaining gaps against the objective's success
   criteria.
10. **Checkpoint** — update the drive anchor and live tickets so a fresh chat can
    resume without prior conversation context.
11. **Continue or stop** — create the next tranche, run required critique/wiki or
    retrospective, ask the user, or stop because the objective is satisfied,
    blocked, unsafe, over budget, or outside delegated authority.

See `references/drive-loop.md` for the fuller parent checklist.

## Optional Outer-Loop Subagent Transport

A dedicated outer-loop subagent may be used for context management when the
parent needs fresh synthesis of an objective chain, option set, tranche plan, or
risk list.

This is transport only: the subagent proposes owner-record changes, tickets, and
risks; the parent reviews and reconciles the output before depending on it;
canonical records and tickets retain truth ownership.

Use `references/outer-loop-subagent-transport.md` when optional outer-loop
subagent transport is relevant. Use `templates/outer-loop-handoff.md` only when a
bounded handoff would reduce context pressure or improve reviewability.

## Stop Or Ask The User When

- success criteria, Delegated Authority / Autonomy Boundaries, Objective-Level
  Stop Conditions, or non-goals remain materially ambiguous
- a pressure check exposes an evidence, specificity, counterfactual, attachment,
  or durability gap that would change the objective or first tranche
- the next step would invent product direction the user has not delegated
- scope would widen beyond the current initiative, plan, ticket, or write boundary
- required evidence is missing or contradicted
- open or unresolved medium/high critique findings lack ticket-owned dispositions
  of `resolved`, `accepted_risk`, `superseded`, or `converted_to_follow_up`
- a ticket is blocked, write scopes overlap unsafely, or parallel work could
  corrupt shared state
- budget, time, safety, privacy, or risk limits are reached
- continuation would depend on state or capabilities that cannot be expressed in
  Loom owner records or bounded packets

When a user decision is required, ask one focused question or a small batch of
related choices, state why owner records and delegated autonomy cannot safely
answer it, and name the owner record that should be updated after the response.
Do not ask the user merely to approve low-risk, reversible assumptions that stay
inside delegated authority.

## Common Rationalizations

| Rationalization | Reality |
| --- | --- |
| "The user said continue, so I can decide the product direction." | Delegated autonomy advances recorded objectives. It does not invent materially new direction. |
| "A drive summary can be the live ledger." | Drive coordinates. Tickets own live execution state and acceptance. |
| "A big objective needs a big plan before action." | Decompose only enough to make the next safe tranche clear. |
| "The subagent output looks complete, so I can depend on it." | Child or support output must be reconciled into owner records before it becomes usable truth. |
| "Drive can handle every workflow directly." | Drive coordinates objectives; specialized playbooks own recurring route discipline when their trigger fits. |

## Red Flags

- current tranche, blockers, or acceptance state exists only in chat
- continuation depends on an assumption that should be an initiative, spec, plan, or ticket fact
- several tickets are launched without dependency or write-scope checks
- drive keeps asking for approval on obvious in-scope moves, or keeps moving after explicit stop conditions
- support handoffs summarize owner truth but owner records remain stale
- drive keeps product discovery, spec, planning, implementation, testing, review,
  CI/CD, documentation, architecture, migration, security, performance, UI, or
  simplification decisions in chat instead of routing to the specialized playbook
  and owner records

## Verification

- [ ] Objective, autonomy boundaries, and stop conditions live in owner records.
- [ ] Current tranche and live execution state live in tickets.
- [ ] Evidence, critique, wiki, and retrospective needs are routed to their owners.
- [ ] Child/subagent output has been parent-reconciled before downstream dependence.
- [ ] The next action is a bounded owner mutation, workflow pass, local execution, or packet.

## Done Means

- the objective and success criteria live in the correct owner record
- current execution state lives in tickets, not chat or a plan
- each child or local execution step has been reconciled into ticket truth
- evidence and ticket-owned critique dispositions are explicit enough for the next
  decision
- the parent has either created the next bounded tranche, asked the user a focused
  question, completed required critique/wiki/retrospective follow-through, or
  recorded why the loop stops

## Read In This Order

Read immediately when activating `loom-drive`:

1. `references/drive-loop.md` for the parent-loop checklist.
2. `references/continuity-contract.md` for the owner-record fields that must
   carry resumable drive state.
3. `references/tranche-decision-protocol.md` for conditional objective-gap
   summaries, optional tranche detail, decision priority, and reconciliation
   targets.
4. `references/checkpoint-resume-protocol.md` for hard safety gates, checkpoint
   updates, and deterministic resume.
5. the core `loom-records` route-vocabulary reference when distinguishing
   workflow choices from statuses, packet outcomes, commands, or support cues.
6. the core `loom-workspace` routing reference if the owner layer or workflow
   coordinator is still unclear.

Then read conditionally:

7. the core `loom-initiatives` skill when creating or refining the objective and
    success metrics.
8. the core `loom-research`, `loom-specs`, or `loom-plans` skills when evidence,
    intended behavior, or complex planning truth is missing.
9. the core `loom-tickets` skill before creating, advancing, or accepting
    bounded execution work.
10. the core `loom-ralph` skill before packetized implementation execution.
11. the core `loom-evidence`, `loom-critique`, `loom-wiki`, or
    `loom-retrospective` skills when observations, review, accepted explanation,
    or learning assimilation is next.
12. optional playbooks such as `loom-product-discovery`,
    `loom-incremental-implementation`, `loom-tdd`, `loom-source-grounding`,
    `loom-context-engineering`, `loom-code-review`, `loom-ci-cd`,
    `loom-docs-sync`, `loom-architecture`, `loom-ui-browser`, `loom-security`,
    `loom-performance`, `loom-migration`, `loom-simplification`, or
    `loom-agent-orchestration` when their specialized trigger fits better than
    generic objective driving.
13. `references/outer-loop-subagent-transport.md` when optional outer-loop
    subagent transport is relevant.
14. `templates/outer-loop-handoff.md` only when launching an optional bounded
    outer-loop synthesis subagent.
