---
id: research:codex-command-skill-installation
kind: research
status: active
created_at: 2026-04-19T21:59:26Z
updated_at: 2026-04-19T21:59:26Z
scope:
  kind: repository
  repositories:
    - repo:root
links:
  ticket:
    - ticket:p9m4x2qt
  related:
    - research:harness-install-surfaces
---

# Question

How should the Codex installer adapt Loom's top-level `commands/*.md` files now
that Codex workflows should be installed as skills rather than legacy prompt
files?

# Why This Matters

The current installer maps Loom commands into `~/.codex/prompts/*.md`. That
keeps the old command shape alive, but it no longer matches Codex's current
skills-first extension model.

The adaptation must also preserve the original command intent: these surfaces
were user-initiated workflow drivers, not broad implicit behavior triggers.

# Scope

- Codex install and uninstall behavior only
- Loom's existing top-level `commands/*.md` files as source material
- generated user-level skill directories under `~/.agents/skills`
- legacy Loom-managed prompt cleanup under `~/.codex/prompts`

# Method

Read the current OpenAI Codex skills documentation and compare it with the
repository installer implementation, existing command frontmatter, and installed
skill names.

# Sources

- OpenAI Codex skills docs: `https://developers.openai.com/codex/skills`
- OpenAI Codex app commands docs:
  `https://developers.openai.com/codex/app/commands`
- Local installer: `scripts/install-loom.sh`
- Local command corpus: `commands/*.md`
- Local skill corpus: `skills/*/SKILL.md`

# Evidence

- Codex skills are directories with a required `SKILL.md`; optional
  `agents/openai.yaml` can configure interface metadata and invocation policy.
- Codex discovers user skills from `$HOME/.agents/skills`.
- Codex can activate skills explicitly when the user mentions a skill with
  `$skill`; skills can also appear in the slash command list.
- `agents/openai.yaml` supports `policy.allow_implicit_invocation: false`, which
  keeps a skill available for explicit use without matching it implicitly from
  general prompt text.
- Loom commands are explicit workflow drivers with frontmatter fields for
  `name`, `description`, and `arguments`, plus bodies that use `$ARGUMENTS`.
- Two command names collide with existing lower-level skill names:
  `loom-research` and `loom-wiki`. Installing generated command skills under the
  exact command names would overwrite those canonical skills in
  `$HOME/.agents/skills`.

# Conclusions

Codex should not receive Loom commands as `~/.codex/prompts/*.md`.

The safest Codex mapping is to generate separate command adapter skills from
each command file. Those generated skills should use a non-colliding namespace,
for example `loom-command-research`, while retaining interface metadata that
points back to the original `/loom-research` command.

Implicit invocation should be disabled on every generated command adapter skill
because the command layer is meant to be invoked intentionally.

# Recommendations

- Keep copying the canonical lower-level Loom skills into `$HOME/.agents/skills`.
- Generate one additional Codex command adapter skill for each top-level command
  file, using `loom-command-*` names to avoid collisions.
- Add `agents/openai.yaml` to each generated command adapter with
  `allow_implicit_invocation: false`.
- Replace `$ARGUMENTS` in generated skill bodies with a clear invocation-request
  placeholder.
- Remove old Loom-managed prompt files during both install and uninstall so
  previous installs do not leave deprecated Codex prompt entries behind.

# Open Questions

- Whether future Codex UI behavior should display the adapter skill name or the
  original command name more prominently. The current mapping uses the original
  command name in `interface.display_name`.

# Linked Work

- `ticket:p9m4x2qt`
- `research:harness-install-surfaces`
