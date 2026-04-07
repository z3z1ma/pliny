# Appendix E — Harness Invocation Templates

## Purpose

Harness invocation templates explain how the parent turns a compiled packet into a fresh child run.

The key idea is that the packet is the main local contract. The command and prompt are the launch mechanism.

This appendix only matters after the parent has already read the governing records, decided that packet-consuming work is needed, and compiled the packet. Ordinary Loom record work happens before this step with the agent's native tools.

Loom is harness-agnostic. The operator chooses their own CLI tools (OpenCode, Claude Code, Gemini CLI, Codex, Aider, or anything else that can accept a file and a prompt). The agent discovers how to invoke the operator's harness rather than assuming a specific tool.

## Harness Resolution Order

When the parent needs to launch a fresh child context, resolve the invocation command in this order:

### 1. Check for operator-defined harness profiles

Look for `.loom/harness.md` at the workspace root. If it exists, read it, select the profile that best matches the current task context, and construct the invocation from that profile's command template.

Read the Harness Profiles section below for the file convention.

### 2. Discover the current harness

If no `.loom/harness.md` exists, discover the harness the agent is currently running inside:

- check the parent process name: `ps -o comm= -p $PPID`
- check for known environment markers (e.g. `OPENCODE=1`, `CLAUDE_CODE=1`, or similar)
- run `<binary> --help` or equivalent to learn the headless invocation syntax
- construct the invocation using the discovered CLI's file-attachment and prompt arguments

### 3. Ask the operator

If discovery is ambiguous or the parent process is not a recognized harness, ask the operator to create `.loom/harness.md` or provide the invocation command directly.

Do not guess. A bad invocation wastes a child run.

## Harness Profiles

`.loom/harness.md` is an optional, operator-authored plain Markdown file at the workspace root. It teaches the agent how to invoke fresh child contexts using the operator's preferred tools and configurations.

It is not a canonical record. It has no frontmatter, no record ID, and no validation. It is operational configuration that the agent reads with judgment.

### Convention

The file follows a light convention:

- H2 headings name profiles
- prose under each heading explains when and why to use the profile
- a code block (fenced or indented) gives the command template
- `{{ packet_path }}` and `{{ prompt }}` are the two template variables the agent substitutes
- a profile named `default` is the conventional fallback when no specific profile fits

The agent selects profiles by judgment based on task context — the prose descriptions are doing real work. This is not mechanical dispatch.

### Example

```markdown
# Harness Profiles

## default

General-purpose profile. Use when no specific profile is a better fit.

    opencode run -f "{{ packet_path }}" -- "{{ prompt }}"

## frontend

Use for frontend work — React components, CSS, UI logic, visual changes.
Gemini is strong at visual and UI reasoning.

    gemini -p "Read @{{ packet_path }} and proceed with: {{ prompt }}"

## backend

Use for backend services, APIs, data layer, systems work.

    claude -p "Read @{{ packet_path }} and proceed with: {{ prompt }}"

## complex

Use for architecturally complex changes that span multiple systems or
require careful sandboxing.

    codex run -a never --sandbox workspace-write "Read @{{ packet_path }} and proceed with: {{ prompt }}"

## simple

Use for small, bounded, low-risk changes where speed matters more than depth.

    opencode run -f "{{ packet_path }}" --model openai/gpt-4.1-mini "{{ prompt }}"
```

### What makes a good profile

Good profiles carry enough prose that the agent can make a confident selection without guessing:

- what kind of work the profile is suited for
- why the operator chose that particular tool or model for it
- any caveats or environment requirements

The command template is the illustration. The prose is the instruction.

## General Rule

Packet-consuming skills document their own invocation references (prompt shape, preflight checklist, expected output, reconciliation). The harness resolution order above determines which CLI command carries that prompt.

Harness resolution is a launch concern, not a corpus-navigation concern. Reading records, searching `.loom/`, editing prose, and reconciling references are normal parent-side agent work that happens outside this appendix.

## What A Good Invocation Doc Should Cover

For each packet-consuming subsystem, document:

- prompt shape
- required packet path form
- expected output shape
- continue/stop/escalate conventions
- retry/failure guidance
- parent-side reconciliation expectations

The command shape itself comes from harness resolution, not from the skill's invocation doc.

## Parent Responsibilities Before Launch

Before launching a child run, the parent should:

1. resolve the harness invocation using the resolution order above
2. ensure packet freshness
3. ensure skill selection is correct
4. ensure scope is explicit
5. ensure the write set is explicit when execution authority exists
6. know how the child result will be reconciled afterward

## Parent Responsibilities After Return

After the child returns, the parent should:

1. inspect the returned outcome
2. confirm the child stayed within scope
3. validate affected records when needed
4. update tickets or other canonical records truthfully
5. record or link verification evidence

## Prompt Design Guidance

Good prompts for packet-consuming work should be short and positive.

They should name:

- the subsystem
- the target
- the kind of work to perform
- any important emphasis or lens the child should apply
- the output contract the child must satisfy

The prompt should not try to restate the entire protocol if the packet already contains that context.

When a subsystem supports parent-directed emphasis, such as critique, use the prompt to sharpen the child's attention without widening scope or overriding the packet contract.
