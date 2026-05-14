---
name: loom-knowledge
description: "Use when reusable understanding, preferences, procedures, concepts, references, troubleshooting notes, atlases, entities, or task-relevant recall should remain available beyond the current session."
---

# loom-knowledge

Knowledge is Loom's reusable understanding and retrieval surface.

It preserves current preferences, procedures, concepts, references,
troubleshooting patterns, codebase atlases, entity notes, and other knowledge
future agents should be able to find quickly.

## Use This Skill When

Use this skill when:

- a preference should shape future collaboration
- a repeatable procedure should be easy to reuse
- accepted explanation should be easier to read than its source records
- a troubleshooting pattern should prevent repeated diagnosis
- a codebase, module, tool, service, package, person, or recurring topic needs a
  retrieval record
- a small cue should help future agents find relevant records, code, tools, or
  domain context
- a knowledge record is outdated, duplicated, misleading, too broad, poorly named,
  or no longer useful

Create knowledge when future retrieval, reuse, orientation, diagnosis, or
collaboration would be materially better with a current record.

Small one-off notes, chat residue, live execution details, and unresolved
investigations belong elsewhere or nowhere.

## Dispatch

If creating or materially updating knowledge:

- read `references/knowledge-shape.md`
- read `references/retrieval-and-loading.md`
- read `references/maintaining-knowledge.md`
- search existing knowledge before creating a new record
- choose a keyword-rich slug that future agents are likely to search
- choose the narrowest useful `Type: Knowledge <Subtype>`
- include `Triggers:` that match likely task words
- include `Applies To:` when path, domain, tool, or workflow scope matters
- use the matching template from `templates/`

If loading knowledge for a session or task:

- after `using-loom` doctrine, load active `Type: Knowledge Preference` records
- for task-specific work, search slugs, titles, `Triggers:`, `Applies To:`, and
  body text using words from the task, ticket, paths, tools, errors, and domain
  concepts
- read likely hits only when they can change the work
- follow related records or code paths when they are needed to apply the knowledge
  safely

If pruning or correcting knowledge:

- update in place when the same topic remains useful
- rename when the slug hurts retrieval, then repair refs with grep
- merge records that serve the same retrieval job
- split records that serve unrelated retrieval jobs
- delete records that no longer help future retrieval, current practice, or safe
  reuse

If only finding or summarizing knowledge:

- inspect `.loom/knowledge/`
- report what the knowledge record says
- preserve the scope and limits the knowledge record states

## Finding Knowledge

Knowledge records live flat under `.loom/knowledge/`.

Useful starting points:

```bash
find .loom/knowledge -maxdepth 1 -name '*.md' -print 2>/dev/null | sort
grep -R '^ID: knowledge:' .loom/knowledge 2>/dev/null || true
grep -R '^Type: Knowledge' .loom/knowledge 2>/dev/null || true
grep -R '^Type: Knowledge Preference' .loom/knowledge 2>/dev/null || true
grep -R '^Triggers:' .loom/knowledge 2>/dev/null || true
grep -R '^Applies To:' .loom/knowledge 2>/dev/null || true
```

A good search combines filename slugs, titles, trigger words, path names, domain
terms, tool names, error text, and known record IDs.

## Knowledge IDs And Filenames

Use stable, keyword-rich IDs:

```text
knowledge:<keyword-rich-slug>
```

Use matching filenames without the `knowledge:` prefix:

```text
.loom/knowledge/<keyword-rich-slug>.md
```

Slugs are retrieval tools, not just identifiers. Choose words future agents are
likely to search.

Prefer:

- `operator-preferences-review-style`
- `ticket-closure-audit-procedure`
- `react-query-cache-invalidation-reference`
- `checkout-timeout-troubleshooting`

Avoid:

- `notes`
- `misc`
- `workflow`
- `person-name`
- `new-thing`

## Record Shape

Knowledge uses plain body labels near the top:

```text
ID: knowledge:<keyword-rich-slug>
Type: Knowledge Preference
Status: active
Created: YYYY-MM-DD
Updated: YYYY-MM-DD
Triggers: comma-separated retrieval words and task cues
Applies To: optional paths, domains, tools, workflows, or contexts
```

Use only `Status: active`.

If a knowledge record is no longer active, update it, rename it with refs
repaired, merge it into a better record, or delete it.

Starter types:

- `Knowledge Preference`
- `Knowledge Procedure`
- `Knowledge Concept`
- `Knowledge Reference`
- `Knowledge Troubleshooting`
- `Knowledge Atlas`
- `Knowledge Entity`
- `Knowledge Note`

New `Knowledge <Subtype>` labels are allowed when they have a real retrieval job.
Use `Knowledge Note` when no sharper subtype improves retrieval or use.

## Knowledge Invariants

Every knowledge record should preserve these invariants:

- current enough to use
- topic-sized rather than sprawling
- keyword-rich slug, title, and `Triggers:` for retrieval
- `Type:` specific enough to guide loading and use
- optional `Applies To:` when path, domain, tool, or workflow scope matters
- provenance, boundary, or related-record notes when they make use safer
- no secrets, credentials, private keys, tokens, passwords, or sensitive personal
  data

Preferences are the eager-loaded knowledge type. Other knowledge is retrieved when
the task, path, tool, error, record, or domain makes it relevant.

## Done Means

Knowledge work is done when:

- the record can be found by likely task words
- the type, triggers, slug, and title make retrieval cheaper
- the prose is useful on its own
- applicability and limits are clear enough to prevent overclaiming
- outdated or duplicate knowledge was updated, merged, renamed with refs repaired,
  or deleted
