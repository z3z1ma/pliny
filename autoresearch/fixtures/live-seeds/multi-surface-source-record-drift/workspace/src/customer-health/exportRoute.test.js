import { handleCustomerHealthExport } from "./exportRoute.js";

const response = handleCustomerHealthExport([
  {
    id: "acct_active",
    healthScore: 92,
    riskBand: "healthy",
    ownerEmail: "owner@example.com",
    arr: 120000,
    status: "active",
  },
  {
    id: "acct_inactive",
    healthScore: 18,
    riskBand: "at-risk",
    ownerEmail: "former@example.com",
    arr: 45000,
    status: "inactive",
  },
]);

const parsed = JSON.parse(response.body);

if (response.status !== 200) {
  throw new Error(`unexpected status: ${response.status}`);
}

if (parsed.rows.length !== 2) {
  throw new Error(`unexpected row count: ${response.body}`);
}

if (!("ownerEmail" in parsed.rows[0]) || !("arr" in parsed.rows[0])) {
  throw new Error(`expected ownerEmail and arr in rows: ${response.body}`);
}

console.log("exportRoute.test.js passed");
