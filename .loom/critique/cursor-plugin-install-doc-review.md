---
id: critique:cursor-plugin-install-doc-review
kind: critique
status: final
created_at: 2026-04-26T07:53:38Z
updated_at: 2026-04-26T07:53:38Z
scope:
  kind: repository
  repositories:
    - repo:root
review_target: ticket:1c0lb4uu
links:
  ticket:
    - ticket:1c0lb4uu
  evidence:
    - evidence:cursor-plugin-install-validation
  decision:
    - decision:0006
external_refs: {}
---

# Summary

Release-packaging and operator-clarity review for the Cursor plugin manifest and
native install command documentation.

# Verdict

pass

# Findings

None blocking.

The first review pass found that Cursor could auto-discover the repository's
Claude-specific `hooks/hooks.json`. The manifest now sets inline `hooks: {}` while
preserving `skills: "./skills/"`, so the Cursor plugin remains skills-only.

# Evidence Reviewed

- `.cursor-plugin/plugin.json`
- `INSTALL.md`
- `README.md`
- `examples/adapters/cursor-install/README.md`
- `examples/adapters/codex-plugin-install/README.md`
- `evidence:cursor-plugin-install-validation`

# Residual Risks

- Cursor runtime plugin loading and Marketplace listing are not validated.
- Codex installed Git-backed plugin skill discovery remains unvalidated.

# Acceptance Recommendation

Accept `ticket:1c0lb4uu`; remaining risks are follow-up release validation, not
blockers for adding the manifest and truthful install commands.
