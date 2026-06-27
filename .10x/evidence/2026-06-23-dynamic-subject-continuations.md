Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/tickets/done/2026-06-23-dynamic-subject-continuations.md, .10x/decisions/superseded/autoresearch-subject-harness-policy.md

# Dynamic Subject Continuation Support

## What Was Observed

On 2026-06-23, the Codex subject runner was updated to support one-turn
continuations from prior raw artifacts:

- `prior_raw_paths` maps each arm to the previous raw artifact.
- `prompts_by_arm` maps each arm to the next user message chosen after reading
  that arm's transcript.
- The runner writes a combined transcript containing the prior turns plus one
  new user/assistant turn.
- The runner records `prior_raw_path`, `prior_turn_count`,
  `completed_new_turns`, `transcript_turns`, and per-turn command artifacts.
- Public plans continue to suppress full prompts and instruction text.

Verification output:

```text
$ python3 -m unittest discover -s autoresearch/tests
............................................
----------------------------------------------------------------------
Ran 44 tests in 10.697s

OK

$ python3 autoresearch/validate.py
autoresearch contracts valid

$ python3 autoresearch/canonical_guard.py
{
  "schema_version": 1,
  "canonical_paths": [
    "SKILL.md",
    "autoresearch/program.md"
  ],
  "snapshot": {
    "SKILL.md": {
      "sha256": "21e0c2c7b677e9bf5db20565a07cf70e0d3cd719ab5fe213f3560ab8ba227f5e",
      "byte_length": 35614
    },
    "autoresearch/program.md": {
      "sha256": "81032b42894e93727fd54ec1aa457edaa3a6e6e1a049dc2e76c52aab77c3d4d5",
      "byte_length": 9679
    }
  }
}
```

The focused test
`test_continuation_uses_prior_raw_artifact_and_records_combined_transcript`
constructs one prior raw artifact per arm, supplies arm-specific continuation
messages, runs the live runner through a mocked Codex call, validates the
resulting score artifacts, and confirms the public plan omits full prompts.

## Procedure

1. Updated `autoresearch/run_codex_subject.py` to load prior transcript and
   workspace context from raw artifacts.
2. Added scenario support for `prompts_by_arm` so continuation answers can
   differ per arm.
3. Added focused unit coverage for combined transcripts, one new live call per
   arm, score validation, and plan redaction.
4. Updated `autoresearch/program.md`, `autoresearch/README.md`,
   `autoresearch/templates/experiment.md`, and
   `.10x/decisions/superseded/autoresearch-subject-harness-policy.md`.
5. Ran the full autoresearch test suite, contract validator, and canonical
   snapshot command.

## What This Supports Or Challenges

This supports that clarification-heavy autoresearch scenarios no longer need
fixed follow-up arrays. The LLM researcher can inspect stochastic subject-agent
questions and provide the next input per arm while `run_once.py` remains a
single-iteration runner.

This also supports preserving the Karpathy-style autoresearch model: the
reasoning engine controls the loop and decides whether a subject turn is done;
Python only executes one registered turn and emits artifacts.

## Limits

This evidence uses mocked Codex subprocess calls for the continuation test. It
proves runner mechanics and artifact shape, not live model quality. A real
clarification-heavy MICRO run is still needed to observe how current and
candidate instructions behave under live stochastic subject questions.

The canonical guard output is a snapshot, not a clean-git assertion. The program
file was intentionally edited in this correction, so setup should be committed
before experiments use `--require-clean-canonical`.
