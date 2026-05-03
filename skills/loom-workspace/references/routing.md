# Routing

Use these questions to decide the next owner layer or workflow coordinator.

When recording a route field such as `next route:` or `Route:`, use the shared
route-token grammar in `skills/loom-records/references/route-vocabulary.md`.

## Which layer owns the next truth change?

- project identity, principles, constraints -> `loom-constitution`
- strategic outcome framing -> `loom-initiatives`
- evidence synthesis, investigation, option comparison, rejected path, or null result -> `loom-research`
- intended behavior or acceptance contract -> `loom-specs`
- sequencing or rollout strategy -> `loom-plans`
- live execution status or next bounded work item -> `loom-tickets`
- observed artifacts, validation output, screenshots, logs, reproduction, red/green
  results, or scan artifacts -> `loom-evidence`
- adversarial review -> `loom-critique`
- persistent explanation / interlinked knowledge -> `loom-wiki`

## Which workflow or support coordinator should drive the route?

- high-level objective continuation through owner records, ticket tranches,
  Ralph/local execution, evidence, critique, wiki, and reassessment ->
  `loom-drive`
- support-only recall, preferences, retrieval cues, entities, reminders, or hot
  context -> `loom-memory`
- shared grammar, naming, linking, status, or validation conventions -> `loom-records`
- one bounded fresh-context implementation step -> `loom-ralph`, after the ticket
  is Ralph-ready
- implementation isolation, branch/worktree hygiene, or Git provenance -> `loom-git`
- debugging or incident flow -> route token `debugging`, coordinator
  `loom-debugging`
- bounded experiment, prototype, or sketch -> route token `spike`, coordinator
  `loom-spike`
- codebase/module atlas work -> route token `codemap`, coordinator
  `loom-codemap`
- merge, release, PR, or handoff packaging -> route token `ship`, coordinator
  `loom-ship`
- accepted learning assimilation before closure -> `loom-retrospective`
- `acceptance_review` or closure disposition -> `loom-tickets`
- graph repair, broken links, naming, or drift -> `loom-records`
- wiki write or audit mechanics -> `loom-wiki`

## The Constitution First Rule

If the workspace has Loom, read `constitution:main` before making important downstream decisions.

## Quick Sanity Heuristic

If you are about to ask "where should this live?", you are still in workspace/routing territory.

If you are about to ask "what exactly should this record say?", move to the
owning skill.

Do not invoke skills by a vague "maybe relevant" sweep. Pick the owner layer for
the next truth change, then load the skill or workflow coordinator that can move
that truth honestly.

Workflow skills coordinate routes through owner layers. They do not create new
truth layers or outrank the owner records they update.

Commands are optional invocation adapters for these routes. They are not owner
layers or workflow truth owners.
