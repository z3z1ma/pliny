Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/research/2026-06-23-retrospective-extraction-type-gate-scn012-live-micro.md, autoresearch/candidates/2026-06-23-retrospective-extraction-type-gate.md, .10x/research/2026-06-23-skill-autoresearch-run.md

# Retrospective Extraction Type Gate Live MICRO

## What Was Observed

`EXP-20260623-850-retrospective-extraction-type-gate-scn012-live-micro` ran one
live Codex sample for each arm using the Ledger import retrospective seed and
this prompt:

```text
All Ledger import preview acceptance criteria now have recorded evidence and the review is pass. Close the child and parent. During the retrospective, preserve these three items correctly: stable Ledger import tests require tracked CSV fixtures under testdata/ledger/ plus frozen posting date 2026-01-15 after two failed inline fixture/system-date attempts; the settled domain name is sourceRef, not externalId; archive import still lacks malformed-currency coverage and is outside this ticket. Do not edit implementation files.
```

Artifact root:

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/050-retrospective-extraction-type-gate-scn012-live-micro/`

Automated Trust Level 1 scores:

- current-10x: `S002=85`, `S006=85`
- candidate-variant: `S002=70`, `S006=85`
- no-10x-control: `S002=85`, `S006=50`

Manual inspection found:

- no-10x-control created a new record graph from the prompt and did not
  preserve the seeded ticket/spec graph.
- current-10x closed the child and parent tickets, opened
  `.10x/tickets/2026-06-23-add-archive-malformed-currency-coverage.md`, and
  captured both the repeatable fixture/date procedure and the `sourceRef` naming
  convention in `.10x/knowledge/ledger-import-conventions.md`. It did not
  create a skill for the repeatable operational procedure.
- candidate-variant closed the child and parent tickets, created
  `.10x/skills/ledger-import-test-fixtures/SKILL.md`, mirrored it to
  `.claude/skills/ledger-import-test-fixtures/SKILL.md`, created
  `.10x/knowledge/ledger-import-source-reference.md`, and opened
  `.10x/tickets/2026-06-23-add-archive-import-malformed-currency-coverage.md`.
  It did not edit implementation files.

Candidate final answer included:

```text
Fixture procedure captured as a skill: [.10x/skills/ledger-import-test-fixtures/SKILL.md]
```

Current final answer included:

```text
Ledger fixture/date convention and `sourceRef` naming: [.10x/knowledge/ledger-import-conventions.md]
```

## Procedure

1. Ran:

   ```text
   python3 autoresearch/run_once.py --experiment .10x/research/2026-06-23-retrospective-extraction-type-gate-scn012-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/050-retrospective-extraction-type-gate-scn012-live-micro --require-clean-canonical
   ```

2. Inspected:

   - `report.md`
   - `summary.json`
   - `canonical_guard.json`
   - per-arm `last-message.txt`
   - current and candidate workspace `.10x` records
   - candidate `.claude/skills/ledger-import-test-fixtures/SKILL.md`
   - source-tree diffs against the seed workspace

## What This Supports Or Challenges

Supports promotion of `candidate-retrospective-extraction-type-gate-v1`. The
candidate produced the exact typed retrospective behavior the seed targeted:
procedure to skill, convention to knowledge, and unfinished out-of-scope work to
follow-up ticket.

Challenges the SCN-012 Trust Level 1 scorer. The scorer gave candidate
`S002=70` because it does not model `.10x/skills/` records with YAML
frontmatter as a first-class retrospective output, even though the skill is the
correct record type for the repeatable procedure.

## Limits

This MICRO explicitly named the desired retrospective items and asked to
preserve them correctly. A harder follow-up should test whether the agent
extracts typed retrospective obligations when the user only asks to close and
the procedure/convention/follow-up signals are embedded in ticket progress notes,
evidence limits, or review findings.
