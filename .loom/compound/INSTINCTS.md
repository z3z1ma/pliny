# INSTINCTS

<!-- BEGIN:compound:instincts-md -->
## Active instincts (top confidence)

- **avoid-tooling-artifacts-in-templates** (90%) [compound, hygiene, templates]
  - Trigger: When adding or reviewing files under template trees like src/agent_loom/compound/opencode/ (or other scaffolded outputs).
  - Action: Exclude tool-specific project files (e.g., `.serena/*`, local IDE metadata, assistant-runner configs) from templates and committed scaffolds unless they are a deliberate product feature; prefer removi...
- **avoid-lsp-diagnostics-use-basedpyright** (86%) [python, quality, typing]
  - Trigger: When tempted to check typing errors via editor/LSP or `lsp_diagnostics`
  - Action: Use `uv run basedpyright` as the source of truth; treat LSP output as advisory only.
- **post-refactor-quality-gates** (86%) [lint, quality, tests, typing, uv]
  - Trigger: After a broad refactor that touches many files and tests
  - Action: Run `uv run ruff check .`, `uv run basedpyright`, then `uv run pytest`; treat failures as part of the refactor (not follow-up work).
- **compound-template-determinism-first** (82%) [compound, determinism, templates, tests]
  - Trigger: When changing compound scaffold/template contents or compound install logic (e.g., src/agent_loom/compound/scaffold.py, src/agent_loom/compound/paths.py, src/agent_loom/compound/docs.py, compound open...
  - Action: Treat the installed `.opencode/` (and any `.loom/compound/` docs) as a contract: preserve stable paths, stable file ordering, stable newline formatting, and stable rendered content; immediately update...
- **prefer-uv-gates-before-tests** (82%) [python, quality, tooling, uv]
  - Trigger: After non-trivial Python edits (new modules, refactors, deletes) and before running tests or claiming done
  - Action: Run `uv run basedpyright` then `uv run ruff check .` and fix all issues before `uv run pytest`.
- **subsystem-removal-sweep** (82%) [deletion, docs, maintenance, python, refactor, tests]
  - Trigger: When deleting or deprecating a substantial module/package (especially with many submodules)
  - Action: Immediately sweep for imports/exports, docs references, CLI help/examples, tests, and any API schemas; remove or rewrite references so the repo remains coherent and discoverable.
- **remove-orphans-after-large-deletions** (80%) [cleanup, packaging, python, refactor]
  - Trigger: When removing many files or an entire subtree (e.g., `.../poly/*`)
  - Action: Check `__init__.py` exports, public module surface, and docs/README links for orphans; ensure imports fail nowhere and no dead entrypoints remain.
- **refactor-delete-module-chase-imports** (78%) [maintenance, python, refactor]
  - Trigger: A refactor removes/renames modules (large deletions or package reshapes)
  - Action: Search for old module names and key symbols (e.g. with ripgrep/grep), update imports, docs, and tests together; ensure no dead entrypoints remain.
- **template-docs-use-root-relative-paths** (78%) [compound, docs, portability]
  - Trigger: When editing README/docs content that will be scaffolded into a repo (e.g., src/agent_loom/compound/opencode/README.md, src/agent_loom/compound/opencode/.loom/compound/README.md, `.opencode/commands/*...
  - Action: Write links and references using repo-root-relative paths (no absolute machine paths, no editor URIs) and avoid references to removed/retired template files (e.g., AGENTS.md copies) to keep docs porta...
- **keep-openapi-and-ui-in-sync** (76%) [api, contract, dashboard, openapi]
  - Trigger: When changing server routes, request/response shapes, or endpoint behavior
  - Action: Update `docs/openapi.yaml` in the same change and verify any dashboard readers/clients that depend on those endpoints still work; treat schema drift as a bug.
- **cli-ux-change-needs-tests** (74%) [cli, regression, tests, ux]
  - Trigger: When modifying CLI output, help text, defaults, or command structure
  - Action: Update/extend UX-focused tests to lock in the intended ergonomics and prevent regressions; avoid untested copy changes that silently degrade UX.
- **large-change-update-cli-ux-tests** (74%) [cli, tests, ux]
  - Trigger: Any change to CLI output, flags, or subcommand routing
  - Action: Locate and update the UX snapshot/expectation tests (e.g. `tests/test_*_cli_ux.py`) in the same change; ensure wording is intentional and stable.
- **prefer-command-docs-over-embedded-skill-copies** (74%) [commands, compound, docs, skills]
  - Trigger: When documenting workflows for end-users inside compound-installed `.opencode/` trees.
  - Action: Put loom command guidance in `.opencode/commands/loom-*.md` (command-discoverable docs) and avoid duplicating full skill content inside the compound template unless required; keep skills procedural an...
- **greenfield-no-backcompat-language** (70%) [design, docs, product]
  - Trigger: Writing docs, flags, deprecations, or migration behaviors in early-stage systems
  - Action: Prefer clean breaks and simple interfaces; remove/avoid 'backcompat' language unless there is a real external user contract that requires it.
- **openapi-keep-spec-deterministic** (66%) [api, docs, openapi]
  - Trigger: Editing `docs/openapi.yaml` during endpoint/schema updates
  - Action: Avoid volatile fields like timestamps; keep component and path ordering stable; validate references and schema names stay consistent with the code.

## Notes

- Instincts are the pre-skill layer: small, repeatable heuristics.
- When an instinct proves useful across sessions, promote it into a Skill.
<!-- END:compound:instincts-md -->
