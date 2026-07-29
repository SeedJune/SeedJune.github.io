# seedjune.github.io

My personal site. Hand-built with [Astro](https://astro.build) — no theme, no
CSS framework. Every component and every line of CSS in `src/` is mine.

Live at <https://seedjune.github.io>.

## Running it

```bash
pnpm install
pnpm dev           # http://localhost:4321
pnpm build         # writes dist/
pnpm preview       # serves dist/ exactly as GitHub Pages will
pnpm astro check   # type + content-schema errors
```

## Where the content lives

Two places, split by one rule: **anything with a picture or a paragraph of
prose is a Markdown file; anything that is a short list is a TypeScript array.**

| What | File |
|---|---|
| Name, bio, research interests, skills, social links | `src/data/site.ts` |
| News items | `src/data/site.ts` → `news` |
| Education, research/internships, awards | `src/data/site.ts` |
| Projects | `src/content/projects/*.md` |
| Tools | `src/content/tools/*.md` |
| Photos | `src/content/gallery/*.md` |
| Publications | `src/content/publications/*.md` |
| Images | `src/assets/{profile,projects,tools,gallery}/` |

### Adding one of something

Every collection folder has a `_template.md`. Files starting with `_` are
ignored by the build, so the template never shows up on the site.

1. Put the image in the matching `src/assets/…` folder.
2. Copy `_template.md`, rename it **without** the underscore.
3. Fill in the frontmatter and point the image field at your file.

For a new award or news item, just add an object to the array in
`src/data/site.ts`.

### Images

Images belong in `src/assets/`, **never** in `public/`. Files in `src/assets/`
are resized and converted to WebP at build time; files in `public/` are copied
byte-for-byte. A 2 MB photo in the wrong folder ships as 2 MB.

### If the build fails

That is the schema doing its job. Every collection is validated, so a missing
image, a malformed date, or a forgotten required field fails the build and
names the file. Nothing publishes half-broken.

## Structure

```
src/
├── data/site.ts          all short, image-free content
├── content/              Markdown collections
├── content.config.ts     schemas — the thing that catches typos
├── assets/               source images (optimized at build time)
├── styles/global.css     design tokens; the colour system is documented at the top
├── layouts/Base.astro    <head>, the two-column shell
├── components/           cards, nav, sidebar, section wrapper
│   └── sections/         one file per section of the page
└── pages/index.astro     the whole site, one line per section
```

### Adding a whole new section

1. Create `src/components/sections/Thing.astro`.
2. Add one line to `src/pages/index.astro`.
3. Add one line to `navItems` in `src/components/Nav.astro`.

## Design notes

The palette runs on two axes, documented in full at the top of
`src/styles/global.css`:

- **Blue** — academic and clickable. Links, active nav, project tags, sidebar.
- **Pink** — personal. Avatar ring, gallery accents, hobby tags.

Pink never appears on anything clickable. The pale `-soft` / `-tint` shades are
decorative fills only and never carry text — every text-bearing accent clears
WCAG AA on white.

Gallery cards are deliberately **not** clickable: `PhotoCard.astro` renders a
`<figure>` with no link, no tabindex, and no hover state. Everything a visitor
should read is in the card's title, date, and location.

## Deployment

Pushing to `main` triggers `.github/workflows/deploy.yml`, which builds and
publishes to GitHub Pages. Repo Settings → Pages → Source must be set to
**GitHub Actions**.
