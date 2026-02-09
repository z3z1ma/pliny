---
id: 20260209212240-starter-snippets-what-why-when-13d3368f
title: "Starter snippets: WHAT/WHY/WHEN"
tags:
- agents
- docs
scopes:
- kind: file
  raw: README.md
  path: README.md
visibility: shared
status: active
created_at: "2026-02-09T21:22:40Z"
updated_at: "2026-02-09T21:39:33Z"
---



When writing copy/paste starter snippets for Loom subsystems, optimize for WHAT/WHY/WHEN and push HOW to progressive disclosure via `loom <subsystem> -h` and `loom <subsystem> prime`. Include on-disk footprint and 2-4 starter commands. Prefer steering agents to use Loom CLIs rather than hand-editing `.loom/**` artifacts.

Additional guidance: for LLM compliance, start each snippet with a definitive policy sentence like "We use Loom <Subsystem> for <purpose>" and still keep explicit WHAT/WHY/WHEN lines (semi-redundancy is good).

Style note: In README-facing starter snippets, prefer cohesive paragraphs over literal "WHAT/WHY/WHEN" labels; keep the same information, but blend it into unambiguous policy + reasoning that reads naturally for humans and models.
