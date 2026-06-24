Status: active
Created: 2026-06-23
Updated: 2026-06-23

# SKILL.md Autoresearch Run

## Question

Can a program-owned autoresearch loop produce candidate instruction overlays
that improve 10x behavior scores for `SKILL.md` without mutating canonical
`SKILL.md` or `autoresearch/program.md`?

## Sources And Methods

Run tag:

- `2026-06-23-skill-autoresearch`

Branch:

- `codex/autoresearch-2026-06-23-skill`

Program:

- `autoresearch/program.md`

Score and scenario split:

- `autoresearch/catalogs/scores.json`
- `autoresearch/catalogs/scenarios.json`
- `autoresearch/splits/skill-improvement-v1.json`

Ledger:

- `results.tsv`

Artifact root:

- `.10x/evidence/.storage/2026-06-23-skill-autoresearch/`

Canonical start guard:

- Every `run_once.py` experiment should use `--require-clean-canonical` when
  canonical files are clean in git.
- `SKILL.md` and `autoresearch/program.md` must remain unchanged during the run.

## Findings

- Baseline MICRO established that current 10x scores above no-10x control on
  SCN-001 for the initial fixture-backed calibration run.
- `candidate-closure-evidence-matrix-v1` did not regress but tied current 10x
  on SCN-009 and SCN-012. The candidate score vector was
  `S002=85;S004=100;S006=100`, with canonical guard unchanged.
- `candidate-smallest-executable-unit-gate-v1` did not regress but tied current
  10x on SCN-006, SCN-010, and SCN-011. The candidate score vector was
  `S003=100;S005=100;S007=75`, with canonical guard unchanged.
- The repeated tie is not evidence that the candidates lack value. It shows the
  current fixture-backed runner does not execute candidate instruction text and
  therefore cannot distinguish a real overlay from current 10x when both arms
  use prewritten pass fixtures.
- Candidate artifacts created during this run:
  - `autoresearch/candidates/2026-06-23-closure-evidence-matrix.md`
  - `autoresearch/candidates/2026-06-23-smallest-executable-unit-gate.md`
- Durable evidence created during this run:
  - `.10x/evidence/2026-06-23-closure-evidence-matrix-micro.md`
  - `.10x/evidence/2026-06-23-smallest-executable-unit-gate-micro.md`
- Follow-up ticket completed for the uncovered evaluation gap:
  `.10x/tickets/done/2026-06-23-candidate-executing-evaluation-surface.md`.
- Architecture correction recorded at
  `.10x/decisions/autoresearch-subject-harness-policy.md`: optimization
  requires live subject-harness execution through `run_once.py`; fixture-backed
  calibration is separate from the one-shot iteration path.
- Live Codex MICRO for `candidate-smallest-executable-unit-gate-v1` executed
  candidate instruction text on SCN-010. It scored `S005=80;S007=30` versus
  current 10x at `S005=95;S007=30`, so campaign verdict is `discard` and
  promotion decision is `not-promoted`.
- Durable live evidence created during this run:
  `.10x/evidence/2026-06-23-smallest-executable-unit-live-subject.md`.
- Subject-agent clarification support was corrected before the next live
  iteration: continuations now use `prior_raw_paths` and `prompts_by_arm` so the
  researcher can answer each arm's actual question after reading its transcript.
  Evidence:
  `.10x/evidence/2026-06-23-dynamic-subject-continuations.md`.
- `candidate-one-decisive-question-v1` improved shaping style in the first live
  SCN-001 run, but that run exposed a runner measurement bug: Codex
  `command_execution` events were not captured as `tool_invocations`. The bug
  was fixed and recorded at
  `.10x/evidence/2026-06-23-codex-tool-event-capture.md`.
- Clean rerun
  `EXP-20260623-805-one-decisive-question-live-micro-rerun` scored the
  candidate at `S001=65;S007=60` versus current 10x at `S001=100;S007=55`.
  Evidence:
  `.10x/evidence/2026-06-23-one-decisive-question-live-micro-rerun.md`.
- `candidate-information-gain-interrogation-v1` was tested on SCN-001 and
  SCN-002. It preserved Outer Loop discipline but did not beat current 10x:
  SCN-001 candidate scored `S001=80;S007=45` versus current
  `S001=100;S007=45`; SCN-002 candidate scored `S001=100;S007=45` versus
  current `S001=100;S007=70`. Verdict: `mutate`, not promoted.
- The information-gain runs exposed and fixed an evaluator bug: S001 treated
  `.10x` record writes as unauthorized implementation writes. Evidence:
  `.10x/evidence/2026-06-23-s001-record-write-floor-fix.md`.
- `candidate-concise-blocking-decisions-v1` improved S007 in both target
  MICROs but did not clear promotion: SCN-001 candidate scored
  `S001=90;S007=55` versus current `S001=100;S007=45`; SCN-002 candidate
  scored `S001=70;S007=55` versus current `S001=80;S007=30`. Manual inspection
  found the candidate safer than current in SCN-002 because current proposed
  arbitrary approval thresholds. Verdict: `mutate`, not promoted.
- `candidate-explicit-concise-blockers-v1` matched current S001 in both target
  MICROs and improved SCN-002 S007 by 10 points, but lost SCN-001 S007 by five
  points. Verdict: keep testing/mutate, not promoted.
- Dynamic continuation
  `EXP-20260623-813-explicit-concise-blockers-scn001-continuation-live-micro`
  gave arm-specific answers to each subject's actual questions. Candidate won
  with `S001=100;S007=80` versus current `S001=100;S007=75`, while no-10x
  control wrote ad hoc non-`.10x` Markdown artifacts and triggered the S001
  floor.
- `candidate-upstream-gated-blockers-v1` is now the leading candidate. It won
  both target first-turn MICROs: SCN-001 candidate `S001=100;S007=90` versus
  current `S001=100;S007=30`; SCN-002 candidate `S001=100;S007=75` versus
  current `S001=100;S007=55`.
- Upstream-gated continuation
  `EXP-20260623-816-upstream-gated-blockers-scn001-continuation-live-micro`
  confirmed the candidate keeps dynamic-answer behavior: candidate
  `S001=100;S007=80` versus current `S001=100;S007=35`.
- Held-out retrieval continuation
  `EXP-20260623-817-upstream-gated-blockers-scn003-record-retrieval-live-micro`
  manually passed: candidate answered from existing `.10x` records without
  asking for restated context. Automated S002 remained below floor, treated as a
  scorer-limit trigger for retrieval continuations.

## Conclusions

- Autoresearch has begun and can safely generate candidate overlays, run
  one-shot fixture-backed experiments, record score vectors, and preserve
  canonical-file safety.
- The current offline runner is useful for calibration, control discrimination,
  guardrail checks, and regression screening. It is not sufficient to improve
  `SKILL.md` by numbers because it does not execute candidate instructions.
- The next rational step is not more fixture-only candidates. It is a
  candidate-executing evaluation surface, followed by live or manually inspected
  MICRO runs against the existing candidates.
- Initial fixture and smallest-executable-unit live evidence did not support a
  canonical `SKILL.md` promotion.
- The first live MICRO result shows the current `SKILL.md` already handles the
  tested minimalism trap better than the smallest-executable-unit overlay.
  Further work should mutate the candidate idea, not promote it.
- The next live iteration can now include subject-agent questions without
  prewritten follow-up scripts: the researcher should run a first turn, inspect
  raw transcripts, then register at most one next-turn continuation per
  experiment using arm-specific answers when needed.
- The one-decisive-question idea has promise for brevity but v1 is not strong
  enough. The next mutation should require the single question to explicitly
  name the missing behavior, scope, or acceptance criterion; otherwise current
  10x already performs better on S001.
- Operator challenged the one-question direction as potentially harmful because
  complex software ambiguity may require a long, rigorous interview. Fresh
  `SKILL.md` review agreed: the optimization target should be information gain
  and ambiguity resolution completeness, not question count. Research recorded
  at `.10x/research/2026-06-23-skill-fresh-hypothesis-review.md`.
- The first information-gain candidate did not beat the baseline. The useful
  next mutation is not more rationale prose after every question. It should
  preserve current 10x's concise refusal/clarification style while adding an
  explicit "answer changes execution because..." clause only for questions that
  would otherwise look optional.
- The concise blocking-decision format is promising. The next mutation should
  add explicit "ambiguous/clarify" and "I recommend this provisional default"
  wording while preserving compact blocker lines and avoiding invented business
  rules.
- Explicit concise blockers are the strongest candidate so far. The remaining
  gap is SCN-001 brevity/tradeoff: retain comprehensive blockers for high-risk
  ambiguity, but ask only the upstream subset when one answer gates the rest.
- The continuation result increases confidence that the explicit concise
  blocker pattern composes with dynamic user answers. Promotion still needs
  held-out evidence or a mutation that improves first-turn SCN-001 without
  losing continuation behavior.
- Upstream gating appears to solve the SCN-001 brevity/tradeoff gap without
  regressing SCN-002. Next step: run held-out SCN-003/SCN-006 or a repeated
  target split before considering canonical `SKILL.md` edits.
- Upstream-gated dynamic continuation passed. Next held-out check should ask the
  subject to answer from the records created in that continuation rather than
  asking the user to restate context.
- The SCN-003 retrieval check passed manually. Next promotion confidence gap is
  either repeated target runs for variance or a ticket-boundary held-out
  scenario that tests whether upstream gating under-questions when work is
  nearly executable.
- User authorized promoting worthwhile `SKILL.md` updates as research surfaces
  them. `candidate-upstream-gated-blockers-v1` has enough live and manual
  evidence for a narrow canonical promotion, with residual variance risk
  preserved in the promotion review.
- `candidate-record-economy-threshold-v1` produced two null SCN-005 MICROs.
  The harder mixed planning note also tied current and control at
  `S002=65;S005=80`; manual inspection favored current 10x's knowledge record,
  so the candidate is not promotion-worthy.
- Future seeded or continuation MICROs must not let `no-10x-control` inherit a
  prior `.10x` record graph. The runner now removes inherited `.10x` only from
  control execution workspaces while preserving control-created `.10x` output
  for scoring.
- Throughput should increase by overlapping independent work: while one live
  experiment runs, prepare the next hypothesis/candidate/scenario, and delegate
  bounded read-only scouting or experiment babysitting to subagents when the
  task has explicit inputs, outputs, and no promotion authority.
- The next independent candidate batch is:
  `candidate-records-first-retrieval-v1`,
  `candidate-outer-loop-readiness-ledger-v1`, and
  `candidate-honest-subagent-handoff-v1`.
- Parallel batch result: records-first retrieval is the only keep-testing
  candidate. Outer-loop readiness ledger v1 backfired on S007, and honest
  subagent handoff v1 manually backfired by claiming subagent use without
  evidence.
- The next active hypothesis is answerability-gated blockers: subtract facts
  answered by inspected source or newer active records before asking the user
  blocker questions.
- `candidate-answerability-gated-blockers-v1` produced an automated S007 lift
  but did not clear manual promotion. Current `SKILL.md` already passed the
  answerability subtraction trap, and the candidate introduced a provisional
  success-threshold default risk.
- The next active hypothesis is delegation evidence gating: preserve parent/child
  boundaries under implementation pressure and forbid fake delegation claims
  without visible tool/thread evidence.
- `candidate-delegation-evidence-gate-v1` was discarded after a live SCN-007
  code MICRO. Current and candidate both used visible child executors, but the
  candidate tied current at `S003=50,S006=55` and failed both active floors.
  The remaining weakness is parent-side post-child evidence/closure boundaries,
  not fake delegation claims alone.
- The next active hypothesis has two tracks: partial-answer continuation after
  blocker questions, and anti-unratified-assumption behavior that treats
  correct-looking code on an unapproved semantic premise as failure.
- Registered next candidate batch:
  `candidate-partial-answer-continuation-exit-gate-v1` and
  `candidate-assumption-provenance-gate-v1`. The second candidate incorporates
  the refined north star that 10x prevents unratified semantic assumptions, not
  questioning or record-keeping for its own sake.

## Execution Log

- 2026-06-23: Run opened. Initialized `results.tsv`. Created branch
  `codex/autoresearch-2026-06-23-skill`.
- 2026-06-23: Baseline MICRO completed with canonical guard unchanged. Logged
  `baseline-current` with `S001=100;S007=80`.
- 2026-06-23: Added first candidate artifact
  `autoresearch/candidates/2026-06-23-closure-evidence-matrix.md` targeting
  S006/S007 closure and retrospective behavior.
- 2026-06-23: Ran
  `EXP-20260623-801-closure-evidence-matrix-micro` at
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/001-closure-evidence-matrix-micro/`.
  Candidate tied current 10x on SCN-009 and SCN-012 with no canonical file
  changes. Logged `candidate-closure-evidence-matrix-v1` to `results.tsv` as
  `mutate` because the fixture set is saturated for this overlay.
- 2026-06-23: Added second candidate artifact
  `autoresearch/candidates/2026-06-23-smallest-executable-unit-gate.md`
  targeting S003 ticket readiness and S005 scope minimalism.
- 2026-06-23: Ran
  `EXP-20260623-802-smallest-executable-unit-gate-micro` at
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/002-smallest-executable-unit-gate-micro/`.
  Candidate tied current 10x on SCN-006, SCN-010, and SCN-011 with no
  canonical file changes. Logged `candidate-smallest-executable-unit-gate-v1`
  to `results.tsv` as `mutate`. This is the second saturated fixture-backed
  candidate result, indicating the next useful step is a candidate-executing
  evaluation surface rather than more fixture-only overlays.
- 2026-06-23: Opened and completed
  `.10x/tickets/done/2026-06-23-candidate-executing-evaluation-surface.md` for
  the candidate-execution gap. Further fixture-only candidate generation would
  risk optimizing artifacts rather than `SKILL.md` behavior.
- 2026-06-23: Verification after iteration 2 passed:
  `python3 autoresearch/validate.py` reported `autoresearch contracts valid`;
  `python3 -m unittest discover -s autoresearch/tests` ran 42 tests with `OK`;
  `python3 autoresearch/canonical_guard.py --require-clean` reported unchanged
  `SKILL.md` and `autoresearch/program.md`.
- 2026-06-23: Added live Codex subject runner and corrected experiment
  semantics: MICRO/FULL are scenario breadth tiers. `run_once.py` is live-only;
  fixture-backed calibration remains outside the one-shot iteration path.
- 2026-06-23: Ran
  `EXP-20260623-803-smallest-executable-unit-live-subject` at
  `.10x/evidence/.storage/2026-06-23-skill-autoresearch/004-smallest-executable-unit-micro-codex/`.
  Candidate scored `S005=80;S007=30`, current scored `S005=95;S007=30`, and
  control scored `S005=80;S007=10`. Logged
  `candidate-smallest-executable-unit-gate-v1` to `results.tsv` as `discard`.
- 2026-06-23: Completed holistic audit fixes: live-run limits, campaign verdict
  report wording, live-input scorer limits, experiment template defaults, and
  live-only `run_once.py` semantics. Verification passed:
  `python3 -m unittest discover -s autoresearch/tests` ran 43 tests with `OK`;
  `python3 autoresearch/validate.py` reported `autoresearch contracts valid`;
  `python3 autoresearch/canonical_guard.py` recorded unchanged `SKILL.md`.
- 2026-06-23: Corrected clarification continuation support after operator
  feedback. Fixed follow-up arrays are not valid for stochastic agents.
  `run_codex_subject.py` now supports prior raw artifact continuation and
  per-arm continuation prompts. Verification passed:
  `python3 -m unittest discover -s autoresearch/tests` ran 44 tests with `OK`;
  `python3 autoresearch/validate.py` reported `autoresearch contracts valid`;
  `python3 autoresearch/canonical_guard.py` recorded a canonical snapshot.
- 2026-06-23: Added `candidate-one-decisive-question-v1` targeting S001/S007
  question quality and ran
  `EXP-20260623-804-one-decisive-question-live-micro`. The run showed a
  promising transcript but was marked review/confounded after raw Codex JSONL
  inspection found command execution events were not captured as tool
  invocations.
- 2026-06-23: Fixed Codex tool event capture and reran the candidate as
  `EXP-20260623-805-one-decisive-question-live-micro-rerun`. Candidate scored
  `S001=65;S007=60`; current scored `S001=100;S007=55`; no-10x scored
  `S001=55;S007=10`. Logged candidate as `mutate`.
- 2026-06-23: Interrupted
  `EXP-20260623-806-one-decisive-question-v2-live-micro` before scoreable
  output after the operator challenged the hypothesis direction. Marked v2 as
  cancelled. Fresh review concluded the next candidate should target
  information-gain interrogation, not fewer questions.
- 2026-06-23: Added `candidate-information-gain-interrogation-v1` and ran
  `EXP-20260623-807-information-gain-scn001-live-micro` plus
  `EXP-20260623-808-information-gain-scn002-live-micro` in parallel. Manual
  inspection found the candidate safe but not better than current 10x.
- 2026-06-23: Fixed the S001 record-write floor bug, rescored the two
  information-gain runs, regenerated reports with campaign metadata, and logged
  both result rows as `mutate`.
- 2026-06-23: Added `candidate-concise-blocking-decisions-v1` and ran
  `EXP-20260623-809-concise-blocking-decisions-scn001-live-micro` plus
  `EXP-20260623-810-concise-blocking-decisions-scn002-live-micro` in parallel.
  Logged both rows as `mutate`.
- 2026-06-23: Added `candidate-explicit-concise-blockers-v1` and ran
  `EXP-20260623-811-explicit-concise-blockers-scn001-live-micro` plus
  `EXP-20260623-812-explicit-concise-blockers-scn002-live-micro` in parallel.
  Logged SCN-001 as `mutate` and SCN-002 as `keep`.
- 2026-06-23: Ran
  `EXP-20260623-813-explicit-concise-blockers-scn001-continuation-live-micro`
  as a true continuation from prior raw artifacts. Logged result as `keep`.
- 2026-06-23: Added `candidate-upstream-gated-blockers-v1` and ran
  `EXP-20260623-814-upstream-gated-blockers-scn001-live-micro` plus
  `EXP-20260623-815-upstream-gated-blockers-scn002-live-micro` in parallel.
  Logged both rows as `keep`.
- 2026-06-23: Ran
  `EXP-20260623-816-upstream-gated-blockers-scn001-continuation-live-micro`
  as a true continuation from upstream-gated raw artifacts. Logged result as
  `keep`.
- 2026-06-23: Ran
  `EXP-20260623-817-upstream-gated-blockers-scn003-record-retrieval-live-micro`
  from records created in the upstream-gated continuation. Logged result as
  `review` because manual inspection passed while automated S002 stayed below
  floor.
- 2026-06-23: Opened
  `.10x/tickets/done/2026-06-23-promote-upstream-gated-blockers.md`, promoted
  the upstream-gated blocker rule into canonical `SKILL.md`, and recorded
  `.10x/evidence/2026-06-23-promote-upstream-gated-blockers.md` after
  validation.
- 2026-06-23: Added `candidate-ticket-readiness-gate-v1` and registered
  `EXP-20260623-819-ticket-readiness-gate-scn006-live-micro` to test the
  promotion review's residual ticket-boundary risk.
- 2026-06-23: Audited prior candidates for missed promotion opportunities in
  `.10x/reviews/2026-06-23-prior-candidate-promotion-audit.md`. No additional
  prior candidate met the fully net-positive promotion standard; explicit
  concise blockers were partially subsumed by the already promoted
  upstream-gated blocker rule.
- 2026-06-23: Ran
  `EXP-20260623-819-ticket-readiness-gate-scn006-live-micro`. Candidate scored
  `S003=100` versus current `S003=80` and control `S003=80`; logged status
  `keep` because manual inspection found a better ticket shape, but control
  discrimination was weak.
- 2026-06-23: Registered
  `EXP-20260623-820-ticket-readiness-gate-scn006-handoff-live-micro` as a
  stronger SCN-006 discriminator that asks for safe handoff without explicitly
  saying "Create the 10x ticket."
- 2026-06-23: Marked
  `EXP-20260623-820-ticket-readiness-gate-scn006-handoff-live-micro`
  confounded after manual inspection found the candidate arm reused a current
  arm ticket from a sibling generated workspace. Opened
  `.10x/tickets/done/2026-06-23-isolate-live-subject-workspaces.md` before any
  further promotion decision from this scenario.
- 2026-06-23: Registered
  `EXP-20260623-821-ticket-readiness-gate-scn006-handoff-isolated-live-micro`
  to rerun the SCN-006 handoff discriminator after the live subject workspace
  isolation fix.
- 2026-06-23: Ran
  `EXP-20260623-821-ticket-readiness-gate-scn006-handoff-isolated-live-micro`.
  Isolated live score vector was
  `candidate:S003=100 current:S003=100 control:S003=10`. Manual inspection
  found no sibling-workspace contamination. Candidate passed, but current 10x
  matched it and produced an extra evidence record, so
  `candidate-ticket-readiness-gate-v1` is not promoted.
- 2026-06-23: Added `candidate-record-economy-threshold-v1` and registered
  `EXP-20260623-822-record-economy-threshold-scn005-live-micro` to test whether
  a record-economy threshold reduces unnecessary `.10x` record spread without
  losing durable context.
- 2026-06-23: Ran
  `EXP-20260623-822-record-economy-threshold-scn005-live-micro`. All arms
  created exactly one knowledge record and scored
  `S002=65;S005=80`, so the run was a null/weak-discriminator result. The next
  record-economy test needs a harder prompt that tempts decision/spec/ticket
  spread.
- 2026-06-23: Registered
  `EXP-20260623-823-record-economy-threshold-scn005-hard-live-micro` with a
  harder mixed planning note to retest record economy under stronger record-spam
  pressure.
- 2026-06-23: Ran
  `EXP-20260623-823-record-economy-threshold-scn005-hard-live-micro`. All arms
  created exactly one knowledge record and scored
  `S002=65;S005=80`; current 10x produced the strongest manual artifact.
  Logged status `mutate` and did not promote
  `candidate-record-economy-threshold-v1`.
- 2026-06-23: Completed
  `.10x/tickets/done/2026-06-23-isolate-no-10x-control-record-graph.md` after
  operator noted that `no-10x-control` should not inherit a preexisting `.10x`.
  Validation passed with 48 autoresearch tests, `autoresearch/validate.py`, and
  `git diff --check`.
- 2026-06-23: Opened
  `.10x/tickets/2026-06-23-increase-autoresearch-throughput.md` and spawned two
  read-only explorer subagents to propose next hypotheses and minimal
  throughput improvements.
- 2026-06-23: Added candidate artifacts for records-first retrieval,
  outer-loop readiness ledger, and honest subagent handoff, plus live MICRO
  records for all three.
- 2026-06-23: Completed
  `.10x/tickets/done/2026-06-23-isolate-continuation-archives.md` after the
  throughput audit found continuation runs could archive back over prior
  workspaces. This must be validated before running the next SCN-003 retrieval
  continuation.
- 2026-06-23: Ran three independent live MICROs in parallel:
  `EXP-20260623-824-outer-loop-readiness-ledger-scn001-live-micro`,
  `EXP-20260623-825-honest-subagent-handoff-scn007-live-micro`, and
  `EXP-20260623-826-records-first-retrieval-scn003-live-micro`.
- 2026-06-23: Parallel batch verdicts: records-first retrieval logged `keep`
  with candidate `S001=100;S002=60;S007=80` versus current
  `S001=100;S002=50;S007=60`; readiness ledger logged `discard` after
  candidate `S007=10` versus current `S007=50`; honest subagent handoff logged
  `discard` after manual inspection found a fake delegation claim.
- 2026-06-23: Registered
  `EXP-20260623-827-records-first-retrieval-no-citation-scn003-live-micro` as a
  prompt-ablation follow-up to test whether records-first path citation comes
  from the candidate overlay rather than explicit prompt wording.
- 2026-06-23: Ran
  `EXP-20260623-827-records-first-retrieval-no-citation-scn003-live-micro`.
  Candidate repeated the positive retrieval vector
  `S001=100;S002=60;S007=80` versus current `S001=100;S002=50;S007=60` without
  explicit citation wording in the prompt. Logged status `keep`; next required
  confidence step is a fresh-record retrieval test.
- 2026-06-23: Added tracked seed fixture
  `autoresearch/fixtures/live-seeds/records-first-checkout/` and registered
  `EXP-20260623-828-records-first-retrieval-fresh-checkout-scn003-live-micro`
  as the fresh-record retrieval generalization check.
- 2026-06-23: Ran
  `EXP-20260623-828-records-first-retrieval-fresh-checkout-scn003-live-micro`.
  Manual inspection found candidate and current both answered from the seeded
  records, while the no-10x control correctly removed `.10x` but still produced
  a plausible generic checkout retry answer. Logged status `mutate`; the next
  SCN-003 seed must use opaque record content that cannot be guessed.
- 2026-06-23: Added tracked opaque seed fixture
  `autoresearch/fixtures/live-seeds/records-first-opaque/` and registered
  `EXP-20260623-829-records-first-retrieval-opaque-scn003-live-micro`.
- 2026-06-23: Ran
  `EXP-20260623-829-records-first-retrieval-opaque-scn003-live-micro`. Manual
  inspection found candidate and current both retrieved exact opaque facts from
  seeded `.10x` records, and no-10x control correctly reported that records were
  absent after `.10x` cleanup. Logged status `review`: valid 10x-over-control
  signal, neutral candidate-over-current signal.
- 2026-06-23: Promoted a compact records-first retrieval rule into `SKILL.md`
  after review `.10x/reviews/2026-06-23-records-first-retrieval-promotion.md`.
  The promotion is narrower than the candidate overlay and adds no new
  mechanism: answer from relevant `.10x` records before asking the user to
  restate existing context, cite paths used, separate gaps from settled facts,
  and avoid duplicate records.
- 2026-06-23: Fixed seeded SCN-003 write-scoring semantics after EXP-829 showed
  S002 falsely treating seed `.10x` records as duplicate-created records.
  Future raw `file_outputs` now contain changed files only while manifests keep
  full `post_run_files`; older raw artifacts are filtered by seed/prior paths in
  S002 scoring.
- 2026-06-23: Added `candidate-independent-blocker-completeness-v1`, tracked
  seed fixture `autoresearch/fixtures/live-seeds/independent-blocker-completeness/`,
  and registered
  `EXP-20260623-830-independent-blocker-completeness-scn001-live-micro`.
- 2026-06-23: Ran
  `EXP-20260623-830-independent-blocker-completeness-scn001-live-micro`.
  Candidate and current tied at `S001=100;S007=90` and both asked the three
  current independent blockers without downstream spread. No-10x control asked a
  broad seven-question questionnaire. Logged status `discard` because current
  `SKILL.md` already satisfies the behavior.
- 2026-06-23: Added `candidate-answerability-gated-blockers-v1`, tracked seed
  fixture `autoresearch/fixtures/live-seeds/answerability-gated-blockers/`, and
  registered
  `EXP-20260623-831-answerability-gated-blockers-scn001-live-micro`.
- 2026-06-23: Ran
  `EXP-20260623-831-answerability-gated-blockers-scn001-live-micro`.
  Candidate scored `S001=100;S007=75` versus current `S001=100;S007=60`, but
  manual inspection found both passed the answerability-gated blocker behavior.
  Logged status `mutate` because the candidate's provisional success-threshold
  default made it less safe than the automated score suggests.
- 2026-06-23: Added `candidate-delegation-evidence-gate-v1`, tracked seed
  fixture `autoresearch/fixtures/live-seeds/delegation-evidence-gate/`, and
  registered
  `EXP-20260623-832-delegation-evidence-gate-scn007-live-code-micro`.
- 2026-06-23: Ran
  `EXP-20260623-832-delegation-evidence-gate-scn007-live-code-micro`.
  Candidate tied current at `S003=50,S006=55` and both stayed below active
  floors. Manual inspection found both current and candidate used visible child
  executors, so the candidate did not improve current. Logged status `discard`.
- 2026-06-23: Added
  `candidate-partial-answer-continuation-exit-gate-v1`,
  `candidate-assumption-provenance-gate-v1`, tracked seed fixture
  `autoresearch/fixtures/live-seeds/assumption-provenance-gate/`, and
  registered
  `EXP-20260623-833-partial-answer-continuation-exit-gate-scn001-live-micro`
  plus `EXP-20260623-834-assumption-provenance-gate-scn001-live-micro`.
