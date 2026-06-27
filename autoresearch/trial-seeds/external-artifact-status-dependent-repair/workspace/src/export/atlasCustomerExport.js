export function atlasCustomerExportRow(customer) {
  return {
    customerId: customer.customerId,
    accountId: customer.accountId,
    email: customer.email
  };
}
