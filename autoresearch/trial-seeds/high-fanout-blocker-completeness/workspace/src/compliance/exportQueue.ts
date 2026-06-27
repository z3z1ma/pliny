export type ComplianceExportRequest = {
  id: string;
  accountId: string;
  requesterId: string;
  status: "pending" | "approved" | "rejected" | "expired";
};

export function listPendingComplianceExports(
  requests: ComplianceExportRequest[],
): ComplianceExportRequest[] {
  return requests.filter((request) => request.status === "pending");
}
