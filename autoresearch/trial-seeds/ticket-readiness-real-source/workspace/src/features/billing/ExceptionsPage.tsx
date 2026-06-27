import { PricingExceptionsTable } from "./PricingExceptionsTable";
import { usePricingExceptions } from "./usePricingExceptions";

export function ExceptionsPage() {
  const { visibleRows, isLoading } = usePricingExceptions();

  return (
    <section>
      <header>
        <h1>Pricing exceptions</h1>
      </header>

      <PricingExceptionsTable rows={visibleRows} isLoading={isLoading} />
    </section>
  );
}
