import assert from "node:assert/strict";
import test from "node:test";

import { buildVendorTaxExport } from "../src/export/vendorTaxExport.js";

test("exports vendor tax identifiers as last four only", () => {
  assert.deepEqual(
    buildVendorTaxExport([{ vendorId: "ven_1", taxId: "12-3456789" }]),
    [{ vendorId: "ven_1", taxLast4: "6789" }],
  );
});
