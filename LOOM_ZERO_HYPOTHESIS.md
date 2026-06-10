# Loom Zero Hypothesis

Created: 2026-06-10
Branch: `loom-zero`

## Why This Branch Exists

This branch is intentionally destructive. It is not another incremental protocol-compression pass. The point is to challenge the premise that Loom needs a large skill corpus, record station skills, templates, named workflow doctrine, or Ralph-specific machinery.

The hypothesis: **Loom can be expressed as a tiny always-on Markdown doctrine snippet that a user can paste into `AGENTS.md`, `CLAUDE.md`, or equivalent harness instructions.** The agent's latent engineering intelligence can fill in the workflow gaps as long as Loom gives it a small, unambiguous set of record types, headers, ownership rules, and closure/evidence invariants.

If this is true, the existing skill system was scaffolding: useful for discovering the ontology, but not necessary as the final product.

## Core Bet

Less prescription may produce better agents.

A small finite rule set can blend into the background, like Karpathy-style `CLAUDE.md` guidance or compact “grill me” skills. A large doctrine corpus consumes attention, creates inertia, and may make agents behave procedurally instead of intelligently. Loom Zero should preserve the durable memory/resolution substrate while giving the agent more freedom in how it thinks, plans, asks, implements, tests, reviews, and learns.

## What We Learned From Existing Compact Skills

- Karpathy-style guidance works because it installs a few behavioral gates, not a methodology manual.
- `grill-me` works because it changes the interaction shape with very little text: ask sharp questions, one at a time, with a recommended answer.
- `grill-with-docs` works because it captures shared language and decisions as they crystallize, without turning the whole workflow into ceremony.
- Superpowers works because skills are behavior/workflow amplifiers: brainstorming, TDD, debugging, review, branch finish. They are not a canonical truth ontology.

The lesson for Loom: **make Loom the ambient truth substrate; let Superpowers-style skills handle behavior and workflows.**

## Radical Simplification Direction

Current Loom says roughly:

> Use Loom workflows to produce records.

Loom Zero should say:

> Use whatever workflow makes sense. If the work creates durable truth, store it in the right Loom record.

That means Loom is not primarily a skill system. Loom is a lightweight filesystem grammar for project memory, evidence, resolution, and recovery.

## Candidate Minimal Doctrine

Do not treat any snippet in this file as the starting doctrine.

The next step is interactive: decide the smallest possible wording through
back-and-forth, not by inheriting the current corpus or a prematurely drafted
replacement. The doctrine may be only a few sentences, and it may not name every
record type in advance.

What likely survives is not a template but a handful of invariants:

- durable project truth should survive chat
- records need enough header shape to be found and resolved later
- different kinds of knowledge should not be collapsed into one blob
- resolution/closure must be honest about evidence, review, and remaining risk
- the agent should use its own judgment for structure beyond the invariants

The starting text remains unsettled on purpose.

## Candidate Loom Zero Directory Shape

```text
.loom/
  decisions/
  research/
  specs/
  tickets/
  evidence/
  reviews/
  knowledge/
```

Open questions:

- Should `plans/` exist, or are plans just sections inside tickets/specs/knowledge?
- Should `constitution/` become `decisions/`?
- Should `audit/` become `reviews/`?
- Should all templates disappear, leaving only required headers and examples?
- Should statuses collapse to `current`, `resolved`, `superseded`, `cancelled`?

## Pieces That May Disappear

- `using-loom` skill and ordered references
- all record station skills
- most or all templates
- Ralph as a named concept
- `plans/` as a core record type
- `constitution/` as a core record type
- `audit/` terminology in favor of ordinary `review`
- Playbook activation doctrine inside Loom
- adapter-specific Loom doctrine beyond installation/transport

## Pieces That Probably Stay As Invariants

1. Stable record headers: `ID`, `Type`, `Status`, `Created`, `Updated`.
2. Typed ownership: decision, research, spec, ticket, evidence, review, knowledge.
3. Links by stable record ID.
4. Evidence honesty: distinguish observed fact from inference and from proof limits.
5. Closure honesty: tickets close only when scope, acceptance, evidence, review state, and risk are coherent.
6. No chat-only durable truth.
7. Reference repair when records are renamed, superseded, or contradicted.
8. Minimal structure: write only what helps future recovery.

## How Superpowers Fit

Superpowers-style skills should be workflow amplifiers, not Loom ontology:

- grilling/shaping clarifies behavior -> spec, ticket, research, or decision
- TDD produces proof -> evidence
- debugging discovers root cause -> research, evidence, or knowledge
- code review finds risks -> review
- branch finish resolves work -> ticket closure
- retrospective captures lessons -> knowledge, decision, research, or spec

The rule for any workflow skill is simple:

> If this workflow creates durable truth, put that truth in the Loom record type that owns it.

## Testing The Hypothesis

Build a Loom Zero prototype and compare it against current Loom.

Suggested eval prompts:

1. “Build a feature.” Does the agent naturally shape/spec/ticket before broad execution?
2. “Fix this bug.” Does it preserve reproduction and evidence?
3. “We decided to use X over Y.” Does it create a decision or research record?
4. “Continue this old ticket.” Can it recover state from records alone?
5. “Is this done?” Does it require coherent ticket/evidence/review state?
6. “Review this implementation.” Does it create a review record with findings and residual risk?
7. “Summarize what future agents need to know.” Does it create knowledge instead of transcript-only prose?
8. “Rename/supersede this spec.” Does it repair links?

Compare:

- record quality
- agent autonomy
- token drag
- false bureaucracy
- missed evidence
- closure honesty
- human friction
- fresh-context recovery

## Success Criteria

Loom Zero is promising if agents with only the tiny doctrine:

- create recognizable useful records without templates
- route durable facts to sensible record types
- avoid chat-only project truth
- preserve evidence and proof limits
- avoid closing work on vibes
- recover old work from `.loom/` records
- use external workflow skills freely without losing Loom truth
- feel less constrained and more intelligent than current Loom

## Failure Criteria

Loom Zero is too small if agents consistently:

- skip evidence or overclaim tests
- close tickets without review/risk coherence
- mix intended behavior, investigation, evidence, and execution state in one blob
- fail to recover state from prior records
- produce records too inconsistent for future agents to use
- need exact templates to avoid quality collapse

## Working Bias For This Branch

Be bold. Do not protect the existing corpus by default. Treat current Loom as discovered knowledge, not sacred architecture. Preserve only the invariants that actually make future recovery and truthful closure work.

The question is not “how do we compress current Loom?”

The question is:

> What is the smallest background doctrine that lets a strong coding agent recreate the useful behavior of Loom by itself?
