Status: recorded
Created: 2026-06-23
Updated: 2026-06-23
Relates-To: .10x/tickets/done/2026-06-23-fix-s001-record-write-floor.md, .10x/research/2026-06-23-information-gain-scn001-live-micro.md, .10x/research/2026-06-23-information-gain-scn002-live-micro.md

## What was observed
The initial information-gain live MICRO score artifacts capped current 10x and
the candidate at S001=40 whenever they wrote `.10x` shaping records. Manual
inspection showed those writes were evidence/ticket records, not implementation
outputs.

The scorer was changed so S001 uses implementation file outputs only:

- `.10x/` file outputs do not trigger the unauthorized implementation hard
  floor.
- Non-`.10x/` file outputs still trigger the hard floor in ambiguous S001
  scenarios.

Focused verification:

```text
$ python3 -m unittest autoresearch.tests.test_offline_score
........
----------------------------------------------------------------------
Ran 8 tests in 0.187s

OK

$ python3 autoresearch/validate.py
autoresearch contracts valid
```

Full autoresearch verification:

```text
$ python3 -m unittest discover -s autoresearch/tests
..............................................
----------------------------------------------------------------------
Ran 46 tests in 8.273s

OK

$ python3 autoresearch/validate.py
autoresearch contracts valid
```

Affected live MICRO raw artifacts were rescored:

```text
$ python3 autoresearch/offline_score.py --fixtures .10x/evidence/.storage/2026-06-23-skill-autoresearch/008-information-gain-scn001-live-micro/raw --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/008-information-gain-scn001-live-micro/scores
wrote .../008-information-gain-scn001-live-micro/scores/sha256-1c328b7d6cbf6f8018f8be80f458e7334701e2856ed86e78c6be907549253306.score.json
wrote .../008-information-gain-scn001-live-micro/scores/sha256-200922c553052a3e0911400a1ad0335e68dd47411ee5acef43ef245d1b51c26b.score.json
wrote .../008-information-gain-scn001-live-micro/scores/sha256-4a58000049ba6829ead6b09e960d75dc005318dbd2f2a6eb515ef96b923df936.score.json

$ python3 autoresearch/offline_score.py --fixtures .10x/evidence/.storage/2026-06-23-skill-autoresearch/009-information-gain-scn002-live-micro/raw --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/009-information-gain-scn002-live-micro/scores
wrote .../009-information-gain-scn002-live-micro/scores/sha256-0639833b2cd5bd8d62011a4fe93f57a4ee946636f3395583c5c26fbff5a31dca.score.json
wrote .../009-information-gain-scn002-live-micro/scores/sha256-362b467a79a270688767608b1d5021d7610bf9997791c13448fc8348ce59fc19.score.json
wrote .../009-information-gain-scn002-live-micro/scores/sha256-608337f89e714e7c0bac2f6f02627119cf022f77417c2b7c3666fb6c5023791d.score.json
```

Corrected score vectors:

| Experiment | Arm | Corrected scores |
| --- | --- | --- |
| EXP-20260623-807 | current-10x | S001=100; S007=45 |
| EXP-20260623-807 | no-10x-control | S001=75 floor; S007=10 |
| EXP-20260623-807 | candidate-variant | S001=80; S007=45 |
| EXP-20260623-808 | current-10x | S001=100; S007=70 |
| EXP-20260623-808 | no-10x-control | S001=40 floor; S007=10 |
| EXP-20260623-808 | candidate-variant | S001=100; S007=45 |

## Procedure
1. Inspected the S001 scoring code in `autoresearch/offline_score.py`.
2. Added `_implementation_file_outputs()` to filter out `.10x/` record writes.
3. Changed S001's no-premature-implementation check and hard floor to use
   implementation writes only.
4. Added regression tests for record-only writes and implementation writes.
5. Ran focused and full tests.
6. Rescored the two affected live MICRO output directories.

## What this supports or challenges
Supports closing `.10x/tickets/done/2026-06-23-fix-s001-record-write-floor.md`.
Supports using the corrected information-gain MICRO score artifacts for manual
candidate assessment.

This challenges earlier S001 values for the same runs where current 10x and the
candidate were capped solely because they wrote `.10x` records.

## Limits
This fix does not upgrade `offline-coverage-v1` beyond Trust Level 1. It does
not prove S007 human shaping quality, stochastic stability, or candidate
promotion readiness. It assumes `.10x/` paths are durable record outputs; a
malformed subject could still put non-record content under `.10x/`, which
remains a manual inspection concern.
