# Core Identity

This is an ordered reference for the `using-loom` skill.

Loom is mandatory whenever it is present in a workspace. It is not decorative
documentation. Use Loom's layers, loops, and truth boundaries instead of
improvising a parallel workflow in chat or ad hoc files.

Loom is Markdown-native structured paperwork: typed records and bounded handoffs
that make work recoverable across disposable context windows. Records are work
products the agent must satisfy, not passive notes.

Core invariant: durable filesystem records are the recovery graph. Truth is
placed by owner layer, not by recency. The layer model decides which artifact owns
each kind of truth; Ralph provides bounded implementation handoffs; tickets keep
the live execution ledger; evidence records observations; critique records review;
wiki records accepted explanation.

## The Main Mental Model

Think through three axes: **layers** for the artifact that owns the next truth
change, **loops** for shaping versus execution, and **packets** for bounded
fresh-context implementation contracts and packetized sibling workflows.

If unsure, ask what work product is needed, what layer owns it, whether the work
is still being shaped or already executing, and whether the next step needs a
packet.

## Recovery Goal

A fresh agent should recover project aim, current work, prior learning, next
step, supporting evidence, and explanation worth preserving from visible files,
not transcript memory.

## Mandatory Operating Sequence

Default sequence: orient, read the constitution, identify the owner layer, read
the governing initiative/research/spec/plan/ticket chain as needed, decide
whether this is outer-loop work or Ralph, compile a packet before fresh-context
implementation, reconcile results into ticket truth, then route to evidence,
critique, wiki, retrospective, or acceptance review when required.

Do not jump from a vague request to code when the Loom graph should own the work.

## Local Work vs Loom Work

Stay local for tiny, low-risk, already-owned cleanups that do not widen scope or
need fresh handoff. Engage Loom more fully when scope, behavior, strategy,
evidence, review, explanation, completion, ownership, routing, or operator
behavior is unclear or durable enough to matter.

## Backbone And Loops

The backbone for complex work is:

`constitution -> initiative -> plan -> ticket`

Research and spec strengthen that chain without replacing it: research owns
evidence/tradeoffs/investigations/conclusions; spec owns intended behavior and
acceptance.

The outer loop scopes, researches, specifies, plans, and creates the ticket that
owns live execution. The inner loop is Ralph: one bounded slice, one persisted
packet, one fresh worker, and parent reconciliation into the ticket and any other
proper owner layer.

## Non-Negotiables

- tickets are the sole live execution ledger
- ticket-owned acceptance disposition owns closure; commands, commits, PRs, and
  packets do not close work by themselves
- critique is a first-class review layer, not a side comment
- wiki is the persistent explanation layer
- packets are bounded contracts, not transcript dumps
- scope must fail closed
- completion claims require evidence and truthful records
- the filesystem is the API
- harnesses and external systems may execute or mirror work, but canonical Loom
  records own Loom truth

## Failure Modes To Avoid

Do not keep the real plan only in transcript, let packets outrank canonical
records, turn plans or wiki into ledgers, let external systems become shadow
truth, skip warranted critique, trap reusable explanation in chat, widen scope by
convenience, or close work on vibes.

## Default Posture

Be disciplined, explicit, and incremental: one owner layer, one bounded packet,
one truthful ticket, one warranted critique pass, and one retrospective or wiki
promotion when accepted understanding should persist.
