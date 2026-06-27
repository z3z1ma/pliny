const assert = require("node:assert/strict");
const { buildAccountExportRows } = require("./accountExport");

const rows = buildAccountExportRows([
  {
    accountId: "a1",
    status: "active",
    balanceCents: 1200,
    email: "visible@example.test",
    isVisible: true,
    isTest: false,
  },
  {
    accountId: "a2",
    status: "active",
    balanceCents: 3400,
    email: "hidden@example.test",
    isVisible: false,
    isTest: false,
  },
  {
    accountId: "a3",
    status: "test",
    balanceCents: 5600,
    email: "test@example.test",
    isVisible: true,
    isTest: true,
  },
]);

assert.deepEqual(rows, [
  {
    accountId: "a1",
    status: "active",
    balanceCents: 1200,
  },
]);

console.log("accountExport.test.js passed");
