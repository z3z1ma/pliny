---
name: loom
description: Protocol for project memory and execution discipline. Structures how knowledge, decisions, research, specs, work, evidence, and reviews are captured across sessions and agents.
---

# Loom

Loom is a protocol for project memory and execution discipline. It structures how knowledge, decisions, research, specs, work, evidence, and reviews are captured and used across sessions and agents. Follow it without exception.

## Outer Loop

When intent is unclear, don't implement. Interrogate.

Ask focused questions. Root out ambiguity. Challenge vague terms — especially domain-specific ones that seem overloaded or hand-wavy. Propose concrete scenarios that test the boundaries of what someone actually means. When you think you understand, state your understanding back and let them correct you.

When you have a recommended answer, say so. Give the user something concrete to react to rather than only asking open-ended questions.

Before shaping new work, fish through what already exists. Grep open tickets to understand what's in progress and avoid duplicating effort. Scan knowledge records for shared vocabulary and conventions. Read active decisions for constraints that might already apply. Search research for prior investigations on the topic — if relevant research exists but is old, note the staleness and consider whether it needs updating before relying on it. Check if specs already describe the behavioral surface being discussed. The `.loom/` directory is cumulative. Don't re-derive what the project already knows — build on it.

As things crystallize during conversation, externalize them into the right record shape immediately. A decision made mid-conversation is still a decision. A term of art clarified is still knowledge. A behavior described concretely is a spec. Don't wait for a neat stopping point — write things down as they become clear.

Other tools, skills, or workflows may produce artifacts that overlap with Loom record types. When something lands outside `.loom/` but corresponds to a Loom record type, create the Loom record anyway. It can be thin — some context, headers, and a pointer to the canonical location — but it must exist so the `.loom/` graph remains complete and navigable. The graph is the index; gaps in it are invisible work.

Build a shared glossary. When domain-specific terms, project conventions, or terms of art emerge, capture them as knowledge records. Challenge terms that seem fuzzy or mean different things to different people. This vocabulary accumulates over time and becomes the shared language of the project.

You are in the outer loop whenever scope, behavior, constraints, terminology, or acceptance criteria are not yet concrete enough to execute against.

## Record Shapes

Important context that should outlive the current conversation belongs on disk, split into layers by provenance.

Records live under `.loom/` in directories named by type. Each record is a Markdown file. Terminal statuses get sub-folders; active work stays at the top level.

```
.loom/
  decisions/
    superseded/
  research/
    .storage/
    superseded/
  specs/
    superseded/
  tickets/
    done/
    cancelled/
  evidence/
    .storage/
  reviews/
  knowledge/
```

**Naming convention.** Temporal records — tickets, evidence, reviews, and research — use a date-stamped filename: `YYYY-MM-DD-descriptive-slug.md`. Non-temporal records — decisions, specs, and knowledge — use a descriptive slug only: `descriptive-slug.md`. This makes it immediately visible which records represent a moment in time versus durable ongoing truth.

Every record starts with grepable headers:

```
Status: <status>
Created: YYYY-MM-DD
Updated: YYYY-MM-DD
```

Beyond the headers, write detailed records. These aren't placeholders — they're durable project memory. The more precise and thorough the content, the more useful it is when revisited weeks or months later in a completely different context.

Records reference each other by file path. When you delete or rename a record, repair the references.

### Decisions

Use ADR (Architecture Decision Record) format. A decision captures a durable choice — something hard to reverse, surprising, or involving a real tradeoff.

A decision record should contain at least:

- **Context** — the situation, constraints, and forces that made this decision necessary. Be specific: what was happening, what was unclear, what options existed.
- **Decision** — what was chosen, stated plainly and actively.
- **Alternatives considered** — what else was evaluated, and why each was rejected. This prevents future revisiting of already-settled debates.
- **Consequences** — what this enables, what it restricts, and what tradeoffs were accepted.

Include whatever additional context makes the decision fully understandable to someone encountering it cold — diagrams, code examples, links to discussions, performance data, risk assessments.

Once a decision is accepted, don't modify it. If the decision changes, create a new record that supersedes the old one and move the old one to `superseded/`.

Statuses: `active`, `superseded`

### Research

An investigation record. Use one when the answer took real work to find — multiple sources, tradeoffs evaluated, options rejected, or dead ends encountered — and nobody should have to re-derive it.

A research record should contain at least:

- **Question** — what prompted the investigation. Be precise about what you needed to learn.
- **Sources and methods** — what was consulted, tried, tested, or read. Include versions, dates, and links where relevant.
- **Findings** — what was discovered, including null results and dead ends. Dead ends are valuable — they prevent repeating failed approaches.
- **Conclusions** — the synthesis. What do the findings mean for the project? What should be done or avoided based on this?

Include raw data, benchmarks, code snippets, comparison tables, timelines, or anything else that substantiates the findings. Research is temporal — it can go stale as libraries evolve, APIs change, or the project's context shifts. When reusing old research, verify its conclusions still hold.

Store reference materials — PDFs, papers, exported pages, datasets — in `.loom/research/.storage/` and reference them by file path from the research record.

Statuses: `active`, `done`, `superseded`

### Specs

A behavior contract. Use one when "what should happen" needs to outlive the current conversation — when multiple tickets, sub-agents, or future work need to agree on the same behavioral surface.

A spec record should contain at least:

- **Purpose and scope** — what product surface or behavior this spec covers, and what it explicitly does not cover.
- **Behavior** — what the system should do, described concretely. Prefer scenarios and examples over abstract requirements. Given-when-then or if-then formats are useful when they fit.
- **Acceptance criteria** — how you know the behavior is correctly implemented. Specific, testable, and unambiguous enough that two people would agree on pass/fail.
- **Constraints** — technical, performance, security, or compatibility requirements that bound the implementation without dictating it.

Include interface sketches, state diagrams, data models, edge cases, error handling expectations, or any other detail that makes the intended behavior unambiguous. A spec should be regeneration-grade: clear enough that someone could rebuild the behavior from the spec alone without guessing.

Keep specs focused on one coherent behavioral surface. When a spec covers multiple independent actors, workflows, or interfaces, split it.

Statuses: `draft`, `active`, `superseded`

### Tickets

A bounded unit of work. Use one when the work is non-trivial enough to benefit from explicit scope, progress tracking, and closure discipline.

A ticket record should contain at least:

- **Scope** — what's in and what's not. Be explicit about boundaries.
- **Acceptance criteria** — what "done" looks like, concretely.
- **Progress and notes** — an append-only log of what's been done, tried, learned, and decided during execution. Update as you go.
- **Blockers** — anything preventing forward progress, with enough context to act on.

Include implementation notes, design sketches, links to relevant code, failed approaches, open questions, or anything else that helps someone pick up the work mid-stream.

Statuses: `open`, `active`, `blocked`, `done`, `cancelled`

Additional headers:
```
Parent: <path>
Depends-On: <path>, <path>, …
```

**Parent tickets are plans.** When a change involves multiple independent pieces of work, create a parent ticket that describes the aggregate change, the sequencing of child tickets, what can be parallelized, and what depends on what. Child tickets are the actual executable units. The parent tracks overall progress and coherence across children.

**Tickets are executed by sub-agents.** Point a sub-agent at the ticket and the records it needs — relevant specs, decisions, knowledge, and prior evidence. The sub-agent works within the ticket's scope. The parent agent orchestrates, sequences, and ensures coherence across the broader record graph.

**Open tickets autonomously.** When you notice something out of place, incomplete, broken, or risky during any work — open a ticket for it. Don't hold the observation in your head or leave it as a comment. If it's worth mentioning, it's worth tracking. This applies especially to sub-agents in the inner loop: if you encounter something outside your current ticket's scope that needs attention, create a new ticket for it and keep moving.

**Fish before opening.** Before creating a new ticket, grep through existing tickets — both active and in `done/` — for similar prior work. You might find a ticket that already covers this, or a completed one whose progress notes and evidence inform your approach. Don't duplicate; build on what exists.

### Evidence

A durable observation. Use one when temporal facts — test results, command output, reproduction steps, screenshots, inspected file state — need to survive the session they were produced in.

An evidence record should contain at least:

- **What was observed** — the raw facts. Commands run, output received, files inspected, behavior witnessed. Be precise and timestamped where relevant.
- **Procedure** — how the observation was made, reproducibly if possible.
- **What this supports or challenges** — which ticket, spec, or review this evidence relates to, and what claim it bears on.
- **Limits** — what this evidence does not prove. A passing test does not prove absence of bugs. A single reproduction does not prove frequency. Name the boundaries explicitly.

Include full output logs, screenshots, file diffs, or any raw artifact that substantiates the observation. Evidence doesn't decide anything. It records what happened and is honest about its scope.

Store binary artifacts — screenshots, recordings, exported files, build outputs — in `.loom/evidence/.storage/` and reference them by file path from the evidence record.

Status: `recorded`

Additional headers:
```
Relates-To: <path>, <path>, …
```

### Reviews

Adversarial critique of a change, implementation, or record. Use one when work should be challenged before it's considered solid — when risks need to be surfaced, assumptions tested, or gaps identified.

A review record should contain at least:

- **Target** — what's being reviewed. A diff, a file, a ticket, a spec, a set of changes.
- **Findings** — specific issues, risks, or concerns, each with enough context to act on. Include severity when useful (critical, significant, minor, nitpick).
- **Verdict** — an honest overall assessment: pass, concerns raised, or fail.
- **Residual risk** — what remains uncertain or risky even after the review. What could still go wrong. What was not examined.

Include code snippets, references to specific lines or files, reproduction steps for issues found, or suggested alternatives. Reviews challenge work. They raise concerns, identify gaps, surface risks. They don't close tickets — that's the ticket's job based on the coherence of all its related records.

Status: `recorded`

Additional headers:
```
Target: <path or ref>
Verdict: <pass|concerns|fail>
```

### Knowledge

Reusable context that accumulates over time. The shared vocabulary, conventions, preferences, and how-we-work-here understanding of the project.

Knowledge records cover things like:

- **Glossary terms** — domain-specific language, project jargon, overloaded terms with precise definitions.
- **Conventions and preferences** — coding style decisions, naming patterns, architectural preferences, tooling choices that aren't important enough for a formal decision record but should be consistent.
- **Procedures** — repeatable steps for common tasks: deployment, environment setup, debugging patterns, release processes.
- **Troubleshooting** — known issues, symptoms, fixes, and workarounds.

Include examples, code snippets, links to relevant files, or anything else that makes the knowledge immediately actionable. Keep each knowledge record focused on one topic. If it starts covering unrelated things, split it.

Knowledge is the first place to check when encountering an unfamiliar domain term, project convention, or recurring task.

Status: `active` (delete or update when no longer true)

## Inner Loop

When scope and intent are clear, execute with discipline.

Before starting work on a ticket, read it fully. Read the specs that describe the behavior you're implementing — and related specs for adjacent surfaces that might be affected. Read decisions that constrain your approach. Search for relevant research, especially if the work involves technical choices or integrations where prior investigation might exist. Check knowledge for relevant conventions and procedures. Read prior evidence from earlier attempts at similar work. Understand the landscape before changing it.

Tickets are your unit of work. Don't let them bloat — if a ticket covers multiple independent outcomes, split it. Log progress and notes inside the ticket as you go. Move it through statuses honestly.

Sub-agents produce claims, not truth. The parent agent has the broader execution context to judge where sub-agent output belongs — which ticket to update, what evidence to record, whether findings warrant a review. Sub-agents may update records directly when their scope is clear, but the parent is responsible for coherence across the record graph.

When you encounter something outside your current scope that needs attention — a bug, an inconsistency, a missing test, a violated convention, an incorrect assumption in a spec — open a ticket for it. Don't let observations die in the context window. The project's memory is only as good as what gets written down.

Before closing a ticket, verify coherence. Read the acceptance criteria you set at the start. Check the evidence you collected against those criteria. If reviews were performed, check that their findings are addressed or explicitly accepted as risk. Check that related specs still reflect reality after your changes. Closure means the records agree — not that you feel done.
