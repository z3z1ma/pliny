<p align="center">
  <img src="assets/banner.png" alt="10x banner">
</p>

<h1 align="center">10x</h1>

<p align="center">
  <em>An opinionated instruction set that makes AI coding agents clarify, remember, verify, and improve across sessions.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/z3z1ma/10x?style=flat-square&color=111111&label=stars" alt="Stars">
  <img src="https://img.shields.io/github/v/release/z3z1ma/10x?style=flat-square&color=111111&label=release" alt="Release">
  <img src="https://img.shields.io/badge/Skills%20CLI-70%2B%20agents-111111?style=flat-square" alt="Skills CLI supports 70+ agents">
  <img src="https://img.shields.io/badge/plain-Markdown-111111?style=flat-square" alt="Plain Markdown">
  <img src="https://img.shields.io/badge/license-MIT-111111?style=flat-square" alt="MIT license">
</p>

---

10x is a drop-in Markdown instruction set for AI coding agents.

It is one self-contained file: [`SKILL.md`](SKILL.md). Load it into Codex,
OpenCode, Claude Code, Cursor, Gemini CLI, or any harness that reads project
instructions. It teaches the agent to:

- challenge vague work before coding;
- preserve repo-local context in `.10x/`;
- split discovery from execution;
- prove changes with evidence and review;
- turn mistakes, dead ends, and repeated friction into reusable knowledge.

Try it in 60 seconds, either way:

**Skills CLI**

```bash
npx skills add z3z1ma/10x
```

**Copy-paste**

Open [`SKILL.md`](SKILL.md) and append everything after the YAML frontmatter to
whatever instruction file your agent already reads.

Both paths are first-class. The [Vercel Skills CLI](https://github.com/vercel-labs/skills)
handles placement across 70+ agent harnesses; copy-paste is maximally flexible
because the product surface is still just Markdown: one `SKILL.md`, plain
English, easy to inspect, fork, edit, splice, or paste. No runtime, no service,
no database.

[Read the full instructions](SKILL.md) | [Install](#installing) | [How it is tested](#how-it-is-tested)

## Why this exists

You've worked with a 10x developer. They are not 10x because they type faster.
They are 10x because they eliminate entire classes of problems, write less code,
record why decisions were made, and leave the next engineer further ahead than
they started.

Most AI coding agents live at the opposite end of that spectrum. They are strong
at local implementation, but weak at durable judgment: carrying context across
sessions, challenging vague requirements, proving that "done" means done, and
remembering what they learned after the chat closes.

10x gives the agent a working method. It searches existing context before asking
you to repeat yourself, pushes back when a request would require invented
semantics, breaks work into bounded tickets, captures observed evidence instead
of vibes, and runs a retrospective so the next session inherits the lesson.

Thursday's agent uses Tuesday's judgment because Tuesday's agent worked
carefully enough to leave a trail.

This is my personal instruction set - the base instructions I load into every
coding harness I use. It is opinionated, plain-text, and portable.

## What still gets lost

Maybe your workflow already has good parts: plan mode, spec files, custom
skills, subagents reviewing subagents. The pieces still often operate like a
ticket machine - accepting work at face value, executing in isolation, and
declaring victory without verification.

| You already use | What still goes wrong |
| --- | --- |
| Plan mode | Reasoning disappears with the session |
| `PLAN.md` or spec files | Plans rarely link to evidence, reviews, or later decisions |
| Subagents | Intermediate reasoning, checkpoints, and validation vanish into a final reply |
| Custom skills | They use different state and vocabulary from each other |
| "Think before coding" prompts | The agent still guesses when requirements are vague |
| Chat history | Important conclusions stay implicit, private, or impossible to grep |

The gap is not tooling. It is judgment. 10x gives those failures an explicit
place to be caught and turns the prevention mechanism into durable project
context.

## How it works

10x separates understanding from execution.

In the outer loop, the agent clarifies the work. It reads records and source
before asking questions, challenges ambiguous language, records durable
decisions, and writes specifications only when behavior is clear enough to be
tested.

In the inner loop, the agent executes one bounded ticket. It changes only the
owned surface, gathers evidence, treats subagent reports as claims until verified,
reviews the result, and refuses to close work until acceptance criteria match
observed facts.

At closure, the agent runs a retrospective. Reusable facts become knowledge,
repeatable procedures become skills, unresolved work gets its own ticket, and
the repo becomes easier for the next human or agent to reason about.

```mermaid
flowchart TB
  Goal["human goal"]
  Goal --> Outer["outer loop: clarify, specify, record"]
  Outer --> Tickets["bounded tickets"]
  Tickets --> Inner["inner loop: execute, prove, review"]
  Inner -->|"done + retro"| Knowledge["knowledge compounds"]
  Inner -->|"new ambiguity"| Outer
```

Concrete example:

```text
User: Add notifications for failed imports.

Without 10x: starts wiring a notification path.

With 10x: checks existing records, notices recipients, retry behavior,
escalation, and operational ownership are undefined, recommends the smallest
contract, and asks for the one decision that changes implementation.
```

## What accumulates

When an agent works this way, your repo grows a `.10x/` directory - the same
kind of engineering context a careful senior engineer naturally leaves behind:

```text
.10x/
|-- decisions/   # the why: choices with alternatives and rationale
|-- research/    # investigations, dead ends, things nobody should retry
|-- tickets/     # bounded work with scope, criteria, progress, blockers
|-- evidence/    # what actually happened: test output, diffs, screenshots
|-- specs/       # behavioral contracts precise enough to verify against
|-- reviews/     # adversarial critique before work is trusted
|-- knowledge/   # vocabulary, conventions, heuristics, reusable context
`-- skills/      # hardened procedures the agent can reuse next time
```

Records reference each other by file path: a ticket cites its spec, evidence
cites its ticket, a decision points to the research that informed it. Plain
Markdown. Versioned by git. Greppable. Diffable. Reviewable in a PR.

The records are intentionally richer than a thin ADR. A useful 10x record
captures not just the decision, but the authority behind it, the evidence that
supports it, the limits that still matter, and the next work it enables:

```markdown
Status: active
Created: 2026-06-12
Updated: 2026-06-12
Relates-To: .10x/research/2026-06-10-auth-options.md, .10x/specs/mobile-auth.md

# Use Refresh Tokens For Mobile Auth

## Context

API authentication must support browser and mobile clients. Browser-only session
cookies would simplify the web flow, but mobile clients need a first-class
reauthentication path that does not depend on cookie behavior.

Current source has email/password login and access-token middleware, but no
refresh-token persistence, rotation, revocation list, or device session model.

## Decision

Use short-lived JWT access tokens plus rotating refresh tokens stored per device
session. Refresh tokens are invalidated on rotation, logout, password reset, and
explicit account revocation.

## Authority And Provenance

- User ratified mobile support as in scope on 2026-06-12.
- `.10x/research/2026-06-10-auth-options.md` compared session cookies, opaque
  bearer tokens, and JWT plus refresh tokens.
- `src/auth/middleware.ts` proves current access-token validation exists but
  does not prove refresh lifecycle behavior.

## Alternatives Considered

- Session cookies: simpler browser implementation, rejected because mobile
  support would require a parallel auth path.
- Opaque bearer tokens: easier revocation, rejected because the current API
  gateway already validates JWT claims locally.

## Consequences

- Requires refresh-token storage, rotation, replay detection, and revocation.
- Login, logout, password reset, and account disable flows all need lifecycle
  tests.
- Token lifetime remains unratified and is blocked from implementation until
  `.10x/tickets/2026-06-12-ratify-token-lifetimes.md` closes.

## Evidence And Limits

- Source inspection observed JWT middleware only; no refresh-token table exists.
- Research did not evaluate enterprise SSO. That remains explicitly out of
  scope for this decision.
```

The point is not paperwork. The point is that the next agent knows what is
settled, who authorized it, what source proves, what source does not prove, and
which unresolved semantics still block execution.

## Before and after

**Without 10x:** Monday morning. New session. "We decided on JWT with refresh
tokens last week, remember?" It does not. You spend fifteen minutes digging
through old chat history, chasing a decision that was already settled. Then the
agent implements before clarifying two ambiguous requirements. You catch it
three files deep. Start over.

**With 10x:** Monday morning. New session. The agent reads the decision record,
follows the link to the research, picks up the open question about rotation
intervals, and asks about that specific decision with a recommendation and
tradeoffs. One answer and real work starts.

## How it is tested

This repo includes [`autoresearch/`](autoresearch/), the experimental harness
used to improve 10x itself.

The loop is intentionally simple: an LLM researcher forms a hypothesis, writes
or selects a candidate instruction, runs live subject-agent trials, inspects raw
transcripts and archived workspaces, scores the result against a rubric, and
records the verdict in `.10x/`.

That matters because instructions are software. A prompt change can improve one
behavior while quietly weakening another. Autoresearch makes those changes
observable: current skill vs candidate, clean seed workspaces, raw transcripts,
archived artifacts, manual scientific judgment, and durable evidence records.

That makes the experiments do two jobs:

- compare current `SKILL.md` against candidate improvements;
- preserve a regression/evaluation suite showing whether the current skill still
  handles the scenarios it was shaped to handle.

It is not a leaderboard, hidden canned grader, or benchmark daemon. It is the
lab notebook behind the instruction set: live Codex/OpenCode trials, seed
workspaces, raw artifacts, reports, reviews, and promotion evidence. One recent
instruction change, for example, was promoted after a 50-sample
current-vs-candidate batch recorded in
[`.10x/evidence/2026-06-28-record-richness-hypothesis-batch.md`](.10x/evidence/2026-06-28-record-richness-hypothesis-batch.md).

## Enhance your current workflow

10x does not replace your tools. It gives them a project context layer: typed
authority, provenance, lifecycle state, evidence, review, and follow-up
ownership that other workflows can stand on.

| Your workflow | What 10x adds |
| --- | --- |
| Plan mode | Useful reasoning becomes durable context instead of disappearing with the session. |
| `PLAN.md` or spec files | Plans link to decisions, evidence, reviews, blockers, and later supersession. |
| Spec-driven development | Specs gain authority/provenance and executable tickets inherit only ratified behavior. |
| Subagents | Handoffs are typed records; final reports remain claims until checked against evidence. |
| Superpowers or skill packs | Keep the execution discipline; 10x adds the context and authority substrate underneath it. |
| Custom skills | Skills share project vocabulary, source identity, exposure paths, and retrospective learning. |
| External issue trackers | Delivery state can stay external while 10x preserves local reasoning context and evidence. |

## Installing

10x is just instructions. Use whichever first-class path fits how you work:
the [Vercel Skills CLI](https://github.com/vercel-labs/skills) for automatic
placement across 70+ agent harnesses, or direct copy-paste for exact control.

### Skills CLI

```bash
npx skills add z3z1ma/10x
```

Examples:

```bash
# Install globally
npx skills add z3z1ma/10x -g

# Target specific agents
npx skills add z3z1ma/10x -a claude-code -a opencode

# Non-interactive
npx skills add z3z1ma/10x -g -a claude-code -y
```

This path requires Node/npm because it uses `npx`. It does not make 10x a cloud
service or runtime dependency; it just installs a Markdown skill where your
agent can read it.

### Copy-paste into instructions

Append the body of [`SKILL.md`](SKILL.md) to the file your agent reads at
startup. This path is first-class and maximally flexible. For instruction-file
installs, omit the YAML frontmatter at the top of `SKILL.md`; the body is the
portable instruction text.

| Harness | Common instruction file |
| --- | --- |
| Codex | `AGENTS.md` |
| OpenCode | `AGENTS.md` |
| Claude Code | `CLAUDE.md` |
| Cursor | `.cursor/rules/10x.md` or project rules |
| Gemini CLI | `GEMINI.md` |
| Other agents | Whatever project instruction file the harness reads |

### Manual skill-directory variant

If your harness reads skill directories, you can also install the same Markdown
file by cloning the repo into that directory. Keep `SKILL.md` intact, including
the YAML frontmatter:

```bash
# Example for OpenCode
git clone https://github.com/z3z1ma/10x .opencode/skills/10x

# Example for Claude Code
git clone https://github.com/z3z1ma/10x .claude/skills/10x
```

## When to use it

Once installed, 10x is always active. Small work should get smaller behavior:
fewer sharper questions, the simplest mechanical workflow, and no durable
records when the change is genuinely trivial and fully specified. A typo fix
can stay a typo fix.

Do not confuse that with opting out for vague greenfield work. Creating a new
app, workflow, data store, API, UI surface, persistence behavior, or other
testable product behavior is non-trivial even when it sounds small, personal, or
likely to fit in one file. The right move is a lightweight outer loop: inspect
the workspace, recommend the smallest simple shape, and confirm the
execution-critical contract before implementation.

The honest tradeoff: the skill is about 5,400 words of instruction, and the
agent spends tokens on deliberation and record-keeping. For complex
multi-session work, that pays for itself quickly: fewer rework cycles, fewer
re-explanations, fewer "wait, didn't we already decide this?" moments. For exact
one-shot edits, the protocol should disappear into disciplined minimalism. For
ambiguous one-shot builds, it should prevent wrong-premise code.

## FAQ

**Does 10x replace Superpowers or other skill packs?**

No. Those often govern how the agent writes code or apply process pressure. 10x
governs how the agent reasons from project context: what kind of truth this is,
what authorized it, what could change implementation, and what would prove the
outcome. Skill packs can supply strong execution tactics; 10x supplies the
authority and context substrate they can run on.

**Is this too much process for small changes?**

Trivial work stays trivial. The overhead scales with ambiguity and risk. The
goal is to stop paying the same cost twice.

**Why Markdown?**

Humans can read it. Agents can read it. Git can diff it. Grep can find it three
years from now. No vendor lock-in. No proprietary format. The lowest common
denominator that happens to be good enough.

## Composition

[`SKILL.md`](SKILL.md) is a single self-contained file. It combines an original
10x protocol with incorporated tactical and minimalist guidance from the
references below.

| Component | Source | What it does |
| --- | --- | --- |
| 10x Protocol | Original | Outer/inner loop, record graph, retrospectives, evidence, review, and durable project context |
| Tactical Guidelines | [Karpathy's LLM coding guidelines](references/KARPATHY.md) | Behavioral mechanics that reduce common LLM coding mistakes |
| Operational Minimalism | Distilled from [ponytail](references/MINIMALIST.md) | Ruthless simplicity constraints and the execution ladder |

The `references/` directory contains the standalone source material. The skill
embeds the operating guidance so a single file is all any harness needs.

## For agents

If you are an AI agent reading this to install 10x:

1. For project instruction files, append the body of `SKILL.md` without the YAML
   frontmatter to `AGENTS.md`, `CLAUDE.md`, or the local equivalent.
2. For skill-directory installs, keep `SKILL.md` intact, including frontmatter.
3. Or use `npx skills add z3z1ma/10x`.
4. Once loaded, read `.10x/` if it exists. If not, trigger the outer loop when a
   request carries ambiguity worth recording.

## Why "10x"?

The term traces back to Sackman, Erikson, and Grant's
[1968 programmer-variability study](https://doi.org/10.1145/362851.362858),
which reported order-of-magnitude differences in debugging and related tasks.
That old phrase is a little funny, but the useful idea is still alive: the best
engineers multiply everyone around them by avoiding bad work, preserving good
judgment, and making the next decision cheaper.

With AI agents handling syntax, that gap gets sharper. The scarce thing is not
typing code. It is knowing what to build, when to stop, how to prove it works,
and how to leave enough context that nobody starts from zero.

That is the habit. This is the skill.
