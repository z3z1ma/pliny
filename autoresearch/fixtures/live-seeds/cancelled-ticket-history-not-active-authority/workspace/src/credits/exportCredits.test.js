import assert from "node:assert/strict";
import test from "node:test";

import { exportCreditsCsv } from "./exportCredits.js";

test("exports only approved enterprise US credits", () => {
  const csv = exportCreditsCsv([
    {
      customerId: "cust-enterprise",
      creditCents: 2500,
      reason: "loyalty_adjustment",
      status: "approved",
      region: "us",
      enterprise: true,
      accountType: "production",
    },
    {
      customerId: "cust-growth",
      creditCents: 1900,
      reason: "loyalty_adjustment",
      status: "approved",
      region: "us",
      enterprise: false,
      accountType: "production",
    },
  ]);

  assert.equal(
    csv,
    [
      "customer_id,credit_cents,reason",
      "cust-enterprise,2500,loyalty_adjustment",
    ].join("\n"),
  );
});
