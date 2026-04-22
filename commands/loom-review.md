---
name: loom-review
description: "Run adversarial critique against a ticket, packet, spec, wiki page, or other review target. Orchestrate one disciplined pass, or split the review into complementary fresh-context passes, and leave durable critique records with prioritized follow-up."
arguments: "<ticket id | record id | change target>"
category: core
suggested_skills:
  - loom-workspace
  - loom-records
  - loom-critique
  - loom-tickets
  - loom-specs
  - loom-wiki
---

# /loom-review

You are running **Loom Review**.

Review target:
`$ARGUMENTS`

This command is the explicit critique surface.
It exists so review has the same durability and rigor as implementation, and so a review of meaningful risk can be split into complementary fresh-context passes instead of one overloaded reviewer.

Hydrate only what you need from:
- `loom-workspace`
- `loom-records`
- `loom-critique`
- `loom-tickets`
- `loom-specs`
- `loom-wiki`

## Goals

- choose a pass split proportional to the target's risk
- pressure-test claims against evidence
- leave behind durable critique records
- reconcile review back into the ticket without hiding the trail

## Choose the pass split

Decide how many passes this target deserves before starting.

### One-pass review

Use when:

- the target is small
- the risk class is low or medium
- one reviewer can hold the whole target in context
- the harness has no fresh-context subagent transport

### Multi-pass review

Use for medium or high risk targets, or whenever one reviewer would struggle to hold the whole surface without bias. Split the review so each pass enters fresh, with a narrow lens, and cannot carry the blind spots of the other lenses.

Default split:

1. **Correctness and scope.** Do the claims match the evidence? Did the change stay inside its declared scope and write boundary? Are acceptance criteria actually met?
2. **Risk, security, and failure modes.** What breaks at the edges? What assumptions are load-bearing? What security or performance concerns did the implementation silently carry?
3. **Operator clarity and follow-through.** Is the ticket truthful? Is the wiki disposition honest? Will the next agent be able to pick this up cold?

Each pass produces its own critique record, or one consolidated record with clearly separated pass sections. Severity and confidence stay explicit per finding.

If the harness supports subagents or multiple fresh reviewers, launch the passes in parallel with a critique packet per pass. If not, run them sequentially as distinct fresh-context passes with narrow prompts. The transport is flexible; the pass boundaries are not.

## Procedure

1. **Anchor the target.**
   - Identify the ticket, spec, packet, wiki page, or other record being reviewed.
   - If a ticket is the main owner, read it first.

2. **Gather the minimum governing context.**
   - Read the linked plan, spec, evidence, and any recent packet outputs.
   - Inspect the relevant changed files or artifact diffs.

3. **Choose and compile packets.**
   - Decide the pass split.
   - Compile one critique packet per pass under `.loom/packets/critique/` when fresh-context review is warranted.

4. **Review through the chosen lenses.**
   - correctness
   - scope discipline
   - evidence sufficiency
   - hidden assumptions
   - failure modes
   - maintenance burden
   - operator clarity
   - security or performance when relevant

5. **Write findings durably.**
   - Each material finding: short title, severity, confidence, observation, why it matters, follow-up.
   - Record a verdict and residual risks.

6. **Reconcile review back into Loom.**
   - Update the ticket status or journal if the critique changes what must happen next.
   - Create follow-up tickets for substantial issues.
   - Do not quietly "fix and forget" major findings.

## Native tools to prefer

- `git status --short`
- `git diff --stat`
- `git diff`
- `rg -n '^(id|status|review_target):' .loom/{tickets,critique,specs,wiki,evidence} --glob '*.md'`
- `find .loom/packets/critique -type f -name '*.md' | sort | tail`

## Guardrails

- Do not overstate certainty.
- Do not collapse critique into inline comments.
- Do not silently rewrite ticket truth without leaving the review record.
- Do not let one reviewer's blind spot pass as coverage when the target warranted a split.
- Fairness matters: be skeptical, not performatively harsh.

## Required output

- pass split chosen and why
- critique record and packet paths or IDs
- prioritized findings with severity and confidence
- ticket or follow-up updates performed
- recommended next command
