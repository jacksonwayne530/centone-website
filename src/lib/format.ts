export function formatSquareFeet(sqft?: number): string | undefined {
  return sqft ? `${sqft.toLocaleString('en-US')} sq ft` : undefined;
}

export function formatNumber(n: number): string {
  return `#${String(n).padStart(3, '0')}`;
}

/** "40 × 100 ft (4,000 sq ft)" */
export function formatLot(width: number, depth: number): string {
  return `${width} × ${depth} ft (${(width * depth).toLocaleString('en-US')} sq ft)`;
}
