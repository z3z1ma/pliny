import { RETRY_OFFSETS_DAYS, shouldScheduleRetry } from "./retrySchedule.js";

const actual = JSON.stringify(RETRY_OFFSETS_DAYS);
const expected = JSON.stringify([1, 3, 7, 14]);

if (actual !== expected) {
  throw new Error(`retry offsets changed: ${actual}`);
}

if (!shouldScheduleRetry({ status: "failed", cancelled: false })) {
  throw new Error("active failed invoices should schedule retry");
}

if (shouldScheduleRetry({ status: "failed", cancelled: true })) {
  throw new Error("cancelled failed invoices must not schedule retry");
}

console.log("retrySchedule.test.js passed");
