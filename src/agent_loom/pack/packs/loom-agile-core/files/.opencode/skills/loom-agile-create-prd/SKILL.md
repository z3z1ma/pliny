---
name: loom-agile-create-prd
description: Create a PRD with scope, requirements, and acceptance criteria.
license: MIT
compatibility: opencode
---

## Mindset
You are a facilitator. Do not invent requirements.

## Outcomes
- A PRD that is clear enough to plan and build
- Requirements separated from implementation
- Acceptance criteria that are testable
- Open questions captured explicitly

## Inputs to gather (ask only if missing)
- What is the user trying to achieve?
- Who is it for?
- What does success look like (measurable)?
- Constraints (time, platform, compliance, integrations)
- Brownfield vs greenfield context

## Procedure
1) Anchor in Loom
   - `loom ticket show <id>`
   - `loom ticket update <id> --status in_progress`

2) Discover existing context (lightweight)
   - Ask the user what docs exist (briefs, prior PRDs, architecture notes).
   - If repo has a `docs/` folder or existing specs, skim the most relevant pieces.
   - If this is a brownfield project, ask what is changing vs staying the same.

3) Define the problem and goals
   - Problem statement
   - Target users
   - Goals and success metrics (numbers if possible)
   - Non-goals

4) Scope and constraints
   - In scope
   - Out of scope
   - Constraints and assumptions
   - Risks / unknowns

5) User journeys (narrative, not bullet soup)
   - Map all user types that touch the system (not only the primary user): admins, support, moderators, API consumers, internal operators.
   - For each key user type:
     - Opening situation
     - Trigger to act
     - Steps
     - Failure and recovery
     - Outcome
   - Finish with a short "journey -> capability" summary.

6) Requirements
   - Functional requirements: numbered, unambiguous statements.
   - Non-functional requirements: security, privacy, reliability, performance, UX/accessibility, observability.

7) Acceptance criteria
   - For each major requirement/journey, add testable acceptance criteria.
   - Avoid implementation details (tech choices) unless the constraint requires it.

8) Open questions
   - List questions that block implementation or planning.
   - If the user can answer quickly, ask now; otherwise park them.

9) Persist
   - If the PRD is long, store it in a repo file and link it from the ticket.
   - Always add a ticket note with:
     - where the PRD lives
     - what is still unknown
     - recommended next command (often `/loom-agile-create-epics-and-stories` or `/loom-agile-create-architecture`).
