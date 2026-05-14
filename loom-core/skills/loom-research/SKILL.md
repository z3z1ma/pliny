---
name: loom-research
description: "Use when investigation, source synthesis, option comparison, rejected paths, null results, tradeoffs, or evidence-backed conclusions should remain available to future Loom work."
---

# loom-research

Research is Loom's investigation and synthesis surface.

It preserves what was investigated, why it mattered, how the investigation was
grounded, what findings and tradeoffs were discovered, what paths were rejected,
what conclusions are justified, and which surface should consume the result.

Research does not own intended behavior, durable policy, live execution state,
accepted explanation, audit verdicts, or raw observation truth. It gives those
surfaces better reasoning to work from.

## Use This Skill When

Use this skill when:

- an investigation should remain available beyond the current session
- multiple approaches, frameworks, migrations, integrations, or implementation
  strategies need comparison
- external source synthesis or current technical facts matter
- a spike, sketch, prototype, or experiment produced reusable conclusions
- a rejected path or null result would otherwise be rediscovered
- a ticket, plan, spec, constitution record, audit, or knowledge record needs
  investigation-backed support
- implementation discovery is too durable for a ticket journal but not yet
  accepted explanation

Small local investigation can stay in chat or a ticket journal when future work
would not be worse without a research record.

Create research when the question, reasoning, rejection, or conclusion will be
useful to recover.

## Dispatch

If creating or materially updating research:

- read `references/research-shape.md`
- read `references/source-handling.md` when sources, current facts, or source
  quality matter
- inspect relevant records, source, and artifacts before asking the operator to
  repeat facts
- create an `active` record when the question is durable, scope is bounded enough,
  and a likely downstream consumer is known
- use `templates/research.md` as the default starting point

If completing, superseding, or cancelling research:

- preserve the findings, rejected paths, null results, and limits that remain useful
- update `Status:` and `Updated:`
- explain what conclusion, successor record, or cancellation reason now carries
  the durable outcome
- route accepted explanation to knowledge, intended behavior to specs, executable
  work to tickets, complex multi-ticket strategy to plans, and durable judgment to
  constitution

If only finding or summarizing research:

- inspect `.loom/research/`
- report what the research record says
- preserve the distinction between findings, conclusions, recommendations, and
  related surfaces

## Finding Research

Research records live under `.loom/research/`.

Useful starting points:

```bash
find .loom/research -maxdepth 1 -name '*.md' -print 2>/dev/null | sort
grep -R '^ID: research:' .loom/research 2>/dev/null || true
grep -R '^Type: Research' .loom/research 2>/dev/null || true
grep -R '^Status:' .loom/research 2>/dev/null || true
grep -R '^Updated:' .loom/research 2>/dev/null || true
```

Raw source material, when present, lives under:

```text
.loom/research/artifacts/YYYYMMDD-<slug>/
```

The Markdown research record is primary. Source artifacts are support material:
the record should summarize what matters, cite paths or excerpts when useful, and
stand on its own when the artifact directory is absent.

## Research IDs And Filenames

Use `research:YYYYMMDD-<slug>` IDs.

Use matching filenames without the `research:` prefix:

```text
.loom/research/YYYYMMDD-<slug>.md
```

Use the actual current date. Do not copy example dates.

If the slug would collide, choose a clearer slug or add a numeric suffix.

## Record Shape

Research has one record shape:

- `Type: Research`

Use these labels near the top:

```text
ID: research:YYYYMMDD-<slug>
Type: Research
Status: active
Created: YYYY-MM-DD
Updated: YYYY-MM-DD
```

Use these statuses:

- `active`: the investigation is durable and still being worked or evaluated
- `completed`: conclusions and recommendations are bounded enough to cite
- `superseded`: newer research or another surface replaces the conclusion
- `cancelled`: the investigation should not continue, with the reason recorded

Do not create draft research as a parking lot. If the question, scope, and likely
consumer are not clear enough, keep shaping or route to the owner surface first.

## Research Invariants

Every research record should preserve these invariants:

- a durable investigation question
- enough scope to know what is covered and excluded
- enough method and source context to judge the findings
- source quality and freshness notes when they affect the conclusion
- findings separated from conclusions
- meaningful tradeoffs when options are compared
- rejected paths and null results when they prevent future churn
- recommendations routed to the surface that owns the next truth change
- open questions and limits that prevent overclaiming
- no intended behavior, policy, closure, audit verdict, or accepted explanation
  claimed by research itself

Research can cite evidence. Create evidence only when an observation needs to
survive as inspectable support for a claim, ticket, audit, or future review.

Research can produce conclusions. Promote settled reusable explanation to
knowledge when future agents should read the explanation first, not the
investigation history.

## Deep Research

Deep research may collect and compare many sources before conclusions are ready.

For large source sets, keep the research record as the synthesis surface. Use
`.loom/research/artifacts/YYYYMMDD-<slug>/` for raw papers, repo notes, fetched
documents, source lists, generated summaries, benchmark notes, or intermediate
analysis.

The research record should still stand on its own. It should summarize the corpus,
name the important sources, explain source quality, preserve the findings that
matter, and route conclusions to the appropriate surface.

When the investigation becomes too broad for one coherent question, split it into
separate research records and link them.

## Done Means

Research work is done when:

- the record says what was investigated and why
- the source and method context are strong enough for the claim risk
- findings, tradeoffs, conclusions, and recommendations are separated
- rejected paths and null results prevent useful rediscovery
- limits and open questions are visible
- downstream owners can cite the research without treating it as the owner of
  behavior, policy, execution state, evidence, audit, or accepted explanation
