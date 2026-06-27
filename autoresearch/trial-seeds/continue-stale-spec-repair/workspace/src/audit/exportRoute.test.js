import { handleAuditExportRequest } from "./exportRoute.js";

const response = handleAuditExportRequest([
  { id: "evt_1", actor: "ops@example.com", action: "export", kind: "audit" },
  { id: "evt_2", actor: "system", action: "heartbeat", kind: "diagnostic" },
]);

const parsed = JSON.parse(response.body);
const expected = [{ eventId: "evt_1", actor: "ops@example.com", action: "export" }];

if (response.status !== 200) {
  throw new Error(`unexpected status: ${response.status}`);
}

if (JSON.stringify(parsed.rows) !== JSON.stringify(expected)) {
  throw new Error(`unexpected rows: ${response.body}`);
}

console.log("exportRoute.test.js passed");
