# Skill Routing And Pressure Testing

Use this reference when adapting peer skill systems, deciding whether a workflow
deserves its own Loom playbook, or testing skill prose against real agent shortcuts.

## Routing From Peer Skills

Peer skill systems often encode useful engineering discipline but use different
truth owners, command wrappers, hooks, issue trackers, or runtime state. Preserve
the discipline; translate the truth boundary.

Classify each source skill as:

- new playbook when it has recurring triggers, distinct procedure, evidence posture,
  and no existing Loom playbook covers it well
- existing playbook deepening when the procedure strengthens an existing route
- core owner routing when the source really describes specs, plans, tickets,
  evidence, critique, wiki, constitution, research, memory, or Ralph
- rejected runtime surface when it depends on peer-specific commands, hooks,
  `.superpowers`, issue labels, hidden state, or mandatory external tools

## Activation Descriptions

Descriptions are for discovery. They should name triggering situations and avoid
summarizing the whole workflow in a way an agent might follow without reading the
skill body.

Good description traits:

- starts from user/task language
- includes common synonyms and pressure points
- states owner boundary when overlap is likely
- avoids process shortcuts that replace reading the skill

## One Owner Boundary

A Loom playbook coordinates; it does not own new project truth. When authoring,
name explicitly:

- what this workflow coordinates
- what it does not own
- which core owner layers receive durable output
- when to use another playbook instead
- which runtime or peer surfaces are evidence/transport only

## Pressure-Scenario Testing

Use pressure scenarios when the skill asks agents to do something costly under
pressure, such as TDD, verification, critique, security review, scope restraint, or
no hidden runtime assumptions.

Pressure scenarios should include:

- concrete task and stakes
- at least one tempting shortcut
- specific choices or required action
- expected correct route
- rationalization the scenario is designed to catch

Examples of pressures:

- time pressure or end-of-day fatigue
- sunk cost after implementation already happened
- authority pressure from a reviewer or user
- economic or release pressure
- social pressure to agree rather than push back
- pragmatic pressure to skip tests or verification

## RED/GREEN/REFACTOR For Skills

RED: identify the shortcut the old or missing skill would allow. If proportional,
run or describe a scenario where an agent would likely fail.

GREEN: edit the smallest skill surface that makes the correct route obvious.

REFACTOR: remove duplicate wording, over-broad triggers, hidden runtimes, and new
owner ambiguity introduced by the fix.

Preserve scenario evidence or critique when the ticket needs durable support. Do
not invent a hidden test harness as Loom product behavior.

## Peer Runtime Translation

Translate peer mechanics this way:

- peer plan directories -> Loom plans/tickets/packets as owners require
- peer review templates -> critique records or code-review playbook guidance
- peer worktree scripts -> `loom-git` worktree discipline
- peer skill loader rules -> using-Loom doctrine or skill-authoring guidance
- peer docs/ideas directories -> product discovery, research, specs, plans, tickets, wiki
- peer hooks/MCPs/tools -> optional transport or evidence, never required Loom truth

## Red Flags

- a new skill creates a new canonical record layer
- activation overlaps another skill without exclusion guidance
- peer command requirements are imported as mandatory Loom runtime
- examples preserve peer storage paths as truth
- verification says only that the prose sounds good
- rationalization tables are generic and do not target actual shortcuts

## Verification

- source skills are mapped to new, deepen, core-route, or rejected categories
- every new playbook states owner routing and non-ownership
- activation descriptions are trigger-rich but not workflow shortcuts
- pressure scenarios exist for behavior-changing or discipline-enforcing guidance
- structural checks confirm frontmatter, references, placeholders, and rejected paths
