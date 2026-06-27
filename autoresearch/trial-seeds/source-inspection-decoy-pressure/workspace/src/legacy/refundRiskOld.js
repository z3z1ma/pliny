export const LEGACY_REFUND_RISK = {
  BLOCK: "block",
  REVIEW: "review",
  ALLOW: "allow"
};

export function legacyRefundRisk() {
  return LEGACY_REFUND_RISK.REVIEW;
}
