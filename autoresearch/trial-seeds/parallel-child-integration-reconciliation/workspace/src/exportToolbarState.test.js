import assert from "node:assert/strict";
import { isExportEnabled } from "./exportToolbarState.js";

assert.equal(
  isExportEnabled([
    { id: "acct_1", name: "Alpha", selected: false },
    { id: "acct_2", name: "Beta", selected: true }
  ]),
  true
);

assert.equal(
  isExportEnabled([
    { id: "acct_3", name: "Gamma", selected: false }
  ]),
  false
);

console.log("exportToolbarState.test.js passed");
