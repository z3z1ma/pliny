---
name: loom-memory-reflect
description: Reflect on Loom memory and distill what should become patterns, hot-memory updates, threads, or sharper supporting context. Deep synthesis — pattern recognition, condensation, consistency sweeps, thread detection, entity format enforcement, and proactive synthesis suggestions. Use when memory needs a deeper synthesis or consistency pass across observations, patterns, entities, links, and current-state summaries. Not for ordinary one-off memory writes, canonical record updates, or purely mechanical archive rebuilds.
compatibility: Designed for this Markdown-first Loom repository.
metadata:
  author: agent-loom
  version: "0.1"
  loom-layer: supporting-memory
---

# loom-memory-reflect

This skill governs deeper synthesis across `.loom/memories/`.

Self-improvement — pattern recognition, memory maintenance, knowledge base quality.

## Use This Skill When

- observations or self-observations need to be condensed into patterns
- hot memory has drifted away from what warm files now justify
- memory needs a consistency or synthesis pass rather than one local update
- the user says "reflect", "what have you learned", "how can you improve"

## Do Not Use This Skill When

- you only need to store or read one supporting fact
- the work is purely mechanical pruning or index rebuilds
- the result should be a canonical `.loom/` record instead of memory

## Reflection Posture

**You have time and freedom.** This is a deep session — don't rush. Read broadly, cross-reference thoroughly, and ACT on what you find. You are not just observing — you are the maintainer of the knowledge base. Reorganize files, condense observations, archive stale data, fill gaps, fix contradictions. Leave things better than you found them.

Don't just log what you found. Fix stale summaries, tighten routing, merge duplicated ideas, and leave the memory graph more coherent than you found it.

## Reflection Playbook

1. run orientation shell commands to scope work before reading files
2. read system memory files: self-observations, patterns, improvements
3. read all hot-memory files and relevant domain files
4. run consistency sweep: hot-memory vs canonical sources, cross-file fact check, temporal validity
5. run condensation check: look for clusters of 3+ observations on the same theme
6. enforce pattern file caps (70 lines / 5.5KB hard limit)
7. review hot-memory relevance: promote what's heating up, demote what's gone quiet
8. enforce entity registry format: 3-line max, status/last fields, cross-domain pointers
9. detect thread candidates: topics across 3+ dates or 2+ weeks
10. run proactive synthesis suggestions: cluster last 7 days of observations
11. act on findings: write, triage, reorganize, condense, connect
12. compose debrief listing every file modified

## Reflection Focus

- contradictions between hot memory and warmer source files
- clusters of 3+ observations on the same theme
- stale current-state notes that should be demoted or removed
- entity entries that exceed 3 content lines
- scattered notes that want one read-optimized thread
- facts that are living only in memory even though they now deserve canonical status
- pattern file approaching the 70-line cap

## How To Use The Scripts

- `scripts/memory.py memory scan`: scope the current memory surface before broad reads
- `scripts/memory.py memory validate`: confirm the module shape before and after meaningful edits

## Manual Invocation

For explicit human-invoked reflection, use `commands/loom-memory-reflect.md`.

That command carries the full step-by-step process with shell orientation commands and is executable purely by the LLM from the visible memory files and normal file tools.

## Done Means

- patterns capture what repeated observations justify
- hot memory now reflects what matters now
- entity entries comply with the 3-line compact format
- thread candidates have been identified or raised
- memory is more coherent than it was before the pass
- debrief lists every file modified

## Read In This Order

1. `references/reflect-workflow.md`
2. `references/commands.md`
3. `references/scripts.md`

## References

- `references/reflect-workflow.md`
- `references/commands.md`
- `references/scripts.md`
