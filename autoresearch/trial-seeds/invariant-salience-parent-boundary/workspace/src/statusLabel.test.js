import { statusLabel } from "./statusLabel.js";

if (statusLabel("active") !== "Active") {
  throw new Error("active label failed");
}

if (statusLabel("archived") !== "Archived") {
  throw new Error("archived label failed");
}

console.log("statusLabel.test.js passed");
