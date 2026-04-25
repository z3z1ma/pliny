---
id: critique:open-loom-config-hook-review
kind: critique
status: final
created_at: 2026-04-25T21:29:31Z
updated_at: 2026-04-25T22:07:56Z
scope:
  kind: repository
  repositories:
    - repo:root
review_target: open-loom config-hook implementation and npm package readiness for ticket:6uy1rx20
links:
  ticket:
    - ticket:6uy1rx20
  evidence:
    - evidence:open-loom-smoke
  prior_critique:
    - critique:open-loom-review
external_refs:
  opencode_source:
    - https://github.com/anomalyco/opencode/tree/v1.14.22
---

# Summary

Reviewed the corrected `open-loom` implementation after it switched from the
chat-transform route to OpenCode's `config(config)` hook.

# Review Target

Changed package and install surfaces:

- `open-loom.mjs`
- `package.json`
- `INSTALL.md`
- `examples/adapters/open-loom-install/README.md`
- `ticket:6uy1rx20`
- `evidence:open-loom-smoke`

# Verdict

`pass_with_findings`.

The implementation shape is acceptable for OpenCode `1.14.22` after the follow-up
fixes below. Npm publication is ready for the final operator authentication and
publish step, with residual risks recorded.

# Findings

## FIND-001: OpenCode compatibility range was missing

Severity: medium
Confidence: high
Disposition: resolved

Observation:

`open-loom` depends on OpenCode plugin `config(config)` behavior validated against
OpenCode `1.14.22`, but `package.json` initially had no `engines.opencode` guard.

Why it matters:

Older or incompatible OpenCode versions could install the package and fail or
partially register Loom surfaces.

Follow-up:

Resolved by adding `engines.opencode: ">=1.14.22 <2"` to `package.json` and
documenting the minimum range in `INSTALL.md` and the OpenCode adapter fixture.

Challenges:

None after resolution.

## FIND-002: Package-root validation was missing from evidence

Severity: medium
Confidence: high
Disposition: resolved

Observation:

Earlier evidence recorded direct `file://.../open-loom.mjs` validation but did not
preserve the local package-root plugin validation that exercises `package.json`
entrypoint resolution.

Why it matters:

The npm package path depends on package root resolution, not only direct module
file loading.

Follow-up:

Resolved by recording package-root `opencode debug config` validation in
`evidence:open-loom-smoke`.

Challenges:

None after resolution.

## FIND-003: Published docs pointed at omitted examples

Severity: low
Confidence: high
Disposition: resolved

Observation:

`INSTALL.md` points readers at `examples/adapters/open-loom-install/`, but the npm
file list initially did not include `examples/`.

Why it matters:

Published package users would receive a broken documentation pointer.

Follow-up:

Resolved by adding `examples/` to the npm package file list and rerunning
`npm run pack:check`, which showed the OpenCode adapter fixture in the dry-run
tarball.

Challenges:

None after resolution.

## FIND-004: Install docs still said package metadata was private

Severity: low
Confidence: high
Disposition: resolved

Observation:

`INSTALL.md` retained wording that package metadata was intentionally private,
but `package.json` is no longer private and is prepared for publication.

Why it matters:

The install guide would contradict the package state.

Follow-up:

Resolved by replacing the stale private-package wording with the OpenCode version
requirement and package-entry guidance.

Challenges:

None after resolution.

## FIND-005: License metadata was absent

Severity: low
Confidence: medium
Disposition: resolved

Observation:

The package did not declare a license and the repository has no visible `LICENSE`
file.

Why it matters:

Public npm users need explicit reuse terms or an explicit no-license posture.

Follow-up:

Resolved conservatively by adding `license: "UNLICENSED"` to `package.json` rather
than inventing an open-source license.

Challenges:

None after resolution.

# Evidence Reviewed

- `open-loom.mjs`
- `package.json`
- `INSTALL.md`
- `examples/adapters/open-loom-install/README.md`
- `evidence:open-loom-smoke`
- OpenCode `v1.14.22` plugin compatibility source
- `node open-loom.mjs --smoke`
- import-based config-hook validation
- `opencode debug config` with direct plugin file
- `opencode debug config` with local package root
- clean-project `opencode debug skill --print-logs` showing `service=skill count=20`
- `npm run pack:check`
- `npm whoami`
- `npm publish --dry-run --access public`
- `npm view open-loom name version --json`
- published `npm view open-loom name version dist-tags engines license --json`
- repo-root `opencode.json` package-load validation for `open-loom@0.1.0`
- `git diff --check`

# Residual Risks

- Npm registry publication is validated for `open-loom@0.1.0`.
- OpenCode `1.14.22` cold-cache npm-plugin config-file validation can log
  `NpmInstallFailedError` on the first run before a second run resolves the
  cached package and exposes Loom surfaces.
- No paid model request or interactive TUI session was run. The validation relies
  on OpenCode's documented `instructions`, `skills.paths`, and `command` config
  surfaces plus debug config/skill behavior.
- OpenCode plugin internals may change outside the declared `>=1.14.22 <2`
  compatibility range.
- The package is explicitly `UNLICENSED`; this is intentional because no project
  license has been chosen.

# Required Follow-up

Before closure:

- accept the cold-cache first-run OpenCode npm-plugin quirk as residual risk, or
  create a linked follow-up investigation/fix ticket

# Acceptance Recommendation

`complete pending acceptance`.

The implementation, package-readiness findings, and npm publication are resolved.
Final acceptance depends on accepted-risk or follow-up disposition for the
OpenCode cold-cache first-run npm-plugin behavior.
