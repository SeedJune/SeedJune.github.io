import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';
import { blogSeries } from './data/site';

/**
 * Files starting with an underscore are ignored by every collection below.
 * That is how `_template.md` can sit next to real entries as a copy-paste
 * starting point without ever being published.
 *
 * To add an entry: copy `_template.md`, rename it (no underscore), fill it in.
 * If a required field is missing or a date is malformed, `pnpm build` fails
 * and names the offending file — nothing publishes half-broken.
 */
const pattern = ['*.md', '!_*.md'];

const projects = defineCollection({
  loader: glob({ pattern, base: './src/content/projects' }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      date: z.coerce.date(),
      summary: z.string(),
      tags: z.array(z.string()).default([]),
      cover: image().optional(),
      coverAlt: z.string().default(''),
      /* Both optional and independent: a project can have source only, a live
         demo only, both, or neither. The card renders whichever links exist —
         "Code" for `repo`, "Demo" for `demo` — and drops the row entirely when
         there are none. `demo` is what the old Tools section used to be. */
      repo: z.url().optional(),
      demo: z.url().optional(),
      draft: z.boolean().default(false),
    }),
});

const gallery = defineCollection({
  loader: glob({ pattern, base: './src/content/gallery' }),
  schema: ({ image }) =>
    z.object({
      title: z.string(), // the theme of the photo
      date: z.coerce.date(), // when it was taken
      location: z.string().optional(), // omitted -> the line is not rendered
      note: z.string().optional(),
      photo: image(),
      alt: z.string(),
      /* Every card is the same shape, so portrait photos get cropped.
         `focal` decides which part survives the crop. */
      focal: z
        .enum(['center', 'top', 'bottom', 'left', 'right'])
        .default('center'),
      draft: z.boolean().default(false),
    }),
});

const publications = defineCollection({
  loader: glob({ pattern, base: './src/content/publications' }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      authors: z.array(z.string()),
      venue: z.string(),
      year: z.number(),
      /* Marks your own name so it can be bolded in the author list. */
      me: z.string().default('Yuchao Jin'),
      cover: image().optional(),
      coverAlt: z.string().default(''),
      pdf: z.url().optional(),
      code: z.url().optional(),
      project: z.url().optional(),
      award: z.string().optional(),
      draft: z.boolean().default(false),
    }),
});

/* The series ids from src/data/site.ts, as the tuple z.enum needs. Keeping the
   list there rather than here means the tab order and the validation can never
   disagree — there is only one list. */
const seriesIds = blogSeries.map((s) => s.id) as [string, ...string[]];

const blogs = defineCollection({
  loader: glob({ pattern, base: './src/content/blogs' }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      date: z.coerce.date(),
      summary: z.string(),
      /* Must be one of the ids in `blogSeries`. Anything else fails the build
         and names the file — see the note on blogSeries in src/data/site.ts. */
      series: z.enum(seriesIds),
      tags: z.array(z.string()).default([]),
      cover: image().optional(),
      coverAlt: z.string().default(''),
      draft: z.boolean().default(false),
    }),
});

export const collections = { projects, gallery, publications, blogs };
