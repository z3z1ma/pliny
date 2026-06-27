export const systemActor = "system";

export function recordAudit(state, event, actor, targetEmail, workspaceId) {
  state.audit.push({
    event,
    actor,
    targetEmail,
    workspaceId,
    timestamp: new Date().toISOString()
  });
}
