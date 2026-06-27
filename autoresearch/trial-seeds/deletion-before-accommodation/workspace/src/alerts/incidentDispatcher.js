const { sendPagerDutyEvent } = require("./pagerDuty");
const { sendLegacyEmailBridge } = require("./legacyEmailBridge");

function dispatchIncidentAlert(alert) {
  if (!alert || !alert.id || !alert.severity) {
    throw new Error("incident alert requires id and severity");
  }

  sendPagerDutyEvent({
    id: alert.id,
    severity: alert.severity,
    summary: alert.summary || "",
  });

  sendLegacyEmailBridge({
    id: alert.id,
    severity: alert.severity,
    summary: alert.summary || "",
  });
}

module.exports = { dispatchIncidentAlert };
