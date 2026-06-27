import { reportExportUrl } from "./exportUrl.js";

export function ReportsToolbar({ filters }) {
  return (
    <nav aria-label="Reports actions">
      <a href={reportExportUrl(filters)} download>
        Export CSV
      </a>
    </nav>
  );
}
