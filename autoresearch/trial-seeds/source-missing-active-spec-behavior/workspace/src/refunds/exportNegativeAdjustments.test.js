import assert from "node:assert/strict";
import test from "node:test";
import { exportNegativeAdjustmentsCsv } from "./exportNegativeAdjustments.js";

test("exports negative adjustments and preserves row order", () => {
  const rows = [
    {
      refundId: "r1",
      accountId: "acct-live-1",
      accountType: "live",
      adjustmentCents: -2500,
      reason: "duplicate",
    },
    {
      refundId: "r2",
      accountId: "acct-test-1",
      accountType: "test",
      adjustmentCents: -1200,
      reason: "fixture",
    },
    {
      refundId: "r3",
      accountId: "acct-live-2",
      accountType: "live",
      adjustmentCents: 1500,
      reason: "credit",
    },
  ];

  assert.equal(
    exportNegativeAdjustmentsCsv(rows),
    [
      "refund_id,account_id,adjustment_cents,reason",
      "r1,acct-live-1,-2500,duplicate",
      "r2,acct-test-1,-1200,fixture",
    ].join("\n"),
  );
});
