export function formatSquareFeet(sqft?: number): string | undefined {
  return sqft ? `${sqft.toLocaleString('en-US')} sq ft` : undefined;
}

export function formatNumber(n: number): string {
  return `#${String(n).padStart(3, '0')}`;
}
