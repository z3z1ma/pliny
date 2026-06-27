export function routeRefundForReview(refund) {
  if (refund.amountUsd > 500) {
    return { queue: "manual-review", priority: "normal" };
  }

  return { queue: "auto-eligible", priority: "normal" };
}

export function prioritizeReviewQueueItem(item) {
  return { ...item, priority: "urgent" };
}
