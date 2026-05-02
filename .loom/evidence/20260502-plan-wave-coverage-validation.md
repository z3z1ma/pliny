---
id: evidence:plan-wave-coverage-validation
kind: evidence
status: recorded
created_at: 2026-05-02T21:04:27Z
updated_at: 2026-05-02T21:21:53Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:planwv11
  packet:
    - packet:ralph-ticket-planwv11-20260502T210325Z
    - packet:ralph-ticket-planwv11-20260502T211053Z
    - packet:ralph-ticket-planwv11-20260502T212006Z
external_refs: {}
---

# Summary

Observation-first validation for `ticket:planwv11`, checking plan guidance before
and after updates for claim coverage, execution-wave independence, write scope
overlap cues, `child_write_scope`, `parallel`, `None - reason`, and whitespace
validity via `git diff --check`. Refreshed for repair iteration
`packet:ralph-ticket-planwv11-20260502T211053Z` with observations for all four
`critique:plan-wave-coverage-review` findings, then refreshed for repair
iteration `packet:ralph-ticket-planwv11-20260502T212006Z` with record-grammar
observations for both `critique:plan-wave-coverage-rereview` findings.

# Procedure

Baseline observed at 2026-05-02T21:04:27Z from commit
`cb69ab9efdefbe4dabb9c86f34048687a0c8930e` on branch `main`.

Before edit command:

```bash
rg -n "Execution Waves|claim coverage|write scope|child_write_scope|parallel|None - reason" "skills/loom-plans"; git diff --check
```

After edit commands:

```bash
rg -n "Execution Waves|claim coverage|write scope|child_write_scope|parallel|None - reason" "skills/loom-plans"
git diff --check
```

Repair observation commands:

```bash
rg -n "^status: review_required|Route: critique|Disposition status: pending|repair applied pending re-critique" ".loom/tickets/20260502-planwv11-improve-plan-coverage-wave-checks.md"
rg -n "non-overlap summary|No wave|None - reason|child_write_scope" "skills/loom-plans/templates/plan.md"
rg -n "record a compact wave check|ticket journal|packet working notes|scratch notes" "skills/loom-plans/references/plan-shape.md"
rg -n 'initially left packet lifecycle status as `compiled`|parent later marked|status: consumed' ".loom/packets/ralph/20260502T210325Z-ticket-planwv11-iter-01.md"
git diff --check
```

Record-grammar repair observation commands:

```bash
python3 - <<'PY'
from pathlib import Path
p=Path('.loom/tickets/20260502-planwv11-improve-plan-coverage-wave-checks.md')
allowed={'open','supported','supported_pending_review','challenged','accepted_risk','superseded'}
in_matrix=False
bad=[]
vals=[]
for lineno,line in enumerate(p.read_text().splitlines(),1):
    if line.strip()=='# Claim Matrix':
        in_matrix=True
        continue
    if in_matrix and line.startswith('# '):
        break
    if in_matrix and line.startswith('| `'):
        cells=[c.strip() for c in line.strip().strip('|').split('|')]
        status=cells[-1]
        vals.append((lineno,status))
        if status not in allowed:
            bad.append((lineno,status))
print('status_cells=' + ', '.join(f'{lineno}:{status}' for lineno,status in vals))
print('noncanonical=' + ('none' if not bad else ', '.join(f'{lineno}:{status}' for lineno,status in bad)))
PY
rg -n "^status: review_required|Route: critique|Disposition status: pending|supported_pending_review|\| open \||repair applied pending re-critique" ".loom/tickets/20260502-planwv11-improve-plan-coverage-wave-checks.md"
rg -n 'initially left packet lifecycle status as `compiled`|parent later marked|status: consumed' ".loom/packets/ralph/20260502T211053Z-ticket-planwv11-iter-02.md"
git diff --check
```

# Artifacts

## Before observations

```text
skills/loom-plans/templates/plan.md:40:# Execution Waves
skills/loom-plans/templates/plan.md:47:scope. If no wave applies, write `None - reason`.
skills/loom-plans/templates/plan.md:52:write `None - reason`.
skills/loom-plans/templates/plan.md:70:Likely write scopes:
skills/loom-plans/references/plan-shape.md:11:- Execution Waves
skills/loom-plans/references/plan-shape.md:36:- likely write scopes: expected record or source boundaries are narrow enough to
skills/loom-plans/references/plan-shape.md:58:## Execution Waves
skills/loom-plans/references/plan-shape.md:60:Use `# Execution Waves` when a plan contains tickets that may be run in
skills/loom-plans/references/plan-shape.md:61:parallel or must be staged.
skills/loom-plans/references/plan-shape.md:63:Group possible parallel work by independent problem domain before launching
skills/loom-plans/references/plan-shape.md:70:- expected packet `child_write_scope` values do not overlap
skills/loom-plans/references/plan-shape.md:77:After a parallel wave returns, integration validation belongs in the parent route
```

Baseline `git diff --check` produced no output and exited successfully.

## After observations

```text
skills/loom-plans/templates/plan.md:43:criteria into downstream tickets. The plan routes claim coverage; tickets own live
skills/loom-plans/templates/plan.md:48:| `<record>#<claim-or-ACC>` | `ticket:<token>` | What the ticket must cover | Expected evidence or critique | `None - reason` only when no claim-bearing source applies |
skills/loom-plans/templates/plan.md:50:# Execution Waves
skills/loom-plans/templates/plan.md:54:Do not require parallel execution by default. Before any sibling Ralph work runs
skills/loom-plans/templates/plan.md:55:in parallel, record the independence and write scope overlap check here or write
skills/loom-plans/templates/plan.md:56:`None - reason` when no parallel wave applies.
skills/loom-plans/templates/plan.md:61:`child_write_scope` or likely write scope, dependency/contention checks, and the
skills/loom-plans/templates/plan.md:62:parent reconciliation route. If no wave applies, write `None - reason`.
skills/loom-plans/templates/plan.md:66:List real ticket IDs, dependencies on prior wave results, any changed write scope
skills/loom-plans/templates/plan.md:68:`None - reason`.
skills/loom-plans/templates/plan.md:72:| Wave | Tickets | Independent because | Expected `child_write_scope` / write scope overlap check | Dependency / shared-state check | Parent reconciliation |
skills/loom-plans/templates/plan.md:74:| `Wave 1` | `ticket:<token>` | No same-wave dependency | `None - reason` or non-overlap summary | No generated file, lockfile, migration, or stateful contention | Ticket-owned update plus evidence/critique route |
skills/loom-plans/templates/plan.md:94:Likely write scopes:
skills/loom-plans/templates/plan.md:98:Expected packet `child_write_scope` / write scope overlap check:
skills/loom-plans/references/plan-shape.md:12:- Execution Waves
skills/loom-plans/references/plan-shape.md:33:- claim coverage: each initiative objective, spec claim, or ticket-local
skills/loom-plans/references/plan-shape.md:35:  downstream ticket, or marked `None - reason` when no claim-bearing source
skills/loom-plans/references/plan-shape.md:43:- likely write scopes: expected record or source boundaries are narrow enough to
skills/loom-plans/references/plan-shape.md:44:  compare against packet `child_write_scope` values and check for overlap
skills/loom-plans/references/plan-shape.md:45:- execution-wave independence: any proposed parallel wave has no same-wave
skills/loom-plans/references/plan-shape.md:46:  dependency conflict, no write scope overlap, and no shared generated file,
skills/loom-plans/references/plan-shape.md:48:  `None - reason` and run sequentially or loop back to planning
skills/loom-plans/references/plan-shape.md:61:Use claim coverage mapping when a plan translates initiative outcomes, research
skills/loom-plans/references/plan-shape.md:70:- any explicit gap, written as `None - reason`, rather than leaving coverage
skills/loom-plans/references/plan-shape.md:88:## Execution Waves
skills/loom-plans/references/plan-shape.md:90:Use `# Execution Waves` when a plan contains tickets that may be run in
skills/loom-plans/references/plan-shape.md:91:parallel or must be staged. Plans may identify a possible wave, but they do not
skills/loom-plans/references/plan-shape.md:92:make parallel execution the default.
skills/loom-plans/references/plan-shape.md:94:Group possible parallel work by independent problem domain before launching
skills/loom-plans/references/plan-shape.md:101:- expected packet `child_write_scope` values do not overlap
skills/loom-plans/references/plan-shape.md:107:If no parallel or staged wave applies, write `None - reason` rather than leaving
skills/loom-plans/references/plan-shape.md:113:| Wave | Tickets | Independence basis | `child_write_scope` / write scope overlap check | Shared-state check | Parent reconciliation |
skills/loom-plans/references/plan-shape.md:116:For Git-backed parallel Ralph, cross-check
skills/loom-plans/references/plan-shape.md:118:`skills/loom-git/references/parallel-ralph-with-git.md`. Ralph packet
skills/loom-plans/references/plan-shape.md:125:After a parallel wave returns, integration validation belongs in the parent route
```

Post-edit `git diff --check` produced no output and exited successfully.

## Repair observations

Ticket route/disposition grammar check:

```text
.loom/tickets/20260502-planwv11-improve-plan-coverage-wave-checks.md:4:status: review_required
.loom/tickets/20260502-planwv11-improve-plan-coverage-wave-checks.md:78:| `initiative:skills-corpus-council-precision-pass#OBJ-011` | `evidence:plan-wave-coverage-validation` records before/after structural searches and repair observations | `critique:plan-wave-coverage-review` | repair applied pending re-critique |
.loom/tickets/20260502-planwv11-improve-plan-coverage-wave-checks.md:80:| `ticket:planwv11#ACC-002` | `evidence:plan-wave-coverage-validation` shows wave independence, write scope overlap, and separate real-wave/no-wave examples | `critique:plan-wave-coverage-review#PLANWV11-CRIT-002` | repair applied pending re-critique |
.loom/tickets/20260502-planwv11-improve-plan-coverage-wave-checks.md:81:| `ticket:planwv11#ACC-003` | `evidence:plan-wave-coverage-validation` shows guidance preserving ticket/packet authority and canonical owner surfaces | `critique:plan-wave-coverage-review#PLANWV11-CRIT-003` | repair applied pending re-critique |
.loom/tickets/20260502-planwv11-improve-plan-coverage-wave-checks.md:82:| `ticket:planwv11#ACC-004` | `evidence:plan-wave-coverage-validation` records before/after searches, packet lifecycle wording, and `git diff --check` | `critique:plan-wave-coverage-review#PLANWV11-CRIT-004` | repair applied pending re-critique |
.loom/tickets/20260502-planwv11-improve-plan-coverage-wave-checks.md:115:Route: critique
.loom/tickets/20260502-planwv11-improve-plan-coverage-wave-checks.md:157:Disposition status: pending
.loom/tickets/20260502-planwv11-improve-plan-coverage-wave-checks.md:165:Disposition status: pending
```

Plan template real-wave/no-wave example split:

```text
skills/loom-plans/templates/plan.md:48:| `<record>#<claim-or-ACC>` | `ticket:<token>` | What the ticket must cover | Expected evidence or critique | `None - reason` only when no claim-bearing source applies |
skills/loom-plans/templates/plan.md:56:waves require a concrete non-overlap summary; write `None - reason` only when no
skills/loom-plans/templates/plan.md:62:`child_write_scope` or likely write scope, dependency/contention checks, and the
skills/loom-plans/templates/plan.md:63:parent reconciliation route. If no wave applies, write `None - reason`.
skills/loom-plans/templates/plan.md:69:`None - reason`.
skills/loom-plans/templates/plan.md:73:| Wave | Tickets | Independent because | Expected `child_write_scope` / write scope overlap check | Dependency / shared-state check | Parent reconciliation |
skills/loom-plans/templates/plan.md:75:| `Wave 1` | `ticket:<token-a>`, `ticket:<token-b>` | No same-wave dependency | `ticket:<token-a>` writes `<path-a>`; `ticket:<token-b>` writes `<path-b>`; no overlapping `child_write_scope` paths | No generated file, lockfile, migration, or stateful contention | Ticket-owned update plus evidence/critique route |
skills/loom-plans/templates/plan.md:76:| No wave | `None - reason` | `None - reason` | `None - reason` | `None - reason` | Continue with sequential ticket route |
skills/loom-plans/templates/plan.md:100:Expected packet `child_write_scope` / write scope overlap check:
```

Plan-shape owner wording check:

```text
skills/loom-plans/references/plan-shape.md:110:Before any sibling Ralph execution, record a compact wave check in the plan,
skills/loom-plans/references/plan-shape.md:111:ticket journal, or packet working notes; scratch notes are temporary before
```

Packet lifecycle wording check:

```text
.loom/packets/ralph/20260502T210325Z-ticket-planwv11-iter-01.md:5:status: consumed
.loom/packets/ralph/20260502T210325Z-ticket-planwv11-iter-01.md:192:  initially left packet lifecycle status as `compiled`; the parent later marked
.loom/packets/ralph/20260502T210325Z-ticket-planwv11-iter-01.md:193:  frontmatter `status: consumed` during reconciliation.
```

Repair `git diff --check` produced no output and exited successfully.

## Second repair observations

Claim matrix status vocabulary check:

```text
status_cells=80:supported_pending_review, 81:supported_pending_review, 82:supported_pending_review, 83:supported_pending_review, 84:supported_pending_review, 85:open
noncanonical=none
```

Ticket status, route, disposition, and repair-prose check:

```text
.loom/tickets/20260502-planwv11-improve-plan-coverage-wave-checks.md:4:status: review_required
.loom/tickets/20260502-planwv11-improve-plan-coverage-wave-checks.md:80:| `initiative:skills-corpus-council-precision-pass#OBJ-011` | `evidence:plan-wave-coverage-validation` records before/after structural searches and repair observations | `critique:plan-wave-coverage-rereview` | supported_pending_review |
.loom/tickets/20260502-planwv11-improve-plan-coverage-wave-checks.md:81:| `ticket:planwv11#ACC-001` | `evidence:plan-wave-coverage-validation` shows new claim coverage mapping cues | `critique:plan-wave-coverage-rereview` | supported_pending_review |
.loom/tickets/20260502-planwv11-improve-plan-coverage-wave-checks.md:82:| `ticket:planwv11#ACC-002` | `evidence:plan-wave-coverage-validation` shows wave independence, write scope overlap, and separate real-wave/no-wave examples | `critique:plan-wave-coverage-rereview` | supported_pending_review |
.loom/tickets/20260502-planwv11-improve-plan-coverage-wave-checks.md:83:| `ticket:planwv11#ACC-003` | `evidence:plan-wave-coverage-validation` shows guidance preserving ticket/packet authority and canonical owner surfaces | `critique:plan-wave-coverage-rereview` | supported_pending_review |
.loom/tickets/20260502-planwv11-improve-plan-coverage-wave-checks.md:84:| `ticket:planwv11#ACC-004` | `evidence:plan-wave-coverage-validation` records before/after searches, packet lifecycle wording, and `git diff --check` | `critique:plan-wave-coverage-rereview#PLANWV11-RCRIT-002` | supported_pending_review |
.loom/tickets/20260502-planwv11-improve-plan-coverage-wave-checks.md:85:| `ticket:planwv11#ACC-005` | pending oracle re-critique | `critique:plan-wave-coverage-rereview#PLANWV11-RCRIT-001` | open |
.loom/tickets/20260502-planwv11-improve-plan-coverage-wave-checks.md:128:Route: critique
.loom/tickets/20260502-planwv11-improve-plan-coverage-wave-checks.md:177:Disposition status: pending
.loom/tickets/20260502-planwv11-improve-plan-coverage-wave-checks.md:185:Disposition status: pending
```

Repair packet lifecycle wording check:

```text
.loom/packets/ralph/20260502T211053Z-ticket-planwv11-iter-02.md:5:status: consumed
.loom/packets/ralph/20260502T211053Z-ticket-planwv11-iter-02.md:137:   packet compiled and the parent later marked it consumed.
.loom/packets/ralph/20260502T211053Z-ticket-planwv11-iter-02.md:194:  initially left packet lifecycle status as `compiled`; the parent later marked
.loom/packets/ralph/20260502T211053Z-ticket-planwv11-iter-02.md:195:  frontmatter `status: consumed` during reconciliation.
.loom/packets/ralph/20260502T211053Z-ticket-planwv11-iter-02.md:209:  initially left the packet `compiled` and the parent later marked frontmatter
.loom/packets/ralph/20260502T211053Z-ticket-planwv11-iter-02.md:210:  `status: consumed`.
```

Second repair `git diff --check` produced no output and exited successfully.

# Supports Claims

- `initiative:skills-corpus-council-precision-pass#OBJ-011`
- `ticket:planwv11#ACC-001`
- `ticket:planwv11#ACC-002`
- `ticket:planwv11#ACC-003`
- `ticket:planwv11#ACC-004`

# Challenges Claims

None - no new observed challenge from the repair structural checks. The prior
critique and re-critique findings remain ticket-owned pending re-critique
disposition.

# Environment

Commit: `cb69ab9efdefbe4dabb9c86f34048687a0c8930e`
Branch: `main`
Runtime: Markdown/file edits through the local agent harness
OS: Darwin Alexander-Butler 24.6.0 Darwin Kernel Version 24.6.0: Fri Feb 27 19:31:41 PST 2026; root:xnu-11417.140.69.709.8~1/RELEASE_ARM64_T6000 arm64 arm Darwin
Relevant config: no network, no commits, no git config mutation

# Validity

Valid for: Structural presence of the named plan guidance cues in the edited
source state.
Fresh enough for: `ticket:planwv11` repair review and mandatory critique routing.
Recheck when: plan guidance, ticket claim-matrix/status grammar,
ticket route/disposition grammar, Ralph packet grammar, or Git parallel guidance
changes again.
Invalidated by: edits that remove or materially alter the observed plan guidance
without rerunning the searches.
Supersedes / superseded by: None - first evidence record for this ticket.

# Limitations

This evidence records structural searches and whitespace validation. It does not
prove that future plans will be authored correctly, that critique will pass, or
that any ticket is accepted or closed.

# Result

The post-edit search showed new or expanded cues for `claim coverage`,
`Execution Waves`, `write scope`, `child_write_scope`, `parallel`, and
`None - reason` in plan template/readiness guidance and `plan-shape.md`. The
repair observations show canonical `Route: critique`, valid critique disposition
`pending`, a real-wave sample with a concrete non-overlap summary, a separate
no-wave `None - reason` row, canonical owner-surface wording, and packet
lifecycle prose aligned with parent reconciliation. The second repair observations
show that claim matrix status cells use only the claim-coverage vocabulary and
that the iteration 2 packet body names both the child-left-compiled and
parent-marked-consumed lifecycle states. `git diff --check` passed with no
output.

# Interpretation

The baseline showed sparse plan cues: `Execution Waves`, `parallel`,
`child_write_scope`, `write scope`, and `None - reason` appeared, but exact
`claim coverage` language and detailed wave overlap checks were absent from the
plan guidance search results. The post-edit and repair observations support the
structural claims in `ticket:planwv11#ACC-001` through `#ACC-004`; they do not
satisfy the mandatory critique criterion by themselves. The second repair
observations support repair of `PLANWV11-RCRIT-001` and `PLANWV11-RCRIT-002`, but
`ticket:planwv11#ACC-005` remains open pending mandatory oracle re-critique.

# Related Records

- `ticket:planwv11`
- `packet:ralph-ticket-planwv11-20260502T210325Z`
- `packet:ralph-ticket-planwv11-20260502T211053Z`
- `packet:ralph-ticket-planwv11-20260502T212006Z`
