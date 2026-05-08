# Research Shape

## Core sections

- Question
- Why This Matters
- Scope
- Method
- Sources
- Variant / Experiment Matrix when options, prototypes, sketches, or hypotheses are compared
- Evidence Synthesis
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

A useful variant matrix is compact and decision-oriented:

```md
- Variant / hypothesis: <name>
  - Artifact or probe: <path, screenshot, command, or observation>
  - Strength: <evidence-backed strength>
  - Weakness: <risk or limit>
  - Decision: <chosen, rejected, needs follow-up>
```

The matrix should compare meaningfully different options. Three variants that
only change color, wording, or naming are not a sketch; they are surface tweaks.

Use optional `loom-spike` or an equivalent exploration workflow for procedural
spike or sketch detail such as experiment matrices, variant framing, throwaway
write-scope discipline, artifact capture, and downstream routing. Keep the
canonical truth in research, evidence, specs, tickets, critique, and wiki.

## Writing standard

Separate:

- evidence from inference
- conclusions from hypotheses
- rejected paths from chosen paths
- null results from open questions

A good research note makes it easy for later work to inherit the thinking without inheriting confusion.

## Source Quality And Freshness

When research depends on external documentation, peer repositories, generated
summaries, model consultation, or tool output, classify source quality instead of
treating every source equally:

- project-owned records and source code for current implementation reality
- official documentation, specs, standards, changelogs, or release notes for
  external API and version behavior
- primary repository source for peer-practice evidence
- reputable secondary explanation as context, not primary authority
- model, forum, tutorial, or generated summary as untrusted support unless
  verified against stronger sources

Record source state, observed date, version or commit when available, freshness
risk, and recheck trigger. If official sources conflict with project practice,
surface the conflict and route the decision to spec, ticket, or constitution
instead of letting research silently pick a winner.

## Consultation And Debate

External consultation, model debate, or multi-advisor synthesis can support
research when the question benefits from adversarial perspectives. Keep it
bounded:

- name the question and roles or lenses used
- require claims to cite evidence or say they are conjecture
- record concessions, disagreements, unresolved questions, and the parent verdict
- preserve the conclusion in research and route accepted behavior, policy,
  execution, or explanation to the owner layer that owns it

Consultation does not own project truth. It is evidence or analysis for the parent
record to evaluate.

## Rejected Options and Null Results

Capture the dead ends. An option that was considered and rejected, or an approach that was tried and failed, is durable knowledge if another agent would otherwise rediscover the same conclusion. For each, record:

- what was considered or tried
- what rejected it (evidence, constraint, conflict with another layer)
- what the future reader should do instead

When a rejection or null result generalizes beyond this one decision, it is a candidate for promotion into the wiki so future agents encounter it before re-deriving it.

## Deferred Questions

Sometimes an investigation surfaces questions that matter but are not yet heavy enough to justify a dedicated research record. Rather than lose them, keep them in the Open Questions section of the parent research record, or create a research record with `status: deferred_questions` that collects related open questions for a topic.

Deferred questions are a subset of research, not a separate record kind. When a
question matures, promote it into its own research record and name the source and
successor in `links:` or body prose using the shared semantic link guidance.
