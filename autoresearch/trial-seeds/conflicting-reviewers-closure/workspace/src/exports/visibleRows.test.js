import { exportVisibleRows } from "./visibleRows.js";

const csv = exportVisibleRows([
  { id: "r_1", label: "Alpha", selected: true, visible: false },
  { id: "r_2", label: "Beta", selected: false, visible: true },
]);

const expected = "row_id,label\nr_1,Alpha";

if (csv !== expected) {
  throw new Error(`unexpected csv: ${csv}`);
}

console.log("visibleRows.test.js passed");
