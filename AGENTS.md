# Guidelines

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

---

# Loom

Read @PROTOCOL.md

We use loom in the development of loom itself.

---

# Repo Specific Context

## Repo Shape

- This repo ships Loom: a Markdown protocol for project memory and execution discipline.
- The protocol lives in `PROTOCOL.md`. Users copy-paste it into their agent instructions.
- `skills/loom/SKILL.md` is a copy of `PROTOCOL.md` with frontmatter for the skills ecosystem (`npx skills add z3z1ma/agent-loom`).
- First-class harness manifests (`.claude-plugin/`, `.cursor-plugin/`, `.agents/plugins/`, `gemini-extension.json`) enable native marketplace install.
- `loom-mill/` is a companion web application for visualizing and interacting with `.loom/` records.
- `.loom/` is this repo's own dogfood workspace — it is not part of the shipped product surface.

## Loom Mill Dev Servers

CRITICAL: When starting Mill dev servers, ALWAYS use nohup with full stdout/stderr
redirection. Never use bare `&` backgrounding — it hangs because the shell waits
for stdout. Never forget to kill servers after verification.

CRITICAL: Before starting ANY server, ALWAYS kill existing processes on that port
first. Multiple subagents may be running in parallel and will fight over ports if
you don't check. Stale processes from prior runs WILL exist.

Start backend (ALWAYS do the kill first):
```bash
lsof -ti:8765 | xargs kill 2>/dev/null; sleep 1
nohup uv run python -m uvicorn loom_mill.app:app --host 127.0.0.1 --port 8765 > /tmp/loom-mill-backend.log 2>&1 < /dev/null &
```
(Run from `loom-mill/` directory)

Start frontend (ALWAYS do the kill first):
```bash
lsof -ti:5173 | xargs kill 2>/dev/null; sleep 1
nohup npm run dev > /tmp/loom-mill-vite.log 2>&1 < /dev/null &
```
(Run from `loom-mill/frontend/` directory)

Kill servers when done:
```bash
lsof -ti:8765 | xargs kill 2>/dev/null; lsof -ti:5173 | xargs kill 2>/dev/null
```

NEVER:
- Use bare `&` without redirecting stdout/stderr (causes shell hang)
- Use `npm run dev &` (hangs — Vite holds stdout open)
- Forget to kill processes after Playwright verification
- Start servers without killing existing port occupants first
- Assume ports are free — ALWAYS kill first, even if you think nothing is running
- Run two subagents that both try to start servers (coordinate or share)

## Editing Checks

- When changing `PROTOCOL.md`, verify the `.loom/` directory structure and existing records still conform.
