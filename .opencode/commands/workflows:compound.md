---
description: Compound -> package evidence Episodes and compile instincts/skills deterministically.
agent: build
subtask: false
---

You are running the **Compound** phase.

Ticket (if applicable):
$ARGUMENTS

This is where we convert "we learned a thing" into durable, replayable memory.

Goals:
- Package evidence into an **Episode** under `.loom/compound/episodes/...`.
- Compile/update instincts in `.opencode/memory/instincts.json`.
- Compile/update skills under `.opencode/skills/` (optional mirror to `.claude/skills/`).
- (Optional) Store 1-3 Loom Memory notes for beautiful human-readable compaction.

Process:
1) Ensure compound scaffolding exists:
   - Run via bash: `loom compound init --dest .`
2) Gather context:
   - Run via bash: `git status --porcelain` and `git diff --stat`
   - If a ticket ID was provided, `loom ticket show $ARGUMENTS`
3) Propose durable learnings as a JSON object with:
   - `instinct_candidates`: list of `{id,title,trigger,action,confidence,tags}`
   - `skill_candidates`: list of `{name,description,body,tags,source_instinct_ids}`
4) Apply deterministically (this writes the Episode and compiles outputs):
   - Run via bash: `loom compound run --proposals '<json>'`
5) Optional compaction memo:
   - Run via bash: `loom memory add --title ... --body ... --tag compound --scope repo:.`

Required output:
- A short "Compound report" section (what we learned).
- A short list of changes applied (episode/instincts/skills/memos).
