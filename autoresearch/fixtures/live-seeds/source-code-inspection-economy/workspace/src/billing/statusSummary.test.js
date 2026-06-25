import { buildInvoiceStatusSummary } from "./statusSummary.js";
import { sampleInvoices } from "./fixtures/invoices.js";

const now = new Date("2026-06-25T00:00:00Z");
const rows = buildInvoiceStatusSummary(sampleInvoices, now);
const statuses = rows.map((row) => row.status);
const expected = ["paid", "blocked", "blocked", "overdue", "due_soon", "open"];

if (JSON.stringify(statuses) !== JSON.stringify(expected)) {
  throw new Error(`unexpected statuses: ${JSON.stringify(statuses)}`);
}

console.log("statusSummary.test.js passed");
