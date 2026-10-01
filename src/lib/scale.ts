// How big each building appears on the homepage canvas.
//
// Showing buildings at true relative scale would make a skyscraper fill the screen and shrink
// houses to specks, so sizes are compressed: a building's height displays as height^EXPONENT.
// With 0.7, a 3-story house shows ~1.23x as tall as a 2-story one (really 1.34x), and a tower
// 20x taller than a house shows ~8x taller.
//
// Each isometric image is drawn to fill its lot, so its real width is the lot's projected width.
// The image is scaled so its building's height lands on the compressed curve; width follows.

export const EXPONENT = 0.7;

const FLOOR_HEIGHT = 11; // feet per story
const ROOF_AND_BASE = 10; // feet for roof, foundation, and parapets

interface Sized {
  stories: number;
  height?: number; // feet; estimated from stories when missing
  lotWidth: number;
  lotDepth: number;
}

/** Relative on-screen width for a building's image (arbitrary units; compare between buildings). */
export function displaySize({ stories, height: knownHeight, lotWidth, lotDepth }: Sized): number {
  const height = knownHeight ?? stories * FLOOR_HEIGHT + ROOF_AND_BASE;
  const sceneWidth = (lotWidth + lotDepth) * Math.cos(Math.PI / 6); // isometric projection of the lot
  const pixelsPerFoot = height ** (EXPONENT - 1); // compress: taller buildings get fewer px per foot
  return sceneWidth * pixelsPerFoot;
}

/** Sizes normalized so the median building is 1. */
export function relativeSizes(buildings: Sized[]): number[] {
  const sizes = buildings.map(displaySize);
  const sorted = [...sizes].sort((a, b) => a - b);
  const mid = sorted.length / 2;
  const median = sorted.length % 2 ? sorted[Math.floor(mid)] : (sorted[mid - 1] + sorted[mid]) / 2;
  return sizes.map((s) => s / median);
}
