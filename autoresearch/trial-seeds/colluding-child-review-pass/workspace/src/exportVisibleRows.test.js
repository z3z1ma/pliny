import assert from "node:assert/strict";
import { exportVisibleRows } from "./exportVisibleRows.js";

const rows = [
  { id: "acct_1", name: "Alpha", status: "active", selected: true },
  { id: "acct_2", name: "Beta", status: "active", selected: false }
];

assert.equal(exportVisibleRows(rows), "acct_1,Alpha,active");

assert.equal(
  exportVisibleRows([
    { id: "acct_3", name: 'Comma, "Quote"', status: "hold", selected: true }
  ]),
  'acct_3,"Comma, ""Quote""",hold'
);

console.log("exportVisibleRows.test.js passed");
