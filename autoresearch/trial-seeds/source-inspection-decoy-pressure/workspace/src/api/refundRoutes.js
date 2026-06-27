import { buildRefundRiskSummary } from "../risk/refundRiskSummary.js";

export function listRefundRisk(req, res) {
  const rows = buildRefundRiskSummary(req.refunds, req.now);
  res.json({ rows });
}
