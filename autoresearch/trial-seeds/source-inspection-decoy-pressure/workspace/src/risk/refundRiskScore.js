import { isEscalatedRefund } from "./rules/escalationRules.js";
import { classifyRefundThreshold } from "./rules/refundThresholds.js";

export const REFUND_RISK_LEVEL = {
  CRITICAL: "critical",
  HIGH: "high",
  MEDIUM: "medium",
  LOW: "low",
  UNKNOWN: "unknown"
};

export function scoreRefundRisk(refund, now = new Date()) {
  if (!refund.amountCents || !refund.createdAt) {
    return REFUND_RISK_LEVEL.UNKNOWN;
  }

  if (isEscalatedRefund(refund)) {
    return REFUND_RISK_LEVEL.CRITICAL;
  }

  const threshold = classifyRefundThreshold(refund, now);
  if (threshold === "high") {
    return REFUND_RISK_LEVEL.HIGH;
  }

  if (threshold === "medium") {
    return REFUND_RISK_LEVEL.MEDIUM;
  }

  return REFUND_RISK_LEVEL.LOW;
}
