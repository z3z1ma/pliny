const {
  RETRY_HORIZON_HOURS,
  eventKey,
  shouldDeadLetter,
  shouldRetry,
} = require("./webhookRetry");
const assert = require("node:assert/strict");
const test = require("node:test");

test("uses legacy dedupe id", () => {
  assert.equal(eventKey({ dedupeId: "evt_legacy", id: "evt_current" }), "evt_legacy");
});

test("retries all non-2xx responses including conflict", () => {
  assert.equal(shouldRetry(409), true);
  assert.equal(shouldRetry(500), true);
  assert.equal(shouldRetry(204), false);
});

test("dead letters after legacy 72 hour horizon", () => {
  const start = new Date("2026-06-01T00:00:00Z");
  const now = new Date("2026-06-04T00:00:00Z");
  assert.equal(RETRY_HORIZON_HOURS, 72);
  assert.equal(shouldDeadLetter(start, now), true);
});
