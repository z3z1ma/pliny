export function getAuditExportRows(events) {
  return events
    .filter((event) => event.kind !== "diagnostic")
    .map((event) => ({
      eventId: event.id,
      actor: event.actor,
      action: event.action,
    }));
}

export function handleAuditExportRequest(events) {
  return {
    status: 200,
    body: JSON.stringify({ rows: getAuditExportRows(events) }),
  };
}
