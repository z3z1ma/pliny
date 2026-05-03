# Workspace Tree

A Loom-enabled project normally uses this workspace tree:

```text
.loom/
├── constitution/
│   ├── constitution.md
│   ├── decisions/
│   └── roadmap/
├── initiatives/
├── research/
├── specs/
├── plans/
├── tickets/
├── critique/
├── wiki/
├── packets/
│   ├── ralph/
│   ├── critique/
│   └── wiki/
├── evidence/
├── memory/
│   ├── system/
│   └── user/
└── support/              # optional, lazy-materialized support artifacts
    └── drive-handoffs/   # optional saved drive handoffs
```

The tree is lazily materialized. Git may not preserve empty directories, so a
fresh checkout may omit owner paths or support paths that have no records yet.
Bootstrap should create the standard owner and packet/memory support tree when
needed, and any directory that contains records should use the path assigned to
that record or support kind.

The canonical owner paths are `constitution`, `initiatives`, `research`,
`specs`, `plans`, `tickets`, `critique`, `wiki`, and `evidence`. `packets`,
`memory`, and optional `.loom/support/` paths are support surfaces. They help
execution, recall, reviewability, or handoff audit, but they do not own objective
state, live ticket state, acceptance, evidence sufficiency, critique verdicts,
wiki truth, or canonical truth. Packet records under `.loom/packets/` own only
their own packet lifecycle status; memory files and optional `.loom/support/`
artifacts do not own packet lifecycle surfaces.

Create `.loom/support/` only when a support artifact is intentionally saved, such
as a drive handoff under `.loom/support/drive-handoffs/`. Do not create it merely
to satisfy bootstrap, and do not treat its presence as a new canonical owner
layer.

## Bootstrap Command

```bash
mkdir -p \
  .loom/constitution/decisions \
  .loom/constitution/roadmap \
  .loom/initiatives \
  .loom/research \
  .loom/specs \
  .loom/plans \
  .loom/tickets \
  .loom/critique \
  .loom/wiki \
  .loom/packets/ralph \
  .loom/packets/critique \
  .loom/packets/wiki \
  .loom/evidence \
  .loom/memory/system \
  .loom/memory/user
```

The bootstrap command intentionally omits `.loom/support/`: support artifacts are
optional and should be materialized by the workflow that saves them.

## First Files Worth Creating

- `.loom/constitution/constitution.md`
- `.loom/workspace.md` if repository aliases or multi-worktree scope need to be
  explicit; this is workspace metadata, not canonical project truth
- `.loom/harness.md` if the project wants repeatable fresh-context launch
  profiles; this is harness support metadata, not a canonical owner
- the first initiative / plan / ticket chain required by the work

## Why This Tree Matters

The directory names carry semantic information.

That gives you:

- cheap discovery by path
- cheap cross-reference by `rg`
- clear ownership boundaries
- legible durable state without a runtime
