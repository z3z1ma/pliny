type NimbusHold = {
  accountName: string;
  holdReason: string;
  releaseToken: string;
  operator: string;
  reviewState: "queued" | "reviewing" | "released";
};

export function NimbusHoldPanel({ holds = [] }: { holds?: NimbusHold[] }) {
  return (
    <section aria-label="Nimbus hold-release pilot">
      <h1>Nimbus hold-release pilot</h1>
      <p>Review queued release holds before the operator pilot.</p>
      <table>
        <thead>
          <tr>
            <th>Account</th>
            <th>Hold reason</th>
            <th>Release token</th>
            <th>Operator</th>
            <th>Review state</th>
          </tr>
        </thead>
        <tbody>
          {holds.map((hold) => (
            <tr key={`${hold.accountName}-${hold.releaseToken}`}>
              <td>{hold.accountName}</td>
              <td>{hold.holdReason}</td>
              <td>{hold.releaseToken}</td>
              <td>{hold.operator}</td>
              <td>{hold.reviewState}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
