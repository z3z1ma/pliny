export function evaluateInstantPayout(request) {
  if (request.sellerRiskTier === "low" && request.amountCents <= 50000) {
    return {
      payoutId: request.payoutId,
      status: "auto_approved"
    };
  }

  return {
    payoutId: request.payoutId,
    status: "manual_review_required",
    reviewerContext: {
      amountCents: request.amountCents,
      sellerRiskTier: request.sellerRiskTier
    }
  };
}
