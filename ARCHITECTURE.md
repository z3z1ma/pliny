# Architecture Notes

Loom is a Markdown-native control plane for AI knowledge work.

It is not a toolchain, runtime, daemon, model router, MCP, dashboard, or product
CLI. Loom's product surface is the visible skills corpus: the mandatory
`loom-bootstrap` skill, subsystem skills, templates, references, and ordinary
filesystem operations.

## Architectural Kernel

Loom has one central invariant: ownership-preserving mutation.

Every durable claim, behavior, observation, risk, decision, and explanation must
land in the artifact layer that owns that kind of truth. Newer files do not win
by recency. More detailed files do not win by confidence. The owner layer wins
for the truth it owns.

The transaction spine is:

```text
route -> shape -> ready -> execute -> reconcile -> verify -> accept -> promote -> close
```

This spine is the product architecture. Bootstrap doctrine, skills, packets,
evidence, critique, and wiki exist to make those transitions explicit and
recoverable.

## Owner Graph

Canonical owner layers own project truth:

- constitution owns durable identity, principles, constraints, precedent, and decisions
- initiative owns strategic outcomes and success framing
- research owns investigations, tradeoffs, conclusions, rejected paths, and null results
- spec owns intended behavior, scenarios, requirements, and acceptance contracts
- plan owns sequencing, rollout strategy, milestones, and execution waves
- ticket owns live execution state, scoped coverage, blockers, acceptance disposition, and closure
- evidence owns observed artifacts and validation outputs
- critique owns adversarial findings, severities, verdicts, and residual risks
- wiki owns accepted explanation and reusable understanding

Durable support surfaces help operation without owning project truth:

- packets own bounded child-worker contracts
- memory owns optional support recall, retrieval cues, preferences, entities,
  reminders, and hot context without owning project truth
- optional, lazy-materialized `.loom/support/` artifacts, such as saved drive
  handoffs, support recovery or handoff without owning objective state, live
  ticket state, acceptance, evidence sufficiency, critique verdicts, wiki truth,
  canonical truth, or packet lifecycle
- workspace and harness records own scope or transport support only

## Loops

The outer loop makes work legible before execution. It chooses the owner layer,
adds research or specs when evidence or behavior is fuzzy, sequences work through
plans when order matters, and creates or tightens the ticket that will own live
execution.

The inner loop is Ralph. Ralph advances one bounded implementation slice through
one packet, one fresh worker, one output contract, and one parent reconciliation.

Critique and wiki may reuse packet discipline, but they are sibling routes, not
Ralph-governed execution.
They are sibling routes governed by their own domain skills.

## Packets

Packets are explicit Markdown contracts. They declare:

- mission
- governing context
- source fingerprint
- change class and risk posture
- child read and write boundaries
- verification posture
- stop conditions
- output contract
- child output
- parent merge notes

A packet is not project truth and not a transcript dump. It is a bounded handoff
that lets a disposable worker mutate a narrow slice without guessing.

## Evidence, Critique, Acceptance

Evidence stores observations. It can support or challenge claims, but it does not
own policy, behavior, sequencing, live execution state, or explanation.

Critique pressure-tests claims, implementation shape, and evidence sufficiency.
It produces findings and verdicts; it does not close work.

Acceptance disposition belongs to the ticket. Commands, commits, packets, PRs,
critique records, and child workers may inform acceptance, but the ticket owns
whether scoped work may close.

## Promotion

Retrospective is the default promotion gate for non-trivial completed work. It
assimilates durable learning into the owner layer that can maintain it:

- accepted explanation -> wiki
- investigation results -> research
- intended behavior clarifications -> spec
- sequencing changes -> plan
- strategic framing -> initiative
- principles or decisions -> constitution
- observed validation artifacts -> evidence
- support-only recall, preferences, and retrieval cues -> memory

Retrospective is a workflow, not a record kind and not a second ledger.

## Skills And Templates

Skills are flat sibling subsystem playbooks. Each skill must be understandable
from its own `SKILL.md`, references, and templates. Hidden inheritance, shipped
helper scripts, and assembly-time behavior must not become the source of truth.

`loom-bootstrap` is the mandatory package entry skill. It carries Loom's ordered
operating doctrine as references. Harness adapters may preload those references as
always-on context, but that preload is an optimization over the same skill package,
not a separate doctrine surface.

Templates are executable prompts for future agents. A good template should force
real IDs, explicit scope, owner boundaries, evidence expectations, and next
routes instead of inviting placeholder graph edges or vague completion claims.

## Native Adapters

Loom does not ship a command-wrapper surface or a cross-harness installer as the
product. The product surface is `skills/`.

Harness adapters transport Loom into particular tools through native plugin,
extension, or skill-package systems. They may preload `loom-bootstrap` references
when the harness supports it cleanly, but they must not define Loom truth.

## Examples

Examples are internal teaching fixtures, not product-surface guidance and not
canonical project truth. They should remain minimal, internally consistent, and
replayable by a cold reader. A good example
shows the starting `.loom` slice, operator request, expected route, expected
artifacts, final state, and common wrong behavior.

## Design Biases

Loom optimizes for:

- legibility to a fresh agent
- explicit truth ownership
- bounded execution
- grep-friendly traceability
- adversarial review
- evidence-backed completion
- knowledge compounding
- portability across harnesses

Loom rejects:

- hidden runtimes as the real protocol
- helper scripts as a second ontology
- one-command project management
- fallback install scripts as product architecture
- external systems as competing ledgers
- generated context files as independent project truth
- transcript memory as the execution record

A future agent should be able to install the skill package, use `loom-bootstrap`,
read the graph, and operate the protocol without hidden runtime magic.
