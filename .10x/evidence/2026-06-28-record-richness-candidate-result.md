Status: recorded
Created: 2026-06-28
Updated: 2026-06-28
Relates-To: .10x/tickets/done/2026-06-28-improve-record-richness-score.md, .10x/research/2026-06-28-record-richness-score-improvement.md, autoresearch/candidates/2026-06-28-record-regeneration-check.md

# Record Richness Candidate Result

## What Was Observed

Two Codex MICRO experiments tested the candidate
`autoresearch/candidates/2026-06-28-record-regeneration-check.md` against
canonical current 10x on existing `S010` seed workspaces.

Artifact roots:

- `.10x/evidence/.storage/2026-06-28-record-richness-score/record-regeneration-check-codex/`
- `.10x/evidence/.storage/2026-06-28-record-richness-score/record-regeneration-check-continuation-codex/`

Both runs completed successfully:

- Initial experiment: 4 raw artifacts, 4 live subject calls, 0 non-zero exits.
- Continuation experiment: 2 raw artifacts, 2 live subject calls, 0 non-zero
  exits.
- Both `canonical_guard.json` files reported `unchanged_during_run: true`.

## Procedure

1. Selected existing `S010` seeds:
   - `explicit-policy-ratification` / `SCN-006`.
   - `redacted-evidence-capture` / `SCN-008`.
2. Created candidate overlay:
   `autoresearch/candidates/2026-06-28-record-regeneration-check.md`.
3. Ran:

```bash
python3 autoresearch/run_once.py \
  --experiment .10x/research/.storage/2026-06-28-record-richness-score/experiment-record-regeneration-check.json \
  --out .10x/evidence/.storage/2026-06-28-record-richness-score/record-regeneration-check-codex \
  --require-clean-canonical
```

4. The current arm asked a valid clarification in `SCN-006`; registered and ran
   the continuation:

```bash
python3 autoresearch/run_once.py \
  --experiment .10x/research/.storage/2026-06-28-record-richness-score/experiment-record-regeneration-check-continuation.json \
  --out .10x/evidence/.storage/2026-06-28-record-richness-score/record-regeneration-check-continuation-codex \
  --require-clean-canonical
```

5. Inspected raw artifacts, last messages, changed-file manifests, reports, and
   archived `.10x` records for both arms.
6. Promoted only a compressed canonical replacement for the existing
   `SKILL.md` cold-reader paragraph, not the full candidate overlay.

## Findings

### Policy-Ticket Scenario

Initial run:

- Current arm correctly blocked on an ambiguous policy hole: under-USD-500
  payouts from sellers who fail age or chargeback eligibility were not
  explicitly routed.
- Candidate arm created rich records in one turn while preserving that hole as
  an open bound rather than silently defining final disposition.

Continuation after clarification:

- Current arm created rich records: policy ratification evidence, focused
  decisioning spec, focused review-notification spec, parent plan, and two child
  implementation tickets.
- Candidate arm updated its existing evidence, spec, parent, and child tickets
  to remove stale ambiguity and add explicit review routing for every
  non-auto-approved payout.

Manual `S010` judgment:

- Current after continuation: high quality. Strong focused specs and acceptance
  criteria; slightly less explicit cold-start context in child tickets.
- Candidate after continuation: high quality. Slightly less split at the spec
  layer, but stronger explicit cold-start context, references, design notes, and
  stale-ambiguity repair in tickets.
- Result: modest candidate advantage for `S010` ticket handoff richness, with no
  hard floor triggered.

### Evidence-Capture Scenario

- Current arm created a strong evidence record with command, exit status, raw
  artifact path, degraded status, failing check, limits, and detailed redaction
  shape.
- Candidate arm created a strong evidence record with the same core facts and
  limits, but redaction structure was a little less specific.
- Result: candidate preserved `S010` above floor but did not improve this seed.

## Score Judgment

This was not a broad win over current 10x. Current was already strong.

The candidate did identify a safe improvement: make the cold-reader rule
operational as a checklist at record-writing time. The promoted canonical text
captures that narrow behavioral gain while avoiding the candidate overlay's
extra prose.

Promotion judgment:

- Keep: compressed record regeneration check.
- Do not keep: full candidate overlay.
- Confidence: medium.
- `S010` expected movement: small positive on ticket/spec handoff richness;
  neutral on evidence records; no observed hard-floor regression.

## Validation

After promoting the compressed canonical wording:

```bash
python3 - <<'PY'
from autoresearch import validate
from pathlib import Path
print(validate.skill_body_char_count(Path('SKILL.md').read_text()))
PY
python3 autoresearch/validate.py
python3 -m unittest discover -s autoresearch/tests
git diff --check
```

Observed:

- `SKILL.md` body character count: `39912` under the `40000` budget.
- `python3 autoresearch/validate.py`: `autoresearch contracts valid`.
- `python3 -m unittest discover -s autoresearch/tests`: 60 tests passed.
- `git diff --check`: no whitespace or conflict-marker issues.

## What This Supports Or Challenges

Supports:

- A short cold-start regeneration check is useful enough to promote when kept
  inside the existing Record Graph rule.
- Multi-turn handling is necessary for fair scoring; the current arm's
  clarification question was a correct behavior, not a failure.
- The runner preserved enough raw data to compare first-turn and continuation
  behavior.

Challenges:

- The candidate overlay did not materially improve the redacted evidence seed.
- The result should not be described as a large `S010` jump. It is a modest
  robustness improvement to an already strong current skill.

## Limits

Only Codex was tested in this iteration. OpenCode and broader seed replay were
not rerun. The promoted canonical wording is a compressed semantic equivalent
of the useful candidate behavior, not a verbatim promotion of the candidate
overlay.
