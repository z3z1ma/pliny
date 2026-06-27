import { usePricingExceptions } from "./usePricingExceptions";

export function PricingExceptionsPage() {
  const { visibleExceptions } = usePricingExceptions();

  return (
    <section>
      <h1>Pricing exceptions</h1>
      <ul>
        {visibleExceptions.map((exception) => (
          <li key={exception.id}>
            {exception.accountName} - {exception.status} - ARR impact:
            {exception.arrImpactUsd} - Renewal: {exception.renewalDate}
          </li>
        ))}
      </ul>
    </section>
  );
}
