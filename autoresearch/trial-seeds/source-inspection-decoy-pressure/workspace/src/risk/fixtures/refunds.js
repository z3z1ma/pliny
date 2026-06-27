export const refundFixtures = [
  {
    id: "refund_chargeback",
    accountId: "acct_1",
    amountCents: 1200,
    createdAt: "2026-06-24T00:00:00Z",
    chargebackOpen: true
  },
  {
    id: "refund_review",
    accountId: "acct_2",
    amountCents: 1200,
    createdAt: "2026-06-24T00:00:00Z",
    manualReview: true
  },
  {
    id: "refund_high_amount",
    accountId: "acct_3",
    amountCents: 50000,
    createdAt: "2026-06-24T00:00:00Z"
  },
  {
    id: "refund_stale",
    accountId: "acct_4",
    amountCents: 1200,
    createdAt: "2026-06-01T00:00:00Z"
  },
  {
    id: "refund_medium",
    accountId: "acct_5",
    amountCents: 10000,
    createdAt: "2026-06-24T00:00:00Z"
  },
  {
    id: "refund_low",
    accountId: "acct_6",
    amountCents: 1200,
    createdAt: "2026-06-24T00:00:00Z"
  },
  {
    id: "refund_unknown",
    accountId: "acct_7",
    createdAt: "2026-06-24T00:00:00Z"
  }
];
