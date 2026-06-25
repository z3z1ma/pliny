import { previewSettlementRows } from "./reconcile.js";

const rows = previewSettlementRows([
  {
    settlementRef: "stl_123",
    amount: 12.34,
    lifecycleState: "pending_release",
  },
]);

if (rows[0].settlementRef !== "stl_123") {
  throw new Error("settlementRef was not preserved");
}

if (rows[0].amountCents !== 1234) {
  throw new Error("amount was not normalized");
}

if (rows[0].lifecycleState !== "pending_release") {
  throw new Error("lifecycleState was not preserved");
}

console.log("reconcile.test.js passed");
