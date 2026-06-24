export function auditEvent(type, details) {
  return {
    type,
    at: details.at ?? null,
    actorId: details.actorId ?? null,
    subjectId: details.subjectId ?? null,
    metadata: details.metadata ?? {}
  };
}
