Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Target: autoresearch live subject-runner and SKILL.md autoresearch loop
Verdict: concerns

# Live Harness Autoresearch Audit

## Target

Reviewed the active autoresearch implementation and records after the first
live Codex MICRO run:

- `autoresearch/run_codex_subject.py`
- `autoresearch/run_once.py`
- `autoresearch/offline_score.py`
- `autoresearch/report.py`
- `autoresearch/program.md`
- `autoresearch/templates/experiment.md`
- `autoresearch/README.md`
- `.10x/research/2026-06-23-smallest-executable-unit-live-subject.md`
- `.10x/evidence/2026-06-23-smallest-executable-unit-live-subject.md`

## Findings

Significant, fixed: `run_once.py` returned generic limits saying
fixture-backed scores were limited even for live Codex subject runs. The limits
are now conditional: live subject runs are candidate-quality evidence with
Trust Level 1 scorer limits; fixture-backed scores are calibration evidence.

Significant, fixed: the report could show "No negative, null, backfire,
confounded, or other result statuses were present" directly below campaign
metadata that recorded a negative verdict. The report now says no
artifact-embedded statuses were present and points to the Campaign Verdict when
campaign metadata exists.

Significant, fixed: `offline_score.py` emitted a generic limit saying it did
not run live APIs or subject-agent harnesses, even when scoring saved live Codex
subject outputs. Score artifacts now distinguish live subject-agent artifacts
from offline fixtures and state that the scorer evaluates previously captured
live harness outputs.

Significant, fixed: the active FULL fixture-smoke runner created a tempting
FULL-labeled path that did not execute a subject harness. The runner and tests
were deleted from the active code path. `run_once.py` is now live-only and
dispatches MICRO and FULL experiments through the live subject runner.

Significant, fixed: `autoresearch/templates/experiment.md` included a
fixture-backed MICRO definition block. The template now includes only the live
subject-runner definition.

Minor, fixed: active decisions conflicted after FULL smoke deletion. The older
decisions were moved to `.10x/decisions/superseded/`, and
`.10x/decisions/autoresearch-subject-harness-policy.md` is the active policy.

## Verdict

Concerns remain, but the obvious false-validity paths found in this audit were
fixed in the active implementation.

The first live Codex MICRO result is usable candidate-quality evidence for a
single scenario, not promotion-grade evidence. It rejects
`candidate-smallest-executable-unit-gate-v1` for promotion because it
underperformed current 10x on S005 and tied S007.

## Residual Risk

Scores remain Trust Level 1 and require human manual inspection for
promotion-grade claims.

Codex no-10x isolation is materially improved by generated workspaces,
suppressed instruction files, `--disable plugins`, and `--ignore-user-config`,
but Codex system context and authenticated home behavior are not fully
controlled.

One live MICRO repetition is enough to prove the harness surface works and to
reject this exact candidate for promotion. It is not enough to establish stable
effect sizes or broader 10x improvement.

Campaign verdict metadata is still authored by the driver after score
inspection. That is acceptable for the LLM-controlled autoresearch loop, but
future promotion claims need explicit review of the verdict, not just generated
score artifacts.
