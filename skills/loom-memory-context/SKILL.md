---
name: loom-memory-context
description: Maintain Loom's plain-text cognitive layer under `.loom/memories/` — persistent memory with hot/warm/glacier tiers, L0/L1/L2 progressive retrieval, wiki-link navigation, SSOT routing, and progressive condensation. Use when normal work needs targeted non-canonical memory retrieval or updates, including query routing, fact storage, entity tracking, and observation logging. Not for canonical record updates, deep synthesis passes, or mechanical archive maintenance.
compatibility: Designed for this Markdown-first Loom repository.
metadata:
  author: agent-loom
  version: "0.1"
  loom-layer: supporting-memory
---

# loom-memory-context

This skill governs ordinary read and write work inside `.loom/memories/`.

It is the default memory-routing skill: decide what to read, what to update, what to ignore, and when the fact really belongs in canonical `.loom/` instead.

## Use This Skill When

- current work needs supporting context that should not live only in chat
- you need to read or update hot, warm, or glacier memory files
- the user shares information worth remembering
- you need to route a query to the right memory file
- the user asks deep recall questions such as "what did I say about...", "when did we discuss...", "find that conversation about...", or "history of ..."

## Do Not Use This Skill When

- the fact belongs in a canonical `.loom/` record instead
- you are doing a reflection or condensation pass across memory
- you are pruning archives or rebuilding memory indexes

## What This Skill Governs

- `.loom/memories/hot-memory.md`
- `.loom/memories/system/*`
- `.loom/memories/user/*`
- retrieval decisions across hot, warm, and glacier memory

## Read On Start

Always read these files at conversation start:

- `.loom/memories/hot-memory.md`
- `.loom/memories/system/patterns.md`

These are small by design and give you the current-state orientation.

## Operating Posture

Memory is supporting context. Not just recall, but cognition across time.

Read it to help ordinary work stay grounded, but do not let it outrank canonical tickets, specs, plans, research, critique, docs, or constitutional records.

The module is plain text on purpose. The same tools that work on any Markdown — `grep`, `find`, `wc`, `git diff` — work on memory. Read the smallest useful surface first, write facts to their proper home immediately, and keep the file graph legible enough that another agent can recover context without guessing.

Without this skill active, use judgment: if the query maps to user context → activate with `user` domain. If the query is about the agent, workflow, or memory system itself → activate with `system` domain.

## Memory Retrieval Protocol

When responding to any query:

1. **Identify domain** — match query to `system` or `user`.
2. **L0 scan** — once you know the domain, run `grep -rn "<!-- L0:" .loom/memories/{domain}/` to get all file summaries in one call. Use this to pick the right file(s) before opening anything.
3. **Select files by query type:**
   - Tasks, reminders → `action-items.md`
   - Person, "who is" → `entities.md`
   - Overview, "how is" → `hot-memory.md` + `action-items.md`
   - Following a `[[wiki-link]]` → check `link-index.md` for related files
4. **Apply L1 before L2 for long files** — for any file >80 lines, scan section headers before reading fully.
5. **SSOT check on write** — before writing a fact, check if it already exists in its canonical file. Update there, don't duplicate.
6. Default: if unclear, read hot-memory + action-items for the likely domain.

## Deep Recall Mode

Use this mode when the user is asking for history, narrative reconstruction, or memory search that likely spans multiple files.

For simple one-shot lookups, a direct grep or one-file read is enough. Use deep recall only when you need to piece together a timeline or cross-file story.

### Pass 1: Locate

1. Extract search terms from the query: names, topics, dates, phrases, and likely synonyms.
2. Read the domain hot-memory first for current context.
3. Run L0 scans and targeted grep across the likely domain files:
   - `hot-memory.md`
   - `observations.md`
   - `entities.md`
   - `action-items.md`
   - any thread files in the domain directory
4. If current-domain files are not enough, check `.loom/memories/glacier/index.md` and pull only relevant archive files.
5. If matches are too broad, narrow by domain, date, or added query terms.

### Pass 2: Extract

1. Read the top 3-5 most relevant files by hit density, date relevance, and likely authority.
2. Extract the specific passages that answer the query.
3. Track chronology: first mention, major changes, latest state.
4. Follow `[[wiki-links]]` only when they sharpen the answer.

### Pass 3: Synthesize

1. Answer with a concise timeline or narrative rather than raw dumps.
2. Present findings chronologically when history matters.
3. Call out gaps explicitly when memory is partial or inconsistent.
4. If the search reveals a durable memory gap, suggest the proper file to update.

## Progressive Context Loading

- **L0** — read the `<!-- L0: ... -->` header. Answer: "is this file relevant?"
- **L1** — scan section headers (`## ...`, `### ...`). Answer: "which section is relevant?"
- **L2** — read the full file or section.

Hot-memory files are always L2 — they're small by design.

## File Routing

When the user shares information or asks to save something:

- Task/todo → `action-items.md`
- Person/entity → `entities.md`
- Update/log → `observations.md`
- Status/overview → `hot-memory.md`
- Learned rule → `system/patterns.md`
- Self-note → `system/self-observations.md` or `system/improvements.md`

## Memory Rules In Practice

1. **Write immediately** — don't wait to save something worth remembering
2. **Observations are append-only** — `- YYYY-MM-DD [tags]: <observation>` — never edit past entries
3. **Hot memory <50 lines** — prune aggressively, move detail to observations
4. **SSOT check before write** — each fact lives in ONE canonical file. Other files reference via `[[link]]`, never copy.
5. **Wiki-links on write** — when writing or editing ANY memory file, actively add `[[links]]` to related files. This is the main way links get created.
6. **Write-time back-linking** — when you add a link A→B, ask: "does B benefit from pointing back to A?" If yes, open B and add `[[A]]`.

## Behaviors

- When reading memory files, follow `[[wiki-links]]` if the linked topic is relevant — don't chase every link mechanically
- Track entity updates in `entities.md`
- Append notable events to `observations.md`
- Add time-sensitive items to `hot-memory.md`
- After notable interactions, append to `system/self-observations.md`

## Artifact Formats

**Observation**: `- YYYY-MM-DD [tags]: <observation>`
**Action item**: `- [ ] task | due:YYYY-MM-DD | pri:high/medium/low | added:YYYY-MM-DD`
**Entity entry**: `### Name (relationship)` / pipe-separated key facts / `status: active|inactive | last: YYYY-MM-DD | -> [[link]]`

## How To Use The Scripts

- `scripts/memory.py memory scan`: scan memory file summaries before doing wide reads
- `scripts/memory.py memory validate`: validate manifest, required files, and L0 coverage before relying on the module

## Failure Conditions

- memory duplicates canonical truth that should have moved into `.loom/`
- the same supporting fact is copied into several memory files without one owner
- the module quietly grows extra domains or extra truth authority
- hot-memory exceeds 50 lines

## Done Means

- the right memory file now holds the supporting fact
- canonical truth still lives in the proper canonical artifact when required
- the module remains within the `system` and `user` boundary

## Read In This Order

1. `references/retrieval.md`
2. `references/files.md`
3. `references/artifact-formats.md`
4. `references/scripts.md`

## References

- `references/retrieval.md`
- `references/files.md`
- `references/artifact-formats.md`
- `references/scripts.md`
