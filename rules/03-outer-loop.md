# Outer Loop

The outer loop is Loom's scoping and framing engine.

Its job is to make the work small enough, clear enough, and honest enough that the inner loop can execute without guessing.

## The Outer Loop Questions

Before you compile a packet or start coding, answer these questions:

1. what durable problem or opportunity exists
2. what layer currently owns it
3. what larger strategic frame constrains it
4. what evidence is missing
5. what behavior is still fuzzy
6. what sequence makes sense
7. what is the next bounded ticket-sized step

If you cannot answer those, you are not ready for Ralph yet.

## Backbone Progression

The default progression is:

`constitution -> initiative -> plan -> ticket`

Use it like this:

- update **constitution** when principles, identity, or hard constraints changed
- create or refine an **initiative** when the outcome is strategic and cross-cutting
- create **research** when the work needs investigation before committing
- create a **spec** when intended behavior is unclear or acceptance is fuzzy
- create a **plan** when sequencing matters
- create a **ticket** when one bounded execution owner is needed

Not every task needs every layer.
But every non-trivial task should be explainable against this model.

## Ticket Readiness Standard

A ticket is ready for Ralph only when it makes the next iteration obvious enough that a fresh worker does not need transcript context to begin.

A ready ticket should make all of these legible:

- why this work matters now
- what is in scope
- what is out of scope
- what acceptance means
- what artifacts constrain the work
- what evidence the parent will expect

If the ticket cannot do that, keep working in the outer loop.

## When To Add Research

Add or update research when:

- you are making decisions from weak evidence
- multiple options exist and the tradeoffs matter
- you are about to encode assumptions into a spec or plan
- an implementation discovery should remain citable

A research record should end the need to rediscover the same reasoning later.

## When To Add A Spec

Add or update a spec when:

- the intended behavior is under-specified
- acceptance criteria are vague
- different plausible implementations would lead to materially different outcomes
- critique or wiki will need one stable behavior source later

Specs turn "I think we mean X" into "the project currently intends X".

## When To Add A Plan

Add or update a plan when:

- the order of work matters
- one ticket is not enough
- rollout strategy matters
- there are dependencies or phases that future tickets should inherit

Plans are execution strategy, not execution truth.

## Decomposition Rule

The outer loop should keep decomposing until the next step is bounded enough to fit one of these shapes:

- one local edit pass with no packet
- one Ralph packet
- one critique pass
- one wiki pass

If the next step still feels like "do the whole feature", it is not decomposed enough.

## Loopback From Ralph

The inner loop is allowed to discover that the outer loop was incomplete.

When Ralph returns with:

- ambiguous behavior
- missing evidence
- missing strategy
- missing constraints
- ticket too wide
- scope unexpectedly larger than expected

the parent should route back outward instead of forcing execution through ambiguity.

Typical loopback routes:

- Ralph -> research
- Ralph -> spec
- Ralph -> plan
- Ralph -> ticket refinement
- Ralph -> constitution in rare architectural cases

## Consult Constitution Before Deciding

Before making a non-trivial architectural or policy choice, check whether the constitution subsystem already speaks to it.

Constitution, decision records, and roadmap records are precedent, not history. Re-deriving a choice the project already made wastes work and risks contradicting accepted policy.

Practical checks at the start of outer-loop work:

- `rg -n '^id:' .loom/constitution` to list the current constitutional surface
- `find .loom/constitution/decisions -name '*.md' | sort` to scan prior decisions
- `rg -n '<topic>' .loom/constitution` to see whether this topic already has policy

If prior constitutional truth applies, inherit it. If the new work contradicts it, treat that as a loopback into the constitution subsystem — either amend the policy explicitly or change the work, not silently both.

## Strategic Restraint

The outer loop should clarify the work without over-architecting it.

Do not create records just to satisfy bureaucracy.
Create them because a future agent would genuinely need them.

The right question is not "can I make another artifact?"
The right question is "what artifact would reduce ambiguity, improve safety, or preserve understanding here?"
