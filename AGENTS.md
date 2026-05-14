# AGENTS.md

## Repo Shape

- This repo ships a Markdown skill corpus, not an app runtime. Do not add daemon, database, dashboard, CLI, or helper-script assumptions unless explicitly changing architecture.
- Product behavior lives in `loom-core/skills/` and `loom-playbooks/skills/`; package entrypoints, manifests, hooks, and extensions only expose those trees.
- Model-visible Loom doctrine lives only in the shipped skill directories: `loom-core/skills/` and `loom-playbooks/skills/`. `README.md`, `PROTOCOL.md`, `ARCHITECTURE.md`, package READMEs, manifests, and adapter docs are not in the consuming model's context window unless a harness explicitly injects them, which Loom must not assume.
- Do not rely on README or protocol prose to teach model behavior. If models need to follow a rule, encode it in the relevant skill `SKILL.md`, `references/`, or `templates/` under the package skill directories; keep docs as human-facing restatements only.
- Treat product-surface leakage as one of this repo's worst failure modes. Shipped skill content must not explain Agent Loom's packaging, adapter mechanics, smoke checks, repository workflow, dogfood state, skill-authoring preferences, or self-justifications. That material belongs in docs, AGENTS.md, `.loom/` records, tests, or package code, not in model-visible product doctrine.
- Do not confuse instructions for Loom contributors with instructions for Loom consumers. `loom-core/skills/` and `loom-playbooks/skills/` are distributed product surfaces; write them as runtime behavior for an installed workspace, not commentary about how this repo develops, validates, packages, or exposes that behavior.
- `loom-core/` is required and owns `using-loom`, Core record skills, templates, and references.
- `loom-playbooks/` is optional, requires Core, and must not duplicate or preload `using-loom` doctrine.
- Root `skills` is a symlink to `loom-core/skills` for the repo-root Gemini extension shim; treat `loom-core/skills/` as the real Core package surface.
- Package skill content must be self-contained for installed workspaces: use generic `.loom/...` runtime paths, not source-repo-only paths or dogfood assumptions.

## Dogfooding

- `.loom/` is this repo's dogfood workspace state for future Agent Loom development; it is not part of the shipped product surface.
- Use `.loom/` records to coordinate work on this repo, but keep model-visible behavior in `loom-core/skills/` and `loom-playbooks/skills/`. Package entrypoints, manifests, hooks, and docs may expose, preload, or restate skills; they must not become a second source of model doctrine.
- Raw evidence and research artifacts under `.loom/*/artifacts/` stay ignored except scaffold `.gitkeep` files.

## Entrypoints And Adapters

- OpenCode entrypoints are `loom-core/loom-core.mjs` and `loom-playbooks/loom-playbooks.mjs`.
- Core OpenCode config exposes `loom-core/skills` through `config.skills.paths` and injects stripped `using-loom` doctrine plus ordered references into the first user message through `experimental.chat.messages.transform`.
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
- For Markdown-only edits, run `git diff --check`.
- After Claude plugin manifest changes, run `claude plugin validate "$PWD/loom-core"` and `claude plugin validate "$PWD/loom-playbooks"`.
- After Gemini manifest or bootstrap changes, run `gemini extensions validate "$PWD"`, `gemini extensions validate "$PWD/loom-core"`, and `gemini extensions validate "$PWD/loom-playbooks"`.

## Editing Checks

- `SKILL.md` frontmatter needs `name` and `description`; Loom record templates use grepable body labels such as `ID:`, `Type:`, `Status:`, `Created:`, and `Updated:`.
- When changing `using-loom` doctrine, keep the ordered references and every preload surface aligned: `loom-core/loom-core.mjs`, `loom-core/hooks/*`, and `loom-core/gemini-bootstrap.md`.
- When changing a Core surface, check the owning `SKILL.md`, `references/`, `templates/`, and docs that restate the model: `README.md`, `PROTOCOL.md`, `ARCHITECTURE.md`, and package READMEs.
- Before shipping changes under `loom-core/skills/` or `loom-playbooks/skills/`, scan for leaked contributor-facing concepts such as package smoke, adapter mechanics, test harness details, repo paths, dogfood assumptions, skill-description policy, npm packaging, or why Loom is built this way. Remove or move that material unless it is directly needed by a consuming agent at runtime.
- Keep new workflow guidance as movement through existing Core surfaces; do not create a second truth ledger in adapter files, generated context, or helper scripts.
