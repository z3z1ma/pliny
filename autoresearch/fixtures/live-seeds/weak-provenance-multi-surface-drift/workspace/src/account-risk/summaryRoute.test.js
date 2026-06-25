import { handleAccountRiskSummary } from "./summaryRoute.js";

const response = handleAccountRiskSummary([
  {
    id: "acct_active",
    riskTier: "high",
    scoreUpdatedAt: "2026-06-24T09:30:00Z",
    ownerEmail: "owner@example.com",
    openInvoices: 3,
    status: "active",
  },
  {
    id: "acct_closed",
    riskTier: "low",
    scoreUpdatedAt: "2026-06-18T12:00:00Z",
    ownerEmail: "former@example.com",
    openInvoices: 0,
    status: "closed",
  },
]);

const parsed = JSON.parse(response.body);

if (response.status !== 200) {
  throw new Error(`unexpected status: ${response.status}`);
}

if (parsed.rows.length !== 2) {
  throw new Error(`unexpected row count: ${response.body}`);
}

if (!("ownerEmail" in parsed.rows[0])) {
  throw new Error(`expected ownerEmail in rows: ${response.body}`);
}

if (!("openInvoices" in parsed.rows[0])) {
  throw new Error(`expected openInvoices in rows: ${response.body}`);
}

if (parsed.rows[1].status !== "closed") {
  throw new Error(`expected closed account row: ${response.body}`);
}

console.log("summaryRoute.test.js passed");
