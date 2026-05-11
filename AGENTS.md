# AGENTS.md

## Repo Shape

- This repo ships a Markdown skill corpus, not an app runtime. Do not add daemon, database, dashboard, CLI, or helper-script assumptions unless explicitly changing architecture.
- Product behavior lives in `loom-core/skills/` and `loom-playbooks/skills/`; package entrypoints, manifests, hooks, and extensions only expose those trees.
- `loom-core/` is required and owns `using-loom`, Core record skills, templates, and references.
- `loom-playbooks/` is optional, requires Core, and must not duplicate or preload `using-loom` doctrine.
- Root `skills` is a symlink to `loom-core/skills` for the repo-root Gemini extension shim; treat `loom-core/skills/` as the real Core package surface.
- Package skill content must be self-contained for installed workspaces: use generic `.loom/...` runtime paths, not source-repo-only paths or dogfood assumptions.

## Dogfooding

- `.loom/` is this repo's dogfood workspace state for future Agent Loom development; it is not part of the shipped product surface.
- Use `.loom/` records to coordinate work on this repo, but keep exported behavior in `loom-core/skills/`, `loom-playbooks/skills/`, package entrypoints, manifests, hooks, and docs.
- Raw evidence and research artifacts under `.loom/*/artifacts/` stay ignored except scaffold `.gitkeep` files.

## Entrypoints And Adapters

- OpenCode entrypoints are `loom-core/loom-core.mjs` and `loom-playbooks/loom-playbooks.mjs`.
- Core OpenCode config registers the ordered `using-loom` files through `config.instructions` and exposes `loom-core/skills` through `config.skills.paths`.
- Playbooks OpenCode config only exposes `loom-playbooks/skills`; `doesNotPreloadCoreDoctrine: true` is intentional in its smoke output.
- Adapter catalogs live at `.claude-plugin/marketplace.json`, `.cursor-plugin/marketplace.json`, and `.agents/plugins/marketplace.json`.
- Per-package native manifests live under `loom-*/.claude-plugin/`, `loom-*/.codex-plugin/`, and `loom-*/.cursor-plugin/`; Core preload hooks live in `loom-core/hooks/`.
- The root `gemini-extension.json` is a Gemini-only Core shim; full Gemini local installs link `loom-core` and `loom-playbooks` separately.
- NPM `files` currently pack only `README.md`, `package.json`, the package `.mjs`, and `skills/`; native adapter manifests and hooks are Git-install surfaces unless packaging changes.

## Commands

- No install step is needed for current checks; there is no lockfile or external package dependency.
- There is no repo test, lint, typecheck, formatter, codegen config, or CI workflow; current verification is smoke, pack, and Markdown diff checks.
- Core smoke: `npm --prefix loom-core run smoke`.
- Playbooks smoke: `npm --prefix loom-playbooks run smoke`.
- Core package check: `npm --prefix loom-core run pack:check`.
- Playbooks package check: `npm --prefix loom-playbooks run pack:check`.
- Avoid root `npm run smoke:*` and `npm run pack:check` until `package.json` is fixed; they currently point at missing `loom-*/open-loom-*.mjs` files.
- For Markdown-only edits, run `git diff --check`.
- After Claude plugin manifest changes, run `claude plugin validate "$PWD/loom-core"` and `claude plugin validate "$PWD/loom-playbooks"`.
- After Gemini manifest or bootstrap changes, run `gemini extensions validate "$PWD"`, `gemini extensions validate "$PWD/loom-core"`, and `gemini extensions validate "$PWD/loom-playbooks"`.

## Editing Checks

- `SKILL.md` frontmatter needs `name` and `description`; Loom record templates use grepable body labels such as `ID:`, `Type:`, `Status:`, `Created:`, and `Updated:`.
- When changing `using-loom` doctrine, keep the ordered references and every preload surface aligned: `loom-core/loom-core.mjs`, `loom-core/hooks/*`, and `loom-core/gemini-bootstrap.md`.
- When changing a Core surface, check the owning `SKILL.md`, `references/`, `templates/`, and docs that restate the model: `README.md`, `PROTOCOL.md`, `ARCHITECTURE.md`, and package READMEs.
- Keep new workflow guidance as movement through existing Core surfaces; do not create a second truth ledger in adapter files, generated context, or helper scripts.
