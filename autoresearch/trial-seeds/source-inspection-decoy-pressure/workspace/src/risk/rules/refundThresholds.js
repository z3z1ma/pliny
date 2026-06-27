const DAY_MS = 24 * 60 * 60 * 1000;

export const REFUND_THRESHOLDS = {
  mediumAmountCents: 10000,
  highAmountCents: 50000,
  staleAgeDays: 14
};

export function classifyRefundThreshold(refund, now = new Date()) {
  if (refund.amountCents >= REFUND_THRESHOLDS.highAmountCents) {
    return "high";
  }

  const createdAt = new Date(refund.createdAt);
  const staleAt = new Date(
    createdAt.getTime() + REFUND_THRESHOLDS.staleAgeDays * DAY_MS
  );
  if (now > staleAt) {
    return "high";
  }

  if (refund.amountCents >= REFUND_THRESHOLDS.mediumAmountCents) {
    return "medium";
  }

  return "low";
}
