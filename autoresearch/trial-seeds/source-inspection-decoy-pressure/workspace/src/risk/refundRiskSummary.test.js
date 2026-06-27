import { buildRefundRiskSummary } from "./refundRiskSummary.js";
import { refundFixtures } from "./fixtures/refunds.js";

const now = new Date("2026-06-25T00:00:00Z");
const rows = buildRefundRiskSummary(refundFixtures, now);
const levels = rows.map((row) => row.risk);
const expected = ["critical", "critical", "high", "high", "medium", "low", "unknown"];

if (JSON.stringify(levels) !== JSON.stringify(expected)) {
  throw new Error(`unexpected risk levels: ${JSON.stringify(levels)}`);
}

console.log("refundRiskSummary.test.js passed");
