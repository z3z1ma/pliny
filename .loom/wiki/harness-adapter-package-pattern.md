---
id: wiki:harness-adapter-package-pattern
kind: wiki
page_type: workflow
status: active
created_at: 2026-04-25T22:14:57Z
updated_at: 2026-04-25T22:14:57Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  initiative:
    - initiative:loom-install-experience
  plan:
    - plan:install-experience-harness-adapters
  spec:
    - spec:opencode-plugin-install-contract
  ticket:
    - ticket:6uy1rx20
  evidence:
    - evidence:open-loom-smoke
  critique:
    - critique:open-loom-config-hook-review
  research:
    - research:loom-install-distribution-methods
---

# Summary

Adapter packages are harness-native packaging surfaces that make Loom easier to
install without becoming owners of Loom semantics.

`open-loom@0.1.0` is the first accepted example in this repository: an OpenCode
npm plugin that exposes bundled Loom rules, skills, and optional command wrappers
through OpenCode config surfaces.

# When To Use It

Use this pattern when a harness has a first-class package, plugin, or extension
mechanism that can expose Loom's required surfaces more cleanly than direct
user-config mutation.

Do not use this pattern when the harness package system cannot express ordered
always-on rules, skill discovery, or command wrappers without a separate fallback.
In that case, use a hybrid install and document the split.

# Inputs

- canonical top-level `rules/`, `skills/`, and optional `commands/`
- the harness's official package/plugin/extension docs
- a ticket that owns one bounded harness install slice
- evidence for package structure, install behavior, and surface discovery
- critique for operator clarity and release-packaging risk

# Procedure

1. Start from the canonical Loom surfaces. Do not copy dogfooding `.loom/` or
   `.opencode/` state into the package.
2. Choose the smallest harness-native registration path that exposes rules,
   skills, and commands.
3. Keep generated files derivative and source-marked when generation is required.
4. Declare compatibility metadata when the package manager or harness supports it.
5. Validate package layout before publication or release.
6. Validate harness loading through the harness's own debug, install, link, or
   discovery commands when available.
7. Record install caveats as evidence and either accept them explicitly or create
   follow-up tickets.
8. Update install docs only after evidence supports the recommendation.

# Outputs

- package or adapter entrypoint files
- package metadata and compatibility range
- install docs and adapter fixture notes
- evidence record for package contents and harness loading
- critique record or disposition for release-packaging risk
- ticket acceptance decision with residual risks or linked follow-ups

# Failure Modes

- treating package files as the new canonical Loom source
- recommending a plugin path before the harness actually loads the package
- hiding a required fallback step behind plugin-first marketing
- publishing docs that point at files omitted from the package
- claiming cold-cache or first-run behavior works when only warm-cache behavior
  was observed
- overgeneralizing one harness's plugin behavior to other harnesses

# Sources

- `spec:opencode-plugin-install-contract`
- `ticket:6uy1rx20`
- `ticket:us1brnsv`
- `evidence:open-loom-smoke`
- `critique:open-loom-config-hook-review`
- `research:loom-install-distribution-methods`
- `plan:install-experience-harness-adapters`
- `initiative:loom-install-experience`

# Related Pages

No prior wiki pages exist in this workspace. Future Cursor, Gemini, Claude, and
Codex package work should link here only after their harness-specific evidence is
recorded.
