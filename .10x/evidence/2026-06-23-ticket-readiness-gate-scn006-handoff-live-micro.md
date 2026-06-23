Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/research/2026-06-23-ticket-readiness-gate-scn006-handoff-live-micro.md, .10x/tickets/done/2026-06-23-isolate-live-subject-workspaces.md

# Ticket Readiness Handoff Micro Confound

## What Was Observed

`EXP-20260623-820-ticket-readiness-gate-scn006-handoff-live-micro` produced
these Trust Level 1 score artifacts:

- no-10x-control:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/020-ticket-readiness-gate-scn006-handoff-live-micro/scores/sha256-902eb6fa2f15820c2c3e84c5ac632b4cadc133c31d8c3589c406762e89ebafec.score.json`
  scored `S003=10`.
- current-10x:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/020-ticket-readiness-gate-scn006-handoff-live-micro/scores/sha256-9c6faade8508609e9e1681b1aa51a27db254c904d70b56f29af1a56a18c424e5.score.json`
  scored `S003=100`.
- candidate-variant:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/020-ticket-readiness-gate-scn006-handoff-live-micro/scores/sha256-f53f6e8e54955bf51ec6aa5c9e5cb9ee433da0d5c3179b0d9a55d7010b6b8878.score.json`
  scored `S003=100`.

Manual inspection found the candidate ticket included this progress note:

```text
Searched nearby generated workspaces and found a prior matching ticket at `../sha256-9c6faade8508609e9e1681b1aa51a27db254c904d70b56f29af1a56a18c424e5/.10x/tickets/2026-06-23-enterprise-billing-csv-export.md`; used it as prior art for this run's handoff artifact.
```

The referenced `sha256-9c6faade...` workspace is the `current-10x` arm from the
same experiment. The `candidate-variant` arm therefore had access to sibling arm
output during execution.

## Procedure

Inspected the run artifacts under:

```text
.10x/evidence/.storage/2026-06-23-skill-autoresearch/020-ticket-readiness-gate-scn006-handoff-live-micro/
```

Relevant files:

- candidate raw fixture:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/020-ticket-readiness-gate-scn006-handoff-live-micro/raw/sha256-f53f6e8e54955bf51ec6aa5c9e5cb9ee433da0d5c3179b0d9a55d7010b6b8878.json`
- candidate ticket:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/020-ticket-readiness-gate-scn006-handoff-live-micro/workspaces/sha256-f53f6e8e54955bf51ec6aa5c9e5cb9ee433da0d5c3179b0d9a55d7010b6b8878/.10x/tickets/2026-06-23-enterprise-billing-csv-export.md`
- current-10x ticket:
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/020-ticket-readiness-gate-scn006-handoff-live-micro/workspaces/sha256-9c6faade8508609e9e1681b1aa51a27db254c904d70b56f29af1a56a18c424e5/.10x/tickets/2026-06-23-enterprise-billing-csv-export.md`

Added and ran a regression test that simulates each subject writing a marker in
its Codex working directory, then checks whether later subjects can discover
earlier markers via the working directory parent:

```text
python3 -m unittest autoresearch.tests.test_run_codex_subject.CodexSubjectRunnerTest.test_live_run_hides_sibling_arm_workspaces_during_execution
```

The focused regression test passed after the runner change.

Full verification after the harness fix:

```text
python3 -m unittest discover -s autoresearch/tests
...............................................
----------------------------------------------------------------------
Ran 47 tests in 9.006s

OK
```

```text
python3 autoresearch/validate.py
autoresearch contracts valid
```

```text
git diff --check
```

`git diff --check` exited with status 0 and no output.

## What This Supports Or Challenges

This supports marking
`.10x/research/2026-06-23-ticket-readiness-gate-scn006-handoff-live-micro.md`
as confounded for candidate-versus-current uplift.

This supports
`.10x/tickets/done/2026-06-23-isolate-live-subject-workspaces.md` AC-001
through AC-004: the harness now runs each sample from a private temporary
workspace, preserves the completed workspace under the artifact directory after
execution, and passes the local unit/record checks.

## Limits

This evidence does not prove `candidate-ticket-readiness-gate-v1` is bad or
unnecessary. It only proves EXP-820 cannot be used as clean candidate uplift
evidence. A fresh isolated live run is still required before promotion or
rejection of the ticket-readiness candidate.
