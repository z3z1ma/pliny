# Installing Loom

Loom is designed for harnesses that support:

- always-on context files
- conditional skill hydration
- filesystem access

Examples include agents that read `AGENTS.md`, `CLAUDE.md`, `OPENCODE.md`, or an equivalent instruction surface.

## Recommended Loading Model

### Always on

Load these in order:

1. `rules/01-core-identity.md`
2. `rules/02-truth-and-authority.md`
3. `rules/03-outer-loop.md`
4. `rules/04-ralph-inner-loop.md`
5. `rules/05-critique-and-wiki.md`
6. `rules/06-filesystem-and-tooling.md`
7. `rules/07-validation-and-honesty.md`
8. the frontmatter `name` and `description` from each `skills/*/SKILL.md`

This repository does not currently ship aggregate `RULES.md` or `SKILLS.md`
files. Harnesses may generate such aggregates locally, but the source of truth
is the ordered `rules/` directory and the skill directories themselves.

`optional-utilities/` is not part of the default protocol install. Those skills
may be copied manually when a local workspace wants them.

### On demand

When a task clearly belongs to one subsystem, hydrate:

- `skills/<skill-name>/SKILL.md`
- the skill's `references/` files as needed
- the relevant template from the skill's `templates/` directory when you need to create or reshape an artifact

## Minimal Harness Wrapper Pattern

A practical wrapper file usually says some version of:

- Loom rules are mandatory when Loom is present in the workspace
- skill names/descriptions are always visible
- full skill content is loaded only when relevant
- the agent must use the Loom owner layer instead of improvising parallel records
- optional commands are convenience routes, not a second source of truth

## Recommended Tool Baseline

Loom does not require any dependency beyond a shell, a text editor, and the agent itself.

Still, these tools make life materially better:

- `rg` / `ripgrep`
- `find` or `fd`
- `git`
- `awk`, `sed`, `sort`, `uniq`, `xargs`
- `jq` and `yq` when available
- inline Python for bulk parsing or one-off transformations that are clearer in Python than in shell

Use them opportunistically.
Do not make Loom depend on them to exist before the protocol makes sense.

## Bootstrapping A Workspace

The fastest manual bootstrap path is:

```bash
mkdir -p \
  .loom/constitution/decisions \
  .loom/constitution/roadmap \
  .loom/initiatives \
  .loom/research \
  .loom/specs \
  .loom/plans \
  .loom/tickets \
  .loom/critique \
  .loom/wiki \
  .loom/packets/ralph \
  .loom/packets/critique \
  .loom/packets/wiki \
  .loom/evidence \
  .loom/memory/system \
  .loom/memory/user
```

Then:

1. create `constitution:main` from `skills/loom-constitution/templates/constitution.md`
2. optionally create `.loom/harness.md` from `skills/loom-workspace/templates/harness.md`
3. create the first initiative, plan, and ticket as the work requires

## How Skills Replace Scripts

Older Loom shipped Python CLIs to do things like:

- scaffold records
- compile packets
- resolve scope
- validate basic structure
- mutate link fields

This Loom package replaces those helpers with:

- Markdown templates
- explicit record grammar
- native query recipes
- validation checklists
- packet contracts written in ordinary Markdown
- permission for the agent to use inline shell or inline Python when useful

That trade is deliberate.
It keeps the protocol portable and makes the durable asset the methodology itself.

## Recommended Consumer Layout

In a real project, many teams place Loom under a harness-specific directory such as:

```text
.opencode/rules/
.opencode/skills/
```

or expose it via a root instruction file that points to the copied package.

Loom itself is agnostic.
The only important thing is that the rules are always on and the skills are discoverable.

## Optional Command Surface

The top-level `commands/` directory contains optional wrapper prompts for
harnesses that support slash-command style entry points.

Those wrappers should route the agent into the same rules and skills. They do
not own behavior independently and they should not become the protocol core.

## OpenCode Plugin

This repository includes the `open-loom` OpenCode plugin at `open-loom.mjs`.
`open-loom` requires OpenCode `>=1.14.22 <2`. After `open-loom` is published,
normal users should configure OpenCode with a package plugin entry:

```json
{
  "plugin": ["open-loom"]
}
```

Users working from a cloned repository should point OpenCode at the local plugin
file instead:

```json
{
  "plugin": ["file:///absolute/path/to/agent-loom/open-loom.mjs"]
}
```

Git URL plugin specs are not recommended for OpenCode. Current validation found
them unsupported in practice, so use npm package distribution or a local
file/path entry.

With OpenCode `1.14.22`, a cold-cache first run of an npm plugin may log
`NpmInstallFailedError` while still installing the package into OpenCode's cache.
If that happens, run OpenCode again; the second run should resolve the cached
package.

`open-loom` reads the bundled top-level `rules/`, `skills/`, and optional
`commands/` surfaces via module-relative file reads. Its server plugin uses
OpenCode's `config(config)` hook to add ordered rule files to
`config.instructions`, add the bundled skill root to `config.skills.paths`, and
register bundled command wrappers through `config.command`.

For a local structural check that does not require a model request, run:

```bash
node open-loom.mjs --smoke
```

See `examples/adapters/open-loom-install/` for the fixture notes and surface
disposition.

## Makefile Installers

This repository also ships a top-level `Makefile` for global user-level installs
from the canonical product surface in the current working tree.

Use:

```bash
make install harness=opencode
make install harness=claude
make install harness=codex
make install harness=gemini
make install harness=cursor
make install harness=all

make uninstall harness=opencode
```

The Makefile copies only top-level `rules/`, protocol `skills/`, and optional
`commands/`. It does not install `optional-utilities/`.

It does not install dogfooding `.loom/` records or `.opencode/` consumption
state.

Because harnesses do not expose identical file formats, the installer keeps
direct copies where possible and uses the smallest honest translation where
needed:

- OpenCode: copies skills and commands, copies rules into a Loom-owned
  directory, and updates `~/.config/opencode/opencode.json` so those rules load
  through `instructions`
- Claude Code: copies rules, skills, and commands into `~/.claude/`
- Codex: copies skills, converts commands into explicit-only command adapter
  skills under `~/.agents/skills/loom-command-*`, removes Loom-managed legacy
  prompt files from `~/.codex/prompts/`, and mirrors Loom rules into a managed
  block inside `~/.codex/AGENTS.md`
- Gemini CLI: copies skills, converts commands into `~/.gemini/commands/*.toml`,
  and mirrors Loom rules into a managed block inside `~/.gemini/GEMINI.md`
- Cursor: copies skills into `~/.cursor/skills/`, converts commands into
  `~/.cursor/commands/*.md`, copies rules into `~/.cursor/loom/rules/`, and
  writes a managed block into Cursor User Rules so the rules are globally
  always on. The managed source block is also written to
  `~/.cursor/loom/cursor-user-rules.md` for inspection.

Generated aggregate instruction blocks are bracketed with Loom markers so
`make uninstall` can remove only Loom-managed content. Generated directories
use Loom-owned names so uninstall can remove them without touching unrelated
harness files.

## Adapter Fixture Expectations

Adapter checks verify transport fidelity. They do not define Loom semantics.

Useful adapter smoke checks:

- rules are installed or mirrored where the harness actually reads always-on instructions
- skill descriptions are discoverable before full skill hydration
- optional command wrappers remain explicit invocation surfaces
- generated command adapters are marked as Loom-managed when the harness needs generated files
- uninstall removes Loom-managed adapter surfaces without touching project `.loom/` truth

See `examples/adapters/` for non-normative adapter fixture expectations.
