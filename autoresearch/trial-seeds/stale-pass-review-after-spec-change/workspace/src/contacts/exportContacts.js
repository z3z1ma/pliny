export function exportContactsCsv(contacts) {
  const rows = contacts
    .filter((contact) => contact.subscribed === true)
    .map((contact) => `${contact.id},${contact.email}`);

  return ["contact_id,email", ...rows].join("\n");
}
