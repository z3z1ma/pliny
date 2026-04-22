---
id: research:shared-script-cli-inventory
kind: research
status: active
created_at: 2026-04-01T17:44:27Z
updated_at: 2026-04-22T17:20:00Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  plan:
    - plan:bootstrap-cli-reference-docs
  ticket:
    - ticket:z8h0g58e
external_refs: {}
---

# Question

What CLI surface do Loom's shared helper scripts actually expose today, and what details should skill-local script references preserve so future agents do not have to inspect parser code or run `--help` to use them safely?

# Objective

Capture parser-truth for the shared helper family so the first skill-local script references can document real positional arguments, flags, defaults, output shapes, and invocation patterns.

# Scope

- inspect only the shared helper family at the parser-definition level
- capture the exposed arguments and output forms of each shared helper script
- note where the same shared scripts are surfaced through skill-local copies
- identify the smallest credible documentation slice for immediate publication

# Non-goals

- do not redesign helper behavior or rename flags
- do not document every `create_<kind>.py` script in this first pass
- do not claim behavioral guarantees that are not visible in parser code or existing source docs
- do not treat skill-local path variants as separate CLIs when they are shared copies

# Methodology

Read the argparse definitions and top-level print paths in the shared helper scripts that are copied into the skill bundles.

Cross-check those findings against the existing examples in `src/skills/loom-workspace/references/examples.md`, `src/skills/loom-tickets/references/examples.md`, and `src/rules/appendices/worked-example-flow.md`.

Use the parser definitions as the tie-breaker when examples and narrative docs are incomplete.

# Hypotheses

- most shared helpers expose a deliberately small CLI with one positional target or no positional arguments at all
- JSON output is available for the inspection-style helpers and omitted for mutation helpers that only print the created or changed path
- existing examples are enough to show common invocation patterns, but not enough to serve as a complete per-script reference

# Evidence

- `compile_packet.py`
  Positional arguments: `target_ref`, `subsystem` where `subsystem` must be `ralph`, `critique`, or `docs`.
  Flags: `--mode` with default `execution`; `--style` with default `reference-first`; repeatable `--allow-write-ref`; optional `--output`.
  Output: prints the packet path relative to the workspace.
- `list_records.py`
  Positional arguments: none.
  Flags: optional `--kind`; optional `--status`; `--include-runs`; `--json`.
  Output: JSON array when `--json` is set, otherwise tab-separated `id kind status path` lines.
- `validate_record.py`
  Positional arguments: optional `path`.
  Flags: `--json`.
  Output: JSON object with `issues`, human-readable `ERROR ...` lines, or `All checked records are structurally valid` when clean. Exit status is non-zero on problems.
- `resolve_scope.py`
  Positional arguments: none.
  Flags: optional `--path`; `--json`.
  Output: repository list when no path is supplied; owner payload for one path when `--path` is supplied.
- `show_status.py`
  Positional arguments: none.
  Flags: `--json`.
  Output: JSON workspace summary or grouped text counts by kind and status.
- `diagnose_workspace.py`
  Positional arguments: none.
  Flags: `--json`.
  Output: JSON doctor report or a compact health summary including workspace, health, skill count, record issue count, and link issue count. Exit status is non-zero when unhealthy.
- `check_links.py`
  Positional arguments: none.
  Flags: `--json`.
  Output: JSON object with `issues`, human-readable missing-link errors, or `All checked links resolve` when clean. Exit status is non-zero on problems.
- `link_records.py`
  Positional arguments: `target` record ref.
  Flags: repeatable `--add`; repeatable `--remove`.
  Output: prints the changed record path relative to the workspace. Fails fast if neither `--add` nor `--remove` is provided.
- `create_verification.py`
  Positional arguments: `slug`.
  Flags: optional `--title`; repeatable `--link`; repeatable `--section`.
  Output: prints the created verification record path relative to the workspace.
- Exposure pattern
  `show_status.py`, `diagnose_workspace.py`, and `list_records.py` are exposed through `loom-workspace`.
  `compile_packet.py` is exposed through `loom-ralph`, `loom-critique`, and `loom-docs`.
  `create_verification.py`, `check_links.py`, and `resolve_scope.py` are exposed across the execution-adjacent skills.
  `validate_record.py` and `link_records.py` are exposed broadly across multiple artifact skills.

# Experiments

This first slice used static parser inspection rather than command execution against every helper.

One spot check from the workspace skill examples confirmed the documented path-variant pattern:

- `python3 "src/skills/loom-workspace/scripts/show_status.py" --json`
- `python3 "src/skills/loom-workspace/scripts/resolve_scope.py" --json --path "<target-path>"`

The worked-flow appendix also confirms the expected invocation shape for packet compilation:

- `python3 "src/skills/loom-ralph/scripts/compile_packet.py" "<ticket-ref>" ralph --mode execution --style reference-first --allow-write-ref "<ticket-ref>"`

# Rejected Paths

- documenting every skill-local script copy separately was rejected because those files are shared-script copies and would create repeated, drift-prone docs
- documenting only examples without enumerating the parser surface was rejected because the user's need is specifically argument and flag clarity
- widening the first slice to all `create_<kind>.py` scripts was rejected because it would delay the first shared helper reference and mix two different CLI families

# Conclusions

- The shared helper layer is small enough to document comprehensively through skill-local script references.
- The parser surfaces are stable and explicit enough that the reference can be grounded directly in code rather than guesswork.
- The main current usability gap is discoverability, not obvious parser complexity.
- The right operator-facing artifact is skill-local `references/scripts.md`, using package-local `scripts/...` paths and parameter explanations grounded in the parser definitions.

# Recommendations

- Publish `references/scripts.md` files on the skills that expose bundled helper scripts.
- In those references, document positional arguments, flags, defaults, output shapes, and one example command per script.
- Keep the operator-facing examples on package-local `scripts/...` paths instead of source-only build paths.
- Leave the broader `create_<kind>.py` family as a follow-up ticket or expansion to this docs work.

# Open Questions

- Should the `create_<kind>.py` family get one shared family reference or per-skill references later?
- Should helper CLI docs stay hand-written, or eventually be generated from the parser definitions?
- If a future helper adds richer machine-readable output, should the appendix start documenting exit-code conventions explicitly alongside flags?

# Linked Downstream Artifacts

- `plan:bootstrap-cli-reference-docs`
- `ticket:z8h0g58e`
- `src/skills/*/references/scripts.md`
