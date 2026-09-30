// Turns floor plan images into line-only versions for the detail pages.
//
//   npm run floorplans
//
// For every `floorplan*.png` in src/content/buildings/*/, writes `<name>.lines.png` beside it:
// the dark linework (walls, fixtures, labels) is kept and everything else (the gray surround,
// white rooms, light window marks) becomes transparent. Then trims the empty margin.
// The site draws these as a mask in the page's text color, so they work in light and dark mode.
import sharp from 'sharp';
import { readdir } from 'node:fs/promises';
import path from 'node:path';

const DARK = 110; // luminance at or below this is fully kept
const LIGHT = 165; // luminance at or above this is fully removed; in between fades (anti-aliasing)

const root = 'src/content/buildings';
const folders = (await readdir(root, { withFileTypes: true })).filter((d) => d.isDirectory());

for (const folder of folders) {
  const dir = path.join(root, folder.name);
  const files = (await readdir(dir)).filter((f) => /^floorplan.*\.png$/i.test(f) && !f.includes('.lines.'));
  for (const file of files) {
    const input = path.join(dir, file);
    const { data, info } = await sharp(input).removeAlpha().raw().toBuffer({ resolveWithObject: true });
    const out = Buffer.alloc(info.width * info.height * 4);
    for (let p = 0; p < info.width * info.height; p++) {
      const [r, g, b] = [data[p * 3], data[p * 3 + 1], data[p * 3 + 2]];
      const lum = 0.299 * r + 0.587 * g + 0.114 * b;
      const alpha = Math.round(255 * Math.min(Math.max((LIGHT - lum) / (LIGHT - DARK), 0), 1));
      out[p * 4 + 3] = alpha; // RGB stays black
    }
    const output = path.join(dir, file.replace(/\.png$/i, '.lines.png'));
    await sharp(out, { raw: { width: info.width, height: info.height, channels: 4 } })
      .trim({ threshold: 0 })
      .png()
      .toFile(output);
    console.log(`Wrote ${output}`);
  }
}
