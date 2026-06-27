export function isEscalatedRefund(refund) {
  return Boolean(refund.chargebackOpen || refund.manualReview || refund.priorAbuseFlag);
}
