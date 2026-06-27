export function evaluateInstantPayout(request) {
  return {
    payoutId: request.payoutId,
    status: "manual_review_required",
    reviewerContext: {
      amountCents: request.amountCents,
      sellerRiskTier: request.sellerRiskTier
    }
  };
}
