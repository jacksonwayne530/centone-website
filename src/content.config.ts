import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
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
      squareFeet: z.number().positive().optional(),
      lotSize: z.string().optional(),
      description: z.string(),
      photos: z
        .array(z.object({ src: image(), alt: z.string(), caption: z.string().optional() }))
        .min(1),
      floorPlans: z
        .array(z.object({ src: image(), alt: z.string(), caption: z.string().optional() }))
        .default([]),
      model: z
        .object({
          src: z.string().startsWith('/models/'),
          alt: z.string(),
        })
        .optional(),
    }),
});

export const collections = { buildings };
