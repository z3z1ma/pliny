import { exportContactsCsv } from "./exportContacts.js";

const csv = exportContactsCsv([
  { id: "c_1", email: "a@example.com", subscribed: true },
  { id: "c_2", email: "b@example.com", subscribed: false },
]);

const expected = "contact_id,email\nc_1,a@example.com";

if (csv !== expected) {
  throw new Error(`unexpected csv: ${csv}`);
}

console.log("exportContacts.test.js passed");
