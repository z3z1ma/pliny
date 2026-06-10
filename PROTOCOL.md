# Loom

## Outer Loop

When intent is unclear, don't implement. Interrogate.

Ask focused questions. Root out ambiguity. Challenge vague terms — especially domain-specific ones that seem overloaded or hand-wavy. Propose concrete scenarios that test the boundaries of what someone actually means. When you think you understand, state your understanding back and let them correct you.

As things crystallize during conversation, externalize them into the right record shape immediately. A decision made mid-conversation is still a decision. A term of art clarified is still knowledge. A behavior described concretely is a spec. Don't wait for a neat stopping point — write things down as they become clear.

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
    superseded/
  specs/
    superseded/
  tickets/
    done/
    cancelled/
  evidence/
  reviews/
  knowledge/
```

Every record starts with grepable headers:

```
Status: <status>
Created: YYYY-MM-DD
Updated: YYYY-MM-DD
```

Records reference each other by file path. When you delete or rename a record, repair the references.

### Decisions

Use ADR (Architecture Decision Record) format. A decision captures a durable choice — something hard to reverse, surprising, or involving a real tradeoff.

A decision record should contain:

- **Context** — the situation, constraints, and forces that made this decision necessary. Be specific: what was happening, what was unclear, what options existed.
- **Decision** — what was chosen, stated plainly and actively.
- **Alternatives considered** — what else was evaluated, and why each was rejected. This prevents future revisiting of already-settled debates.
- **Consequences** — what this enables, what it restricts, and what tradeoffs were accepted.

Once a decision is accepted, don't modify it. If the decision changes, create a new record that supersedes the old one and move the old one to `superseded/`.

Statuses: `active`, `superseded`

### Research

An investigation record. Use one when the answer took real work to find — multiple sources, tradeoffs evaluated, options rejected, or dead ends encountered — and nobody should have to re-derive it.

A research record should contain:

- **Question** — what prompted the investigation. Be precise about what you needed to learn.
- **Sources and methods** — what was consulted, tried, tested, or read. Include versions, dates, and links where relevant.
- **Findings** — what was discovered, including null results and dead ends. Dead ends are valuable — they prevent future agents from repeating failed approaches.
- **Conclusions** — the synthesis. What do the findings mean for the project? What should be done or avoided based on this?

Statuses: `active`, `done`, `superseded`

### Specs

A behavior contract. Use one when "what should happen" needs to outlive the current conversation — when multiple tickets, sub-agents, or future work need to agree on the same behavioral surface.

A spec record should contain:

- **Purpose and scope** — what product surface or behavior this spec covers, and what it explicitly does not cover.
- **Behavior** — what the system should do, described concretely. Prefer scenarios and examples over abstract requirements. Given-when-then or if-then formats are useful when they fit.
- **Acceptance criteria** — how you know the behavior is correctly implemented. Specific, testable, and unambiguous enough that two people would agree on pass/fail.
- **Constraints** — technical, performance, security, or compatibility requirements that bound the implementation without dictating it.

Keep specs focused on one coherent behavioral surface. When a spec covers multiple independent actors, workflows, or interfaces, split it. A spec should be regeneration-grade: clear enough that someone could rebuild the behavior from the spec alone.

Statuses: `draft`, `active`, `superseded`

### Tickets

A bounded unit of work. Use one when the work is non-trivial enough to benefit from explicit scope, progress tracking, and closure discipline.

A ticket record should contain:

- **Scope** — what's in and what's not. Be explicit about boundaries.
- **Acceptance criteria** — what "done" looks like, concretely.
- **Progress and notes** — an append-only log of what's been done, tried, learned, and decided during execution. Update as you go.
- **Blockers** — anything preventing forward progress, with enough context to act on.

Parent tickets decompose into child tickets. This is how you plan. A parent ticket with children is the plan; no separate planning artifact is needed.

Keep tickets focused — one coherent outcome per ticket. If a ticket covers multiple independent outcomes, split it. A ticket should carry enough context that someone encountering it cold can understand the work without the conversation that created it.

Statuses: `open`, `active`, `blocked`, `done`, `cancelled`

Additional headers:
```
Parent: <path>
Depends-On: <path>, <path>, …
```

### Evidence

A durable observation. Use one when temporal facts — test results, command output, reproduction steps, screenshots, inspected file state — need to survive the session they were produced in.

An evidence record should contain:

- **What was observed** — the raw facts. Commands run, output received, files inspected, behavior witnessed. Be precise and timestamped where relevant.
- **Procedure** — how the observation was made, reproducibly if possible.
- **What this supports or challenges** — which ticket, spec, or review this evidence relates to, and what claim it bears on.
- **Limits** — what this evidence does not prove. A passing test does not prove absence of bugs. A single reproduction does not prove frequency. Name the boundaries explicitly.

Evidence doesn't decide anything. It records what happened and is honest about its scope.

Status: `recorded`

Additional headers:
```
Relates-To: <path>, <path>, …
```

### Reviews

Adversarial critique of a change, implementation, or record. Use one when work should be challenged before it's considered solid — when risks need to be surfaced, assumptions tested, or gaps identified.

A review record should contain:

- **Target** — what's being reviewed. A diff, a file, a ticket, a spec, a set of changes.
- **Findings** — specific issues, risks, or concerns, each with enough context to act on. Include severity when useful (critical, significant, minor, nitpick).
- **Verdict** — an honest overall assessment: pass, concerns raised, or fail.
- **Residual risk** — what remains uncertain or risky even after the review. What could still go wrong. What was not examined.

Reviews challenge work. They raise concerns, identify gaps, surface risks. They don't close tickets — that's the ticket's job based on the coherence of all its related records.

Status: `recorded`

Additional headers:
```
Target: <path or ref>
Verdict: <pass|concerns|fail>
```

### Knowledge

Reusable context that accumulates over time. The shared vocabulary, conventions, preferences, and how-we-work-here understanding of the project.

Knowledge records cover:

- **Glossary terms** — domain-specific language, project jargon, overloaded terms with precise definitions.
- **Conventions and preferences** — coding style decisions, naming patterns, architectural preferences, tooling choices that aren't important enough for a formal decision record but should be consistent.
- **Procedures** — repeatable steps for common tasks: deployment, environment setup, debugging patterns, release processes.
- **Troubleshooting** — known issues, symptoms, fixes, and workarounds.

Keep each knowledge record focused on one topic. If it starts covering unrelated things, split it. Knowledge should be the first place you check when encountering a domain term, project convention, or recurring task.

Status: `active` (delete or update when no longer true)

## Inner Loop

When scope and intent are clear, execute with discipline.

Tickets are your unit of work. Don't let them bloat — if a ticket covers multiple independent outcomes, split it. Log progress and notes inside the ticket as you go. Move it through statuses honestly.

Sub-agents produce claims, not truth. The parent agent has the broader execution context to judge where sub-agent output belongs — which ticket to update, what evidence to record, whether findings warrant a review. Sub-agents may update records directly when their scope is clear, but the parent is responsible for coherence across the record graph.

Closing a ticket means the records agree. The ticket's acceptance criteria, the evidence collected, any reviews performed, the relevant specs and decisions — they should tell one coherent story. If they don't, the work isn't done. Say what's missing instead of pretending coherence exists.
