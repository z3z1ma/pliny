# Critique Schema Reference

## Purpose

Critique records capture one bounded adversarial review in a way that can be resumed, inspected, and linked to follow-up work.

The durable record does not need a special subtype for every critique lens. The parent may steer one critique pass through the launch prompt, and that chosen emphasis should be reflected in the record's review question, focus areas, evidence reviewed, and verdict reasoning.

## A Strong Critique Record Answers

1. what was reviewed
2. what question the review tried to answer
3. what evidence was actually examined
4. what verdict the reviewer reached
5. what risks remain even after review
6. what follow-up work should happen next

It should also answer whether the review was strong enough to change acceptance, routing, or confidence in the work.

## Frontmatter Expectations

Critique records should preserve:

- stable `id`
- `kind: critique`
- truthful `status`
- `repository_scope`
- links to the reviewed artifact, related verification, follow-up tickets, and docs or plans when relevant
- timestamps that move when the durable review state changes

## Section Guidance

- `Target Under Review`: identify the exact artifact or artifact set
- `Review Question`: state the question the critique is answering
- `Focus Areas`: name the dimensions the review emphasized, including any parent-directed lens such as devil's-advocate pressure testing or verifier-style evidence scrutiny when that emphasis materially shaped the review
- `Relevant Context`: include only the context that changes interpretation of the findings
- `Evidence Reviewed`: say what was actually read or checked
- `Verdict`: classify the reviewed target in plain language
- `Residual Risks`: record what remains risky even if the target is broadly acceptable
- `Follow-up Tickets`: point to execution work created by the review
- `Findings Summary`: summarize the concrete problems, not just the overall mood

The body should make it easy for a later reader to tell exactly what was reviewed, what evidence was used, and why the verdict makes sense.

If the parent supplied a specific critique emphasis in the launch prompt, the record should preserve that emphasis in the body rather than leaving it implicit in transient invocation history.

## A Strong Critique Run Should Preserve

- what packet or evidence set was used
- whether the review was performed from a fresh context
- what broader project context materially affected the verdict
- what parent-directed review emphasis materially affected the verdict
- what verification status the reviewer relied on
- what residual uncertainty remains

## Verdict Guidance

The verdict should not be a vibe. It should communicate a durable judgment such as:

- acceptable as-is
- acceptable with follow-up risk
- not acceptable until specific defects are fixed
- not reviewable yet because the evidence set is insufficient

If the evidence is incomplete, say so directly rather than projecting confidence.

## Finding Quality Standard

Each major finding should be specific enough that another agent can act on it without reconstructing the review from scratch.

Each finding should ideally preserve:

- the problem
- why it matters
- evidence
- affected scope
- failure mode or risk
- recommended action

If the review knows something important is unknown, record the open question and what evidence would resolve it instead of hiding uncertainty behind a confident verdict.

## Failure Cases To Avoid

- verdict without evidence
- findings that sound serious but cannot be acted on
- review prose that silently changes execution truth instead of reviewing it
- critique records that never say what was actually reviewed

## Done Means

- the review question is bounded
- verdict and findings are durable and evidence-backed
- residual risk is explicit
- follow-up work is obvious to the next actor
