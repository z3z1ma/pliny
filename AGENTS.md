# AGENTS.md

## What This Repo Is

This repository develops a distributable Markdown-native Loom bundle.

The protocol core is the top-level `rules/` and `skills/` directories.
Top-level `commands/` files may exist as optional harness-wrapper prompt
surfaces, but they are not part of Loom core and the protocol must make sense
without them.

There is no app runtime, build pipeline, or test suite. The durable asset is
the protocol corpus itself: rules, skills, templates, references, and canonical
examples.

Loom should be treated as a control plane for AI knowledge work: a
source-of-truth type system plus a transaction protocol for bounded
fresh-context mutations. Do not reduce it to "docs for agents" or expand it
into a required runtime.

## Agent Boundary

The agent is the primary operator in a Loom workspace.

This core package ships no Python helper scripts. Record creation, packet
authoring, validation, and graph inspection are taught as visible protocol
behaviors using Markdown guidance, templates, and ordinary file tools.

Ad hoc local automation is acceptable when it is clearly helpful, but it stays
derivative. It must not become the real source of Loom behavior or a hidden
second ontology.

Harnesses, external issue trackers, generated context files, dashboards, MCPs,
and command wrappers may transport or mirror Loom work. They must not own Loom
truth unless a future constitutional record explicitly changes that boundary.

## Repo Structure

### Product source

Everything a user receives lives here:

- `rules/` -- always-on doctrine files
- `skills/` -- self-contained skill directories with `SKILL.md`, references,
  and templates
- `commands/` -- optional harness-wrapper prompt files when this repository
  wants to ship them
- `examples/` -- protocol traces and eval fixtures; useful for review, but not
  a truth owner

**Isolation rule**: content inside `rules/`, `skills/`, and any optional
`commands/` files must stay self-contained, use generic `.loom/...` runtime
paths, and avoid source-repo-only assumptions.

### Dogfooding artifacts

This repo uses its own product. `.opencode/` is a consumption surface for the
bundle. `.loom/` contains Loom records created while using the product on this
repo.

Neither `.opencode/` nor `.loom/` is the source of truth for how the product is
designed. Use `rules/`, `skills/`, and optional top-level wrapper prompts for
that.

## Verification

There is no automated test suite.

Verification is structural and manual. Use the smallest honest checks that fit
the claim being made, such as:

- diff review
- targeted `rg` queries for links, IDs, or status fields
- manual comparison against the owning template or skill reference
- spot-checks of canonical path, scope, and cross-record consistency

## Markdown And Record Guidelines

- Loom records use YAML frontmatter between `---` fences
- required sections, statuses, and naming guidance live in the owning skill's
  templates and references
- `SKILL.md` frontmatter must include `name` and `description`
- optional command-wrapper files are pure Markdown prompt definitions, not code

## Editing Guidance

- prefer the smallest correct change
- keep `rules/`, `skills/`, and optional `commands/` aligned when a change
  crosses their boundaries
- when changing a rule or skill, check related templates, references, and any
  canonical `.loom/` examples that teach the same concept
- do not add hidden runtimes, helper-dependent instructions, or monolithic CLI
  assumptions
- express new workflows as routes through existing owner layers before adding
  new artifact kinds
- keep traceability grep-friendly with stable IDs, typed links, explicit
  coverage, evidence, and critique references
- path-local instruction files may point to Loom owner records, but they must
  not define independent project truth

### Cross-surface review checklist

If a change touches multiple surfaces, verify:

- `rules/` doctrine wording
- `skills/*/SKILL.md` instructions
- `skills/*/references/` docs
- `skills/*/templates/` artifacts
- optional `commands/` wrappers when they cover the same workflow
- `examples/` traces when behavior or workflow routing changes
- canonical `.loom/` examples when they are meant to teach the product

## Key Architecture Facts

- rules are always on
- the layer model is Loom's source-of-truth type system
- Ralph is Loom's transaction protocol for bounded worker mutations
- skills own behavior through `SKILL.md`, references, and templates rather than
  shipped scripts
- tickets are the sole live execution ledger
- packets are bounded execution contracts
- wiki is the persistent explanation layer
- evidence stores proof artifacts without becoming project-truth ownership
- optional wrapper commands remain convenience surfaces, not protocol core

## Current Product Direction

The next phase is protocol sharpening rather than platform expansion. Prioritize:

- product-surface consistency across README, install docs, architecture notes,
  AGENTS guidance, rules, skills, templates, and optional commands
- shared non-ticket status lifecycle grammar
- claim-level coverage across specs, tickets, packets, evidence, and critique
- packet freshness and context-budget guidance
- named critique risk profiles
- codebase atlas, debug, spike, sketch, execution-wave, external-reference,
  ship, retrospective-prevention, and golden-example workflows as routes
  through the existing owner graph

Do not borrow external-system complexity as protocol core. A new workflow is a
good Loom workflow when it makes ownership, evidence, review, and recovery more
regular without creating a second ledger.
