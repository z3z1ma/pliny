# Mill Project Scaffold

ID: ticket:20260525-mill-project-scaffold
Type: Ticket
Status: closed
Created: 2026-05-25
Updated: 2026-05-25
Risk: low - greenfield scaffolding with known tools, no production behavior yet.

## Summary

Create the `loom-mill/` directory structure with a Python/Starlette backend and Svelte 5/Tailwind frontend. Dev server runs both with hot reload. No business logic. This is the horizontal prerequisite that unblocks all other Factory Floor tickets.

## Related Records

- `plan:20260525-factory-floor-mvp` - parent plan, Unit 1.
- `spec:loom-mill-factory-floor-mvp` - behavior contract; this ticket only scaffolds, does not implement requirements yet.

## Scope

Read scope:
- `spec:loom-mill-factory-floor-mvp` RD-003, RD-004, RD-005 for stack decisions.
- Existing `loom-core/package.json` and `loom-playbooks/package.json` for monorepo conventions.

Write scope:
- `loom-mill/` directory and all scaffolding files within it.
- Root `package.json` if a workspace script is useful.
- `.gitignore` additions for `.mill/`, Python venv, node_modules, build artifacts.

Non-goals:
- No record parser, watcher, workstation engine, or business logic.
- No Tauri config yet (plain web dev server is sufficient).
- No CI/CD or deployment configuration.
- No database, ORM, or migration system.

Stop conditions:
- Stop if a dependency conflict between Starlette and watchfiles or Svelte and Tailwind requires research.
- Stop if the AGENTS.md constraint about "not an app runtime" needs explicit operator override beyond this ticket.

## Acceptance

- ACC-001: `loom-mill/` exists with a Python package structure (`pyproject.toml`, `src/loom_mill/`, async Starlette app entry).
  Evidence: `ls` output showing structure; `pip install -e loom-mill` or `uv pip install -e loom-mill` succeeds.

- ACC-002: Frontend exists at `loom-mill/frontend/` with Svelte 5, Tailwind CSS, Vite config, and an app shell component.
  Evidence: `npm run dev` (or equivalent) starts Vite dev server and renders an empty dashboard shell.

- ACC-003: A dev command starts both backend and frontend with hot reload.
  Evidence: a single command (or documented two-terminal setup) runs the full dev stack.

- ACC-004: `.gitignore` covers `.mill/`, `__pycache__`, `.venv`, `node_modules`, and build output.
  Evidence: `git status` after build shows no untracked generated artifacts.

## Current State

Complete. All acceptance criteria satisfied. Frontend builds, backend imports clean, health endpoint responds, gitignore covers generated artifacts.

## Journal

- 2026-05-25: Created from `plan:20260525-factory-floor-mvp` Unit 1.
- 2026-05-25: Ralph worker run via `general` subagent completed. Frontend (Svelte 5 + Tailwind + Vite) and backend (Starlette + uvicorn) scaffolded. Verified: npm build passes, pip install succeeds, app imports clean.
