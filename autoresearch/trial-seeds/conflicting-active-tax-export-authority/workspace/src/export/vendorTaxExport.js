export function buildVendorTaxExport(vendors) {
  return vendors.map((vendor) => ({
    vendorId: vendor.vendorId,
    taxLast4: String(vendor.taxId).slice(-4),
  }));
}
