export function PricingExceptionsTable({ rows, isLoading }) {
  if (isLoading) {
    return <p>Loading exceptions...</p>;
  }

  return (
    <table>
      <thead>
        <tr>
          <th>Customer ID</th>
          <th>Account</th>
          <th>Reason</th>
          <th>Discount</th>
          <th>Status</th>
          <th>Requested by</th>
          <th>Created</th>
        </tr>
      </thead>
      <tbody>
        {rows.map((row) => (
          <tr key={row.customer_id}>
            <td>{row.customer_id}</td>
            <td>{row.account_name}</td>
            <td>{row.exception_reason}</td>
            <td>{row.requested_discount_pct}</td>
            <td>{row.status}</td>
            <td>{row.requested_by}</td>
            <td>{row.created_at}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
