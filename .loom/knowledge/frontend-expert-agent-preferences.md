# Frontend Expert Agent: Usage Preferences

ID: knowledge:frontend-expert-agent-preferences
Type: Knowledge Preference
Status: active
Created: 2026-05-25
Updated: 2026-05-25
Triggers: frontend-expert, subagent, frontend work, svelte, UI, visual, playwright, gemini, agent selection, nudge, continuation
Applies To: loom-mill/frontend/, any frontend/UI work, agent selection for visual tasks

## Preference

**Always prefer `frontend-expert` for frontend and visual work.** It has Playwright MCP tools for browser testing and visual verification, uses `google-vertex/gemini-3.1-pro-preview`, and is purpose-built for Svelte 5 + Tailwind + data visualization tasks.

**Do NOT use `general` for frontend work** unless frontend-expert is completely unavailable. The general agent lacks Playwright and produces lower-quality frontend output (literal `\n` in templates, missing visual verification, no screenshot feedback loops).

## Prompting Pattern

When writing the prompt for frontend-expert, always include an explicit Playwright verification loop instruction. Example:

```
## Verification (REQUIRED)

After implementing, you MUST verify visually:
1. Start the backend: `cd /Users/alexanderbutler/code_projects/personal/agent-loom && source loom-mill/.venv/bin/activate && python -m uvicorn loom_mill.app:app --host 127.0.0.1 --port 8765 &`
2. Start the frontend dev server and note the port
3. Navigate to the frontend with Playwright
4. Take a full-page screenshot
5. Inspect the screenshot for visual issues (overlapping text, wrong spacing, missing elements, raw escape characters, clipped content)
6. If issues are found: fix them and screenshot again
7. Repeat until the screenshot looks correct
8. Include the final screenshot filename in your output
```

This forces the agent into a build → render → inspect → fix loop rather than one-shot code generation. The visual feedback loop is what makes frontend-expert valuable over general.

## Continuation / Nudge Procedure

Gemini (the model behind frontend-expert) sometimes returns empty on first invocation or stalls mid-iteration. When this happens:

1. **Resume the same session** using the returned `task_id` parameter.
2. Send a brief nudge prompt: "Continue. The task is not complete. Read the ticket again and implement it."
3. Do NOT switch to `general` agent as a fallback.
4. If the second nudge also fails, try one more resume. Three empty returns in a row = genuine failure, escalate to operator.

## Why This Matters

- Frontend-expert runs Playwright screenshots as part of verification, catching visual bugs (overlapping text, wrong spacing, literal escape characters) that pass a build check.
- The general agent cannot visually verify its output. It produces code that compiles but may render incorrectly.
- The operator explicitly requested: "Please continue to prefer frontend expert."

## Related

- `.opencode/agents/frontend-expert.md` - agent definition (google-vertex/gemini-3.1-pro-preview)
- `knowledge:general-subagent-for-ralph-runs` - general agent preference for non-frontend Ralph runs
