# Research Shape

## Core sections

- Question
- Why This Matters
- Scope
- Method
- Sources
- Evidence
- Rejected Options
- Null Results
- Conclusions
- Recommendations
- Open Questions
- Linked Work

## Spike And Sketch Variants

A spike is a bounded experiment recorded as research.

A sketch is a bounded product or UI variant exploration recorded as research.

Both variants should still preserve:

- question
- method
- evidence
- rejected options
- null results
- conclusions
- downstream route

Use a spike or sketch command when the workflow needs more structure, but keep
the canonical truth in research, evidence, specs, tickets, critique, and wiki.

## Writing standard

Separate:

- evidence from inference
- conclusions from hypotheses
- rejected paths from chosen paths
- null results from open questions

A good research note makes it easy for later work to inherit the thinking without inheriting confusion.

## Rejected Options and Null Results

Capture the dead ends. An option that was considered and rejected, or an approach that was tried and failed, is durable knowledge if another agent would otherwise rediscover the same conclusion. For each, record:

- what was considered or tried
- what rejected it (evidence, constraint, conflict with another layer)
- what the future reader should do instead

When a rejection or null result generalizes beyond this one decision, it is a candidate for promotion into the wiki so future agents encounter it before re-deriving it.

## Deferred Questions

Sometimes an investigation surfaces questions that matter but are not yet heavy enough to justify a dedicated research record. Rather than lose them, keep them in the Open Questions section of the parent research record, or create a research record with `status: deferred_questions` that collects related open questions for a topic.

Deferred questions are a subset of research, not a separate record kind. When a question matures, promote it into its own research record and link back with `superseded_by` or `promoted_to`.
