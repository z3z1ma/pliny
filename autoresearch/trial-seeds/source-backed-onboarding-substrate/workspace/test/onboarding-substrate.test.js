import test from "node:test";
import assert from "node:assert/strict";
import { canManageInvites } from "../src/auth/session.js";
import { maxDeliveryRetries } from "../src/jobs/retryInvitationDelivery.js";
import { systemActor } from "../src/audit/log.js";

test("fixture substrate exposes settled onboarding constants", () => {
  assert.equal(canManageInvites({ role: "admin" }), true);
  assert.equal(canManageInvites({ role: "viewer" }), false);
  assert.equal(maxDeliveryRetries, 3);
  assert.equal(systemActor, "system");
});
