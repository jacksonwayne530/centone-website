# Centone Website

Personal project: a catalog of well-designed buildings (Astro 7, static output, deployed on Vercel).
Keep it entirely separate from any OA / Schell Brothers work: commit only with the repo-local
Git identity (jacksonwayne209@gmail.com), and never change global Git config.

## Structure

- `src/content/buildings/<slug>/building.yaml`: one data file per building, with its photos and floor plans beside it
- `public/models/<slug>.glb`: 3D model referenced by `model.src` in the YAML
- `src/content.config.ts`: schema for building data
- `src/pages/index.astro`: homepage listing all buildings, sorted by `number`
- `src/pages/buildings/[id].astro`: shared building page template
- `src/components/ModelViewer.astro`: GLB viewer (Google `<model-viewer>`)

## Development

When starting the dev server, use background mode:

```
astro dev --background
```

Manage the background server with `astro dev stop`, `astro dev status`, and `astro dev logs`.

Docs: https://docs.astro.build
