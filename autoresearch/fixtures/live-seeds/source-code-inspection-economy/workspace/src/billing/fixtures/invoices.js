export const sampleInvoices = [
  {
    id: "inv_paid",
    customerId: "cus_1",
    paidAt: "2026-06-20T10:00:00Z",
    dueAt: "2026-06-22T00:00:00Z"
  },
  {
    id: "inv_hold",
    customerId: "cus_2",
    manualHold: true,
    dueAt: "2026-06-24T00:00:00Z"
  },
  {
    id: "inv_dispute",
    customerId: "cus_3",
    disputeId: "disp_123",
    dueAt: "2026-06-24T00:00:00Z"
  },
  {
    id: "inv_overdue",
    customerId: "cus_4",
    dueAt: "2026-06-20T00:00:00Z"
  },
  {
    id: "inv_due_soon",
    customerId: "cus_5",
    dueAt: "2026-06-29T00:00:00Z"
  },
  {
    id: "inv_open",
    customerId: "cus_6",
    dueAt: "2026-07-20T00:00:00Z"
  }
];
