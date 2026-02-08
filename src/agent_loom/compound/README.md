## Compound Cookbook

Compound is Loom's deterministic learning loop for agentic work.

It turns recent activity into durable procedural memory (Skills) backed by committed evidence (Episodes) and replayable governance records (Decisions).

Core loop:

- Plan -> Work -> Review -> Compound -> Repeat

Where things live:

- Skills: `.opencode/skills/<name>/SKILL.md`
- Instincts: `.loom/compound/instincts.json` (index: `.loom/compound/INSTINCTS.md`)
- Observations: `.opencode/memory/observations.jsonl` (gitignored)
- Episodes (evidence): `.loom/compound/episodes/YYYY/MM/<episode_id>.json`
- Decisions (ops log): `.loom/compound/decisions/YYYY/MM/<decision_id>.json`

### Commands

Install or upgrade the compound scaffolding:

```bash
loom compound init
loom compound init --dry-run
loom compound init --force
```

Refresh derived docs and rule files (safe to run often):

```bash
loom compound update
```

Apply learning proposals deterministically (writes an Episode; may update skills/instincts):

```bash
loom compound learn --proposals '{"instinct_candidates":[],"skill_candidates":[]}'
```

Commit compound-owned artifacts (manager/ship step):

```bash
loom compound sync
loom compound sync -m "chore: compound"
```

Print this cookbook:

```bash
loom compound prime
```
