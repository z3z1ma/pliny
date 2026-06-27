export function refundAutoApprovalContext(refund) {
  return {
    refundId: refund.refundId,
    accountId: refund.accountId,
    amountCents: refund.amountCents,
    riskTier: refund.riskTier,
    manualReviewRequired: refund.manualReviewRequired,
    failureReason: refund.failureReason
  };
}

export function classifyRefundApproval(refund) {
  if (refund.manualReviewRequired) {
    return { status: "manual_review", reason: "manual_review_required" };
  }

  return { status: "policy_required", reason: "refund_policy_unratified" };
}
