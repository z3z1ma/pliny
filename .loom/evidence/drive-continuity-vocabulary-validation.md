---
id: evidence:drive-continuity-vocabulary-validation
kind: evidence
status: recorded
created_at: 2026-05-02T17:00:25Z
updated_at: 2026-05-02T17:07:31Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:9c2delu8
  packet:
    - packet:ralph-ticket-9c2delu8-20260502T165707Z
    - packet:ralph-ticket-9c2delu8-20260502T170610Z
external_refs: {}
---

# Summary

Structural validation for `ticket:9c2delu8`, covering the drive continuity
vocabulary simplification in `skills/loom-drive`.

# Procedure

- Ran a targeted pre-edit search for `continuity contract`,
  `Drive Continuity Snapshot`, `checkpoint`, `source snapshot`,
  `tranche contract`, `gap matrix`, `route exit`, `resume instruction`,
  `next route`, and `handoff` across `skills/loom-drive` and the ticket.
- Reworked the drive surfaces around the smaller canonical shape of checkpoint,
  continuity snapshot, and next route.
- Made objective gap and tranche detail guidance explicitly conditional.
- Ran post-edit targeted searches and term counts over the same surfaces.
- Ran `git diff --check` from the repository root after the product/ticket edits
  and before writing this evidence record.
- Manually spot-checked cold resume, blocked critique, next-route selection, and
  child handoff pressure scenarios.
- Repair refresh: aligned the continuity snapshot and reassessment examples from
  the old route wording to `next route` / `next route owner` and changed the
  checkpoint stop-rule prose to use `next route` consistently.
- Repair refresh: reran `git diff --check`, targeted route-vocabulary searches,
  route-vocabulary counts, and the pressure-scenario spot checks.

# Artifacts

## `git diff --check`

Command:

```text
git diff --check
```

Output:

```text
<no output; command exited successfully>
```

## Targeted vocabulary searches

Pre-edit search command:

```text
rg -n "continuity contract|Drive Continuity Snapshot|checkpoint|source snapshot|tranche contract|gap matrix|route exit|resume instruction|next route|handoff" "skills/loom-drive" ".loom/tickets/20260502-9c2delu8-simplify-drive-continuity-vocabulary.md"
```

Observed pre-edit result:

- The product drive surface used `Continuity Contract`, `Drive Continuity
  Snapshot`, `tranche contract`, `gap matrix`, and `route exit` as active
  workflow terms in addition to `checkpoint`, `next route`, `source snapshot`,
  `resume instruction`, and `handoff`.
- The densest overlap appeared in `skills/loom-drive/SKILL.md`,
  `references/continuity-contract.md`,
  `references/checkpoint-resume-protocol.md`,
  `references/tranche-decision-protocol.md`, and
  `templates/outer-loop-handoff.md`.

Post-edit count command:

```text
python3 - <<'PY'
from pathlib import Path
terms = ['continuity contract','Drive Continuity Snapshot','checkpoint','source snapshot','tranche contract','gap matrix','route exit','resume instruction','next route','handoff']
paths = [p for p in Path('skills/loom-drive').rglob('*.md')] + [Path('.loom/tickets/20260502-9c2delu8-simplify-drive-continuity-vocabulary.md')]
for term in terms:
    count = 0
    locs = []
    needle = term.lower()
    for path in paths:
        text = path.read_text().lower()
        c = text.count(needle)
        if c:
            count += c
            locs.append(f'{path}:{c}')
    print(f'{term}: {count}' + (f' ({", ".join(locs)})' if locs else ''))
PY
```

Post-edit counts:

```text
continuity contract: 0
Drive Continuity Snapshot: 0
checkpoint: 29
source snapshot: 5
tranche contract: 1 (.loom/tickets/20260502-9c2delu8-simplify-drive-continuity-vocabulary.md:1)
gap matrix: 1 (.loom/tickets/20260502-9c2delu8-simplify-drive-continuity-vocabulary.md:1)
route exit: 1 (.loom/tickets/20260502-9c2delu8-simplify-drive-continuity-vocabulary.md:1)
resume instruction: 3
next route: 21
handoff: 37
```

Interpretation:

- `continuity contract` and `Drive Continuity Snapshot` no longer appear as
  product-surface terms.
- `tranche contract`, `gap matrix`, and `route exit` remain only in the ticket's
  historical council-finding context, not as active drive guidance.
- `checkpoint`, `continuity snapshot`, and `next route` are now the active drive
  continuity vocabulary.
- `source snapshot` and `handoff` remain where support artifacts or bounded child
  contracts need them; the edited guidance keeps those as support/packet facts,
  not drive-owned truth.

## Oracle repair refresh: route vocabulary

Repair search command:

```text
rg -n "next action|next action owner|next route|next route owner|continuity snapshot" "skills/loom-drive" ".loom/tickets/20260502-9c2delu8-simplify-drive-continuity-vocabulary.md"
```

Observed repair search result:

```text
.loom/tickets/20260502-9c2delu8-simplify-drive-continuity-vocabulary.md:97:has been repaired structurally. Oracle re-check is the next route before
.loom/tickets/20260502-9c2delu8-simplify-drive-continuity-vocabulary.md:180:- 2026-05-02T17:07:31Z: Repair iteration aligned continuity snapshot and
.loom/tickets/20260502-9c2delu8-simplify-drive-continuity-vocabulary.md:181:  checkpoint/resume wording on `next route` / `next route owner`, refreshed
skills/loom-drive/templates/outer-loop-handoff.md:31:context while shaping an objective, tranche, or next route. It collects a
skills/loom-drive/templates/outer-loop-handoff.md:59:- Propose owner-record updates, ticket slices, risks, and next routes.
skills/loom-drive/templates/outer-loop-handoff.md:99:- proposed next route: continue / ask-user / critique / wiki / research / spec /
skills/loom-drive/SKILL.md:63:- tickets own live execution state, next route, blockers, scoped coverage,
skills/loom-drive/SKILL.md:74:Use `references/continuity-contract.md` for the continuity snapshot convention:
skills/loom-drive/SKILL.md:75:objective status, current tranche, and next route are pinned to existing
skills/loom-drive/SKILL.md:210:- the subagent proposes owner-record changes, tickets, risks, and next routes
skills/loom-drive/references/checkpoint-resume-protocol.md:19:critique, and next route.
skills/loom-drive/references/checkpoint-resume-protocol.md:35:next route: <ask_user | research | spec | plan | ticket | Ralph | evidence | critique | wiki | retrospective | acceptance | stop>
skills/loom-drive/references/checkpoint-resume-protocol.md:36:next route owner: <which owner skill/layer changes next>
skills/loom-drive/references/checkpoint-resume-protocol.md:55:rg -n 'continuity snapshot|drive anchor:|next route:|resume instruction:' .loom/initiatives .loom/plans .loom/tickets
skills/loom-drive/references/checkpoint-resume-protocol.md:61:   next route.
skills/loom-drive/references/checkpoint-resume-protocol.md:90:- Critique gate: mandatory critique is complete, pending as next route, blocking,
skills/loom-drive/references/checkpoint-resume-protocol.md:128:route recoverable, stop driving. The correct next route is to repair the owner
skills/loom-drive/references/tranche-decision-protocol.md:6:only need a clear checkpoint and next route. Use this fuller protocol when
skills/loom-drive/references/tranche-decision-protocol.md:55:Choose the next route in this order. The first true condition wins unless the
skills/loom-drive/references/tranche-decision-protocol.md:90:Every route result must name the owner records that changed and the next route or
skills/loom-drive/references/continuity-contract.md:20:| live state, blockers, next route, scoped coverage | ticket |
skills/loom-drive/references/continuity-contract.md:52:Use a continuity snapshot as a prose convention inside existing owner records. It
skills/loom-drive/references/continuity-contract.md:76:next route: continue | ask_user | critique | wiki | research | spec | plan | ticket | stop
skills/loom-drive/references/continuity-contract.md:77:next route owner: <which layer must change next>
skills/loom-drive/references/continuity-contract.md:111:next route: continue | ask_user | critique | wiki | research | spec | plan | ticket | stop
skills/loom-drive/references/continuity-contract.md:113:reason: <why this next route follows from the records>
skills/loom-drive/references/continuity-contract.md:121:If the next route is `continue`, the plan or ticket chain should name the next
skills/loom-drive/references/continuity-contract.md:122:tranche. If the next route is `ask_user`, record the exact question and why the
skills/loom-drive/references/continuity-contract.md:147:- a fresh session would lose the reason for the next route
skills/loom-drive/references/drive-loop.md:38:- `continuation`: create the next tranche or choose the next route.
```

Repair count command:

```text
python3 - <<'PY'
from pathlib import Path
terms = ['next action','next action owner','next route','next route owner','continuity snapshot']
paths = [p for p in Path('skills/loom-drive').rglob('*.md')] + [Path('.loom/tickets/20260502-9c2delu8-simplify-drive-continuity-vocabulary.md')]
for term in terms:
    needle = term.lower()
    locs = []
    total = 0
    for path in paths:
        count = path.read_text().lower().count(needle)
        if count:
            total += count
            locs.append(f'{path}:{count}')
    print(f'{term}: {total}' + (f' ({", ".join(locs)})' if locs else ''))
PY
```

Repair counts:

```text
next action: 0
next action owner: 0
next route: 31 (skills/loom-drive/SKILL.md:3, skills/loom-drive/references/continuity-contract.md:9, skills/loom-drive/references/drive-loop.md:1, skills/loom-drive/references/tranche-decision-protocol.md:4, skills/loom-drive/references/checkpoint-resume-protocol.md:7, skills/loom-drive/templates/outer-loop-handoff.md:3, .loom/tickets/20260502-9c2delu8-simplify-drive-continuity-vocabulary.md:4)
next route owner: 3 (skills/loom-drive/references/continuity-contract.md:1, skills/loom-drive/references/checkpoint-resume-protocol.md:1, .loom/tickets/20260502-9c2delu8-simplify-drive-continuity-vocabulary.md:1)
continuity snapshot: 6 (skills/loom-drive/SKILL.md:1, skills/loom-drive/references/continuity-contract.md:2, skills/loom-drive/references/checkpoint-resume-protocol.md:1, skills/loom-drive/templates/outer-loop-handoff.md:1, .loom/tickets/20260502-9c2delu8-simplify-drive-continuity-vocabulary.md:1)
```

Repair interpretation:

- `next action` and `next action owner` no longer appear in the inspected active
  drive product surface or ticket state.
- `continuity-contract.md` now uses the same `next route` / `next route owner`
  fields as `checkpoint-resume-protocol.md`.
- Deterministic resume discovery already searched `next route:`; no broader
  deterministic search expansion was needed after removing the alias.

# Pressure-Scenario Spot Checks

## Cold resume

Result: pass.

- `references/checkpoint-resume-protocol.md` still requires checkpoint fields in
  owner records before stopping, compacting, or launching child work.
- Deterministic resume discovery still searches active tickets and owner-record
  checkpoint phrases.
- The stop rule remains fail-closed when a checkpoint cannot be found or updated.

## Blocked critique

Result: pass.

- The critique gate still requires mandatory critique to be complete, pending as
  next route, blocking, or not required with ticket-owned rationale.
- Unresolved medium/high findings still block acceptance and dependent
  implementation that relies on challenged claims.
- The drive skill still refuses to own critique verdicts or ticket acceptance.

## Next-route selection

Result: pass.

- `references/tranche-decision-protocol.md` still keeps route decision priority
  explicit.
- Objective gap summaries and fuller tranche detail are now conditional on unclear
  gaps, review state, sequencing, dependency order, or write-scope conflicts.
- A single bounded ready ticket may proceed without manufactured matrix/tranche
  paperwork.

## Child handoff

Result: pass.

- Before child work, the drive references still require bounded source/read scope,
  explicit write scope, stop conditions, output contract, and parent reconciliation
  targets.
- The outer-loop handoff template still says saved handoffs are support artifacts,
  not packets or truth owners.
- The checkpoint remains current-before-launch; `can update later` remains
  explicitly disallowed in `skills/loom-drive/SKILL.md`.

## Repair pressure-scenario re-check

Result: pass.

- Cold resume still has one searchable route field: `next route:` in the
  checkpoint protocol and continuity snapshot examples.
- Deterministic resume still searches `continuity snapshot`, `drive anchor:`,
  `next route:`, and `resume instruction:` rather than depending on transcript
  context or the removed alias.
- Blocked critique remains fail-closed because mandatory critique can be pending
  as the next route or blocking, and unresolved medium/high findings still block
  acceptance and dependent implementation.
- Child handoff remains bounded by source/read scope, explicit write scope, stop
  conditions, output contract, and parent reconciliation targets.

# Owner-Layer Boundary Review

- Tickets still own live execution state, next route, blockers, evidence
  disposition, critique disposition, and acceptance decisions.
- Packets and saved handoffs still own bounded child/support context only.
- Evidence, critique, and wiki keep their existing owner roles.
- No new drive record kind, ledger, status family, or hidden runtime was added.

# Supports Claims

- `ticket:9c2delu8#ACC-001`
- `ticket:9c2delu8#ACC-002`
- `ticket:9c2delu8#ACC-003`
- `ticket:9c2delu8#ACC-004`
- `ticket:9c2delu8#ACC-005`
- `initiative:skills-corpus-perfection-council-followup#OBJ-006`

# Challenges Claims

- `ticket:9c2delu8#ACC-006` remains pending because mandatory oracle re-check has
  not yet run after the repair.

# Environment

Commit: `e3fa3b42946a4ccbe519563c6054dfeadff3dd94` plus uncommitted working tree changes for `ticket:9c2delu8`
Branch: `main`
Runtime: Markdown/file validation with git and targeted text search
OS: macOS / Darwin
Relevant config: no build/test runtime for this repository

# Validity

Valid for: the edited `skills/loom-drive` continuity/checkpoint/tranche guidance,
the oracle finding repair, and `ticket:9c2delu8` state in the current working
tree.

Recheck when: drive checkpoint/resume safety, route decision priority, outer-loop
handoff support grammar, ticket critique disposition, or owner-layer boundaries
change.

# Limitations

- This is structural evidence, not mandatory oracle critique.
- Searches establish target term placement in the inspected surfaces; they do not
  prove every future operator will follow the guidance.
- No automated Markdown schema validator or rendered-document check exists in
  this repository.

# Result

The structural checks support returning `ticket:9c2delu8` to `review_required`
for mandatory oracle re-check. The repair removes the `next action` / `next route`
split by using `next route` / `next route owner` consistently in the continuity
snapshot, reassessment, and checkpoint/resume surfaces while preserving
fail-closed checkpoint/resume safety and owner-layer boundaries.

# Related Records

- `ticket:9c2delu8`
- `packet:ralph-ticket-9c2delu8-20260502T165707Z`
- `packet:ralph-ticket-9c2delu8-20260502T170610Z`
