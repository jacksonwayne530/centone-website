// Removes the plain background around an isometric illustration so it can float on the page.
//
//   npm run cutout -- "src/content/buildings/<slug>/<image>.jpg" [--no-pockets]
//
// --no-pockets skips clearing enclosed background-colored areas (gaps between branches). Use it
// when the building itself is close to the background color (e.g. cream stucco on an off-white
// background), which that pass would otherwise punch holes in.
//
// Writes `cutout.png` next to the source image. Works by flood-filling inward from the image
// edges through pixels close to the corner color, so light areas inside the drawing (which are
// enclosed by outlines) are kept. Then trims the empty margin.
import sharp from 'sharp';
import path from 'node:path';

const HARD = 16; // max channel difference from the background that is fully removed
const SOFT = 48; // edge pixels up to this difference get partial transparency (anti-aliasing)

const input = process.argv.slice(2).find((a) => !a.startsWith('--'));
const clearPockets = !process.argv.includes('--no-pockets');
if (!input) {
  console.error('Usage: npm run cutout -- <path-to-image>');
  process.exit(1);
}

const { data, info } = await sharp(input).removeAlpha().raw().toBuffer({ resolveWithObject: true });
const { width: w, height: h } = info;
const rgba = Buffer.alloc(w * h * 4);

// Background color = average of the four corners.
const corners = [0, w - 1, (h - 1) * w, h * w - 1];
const bg = [0, 1, 2].map((c) => corners.reduce((s, p) => s + data[p * 3 + c], 0) / 4);
const diff = (p) => Math.max(...[0, 1, 2].map((c) => Math.abs(data[p * 3 + c] - bg[c])));

for (let p = 0; p < w * h; p++) {
  rgba[p * 4] = data[p * 3];
  rgba[p * 4 + 1] = data[p * 3 + 1];
  rgba[p * 4 + 2] = data[p * 3 + 2];
  rgba[p * 4 + 3] = 255;
}

// Flood fill from every edge pixel.
const removed = new Uint8Array(w * h);
const stack = [];
for (let x = 0; x < w; x++) stack.push(x, (h - 1) * w + x);
for (let y = 0; y < h; y++) stack.push(y * w, y * w + w - 1);
while (stack.length) {
  const p = stack.pop();
  if (removed[p] || diff(p) > HARD) continue;
  removed[p] = 1;
  rgba[p * 4 + 3] = 0;
  const x = p % w;
  if (x > 0) stack.push(p - 1);
  if (x < w - 1) stack.push(p + 1);
  if (p >= w) stack.push(p - w);
  if (p < w * (h - 1)) stack.push(p + w);
}

// Also clear enclosed pockets of background (e.g. gaps between tree branches). A tighter
// tolerance keeps light-colored walls and trim inside the drawing.
const POCKET = 9;
const MIN_POCKET_PX = 12;
const seen = new Uint8Array(w * h);
for (let start = 0; clearPockets && start < w * h; start++) {
  if (removed[start] || seen[start] || diff(start) > POCKET) continue;
  const region = [];
  const s = [start];
  seen[start] = 1;
  while (s.length) {
    const p = s.pop();
    region.push(p);
    const x = p % w;
    for (const q of [x > 0 ? p - 1 : -1, x < w - 1 ? p + 1 : -1, p - w, p + w]) {
      if (q >= 0 && q < w * h && !seen[q] && !removed[q] && diff(q) <= POCKET) {
        seen[q] = 1;
        s.push(q);
      }
    }
  }
  if (region.length >= MIN_POCKET_PX) {
    for (const p of region) {
      removed[p] = 1;
      rgba[p * 4 + 3] = 0;
    }
  }
}

// Feather the one-pixel ring bordering the removed area.
for (let p = 0; p < w * h; p++) {
  if (removed[p]) continue;
  const x = p % w;
  const touches =
    (x > 0 && removed[p - 1]) || (x < w - 1 && removed[p + 1]) || removed[p - w] || removed[p + w];
  if (touches) {
    const d = diff(p);
    if (d < SOFT) rgba[p * 4 + 3] = Math.round((255 * (d - HARD)) / (SOFT - HARD));
  }
}

const out = path.join(path.dirname(input), 'cutout.png');
await sharp(rgba, { raw: { width: w, height: h, channels: 4 } })
  .trim({ threshold: 0 })
  .png()
  .toFile(out);
console.log(`Wrote ${out}`);
