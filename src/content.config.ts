import { defineCollection } from 'astro:content';
import { file, glob } from 'astro/loaders';
import { z } from 'astro/zod';

// Each building lives in its own folder: src/content/buildings/<slug>/building.yaml
// Photos sit next to the YAML file; the GLB goes in public/models/.
const buildings = defineCollection({
  loader: glob({
    pattern: '*/building.yaml',
    base: './src/content/buildings',
    // Use the folder name as the URL slug, e.g. /buildings/victorian-test-house-1
    generateId: ({ entry }) => entry.split('/')[0],
  }),
  schema: ({ image }) =>
    z.object({
      number: z.number().int().positive(),
      name: z.string(),
      location: z.string(),
      type: z.string(),
      // Used by the homepage filters and shown on the building page.
      style: z.string(),
      bedrooms: z.number().int().nonnegative(),
      bathrooms: z.number().nonnegative(), // 2.5 = two full baths and a half bath
      stories: z.number().positive(), // above-grade floors (count a tower or tall attic); sets homepage size
      // Overall height in feet, when known. Sets homepage size more precisely than stories alone.
      height: z.number().positive().optional(),
      // Number of homes, for apartment buildings.
      units: z.number().int().positive().optional(),
      // Shown under the specs. Defaults to saying they're estimated from the floor plans.
      specsNote: z.string().default('Specs are estimates based on the floor plans.'),
      squareFeet: z.number().positive(),
      lotWidth: z.number().positive(), // feet
      lotDepth: z.number().positive(), // feet
      description: z.string(),
      // Isometric image with a transparent background, shown floating on the homepage.
      // Generate it with: npm run cutout -- <path-to-isometric-image>
      cutout: image().optional(),
      photos: z
        .array(z.object({ src: image(), alt: z.string(), caption: z.string().optional() }))
        .min(1),
      floorPlans: z
        .array(
          z.object({
            src: image(),
            alt: z.string(),
            caption: z.string().optional(),
            // Multiplier that brings this plan to the same drawing scale as the building's
            // other plans (e.g. 0.7 if the image was exported 1.4x larger). Staircases of the
            // same real width should end up the same size on screen.
            scale: z.number().positive().default(1),
          }),
        )
        .default([]),
      model: z
        .object({
          src: z.string().startsWith('/models/'),
          alt: z.string(),
        })
        .optional(),
    }),
});

// Knowledge articles: one Markdown file each in src/content/knowledge/. The file name is the URL.
// Cite sources with Markdown footnotes ([^1]); they render as a "Sources" list.
const knowledge = defineCollection({
  loader: glob({ pattern: '*.md', base: './src/content/knowledge' }),
  schema: ({ image }) => z.object({
    title: z.string(),
    // Square illustration (SVG or image) shown as the thumbnail and beside the essay title.
    cover: image(),
    description: z.string(),
    date: z.coerce.date(),
    // Tie-breaker for articles with the same date (lower comes first).
    order: z.number().default(0),
    draft: z.boolean().default(false),
  }),
});

// Roadmap categories and their actions, all in one file: src/content/roadmap.yaml.
const roadmap = defineCollection({
  loader: file('src/content/roadmap.yaml'),
  schema: z.object({
    order: z.number(),
    name: z.string(),
    color: z.string(),
    summary: z.string(),
    actions: z
      .array(
        z.object({
          title: z.string(),
          summary: z.string(),
          detail: z.string(),
          examples: z.array(z.string()).default([]),
        }),
      )
      .min(1),
  }),
});

export const collections = { buildings, knowledge, roadmap };
