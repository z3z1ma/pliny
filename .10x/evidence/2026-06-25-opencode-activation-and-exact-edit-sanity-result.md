Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-opencode-activation-and-exact-edit-sanity-manual-micro.md

# OpenCode Activation And Exact Edit Sanity Result

## What Was Observed

Ran `EXP-20260625-734-opencode-activation-and-exact-edit-sanity-manual-micro`
with OpenCode against two scenarios:

1. Vague small greenfield app request:

   ```text
   Create a tiny personal packing list app in this folder. Keep it simple.
   ```

2. Exact one-line source edit:

   ```text
   In statusLabel.js, change the label returned for "archived" from "Old" to "Archived". Do only that.
   ```

Raw artifacts are under:

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/211-opencode-activation-and-exact-edit-sanity-manual-micro/`

Accepted clean artifacts:

- `clean-logs/current-greenfield.jsonl`
- `clean-logs/current-exact-edit.jsonl`
- `clean-logs/no-10x-greenfield.jsonl`
- `clean-logs/no-10x-exact-edit.jsonl`
- `clean-workspaces/current-greenfield/`
- `clean-workspaces/current-exact-edit/`
- `clean-workspaces/no-10x-greenfield/`
- `clean-workspaces/no-10x-exact-edit/`

Current-10x greenfield output stayed in the Outer Loop. It stated the request
was ambiguous because implementation would have to invent platform,
persistence, interactions, and verification; it wrote only a blocked shaping
ticket:

`.10x/tickets/2026-06-25-personal-packing-list-app.md`

The current-10x greenfield subject workspace contained no app/source files.

Current-10x exact-edit output changed only the subject `statusLabel.js`:

```javascript
export function labelForStatus(status) {
  if (status === "archived") return "Archived";
  if (status === "active") return "Active";
  return "Unknown";
}
```

No `.10x` records were created for the current-10x exact-edit subject
workspace.

The clean no-10x greenfield control implemented directly, creating:

- `index.html`
- `styles.css`
- `app.js`
- `.playwright-mcp/*` smoke-test artifacts

The corrected clean no-10x exact-edit control changed only its subject
workspace `statusLabel.js`.

## Procedure

OpenCode was invoked non-interactively with:

```text
opencode run --pure --format json --dangerously-skip-permissions <prompt>
```

Clean runs isolated OpenCode config by setting `XDG_CONFIG_HOME` to:

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/211-opencode-activation-and-exact-edit-sanity-manual-micro/clean-config`

For current-10x subjects, `AGENTS.md` was copied from canonical `SKILL.md`
without YAML frontmatter.

The corrected no-10x exact-edit calibration ran with the subject workspace as
the process `cwd`. Earlier attempts using `--dir` alone caused fixture escape
and were discarded.

## What This Supports Or Challenges

This supports the claim that current `SKILL.md` activates in OpenCode for vague
small greenfield app creation and does not treat a small personal app as too
small for 10x. It also supports the claim that current `SKILL.md` preserves
minimal behavior for exact one-line source edits in OpenCode.

The no-10x greenfield control supports contrast: absent 10x, OpenCode readily
implemented the vague greenfield app directly.

## Limits

This is a manual OpenCode MICRO, not an automated Trust Level 1 run. It covers
one vague greenfield app phrasing and one exact edit phrasing in OpenCode only.
It does not prove behavior in Claude Code, oh-my-pi, broader OpenCode models,
multi-turn ratification, or larger implementation tasks.

The manual OpenCode harness itself has a discovered isolation hazard: future
OpenCode cells should use isolated `XDG_CONFIG_HOME` and the subject workspace
as process `cwd`, not rely on `--dir` alone.
