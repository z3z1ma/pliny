import { exportVisibleRows } from "./visibleRows.js";

const csv = exportVisibleRows([
  { id: "r_1", label: "Alpha", selected: true, visible: false },
  { id: "r_2", label: "Beta", selected: false, visible: true },
  { id: "r_3", label: "Gamma", selected: true, visible: true, policyHidden: true },
  { id: "r_4", label: "Delta", selected: true, visible: true, policyHidden: false },
]);

const expected = "row_id,label\nr_2,Beta\nr_4,Delta";

if (csv !== expected) {
  throw new Error(`unexpected csv: ${csv}`);
}

console.log("visibleRows.test.js passed");
