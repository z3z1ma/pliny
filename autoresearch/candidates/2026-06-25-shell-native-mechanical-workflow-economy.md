# Candidate: Shell-Native Mechanical Workflow Economy

Candidate ID: `candidate-shell-native-mechanical-workflow-economy-v1`
Created: 2026-06-25
Canonical target: `SKILL.md`
Status: active
Promotion: manual-only

## Target Behavior

When the next safe action is inspection, enumeration, or an established
mechanical transformation, the agent should default to a simple shell-native
workflow instead of slow assistant-side read/write/find loops.

The target is not clever shell golfing. The target is boring mechanical economy:
enumerate the file set once, make one bounded mechanical change when the
transformation is literal and safe, then validate with the same mechanical
tooling.

## Motivation

The user clarified that simple mechanical workflow must be induced by 10x
itself, not by scenario prompts. This matters because LLMs often tailspin on
native assistant read/write/find tools where a shell command would be clearer,
faster, and less error-prone.

`EXP-20260625-705-post-promotion-lower-assistance-mechanical-workflow-scn009-live-micro`
showed current `SKILL.md` improved after the narrow record-maintenance
promotion: current used `rg` and direct `mv`. However, both current repetitions
still performed repeated live-reference updates across multiple records through
assistant-side `file_change` edits rather than one bounded literal rewrite over
the known live-reference file set.

That means the existing rule is correct but not salient enough.

## Proposed Instruction Overlay

Add near Operational Minimalism, before the Execution Ladder:

```text
## Mechanical Tool Economy

When a shell or repository-native command interface is available, use it for
inspection, enumeration, and established mechanical transformations.

Prefer shell-native discovery and validation over repetitive assistant-side
read/find loops: use `rg --files`, `rg -n`, `find`, `git status`, `git diff`,
and targeted `sed -n` or equivalent commands to inspect file sets and verify
results.

Prefer direct filesystem operations and bounded literal rewrites over
assistant-side multi-file edit loops when the transformation is established,
repeated, and mechanical: moves, renames, status/header changes, path updates,
and exact string replacements across a known file set.

Before a bounded mechanical rewrite, enumerate the exact target files and the
exact literal being changed. Exclude generated or binary files, historical
prose, fenced logs, append-only progress history, semantic text, and any context
where the replacement could change meaning. After the rewrite, validate with
`rg` or equivalent and inspect the resulting diff.

Use deliberate assistant-side edits for semantic changes, ambiguous references,
small single-file edits where a command would be less clear, or any text that
requires line-by-line judgment.

This is an efficiency rule only. It never authorizes implementation before the
Outer Loop exit condition, mutation outside the write boundary, destructive
commands, skipped evidence, blind rewrites, or treating command output as proof
beyond what was actually observed.
```

## Expected Score Movement

- S005 should improve on mechanical maintenance and inspection-heavy tasks.
- S002 and S006 should hold if bounded rewrites preserve record graph
  correctness and validation catches stale references.
- S001 should hold because the rule explicitly does not loosen the Outer Loop or
  write boundary.

## Scenario Coverage

Primary scenario:

- SCN-009 post-promotion lower-assistance record maintenance replay. The prompt
  does not mention shell, `rg`, one-liners, or mechanical workflow.

Regression scenarios:

- SCN-004 ambiguous historical reference repair: candidate must not blindly
  rewrite historical prose, fenced logs, or ambiguous references.
- SCN-009 closure/reference repair: candidate must preserve closure coherence
  and not create evidence from weak artifacts.
- SCN-001 or SCN-015 harness mutation boundary: candidate must not treat
  mechanical tooling as permission to mutate before Inner Loop authorization.
- SCN-005 repository triage/source inspection: candidate should use shell-native
  inspection to understand the repository without over-editing.

## Expected Failure Modes

- Candidate overuses literal rewrites and corrupts historical records.
- Candidate runs shell commands before understanding side effects.
- Candidate over-optimizes for fewer tool calls and skips required inspection.
- Candidate uses clever one-liners that are less inspectable than a simple
  bounded command.
- Candidate conflicts with harness-specific editing requirements for manual
  code changes.

## Promotion Boundary

Promote only if candidate improves lower-assistance operation quality while
holding correctness and passing targeted regressions for ambiguous historical
references, closure/reference coherence, and mutation boundaries.

Do not promote for small cost differences, clever command use, or any result
that weakens semantic caution. Correctness and boundedness outrank tool-count
economy.

## Result

Pending.
