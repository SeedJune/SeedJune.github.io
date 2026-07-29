// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// https://astro.build/config
export default defineConfig({
  // This is a GitHub user site (SeedJune.github.io), so it is served from the
  // domain root. That is why there is deliberately no `base` here — adding one
  // would break every asset path.
  site: 'https://seedjune.github.io',
  integrations: [sitemap()],
});
