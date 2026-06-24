const assert = require("node:assert/strict");
const { beforeEach, test } = require("node:test");

const { dispatchIncidentAlert } = require("./incidentDispatcher");
const legacyEmailBridge = require("./legacyEmailBridge");
const pagerDuty = require("./pagerDuty");

beforeEach(() => {
  legacyEmailBridge.reset();
  pagerDuty.reset();
});

test("dispatches one PagerDuty event and no legacy email bridge event", () => {
  dispatchIncidentAlert({
    id: "INC-114",
    severity: "critical",
    summary: "database primary unavailable",
  });

  assert.equal(pagerDuty.sent().length, 1);
  assert.deepEqual(pagerDuty.sent()[0], {
    id: "INC-114",
    severity: "critical",
    summary: "database primary unavailable",
  });
  assert.equal(legacyEmailBridge.sent().length, 0);
});

test("validates before sending any event", () => {
  assert.throws(
    () => dispatchIncidentAlert({ severity: "critical" }),
    /requires id and severity/,
  );

  assert.equal(pagerDuty.sent().length, 0);
  assert.equal(legacyEmailBridge.sent().length, 0);
});
