# Centone Website

A catalog of well-designed buildings, built with [Astro](https://astro.build).

## Run it locally

```
npm install
npm run dev
```

Then open http://localhost:4321.

## Add a building

1. Create a folder: `src/content/buildings/<slug>/` (the folder name becomes the URL, e.g. `/buildings/<slug>/`).
2. Put the photos (and any floor plans) in that folder.
3. Copy `building.yaml` from `victorian-test-house-1/` into the new folder and edit it. Give it the next `number`.
4. Make the floating homepage image: `npm run cutout -- "src/content/buildings/<slug>/<isometric image>"`.
   This writes `cutout.png` in the same folder; add `cutout: ./cutout.png` to the YAML.
5. Put the GLB in `public/models/<slug>.glb` and set `model.src: /models/<slug>.glb`.

The homepage and the building page pick it up automatically. If a field is wrong or missing,
`npm run build` tells you which one.
