import test from "node:test";
import assert from "node:assert/strict";
import { exportVisibleRows } from "./exportVisibleRows.js";

test("exports only the header for empty visible rows", () => {
  assert.equal(
    exportVisibleRows([]),
    "customer_id,account_name,exception_reason,requested_discount_pct,status,requested_by,created_at"
  );
});

test("escapes visible row values", () => {
  const csv = exportVisibleRows([
    {
      customer_id: "cus_123",
      account_name: "Northwind, Inc.",
      exception_reason: "Renewal \"uplift\"\napproved",
      requested_discount_pct: 18,
      status: "pending_review",
      requested_by: "maria@example.com",
      created_at: "2026-06-20"
    }
  ]);

  assert.match(csv, /"Northwind, Inc\."/);
  assert.match(csv, /"Renewal ""uplift""\napproved"/);
});
