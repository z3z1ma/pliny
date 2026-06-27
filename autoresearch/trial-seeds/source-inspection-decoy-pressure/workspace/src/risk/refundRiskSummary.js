import { scoreRefundRisk } from "./refundRiskScore.js";

export function buildRefundRiskSummary(refunds, now = new Date()) {
  return refunds.map((refund) => ({
    refundId: refund.id,
    accountId: refund.accountId,
    risk: scoreRefundRisk(refund, now)
  }));
}
