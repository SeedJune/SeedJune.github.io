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

  markdown: {
    /*
      Code blocks have to follow the day/night switch like everything else.
      Shiki normally bakes one theme's colours into inline `style` attributes,
      which no CSS variable can reach — so a single theme would either be a
      dark slab sitting on the white page or a light one glaring out of the
      black one.

      `defaultColor: false` makes it emit --shiki-light/--shiki-dark custom
      properties instead of a colour, and global.css picks the right pair.
    */
    shikiConfig: {
      themes: { light: 'github-light', dark: 'github-dark' },
      defaultColor: false,
    },
  },
});
