Status: recorded
Created: 2026-06-25
Updated: 2026-06-25
Relates-To: .10x/research/2026-06-25-post-cold-start-exact-ratification-scn006-live-micro.md

# Post-Cold-Start Exact-Ratification Result

## What Was Observed

Ran `EXP-20260625-955-post-cold-start-exact-ratification-scn006-live-micro`
with three repetitions each for no-10x-control, current-10x, and
duplicate-current.

Raw artifacts:

`.10x/evidence/.storage/2026-06-23-skill-autoresearch/220-post-cold-start-exact-ratification-scn006-live-micro/`

`canonical_guard.json` reported `SKILL.md` and `autoresearch/program.md`
unchanged during the run.

The offline scorer gave S003 Ticket Readiness=100 for all nine samples. Manual
inspection found all current and duplicate-current repetitions:

- preserved refund cap `$250`, predicate `riskTier === "low"`, successful
  notification destination `#refund-ops`, Refund Ops ownership, and one
  30-minute retry;
- preserved the existing audit implementation ticket and active audit spec;
- added final escalation behavior: `manualReviewRequired=true`,
  `failureReason="risk_escalation"`, internal notice `#refund-risk`, Risk Ops
  follow-up ownership, and no customer notification;
- promoted `.10x/specs/refund-auto-approval.md` to `active`;
- created exactly one `.10x/tickets/2026-06-25-implement-refund-auto-approval.md`;
- avoided source and test edits;
- avoided duplicate audit specs, duplicate audit tickets, and duplicate refund
  implementation tickets.

Two current repetitions and one duplicate-current repetition also updated
`.10x/knowledge/payout-risk-terms.md` with final refund risk escalation
vocabulary. The additions explicitly preserved the refund/payout boundary and
did not cross-apply payout semantics into the refund ticket or spec.

## Procedure

1. Copied a reviewed current-10x handoff workspace into
   `autoresearch/trial-seeds/post-cold-start-exact-ratification/`.
2. Registered
   `.10x/research/2026-06-25-post-cold-start-exact-ratification-scn006-live-micro.md`.
3. Ran:

   ```bash
   python3 autoresearch/run_once.py --experiment .10x/research/2026-06-25-post-cold-start-exact-ratification-scn006-live-micro.md --out .10x/evidence/.storage/2026-06-23-skill-autoresearch/220-post-cold-start-exact-ratification-scn006-live-micro --require-clean-canonical
   ```

4. Inspected the report, canonical guard, workspace manifests, final messages,
   changed-file lists, refund specs, refund implementation tickets, shaping
   tickets, review notes, and knowledge edits.

## What This Supports Or Challenges

This supports current `SKILL.md` against over-conservatism after strict
cold-start blocker preservation. Once the remaining semantic blocker was
explicitly ratified, current and duplicate-current proceeded to executable
ticket readiness without implementation edits.

## Limits

This was still a one-turn Codex CLI continuation. It does not prove real
subagent execution of the refund ticket or multi-day parent/child coherence.
