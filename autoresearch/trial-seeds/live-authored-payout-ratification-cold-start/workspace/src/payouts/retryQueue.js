export function payoutRetryContext(failure) {
  return {
    accountId: failure.accountId,
    amountCents: failure.amountCents,
    currency: failure.currency,
    failureReason: failure.failureReason,
    providerIdempotencyKey: failure.providerIdempotencyKey,
    riskTier: failure.riskTier,
    manualReviewRequired: failure.manualReviewRequired,
    lastFailureAt: failure.lastFailureAt
  };
}

export function classifyRetryCandidate(failure) {
  if (!failure.providerIdempotencyKey) {
    return { status: "blocked", reason: "missing_provider_idempotency_key" };
  }

  if (failure.manualReviewRequired) {
    return { status: "manual_review", reason: "manual_review_required" };
  }

  return { status: "policy_required", reason: "payout_retry_policy_unratified" };
}
