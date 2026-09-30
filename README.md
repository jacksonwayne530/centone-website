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
5. Name floor plans `floorplan-level-1.png`, `floorplan-level-2.png`, … and run `npm run floorplans`.
   This writes line-only `floorplan-level-N.lines.png` versions; list those under `floorPlans` in the YAML.
   If one plan image was exported at a different size, add `scale:` to it so staircases
   come out the same width across floors (e.g. `scale: 0.7` if its stairs measure 1.4x wider).
6. Put the GLB in `public/models/<slug>.glb` and set `model.src: /models/<slug>.glb`.

The homepage and the building page pick it up automatically. If a field is wrong or missing,
`npm run build` tells you which one.

## Add a Knowledge article

Create a Markdown file in `src/content/knowledge/` (the file name becomes the URL) with this at the top:

```
---
title: Your Title
description: One-sentence summary shown in the list and under the title.
date: 2026-10-15
---
```

Cite sources with footnotes: put `[^name]` in the text and `[^name]: The source, with a link` at
the bottom. They're numbered automatically and listed under "Sources". Add `draft: true` to keep an
article off the live site.

## Edit the Roadmap

All categories and actions live in `src/content/roadmap.yaml`. Each action has a `title`, a short
`summary`, a longer `detail`, and optional `examples`. Categories are placed around the oval in
`order`.
