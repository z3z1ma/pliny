---
name: loom-memory-housekeeping
description: Perform mechanical Loom memory maintenance so `.loom/memories/` stays small, indexed, linked, and structurally healthy. Archive stale data, prune hot-memory by structural rules, enforce entity format, maintain temporal facts, run link audits, rebuild glacier and link indexes, and maintain L0 headers. Use when memory needs pruning, archive upkeep, link-index rebuilds, or index validation across the module. Not for semantic reflection, ordinary one-off memory writes, or canonical record changes.
compatibility: Designed for this Markdown-first Loom repository.
metadata:
  author: agent-loom
  version: "0.1"
  loom-layer: supporting-memory
---

# loom-memory-housekeeping

This skill governs mechanical maintenance across `.loom/memories/`.

## Use This Skill When

- memory files need pruning or archive upkeep
- the glacier or link index needs rebuilding
- the module shape or L0 coverage needs validation after edits
- the user says "housekeeping", "clean up memory", "prune"

## Do Not Use This Skill When

- the work is mainly about semantic synthesis or pattern distillation
- the work is just one ordinary memory read or write
- the result should be a canonical `.loom/` update

## Housekeeping Posture

Keep memory small, legible, and easy to navigate.

Mechanical maintenance should improve the module without pretending to make semantic judgments that belong to reflection or canonical record writing. Relevance judgment (promote/demote) is loom-memory-reflect's job — housekeeping applies structural rules.

Nothing should vanish just because it stopped being current. Prune, condense, or archive it into the right layer. Never silently delete — always move or note removal in debrief.

## Housekeeping Playbook

1. run orientation shell commands to scope work before reading files
2. garbage collect: archive stale observations, action items, improvements per threshold rules
3. prune hot memory: structural rules, priority order, <50 lines
4. surface opportunities & accountability: stale items, dormant domains
5. rebuild glacier index from archive frontmatter
6. run link audit: entity mentions, cross-domain references, action item references
7. enforce entity registry format: 3-line max, glacier candidates, missing metadata
8. maintain temporal facts: strikethrough expired `(until YYYY-MM)`, move to Historical
9. rebuild link index from `[[wiki-links]]`
10. L0 header maintenance: add missing headers
11. compose debrief listing every file modified

## Pruning Priorities

Keep ALL `hot-memory.md` files under 50 lines.

Trim in this order:

1. **Resolved items** — anything with ~~strikethrough~~, "DONE", "RESOLVED"
2. **Past events** — entries about dates that have already occurred
3. **SSOT violations** — same fact in hot-memory AND the canonical file. Keep in canonical file, replace hot-memory copy with `[[link]]` or remove
4. **Stale entries** — items not referenced in 14+ days
5. **Low-signal entries** — FYI items with no action or deadline

Where trimmed entries go:

- Entries with lasting value → append to domain's `observations.md`
- Entries that are purely historical → let them go

## Archive Thresholds

- `observations.md` >50 entries → `glacier/{domain}/observations-{tag}.md` (group by primary tag)
- `system/self-observations.md` >50 entries → `glacier/system/observations-{tag}.md`
- `action-items.md` >10 completed → `glacier/{domain}/action-items-done.md`
- `entities.md` >150 lines, inactive 6mo+ → `glacier/{domain}/entities-inactive.md` (leave stub)
- `system/improvements.md` >10 implemented → `glacier/system/improvements-done-{YYYY}.md`

All glacier files must have JSON-compatible frontmatter.

## How To Use The Scripts

- `scripts/memory.py memory validate`: validate manifest, required files, and L0 coverage
- `scripts/memory.py memory scan`: inspect the current memory surface quickly
- `scripts/memory.py memory rebuild-glacier`: rewrite `.loom/memories/glacier/index.md` from archive frontmatter
- `scripts/memory.py memory rebuild-links`: rewrite `.loom/memories/link-index.md` from `[[wiki-links]]`

## Manual Invocation

For explicit human-invoked housekeeping, use `commands/loom-memory-housekeeping.md`.

That command carries the full step-by-step process with shell orientation commands and is executable purely by the LLM from the visible memory files and normal file tools.

## Done Means

- the memory module validates cleanly
- hot-memory files are under 50 lines
- archive metadata and the glacier index agree
- link index is current
- entity entries comply with format rules
- L0 headers are present on all active memory files
- debrief lists every file modified

## Read In This Order

1. `references/housekeeping-workflow.md`
2. `references/commands.md`
3. `references/scripts.md`

## References

- `references/housekeeping-workflow.md`
- `references/commands.md`
- `references/scripts.md`
