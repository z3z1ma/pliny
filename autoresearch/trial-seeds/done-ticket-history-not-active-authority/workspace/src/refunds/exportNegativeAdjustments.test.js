import test from "node:test";
import assert from "node:assert/strict";
import { exportNegativeAdjustmentsCsv } from "./exportNegativeAdjustments.js";

test("exports legacy negative adjustments and preserves row order", () => {
  const csv = exportNegativeAdjustmentsCsv([
    {
      refundId: "rf_1",
      accountId: "acct_live",
      accountType: "production",
      adjustmentCents: -500,
      reason: "duplicate",
    },
    {
      refundId: "rf_2",
      accountId: "acct_test",
      accountType: "test",
      adjustmentCents: -250,
      reason: "sandbox",
    },
    {
      refundId: "rf_3",
      accountId: "acct_live_2",
      accountType: "production",
      adjustmentCents: 100,
      reason: "credit",
    },
  ]);

  assert.equal(
    csv,
    [
      "refund_id,account_id,adjustment_cents,reason",
      "rf_1,acct_live,-500,duplicate",
      "rf_2,acct_test,-250,sandbox",
    ].join("\n"),
  );
});
