---
id: evidence:promotion-disposition-wording-validation
kind: evidence
status: recorded
created_at: 2026-05-03T01:21:05Z
updated_at: 2026-05-03T01:24:53Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:promdisp2
  packet:
    - packet:ralph-ticket-promdisp2-20260503T011837Z
    - packet:ralph-ticket-promdisp2-20260503T012242Z
external_refs: {}
---

# Summary

Before-state searches found stale wiki-only closure and handoff shorthand across
the expected product surfaces. Replacement packet
`packet:ralph-ticket-promdisp2-20260503T012242Z` expanded scope to include the
previously blocking `skills/loom-records/references/implementation-reality.md`
instance, and this iteration rewrote the stale shorthand to retrospective /
promotion disposition language while preserving route-specific wiki disposition.

# Procedure

At `2026-05-03T01:20Z` from commit
`ee938daf3e32e3a2d1d6806fc7c607828b2624cb`, iteration 1 ran before-state
searches across `skills/`, `README.md`, and `PROTOCOL.md` for:

- `wiki disposition`
- `wiki follow-through`
- `retrospective`
- `promotion disposition`
- `promotion route`
- `not_required`
- `deferred`
- closure / handoff wording

At `2026-05-03T01:24Z`, this replacement iteration refreshed the combined
before-state search before product edits and reran after-state searches after
product wording edits.

Commands:

```bash
rg -n -i "wiki follow-through|wiki disposition" skills README.md PROTOCOL.md
rg -n -i "promotion disposition|promotion route|retrospective|not_required|deferred|blocking" skills README.md PROTOCOL.md
rg -n -i "wiki disposition|wiki follow-through|retrospective|promotion disposition|promotion route|not_required|deferred|closure|handoff" skills README.md PROTOCOL.md
git diff --check
```

# Artifacts

Focused before-state search for `wiki follow-through|wiki disposition` observed
the stale product wording listed below before any product edits for this ticket:

```text
README.md:415:ticket/evidence/critique/wiki disposition -> PR summary, release note, risk summary, follow-up list
PROTOCOL.md:48:- **acceptance disposition**: ticket-owned decision about scoped claims, evidence, critique, wiki follow-through, accepted risk, and closure
skills/loom-bootstrap/references/07-validation-and-honesty.md:26:- wiki follow-through has happened or is explicitly deferred
skills/loom-critique/references/review-pass-splitting.md:32:   Check ticket truth, evidence, critique disposition, wiki disposition, and
skills/loom-ship/SKILL.md:3:description: "Package already-truthful Loom work for merge, release, or handoff without closing tickets. Use when ticket, evidence, critique, and wiki disposition should become a PR summary, release note draft, risk summary, or follow-up list."
skills/loom-ship/SKILL.md:28:- critique and wiki disposition need to be summarized
skills/loom-ship/SKILL.md:45:- wiki disposition
skills/loom-critique/references/critique-lens.md:116:- honest ticket, evidence, and wiki disposition
skills/loom-drive/references/tranche-decision-protocol.md:110:- Ship enters with truthful ticket/evidence/critique/wiki disposition and exits
skills/loom-ralph/references/work-driver.md:14:- critique and wiki disposition
skills/loom-records/references/implementation-reality.md:26:critique, evidence, or wiki follow-through remains open.
skills/loom-git/SKILL.md:135:- ticket, evidence, critique, and wiki disposition remain truthful
```

The refreshed combined before-state search also showed relevant closure/handoff
surfaces in `skills/loom-evidence/references/evidence-quality.md`,
`skills/loom-ship/references/handoff-options.md`, `skills/loom-tickets/SKILL.md`,
and `skills/loom-workspace/references/status-snapshot.md`; these were inside the
expanded packet scope and were updated where the wording was stale or could imply
wiki-only follow-through.

Focused after-state search for `wiki follow-through|wiki disposition` observed
only route-specific wiki wording:

```text
skills/loom-bootstrap/references/05-critique-and-wiki.md:169:closure; wiki disposition records only the route-specific wiki outcome when wiki
skills/loom-bootstrap/references/05-critique-and-wiki.md:189:Wiki does not replace them, and wiki disposition does not replace the broader
skills/loom-retrospective/SKILL.md:100:   `# Wiki Disposition` only for the route-specific wiki outcome when wiki is one
skills/loom-ship/SKILL.md:45:- retrospective / promotion disposition, plus route-specific wiki disposition when
skills/loom-tickets/templates/ticket.md:246:# Wiki Disposition
skills/loom-records/references/retrospective.md:18:  `# Retrospective / Promotion Disposition`; wiki disposition is only the
skills/loom-critique/references/review-pass-splitting.md:33:   disposition, route-specific wiki disposition when applicable, and whether the
skills/loom-critique/references/critique-lens.md:117:  route-specific wiki disposition when applicable
skills/loom-workspace/references/status-snapshot.md:68:  route-specific wiki disposition when applicable, and the next route
skills/loom-tickets/references/acceptance-gate.md:22:- wiki disposition when wiki is one of the promotion routes
skills/loom-tickets/references/acceptance-gate.md:50:  + Wiki Disposition when applicable
skills/loom-tickets/references/acceptance-gate.md:83:- If wiki is one promotion route, does `# Wiki Disposition` record the
skills/loom-tickets/SKILL.md:76:route-specific wiki disposition when applicable, accepted risk, blockers, and
skills/loom-ship/references/handoff-options.md:17:  retrospective / promotion disposition, and route-specific wiki disposition when
skills/loom-ship/references/handoff-options.md:43:  including route-specific wiki follow-through when wiki was selected
```

Focused after-state search for promotion/status outcomes observed the broader
closure gate and preserved honest outcomes:

```text
PROTOCOL.md:48:- **acceptance disposition**: ticket-owned decision about scoped claims, evidence, critique, retrospective / promotion follow-through, accepted risk, and closure
README.md:415:ticket/evidence/critique/promotion disposition -> PR summary, release note, risk summary, follow-up list
skills/loom-bootstrap/references/07-validation-and-honesty.md:23:    `completed`, `deferred`, or `not_required` with rationale
skills/loom-bootstrap/references/07-validation-and-honesty.md:26:- retrospective / promotion follow-through has happened, been explicitly deferred,
skills/loom-bootstrap/references/07-validation-and-honesty.md:144:  closure: `completed`, `deferred`, or `not_required` with rationale
skills/loom-tickets/templates/ticket.md:228:Disposition status: <TBD: choose pending, blocking, completed, deferred, or not_required>
skills/loom-tickets/templates/ticket.md:232:- Use `blocking` when closure would be unsafe because required promotion or
skills/loom-tickets/templates/ticket.md:236:- Use `deferred` when promotion or prevention is intentionally moved to linked
skills/loom-tickets/templates/ticket.md:238:- Use `not_required` when the ticket has no durable lesson to promote.
skills/loom-tickets/references/acceptance-gate.md:19:- retrospective / promotion disposition: ticket-owned status `pending`,
skills/loom-tickets/references/acceptance-gate.md:20:  `blocking`, `completed`, `deferred`, or `not_required`, plus promoted owner
skills/loom-tickets/references/acceptance-gate.md:80:- Is retrospective / promotion disposition resolved for closure as `completed`,
skills/loom-tickets/references/acceptance-gate.md:81:  `deferred`, or `not_required`, or does it remain `blocking` because required
skills/loom-tickets/SKILL.md:110:- critique and retrospective / promotion follow-through are linked or explicitly
skills/loom-tickets/SKILL.md:111:  pending, deferred, completed, or not required
```

`git diff --check` result after product and record updates: passed with no
output.

# Supports Claims

- `ticket:promdisp2#ACC-001` — stale wiki-only closure and handoff shorthand was
  replaced with retrospective / promotion disposition wording in the affected
  scoped product/public surfaces.
- `ticket:promdisp2#ACC-002` — after-state wiki-disposition matches are
  route-specific and do not replace the broader promotion disposition.
- `ticket:promdisp2#ACC-003` — after-state search confirms `completed`,
  `deferred`, `not_required`, and `blocking` outcomes remain available where the
  ticket acceptance gate and template need them.
- `ticket:promdisp2#ACC-004` — before/after searches and a passing
  `git diff --check` result were recorded.

# Challenges Claims

None observed for `ticket:promdisp2#ACC-001` through `ticket:promdisp2#ACC-004`.
`ticket:promdisp2#ACC-005` remains pending mandatory oracle critique and is not
validated by this evidence.

# Environment

Commit: `ee938daf3e32e3a2d1d6806fc7c607828b2624cb`
Branch: `main`
Runtime: Markdown/file search and Git CLI
OS: macOS / darwin
Relevant config: packet child write scope from `packet:ralph-ticket-promdisp2-20260503T012242Z`

# Validity

Valid for: wording search observations and diff whitespace validation at the
recorded source state.
Fresh enough for: routing `ticket:promdisp2` to mandatory oracle critique.
Recheck when: product surfaces change, critique finds a stale wording instance,
or the ticket acceptance gate changes.
Invalidated by: edits to `skills/`, `README.md`, `PROTOCOL.md`, or critique
findings that identify additional stale product wording.
Supersedes / superseded by: Supersedes the blocked iteration-1 scope observation
inside this same evidence record.

# Limitations

The searches are text-pattern observations over `skills/`, `README.md`, and
`PROTOCOL.md`; they do not prove every human interpretation is unambiguous.
Mandatory oracle critique is still required by the ticket before acceptance.

# Result

The expanded-scope wording cleanup completed its product-surface edits and found
no remaining stale wiki-only closure/handoff wording in the required search set.
Remaining `wiki disposition` / `wiki follow-through` matches are route-specific
to wiki as one selected promotion route.

# Interpretation

The ticket should move to `review_required` for mandatory oracle critique using
profiles `closure-honesty`, `workflow-boundary`, and `operator-clarity`.

# Related Records

- `ticket:promdisp2`
- `packet:ralph-ticket-promdisp2-20260503T011837Z`
- `packet:ralph-ticket-promdisp2-20260503T012242Z`
