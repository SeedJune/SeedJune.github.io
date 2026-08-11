// @ts-check
import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

// https://astro.build/config
export default defineConfig({
  // This is a GitHub user site (SeedJune.github.io), so it is served from the
  // domain root. That is why there is deliberately no `base` here — adding one
  // would break every asset path.
  site: 'https://seedjune.github.io',
  integrations: [sitemap()],

  markdown: {
    /*
      Maths. Markdown has none of its own — `$x$` is not in CommonMark — so
      without these two plugins the delimiters ship as literal text AND the
      formula is corrupted on the way: Markdown reads the underscores in
      `\mathbb{E}_{z\sim p_{\theta}}` as emphasis and turns the subscripts
      into <em> tags.

      remark-math has to run first for that reason: it claims `$...$` and
      `$$...$$` as maths nodes before the emphasis rule ever sees them.
      rehype-katex then renders those nodes to HTML at BUILD time, so visitors
      download no maths library and nothing has to run in the browser.
    */
    remarkPlugins: [remarkMath],
    rehypePlugins: [rehypeKatex],

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
