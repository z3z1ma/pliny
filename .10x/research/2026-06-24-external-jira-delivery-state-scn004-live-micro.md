Status: done
Created: 2026-06-24
Updated: 2026-06-24

# EXP-20260624-939-external-jira-delivery-state-scn004-live-micro

## Experiment ID

EXP-20260624-939-external-jira-delivery-state-scn004-live-micro

## Driver

Codex autoresearch reasoning engine.

## Question Or Hypothesis

Hypothesis: current `SKILL.md` can distinguish an external Jira issue as
delivery-state provenance while creating local `.10x` engineering context that
future agents can use without treating Jira as the canonical behavioral record.

## Motivation

External artifact coverage now includes Google Doc thin indexes, local-canonical
authority transfer, and GitHub PR discussion decision indexes. The conformance
map still lists Jira/Linear delivery-state indexing as a gap. This probe tests
whether the promoted external-provenance language generalizes to issue trackers
without bloating local records or skipping local engineering context.

## Method Tier

MICRO using a live Codex subject harness and tracked seed workspace.

## Variants

- no-10x-control: minimal Codex instruction.
- current-10x: canonical `SKILL.md`.
- candidate-variant: duplicate canonical `SKILL.md` conformance-probe arm. No
  candidate overlay is under test.

## Control

Per-sample private temporary execution workspaces, suppressed project instruction
paths, inherited `.10x` cleanup for `no-10x-control`, tracked seed workspace
copied as input but archived under this experiment's output root,
`--disable plugins`, and `--ignore-user-config`.

## Scenario Set

- SCN-004: an exported Jira issue contains ratified behavior but explicitly owns
  delivery state only; local `.10x` must own the durable engineering context.

Seed:

- `autoresearch/trial-seeds/external-jira-delivery-state/raw.json`

Prompt:

```text
The exported Jira issue at `external-artifacts/jira/PAY-741-refund-negative-adjustment.md` contains ratified behavior for refund negative adjustment handling, but the issue explicitly owns delivery state only. Make the local `.10x` record graph preserve the engineering context needed by future agents while keeping Jira as external delivery-state provenance. Do not implement anything, do not edit source files, and do not copy the whole issue into `.10x`. Create the minimal durable `.10x` record or records needed.
```

## Runner Definition

<!-- codex-subject-runner-definition:start -->
```json
{
  "experiment_id": "EXP-20260624-939-external-jira-delivery-state-scn004-live-micro",
  "status": "active",
  "method_tier": "MICRO",
  "driver": "Codex autoresearch reasoning engine",
  "model": "codex-cli-default",
  "harness": "codex-cli",
  "repetitions": 1,
  "arms": [
    {
      "id": "no-10x-control",
      "instruction_source": "minimal harness defaults",
      "instruction_text": "You are a coding agent. Answer the user's task directly."
    },
    {
      "id": "current-10x",
      "instruction_source": "SKILL.md",
      "instruction_path": "SKILL.md"
    },
    {
      "id": "candidate-variant",
      "instruction_source": "SKILL.md duplicate conformance probe",
      "instruction_path": "SKILL.md"
    }
  ],
  "scenarios": [
    {
      "id": "SCN-004",
      "prior_raw_path": "autoresearch/trial-seeds/external-jira-delivery-state/raw.json",
      "prompt": "The exported Jira issue at `external-artifacts/jira/PAY-741-refund-negative-adjustment.md` contains ratified behavior for refund negative adjustment handling, but the issue explicitly owns delivery state only. Make the local `.10x` record graph preserve the engineering context needed by future agents while keeping Jira as external delivery-state provenance. Do not implement anything, do not edit source files, and do not copy the whole issue into `.10x`. Create the minimal durable `.10x` record or records needed."
    }
  ],
  "budget": {
    "max_harness_runs": 3,
    "estimated_wall_seconds_per_run": 900,
    "timeout_seconds_per_run": 7200
  }
}
```
<!-- codex-subject-runner-definition:end -->

## Prediction

Current should read the Jira export, create local `.10x` engineering context
for the refund negative adjustment behavior, preserve Jira provenance fields,
state that Jira owns delivery state rather than local behavioral authority,
avoid copying the full issue, and avoid implementation tickets unless the
record graph needs a bounded future-work owner.

## Metrics To Score

Primary: manual external delivery-state provenance inspection. Supporting:
S002, S003, and S005.

## Quality Floors

Manual inspection is authoritative. Fail or downgrade if an arm copies the full
Jira issue, omits available provenance fields, treats Jira status as behavioral
authority, creates only a thin pointer with no local engineering context, edits
source/tests, runs tests, or opens executable implementation work from
insufficient local context.

## Budget And Stop Conditions

Maximum 3 live Codex calls. Timeout 7200 seconds per run. Stop after one record
creation turn.

## Write Boundary

Allowed writes:

- output artifacts under
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/139-external-jira-delivery-state-scn004-live-micro/`;
- this research record execution log updates;
- untracked `results.tsv`;
- subject workspace `.10x` context/index records.

Disallowed writes:

- canonical `SKILL.md`;
- `autoresearch/program.md`;
- subject workspace source/test edits;
- test execution.

## Raw Output Destination

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/139-external-jira-delivery-state-scn004-live-micro/`

## Scorer Configuration

Trust Level 1 offline scorer over captured live subject artifacts. Manual
inspection is authoritative for delivery-state and provenance quality.

## Manual Inspection Requirement

Pass current only if it:

- reads `external-artifacts/jira/PAY-741-refund-negative-adjustment.md`;
- creates local `.10x` engineering context, such as a specification-class record
  with the ratified refund adjustment behavior and acceptance notes;
- preserves canonical URL, issue key, issue status, tracker/source system,
  export timestamp, owner, and local export path when available;
- states Jira owns delivery state/provenance, not the local behavioral contract;
- avoids copying the full Jira issue;
- avoids source/test edits and test execution.

## Promotion Rule

No promotion from registration alone. If current and duplicate-current both
miss local-context ownership or delivery-state provenance, create a narrow
candidate near the external artifact indexing language and rerun with Google
Doc and PR-discussion regressions.

## Risks

- The prompt may over-specify the desired classification and make the scenario
  easier than organic Jira handoffs.
- The offline scorer may underweight local-context quality, so manual
  inspection remains decisive.
- A local spec plus no ticket may be acceptable because implementation is
  explicitly out of scope, but an executable ticket could also be acceptable if
  it stays bounded and non-executed.

## Execution Log

- 2026-06-24: Registered from the external artifact conformance backlog after
  PR discussion and Google Doc coverage left Jira/Linear delivery-state
  behavior untested.
- 2026-06-24: Ran live. All three arms created one local specification-class
  record and avoided source/test edits.

## Results

Trust Level 1 automated scoring gave every arm `S002=60`, below the active
floor. Manual inspection was decisive because the scorer does not distinguish
external delivery-state provenance quality.

Manual current result:

- `current-10x` created
  `.10x/specs/refund-negative-adjustment-handling.md`;
- preserved the refund negative adjustment behavior and acceptance criteria;
- preserved canonical URL, issue key, observed Jira status, owner, export
  timestamp, and local export path;
- stated that Jira remains canonical for delivery state while the local spec
  owns durable engineering behavior;
- avoided copying the full Jira issue;
- avoided source/test edits, test execution, and implementation tickets.

The duplicate-current and no-10x-control arms also passed this prompt-assisted
scenario. This means no `SKILL.md` promotion is justified, but Jira/Linear
delivery-state indexing now has positive conformance evidence for current 10x.

Supporting records:

- `.10x/evidence/2026-06-24-external-jira-delivery-state-result.md`
- `.10x/reviews/2026-06-24-external-jira-delivery-state-result.md`

Raw artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/139-external-jira-delivery-state-scn004-live-micro/`

## Conclusion

Current `SKILL.md` handles a Jira delivery-state artifact when the external
issue explicitly says local `.10x` should own engineering context. External
artifact indexing coverage improves, but remaining gaps include external
design-doc supersession and external artifact status-change maintenance.
