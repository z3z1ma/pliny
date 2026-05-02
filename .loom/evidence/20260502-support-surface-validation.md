---
id: evidence:support-surface-validation
kind: evidence
status: recorded
created_at: 2026-05-02T19:20:06Z
updated_at: 2026-05-02T19:32:39Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:skills-corpus-council-precision-pass
  plan:
    - plan:skills-corpus-council-precision-pass
  ticket:
    - ticket:supp0x2a
  packet:
    - packet:ralph-ticket-supp0x2a-20260502T191626Z
    - packet:ralph-ticket-supp0x2a-20260502T192522Z
  critique:
    - critique:support-surface-review
external_refs: {}
---

# Summary

Observed and validated the optional `.loom/support/` support-surface alignment and
repair for `ticket:supp0x2a`. The changed product surfaces now describe
`.loom/support/` as optional, lazy-materialized, discoverable, and non-canonical,
with explicit non-ownership boundaries for support artifacts. Iteration 2 added
bootstrap, `PROTOCOL.md`, and `ARCHITECTURE.md` repair evidence.

# Procedure

1. Captured before-state searches for `.loom/support`, `drive-handoffs`,
   `support-artifact`, and support non-ownership language across README, workspace,
   drive, records, and the ticket.
2. Updated workspace tree/status, drive handoff guidance, records/frontmatter,
   records naming/status guidance, and README runtime framing.
3. Captured after-state searches over the same surfaces.
4. Captured repair pre-state searches for bootstrap, `PROTOCOL.md`,
   `ARCHITECTURE.md`, README, workspace, drive, records, ticket, and first packet
   surfaces.
5. Verified the first Ralph packet lifecycle was already parent-reconciled to
   `consumed` with repair notes.
6. Aligned bootstrap, `PROTOCOL.md`, and `ARCHITECTURE.md` with optional,
   lazy-materialized, non-canonical `.loom/support/` framing.
7. Captured repair after-state searches over the expanded surface set.
8. Ran `git diff --check`.

# Artifacts

## Before observation

Command:

```bash
rg -n '\.loom/support|drive-handoffs|support-artifact|support.*(objective state|live ticket state|acceptance|evidence sufficiency|critique verdicts|wiki truth|canonical truth|packet lifecycle|non-canonical)' README.md skills/loom-workspace skills/loom-drive skills/loom-records .loom/tickets/20260502-supp0x2a-canonicalize-support-surface.md
```

Result summary:

- `skills/loom-drive/SKILL.md:219` and
  `skills/loom-drive/templates/outer-loop-handoff.md:38` taught saved handoffs at
  `.loom/support/drive-handoffs/`.
- `skills/loom-records/references/frontmatter.md:101` and
  `skills/loom-records/references/naming-and-ids.md:63,89` mentioned support
  artifacts and `.loom/support/` paths.
- `skills/loom-records/references/naming-and-ids.md:76` already stated support
  artifacts must not own objective state, live ticket state, acceptance, evidence
  sufficiency, critique verdicts, wiki truth, canonical truth, or packet
  lifecycle.
- No before-state matches appeared in `skills/loom-workspace/references/workspace-tree.md`,
  `skills/loom-workspace/references/status-snapshot.md`, or the README runtime
  tree for `.loom/support/`.

## After observation

Command:

```bash
rg -n '\.loom/support|drive-handoffs|support-artifact|support.*(objective state|live ticket state|acceptance|evidence sufficiency|critique verdicts|wiki truth|canonical truth|packet lifecycle|non-canonical)|lazy-materialized' README.md skills/loom-workspace skills/loom-drive skills/loom-records .loom/tickets/20260502-supp0x2a-canonicalize-support-surface.md
```

Selected output:

```text
README.md:222:| `support` | Optional, lazy-materialized saved support artifacts such as drive handoffs; not canonical truth |
README.md:563:└── support/       # optional saved support artifacts; non-canonical
README.md:564:    └── drive-handoffs/
skills/loom-workspace/references/workspace-tree.md:26:└── support/              # optional, lazy-materialized support artifacts
skills/loom-workspace/references/workspace-tree.md:27:    └── drive-handoffs/   # optional saved drive handoffs
skills/loom-workspace/references/workspace-tree.md:38:`memory`, and optional `.loom/support/` paths are support surfaces. They help
skills/loom-workspace/references/workspace-tree.md:43:Create `.loom/support/` only when a support artifact is intentionally saved, such
skills/loom-workspace/references/workspace-tree.md:69:The bootstrap command intentionally omits `.loom/support/`: support artifacts are
skills/loom-workspace/references/status-snapshot.md:13:- optional `.loom/support/` artifacts linked or cited by owner records
skills/loom-workspace/references/status-snapshot.md:47:   next route. Saved `.loom/support/` artifacts are optional support context, not
skills/loom-workspace/references/status-snapshot.md:113:- `.loom/support/` artifacts are carrying objective state, live ticket state,
skills/loom-workspace/references/status-snapshot.md:128:find .loom/support -type f -name '*.md' 2>/dev/null | sort
skills/loom-drive/SKILL.md:218:- saved outer-loop handoffs live under the optional, lazy-materialized,
skills/loom-drive/SKILL.md:220:  `.loom/support/drive-handoffs/<UTC compact timestamp>-<slug>.md` with
skills/loom-drive/SKILL.md:230:- do not create `.loom/support/` merely during bootstrap; create it only when a
skills/loom-drive/templates/outer-loop-handoff.md:37:If saved, place it under the optional, lazy-materialized, non-canonical support
skills/loom-drive/templates/outer-loop-handoff.md:39:`.loom/support/drive-handoffs/<UTC compact timestamp>-<slug>.md` and keep the
skills/loom-records/references/frontmatter.md:74:`.loom/support/` is an optional, lazy-materialized support surface for saved
skills/loom-records/references/frontmatter.md:76:artifact; its presence never makes the support artifact canonical truth.
skills/loom-records/references/naming-and-ids.md:80:`.loom/support/` is optional and lazy-materialized. Use it only for intentionally
skills/loom-records/references/status-lifecycle.md:76:Support artifacts saved under optional `.loom/support/` paths are
skills/loom-records/references/status-lifecycle.md:77:lazy-materialized support files. Their statuses are local to the artifact and do
skills/loom-records/references/status-lifecycle.md:78:not make `.loom/support/` a canonical owner layer or packet lifecycle surface.
```

Non-ownership wording is present in:

- `skills/loom-workspace/references/workspace-tree.md:38-41`
- `skills/loom-workspace/references/status-snapshot.md:113-115`
- `skills/loom-drive/SKILL.md:222-225`
- `skills/loom-drive/templates/outer-loop-handoff.md:41-46`
- `skills/loom-records/references/frontmatter.md:68-76`
- `skills/loom-records/references/naming-and-ids.md:72-81`
- `skills/loom-records/references/status-lifecycle.md:71-78`

## Repair pre-observation

Command:

```bash
rg -n '\.loom/support|drive-handoffs|support-artifact|support.*(objective state|live ticket state|acceptance|evidence sufficiency|critique verdicts|wiki truth|canonical truth|packet lifecycle|non-canonical)|lazy-materialized|support surfaces|support surface' README.md PROTOCOL.md ARCHITECTURE.md skills/loom-bootstrap/references/02-truth-and-authority.md skills/loom-workspace skills/loom-drive skills/loom-records .loom/tickets/20260502-supp0x2a-canonicalize-support-surface.md .loom/packets/ralph/20260502T191626Z-ticket-supp0x2a-iter-01.md
```

Result summary:

- README, workspace, drive, and records surfaces already mentioned optional
  `.loom/support/` support artifacts from the first iteration.
- `PROTOCOL.md:121,184-191` and `ARCHITECTURE.md:43-48` mentioned generic support
  surfaces but did not explicitly name optional `.loom/support/` artifacts.
- `skills/loom-bootstrap/references/02-truth-and-authority.md:115` mentioned
  generic support surfaces but did not explicitly name `.loom/support/`.

## Packet lifecycle observation

Command:

```bash
rg -n '^status:|^updated_at:|^# Parent Merge Notes|Parent received child output|ORACLE-SUPP0X2A-001|Repair packet|packet:ralph-ticket-supp0x2a-20260502T192522Z' .loom/packets/ralph/20260502T191626Z-ticket-supp0x2a-iter-01.md
```

Selected output:

```text
5:status: consumed
13:updated_at: 2026-05-02T19:25:22Z
235:# Parent Merge Notes
237:Parent received child output and accepted the initial support-surface alignment as
238:useful but incomplete after oracle critique. `ORACLE-SUPP0X2A-001` identified this
239:packet lifecycle as stale, so parent marked this packet `consumed`. Repair packet
240:`packet:ralph-ticket-supp0x2a-20260502T192522Z` owns the follow-up iteration for
```

Interpretation: `packet:ralph-ticket-supp0x2a-20260502T191626Z` is already in a
terminal packet lifecycle state for this workflow, and its parent merge notes name
the critique finding and repair packet. No further edit was needed to preserve
that truth.

## Repair after observation

Command:

```bash
rg -n '\.loom/support|drive-handoffs|support-artifact|support.*(objective state|live ticket state|acceptance|evidence sufficiency|critique verdicts|wiki truth|canonical truth|packet lifecycle|non-canonical)|lazy-materialized|support surfaces|support surface' README.md PROTOCOL.md ARCHITECTURE.md skills/loom-bootstrap/references/02-truth-and-authority.md skills/loom-workspace skills/loom-drive skills/loom-records .loom/tickets/20260502-supp0x2a-canonicalize-support-surface.md .loom/packets/ralph/20260502T191626Z-ticket-supp0x2a-iter-01.md
```

Selected output:

```text
README.md:222:| `support` | Optional, lazy-materialized saved support artifacts such as drive handoffs; not canonical truth |
README.md:563:└── support/       # optional saved support artifacts; non-canonical
PROTOCOL.md:121:| support surface | packet, memory, optional `.loom/support/` artifacts, workspace/harness records | recovery, recall, retrieval cues, bounded handoff, or scope support without owning project truth |
PROTOCOL.md:194:Saved support artifacts may live under optional, lazy-materialized
PROTOCOL.md:195:`.loom/support/` paths such as `.loom/support/drive-handoffs/`. They support
ARCHITECTURE.md:48:- optional, lazy-materialized `.loom/support/` artifacts, such as saved drive
ARCHITECTURE.md:49:  handoffs, support recovery or handoff without owning objective state, live
skills/loom-bootstrap/references/02-truth-and-authority.md:114:Optional saved support artifacts may live under a lazy-materialized support tree:
skills/loom-bootstrap/references/02-truth-and-authority.md:116:- `.loom/support/`
skills/loom-bootstrap/references/02-truth-and-authority.md:118:Create `.loom/support/` only when a support artifact is intentionally saved,
skills/loom-bootstrap/references/02-truth-and-authority.md:119:such as a drive handoff under `.loom/support/drive-handoffs/`. Its presence does
skills/loom-drive/SKILL.md:218:- saved outer-loop handoffs live under the optional, lazy-materialized,
skills/loom-drive/templates/outer-loop-handoff.md:37:If saved, place it under the optional, lazy-materialized, non-canonical support
skills/loom-records/references/frontmatter.md:74:`.loom/support/` is an optional, lazy-materialized support surface for saved
skills/loom-records/references/naming-and-ids.md:80:`.loom/support/` is optional and lazy-materialized. Use it only for intentionally
skills/loom-workspace/references/workspace-tree.md:26:└── support/              # optional, lazy-materialized support artifacts
skills/loom-workspace/references/status-snapshot.md:13:- optional `.loom/support/` artifacts linked or cited by owner records
```

Additional non-ownership check:

```bash
rg -n 'objective state|live ticket state|evidence sufficiency|critique verdicts|packet lifecycle|canonical truth|wiki truth' README.md PROTOCOL.md ARCHITECTURE.md skills/loom-bootstrap/references/02-truth-and-authority.md skills/loom-workspace skills/loom-drive skills/loom-records
```

Selected output:

```text
skills/loom-bootstrap/references/02-truth-and-authority.md:130:they do not own objective state, live ticket state, acceptance, evidence
skills/loom-bootstrap/references/02-truth-and-authority.md:131:sufficiency, critique verdicts, wiki truth, canonical truth, or packet lifecycle.
PROTOCOL.md:196:handoff and recovery; they do not own objective state, live ticket state,
PROTOCOL.md:197:acceptance, evidence sufficiency, critique verdicts, wiki truth, canonical truth,
PROTOCOL.md:198:or packet lifecycle.
ARCHITECTURE.md:49:  handoffs, support recovery or handoff without owning objective state, live
ARCHITECTURE.md:50:  ticket state, acceptance, evidence sufficiency, critique verdicts, wiki truth,
ARCHITECTURE.md:51:  canonical truth, or packet lifecycle
skills/loom-workspace/references/workspace-tree.md:40:state, live ticket state, acceptance, evidence sufficiency, critique verdicts,
skills/loom-drive/SKILL.md:224:  `superseded`; it does not own objective state, live ticket state, acceptance,
skills/loom-records/references/frontmatter.md:70:canonical owner layer and must not own objective state, live ticket state,
```

## Whitespace validation

Command:

```bash
git diff --check
```

Result: passed with no output.

# Supports Claims

- `initiative:skills-corpus-council-precision-pass#OBJ-002`
- `ticket:supp0x2a#ACC-001`
- `ticket:supp0x2a#ACC-002`
- `ticket:supp0x2a#ACC-003`
- `ticket:supp0x2a#ACC-004`

# Challenges Claims

None.

# Environment

Commit: `63f68637ae4ff7ae2e13c901a235ad362791fbcc`

Branch: `main`

Runtime: Markdown-only corpus validation with `rg`, file inspection, and `git diff --check`

OS: macOS / Darwin

Relevant config: no runtime/helper dependency added

# Validity

Valid for: the working tree diff for `ticket:supp0x2a` after this Ralph iteration.

Recheck when: support-surface guidance, bootstrap truth/support doctrine,
`PROTOCOL.md`, `ARCHITECTURE.md`, workspace tree/status, drive handoff guidance,
records/frontmatter/status references, or README runtime tree changes.

# Limitations

This evidence does not satisfy `ticket:supp0x2a#ACC-005`; mandatory oracle
critique is still required before closure. The validation is structural and
observational, not an automated behavior test suite.

# Result

The targeted surfaces, including bootstrap, `PROTOCOL.md`, and `ARCHITECTURE.md`,
now agree that `.loom/support/` is optional, lazy-materialized, discoverable for
saved support artifacts, and non-canonical. The first packet lifecycle is already
reconciled to `consumed`. The diff has no whitespace errors according to
`git diff --check`.

# Interpretation

This evidence supports returning `ticket:supp0x2a` to `review_required` for the
mandatory oracle re-check. It does not by itself close the ticket, resolve the
critique record, or accept the support-surface wording.

# Related Records

- `ticket:supp0x2a`
- `packet:ralph-ticket-supp0x2a-20260502T191626Z`
- `packet:ralph-ticket-supp0x2a-20260502T192522Z`
- `initiative:skills-corpus-council-precision-pass`
- `plan:skills-corpus-council-precision-pass`
- `critique:support-surface-review`
