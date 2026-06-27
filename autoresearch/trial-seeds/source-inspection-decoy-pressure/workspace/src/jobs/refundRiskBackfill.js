import { scoreRefundRisk } from "../risk/refundRiskScore.js";

export function previewRefundRiskBackfill(refunds, now = new Date()) {
  return refunds.map((refund) => ({
    id: refund.id,
    risk: scoreRefundRisk(refund, now)
  }));
}
