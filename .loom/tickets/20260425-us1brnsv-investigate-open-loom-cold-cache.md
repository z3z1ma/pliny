---
id: ticket:us1brnsv
kind: ticket
status: closed
change_class: release-packaging
risk_class: medium
created_at: 2026-04-25T22:14:57Z
updated_at: 2026-04-28T18:50:38Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  spec:
    - spec:opencode-plugin-install-contract
  wiki:
    - wiki:harness-adapter-package-pattern
  related:
    - ticket:6uy1rx20
  evidence:
    - evidence:open-loom-smoke
  research:
    - research:loom-install-distribution-methods
external_refs:
  opencode_docs:
    - https://opencode.ai/docs/plugins/
  opencode_source:
    - https://github.com/anomalyco/opencode/tree/v1.14.22
depends_on: []
---

# Summary

Investigate the OpenCode `1.14.22` cold-cache npm-plugin first-run behavior where
`open-loom@0.1.0` can log `NpmInstallFailedError` on the first config-file run
while still installing into OpenCode's package cache, then load successfully on a
second run.

# Context

`ticket:6uy1rx20` published `open-loom@0.1.0` and validated the normal repo-root
`opencode.json` package path after OpenCode had a cached package installation.
Further isolated checks found a first-run caveat:

- first cold-cache config-file run: `NpmInstallFailedError`, Loom surfaces absent
- second run in the same OpenCode cache: package resolves and Loom rules, skills,
  and commands are exposed

The current install docs record this as a caveat. This follow-up owns deeper
investigation without blocking acceptance of the published package.

# Why Now

The package is published, and normal package config can work. The remaining risk
is first-run operator confusion for fresh OpenCode caches.

# Scope

- reproduce the cold-cache behavior in an isolated `HOME` with a normal
  config-file plugin entry
- distinguish OpenCode installer behavior from package metadata or package-layout
  defects
- inspect OpenCode `Npm.add` / plugin loader behavior enough to explain why the
  first run can fail while caching the package
- update `INSTALL.md` and adapter notes if the caveat or workaround needs
  sharper wording
- recommend whether to file an upstream OpenCode issue or adjust package metadata

# Non-goals

- do not change Loom protocol rules or skills
- do not republish `open-loom` unless a package-side fix is proven
- do not re-open `ticket:6uy1rx20`; this ticket owns the follow-up risk
- do not recommend Git URL plugin installs

# Acceptance Criteria

- the cold-cache behavior is reproduced or explicitly marked no longer
  reproducible
- evidence records the command shape, environment, and first/second-run results
- root cause is explained enough to route the fix, or uncertainty is preserved in
  research
- docs are updated if the practical workaround changes
- package-side follow-up, upstream issue, or accepted no-change disposition is
  explicit

# Coverage

Covers:

- None - no spec-owned acceptance IDs exist. This ticket owns a release-packaging
  follow-up from `ticket:6uy1rx20`.

# Claim Matrix

| Claim | Evidence | Critique | Status |
| --- | --- | --- | --- |
| OpenCode cold-cache npm plugin behavior may need follow-up | `evidence:open-loom-smoke` | `critique:open-loom-config-hook-review` | open |

# Execution Notes

Known reproduction shape from acceptance review:

```bash
tmp="$(mktemp -d)"
HOME="$tmp/home" XDG_CONFIG_HOME="$tmp/home/.config" opencode debug config --print-logs --log-level INFO
HOME="$tmp/home" XDG_CONFIG_HOME="$tmp/home/.config" opencode debug config --print-logs --log-level INFO
```

Run from a repository with an `opencode.json` that contains
`"plugin": ["open-loom@0.1.0"]`.

# Blockers

None. Operator accepted no further cold-cache investigation in this ticket.

# Next Move / Next Route

Closed. If cold-cache behavior recurs in a current OpenCode version, open a fresh
ticket with isolated first/second-run evidence.

# Ralph Readiness

Bounded iteration:
Reproduce and explain the cold-cache first-run behavior.

Write boundary:
This ticket, evidence/research records, `INSTALL.md`, and adapter notes if the
workaround wording changes.

Likely verification posture:
Observation-first.

Expected output contract:
Reproduction evidence, root-cause explanation or preserved uncertainty, docs
disposition, and recommendation for upstream/package follow-up.

# Evidence

Expected evidence was not gathered in this ticket before operator closure:

- isolated first/second-run OpenCode output
- installed package cache inspection when useful
- source references for OpenCode npm/plugin behavior when claiming root cause

# Critique Disposition

Risk class: medium

Critique policy: recommended

Policy rationale:
This affects install UX and release packaging. Critique is recommended if a
package-side fix or docs change is proposed.

Required critique profiles:

- operator-clarity

Findings:

- None - no critique yet.

Disposition status: not_required by operator acceptance at closure

Deferral / not-required rationale:

No package-side fix or docs change is being accepted from this ticket; the prior
documented caveat remains the disposition.

# Wiki Disposition

Optional. Promote only if this becomes a reusable OpenCode npm-plugin
troubleshooting pattern.

# Acceptance Decision

Accepted by: operator
Accepted at: 2026-04-28T18:50:38Z
Basis: Operator stated the remaining open work was complete and accepted closing this follow-up without further investigation. The ticket records that no package-side fix, upstream issue, or documentation change is being taken from this record.
Residual risks: The original cold-cache first-run behavior was not reproduced or root-caused in this ticket before closure; future recurrence should be investigated against the current OpenCode package/plugin runtime.

# Dependencies

Follow-up from `ticket:6uy1rx20`. No hard prerequisite blocks starting.

# Journal

- 2026-04-25: created during OpenCode acceptance review so
  `ticket:6uy1rx20` can close with the cold-cache npm-plugin behavior tracked as
  follow-up work rather than hidden residual risk.
- 2026-04-28T18:50:38Z: Operator accepted closing the remaining cold-cache
  follow-up with no further action; residual uncertainty is recorded for any
  future recurrence.
