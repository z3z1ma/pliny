# Core Identity

Loom is a mandatory operating protocol whenever Loom is present in the workspace.

It is not decorative documentation and it is not a loose suggestion.
If the repository uses Loom, you must use Loom's layers, loops, and truth boundaries instead of improvising a parallel workflow in chat or in ad hoc files.

Loom is Markdown-native.
It uses typed records and bounded handoffs to keep AI work recoverable across
disposable context windows.

The layer model decides which artifact owns each kind of truth.
Ralph is the bounded handoff loop for execution.
Every durable claim, behavior, proof, risk, and explanation should land in the
artifact layer that owns that kind of truth.

## The Main Mental Model

Think in three things at once:

1. **layers** — which artifact owns the next truth change
2. **loops** — outer loop for scoping, inner loop for execution
3. **packets** — the bounded contract for any fresh-context run

If you are not sure what to do next, ask:

- what layer owns this
- are we still shaping the work or already executing it
- does the next step require a packet

## What Loom Optimizes For

Loom exists so a fresh agent can enter a project cold and still recover:

- what the project is trying to do
- what is being worked on now
- what has already been learned
- what exact step should happen next
- what evidence supports the current claims
- what explanation should persist after the work lands

That recovery should come from visible files, not from transcript archaeology.

Loom assumes any one context window may be temporary.
The durable graph, not transcript memory, should make the work recoverable.

## Mandatory Operating Sequence

When Loom is present, the default sequence is:

1. orient in the workspace
2. read the constitution
3. identify the owning artifact layer
4. read the governing initiative / research / spec / plan / ticket chain as needed
5. decide whether the next step is outer-loop work or a Ralph iteration
6. if Ralph is needed, compile a packet before launching fresh context
7. reconcile results back into ticket truth
8. route into critique and wiki when the change class requires it

Do not jump directly from vague request to code change if the Loom graph is supposed to own the work.

## Local Work vs Loom Work

Not every small edit needs a new initiative or a new packet.

Stay local when:

- the task is tiny and obviously within an already-owned ticket
- the task is low risk and does not widen scope
- the next mutation is a straightforward record cleanup
- no fresh-context handoff is needed

Engage Loom more fully when:

- scope is unclear
- behavior is unclear
- strategy is unclear
- the work needs durable execution tracking
- the work needs adversarial review
- the work needs a persistent explanation page
- the work should advance through a fresh bounded worker

## The Backbone Hierarchy

The backbone of Loom is:

`constitution -> initiative -> plan -> ticket`

This is the default binding chain.

`research` and `spec` are important but conditional:

- use **research** when evidence is missing
- use **spec** when intended behavior is missing

They strengthen the chain.
They do not replace it.

## The Two Loops

### Outer loop

The outer loop makes the work legible before execution.

It scopes, researches, sharpens behavior, sequences the work, and creates the ticket that will own live execution.

### Inner loop

The inner loop is Ralph.

It advances one bounded slice through a persisted packet and one fresh worker.

## The Non-Negotiables

- tickets are the sole live execution ledger
- critique is a first-class review layer, not a side comment
- wiki is the persistent explanation layer
- packets are bounded contracts, not transcript dumps
- scope must fail closed
- completion claims require evidence and truthful records
- the filesystem is the API
- harnesses and external systems may execute or mirror Loom, but canonical
  Loom records own Loom truth

## Failure Modes To Avoid

Do not:

- keep the real plan only in your transcript
- treat packets as if they outrank canonical records
- let a plan or wiki page quietly become the execution ledger
- let external issues, PR descriptions, generated context files, dashboards, or
  command wrappers become shadow truth
- skip critique because the implementation feels good
- leave useful explanations trapped in chat instead of promoting them into the wiki
- widen scope because a nearby change seems convenient
- close work on vibes

## Default Posture

Loom wants you to be disciplined, explicit, and incremental.

Prefer:

- one owner layer at a time
- one bounded packet at a time
- one truthful ticket at a time
- one critique pass when risk warrants it
- one durable wiki promotion when accepted understanding changes
