import assert from "node:assert/strict";
import test from "node:test";

import { exportRetryInvoicesCsv } from "./exportRetryInvoices.js";

test("exports retryable delinquent enterprise invoices", () => {
  const csv = exportRetryInvoicesCsv([
    {
      invoiceId: "inv-enterprise",
      accountId: "acct-ent",
      amountCents: 5000,
      status: "delinquent",
      retryEligible: true,
      enterprise: true,
      accountType: "production",
      cancelledAt: null,
    },
    {
      invoiceId: "inv-growth",
      accountId: "acct-growth",
      amountCents: 4100,
      status: "delinquent",
      retryEligible: true,
      enterprise: false,
      accountType: "production",
      cancelledAt: null,
    },
  ]);

  assert.equal(
    csv,
    [
      "invoice_id,account_id,amount_cents",
      "inv-enterprise,acct-ent,5000",
    ].join("\n"),
  );
});
