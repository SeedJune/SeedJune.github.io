---
# HOW TO ADD A BLOG POST
#   1. Copy this file and rename it WITHOUT the leading underscore.
#      The filename becomes the URL: my-first-post.md -> /blog/my-first-post/
#      Use lowercase-with-hyphens, no spaces, no Chinese characters.
#   2. Fill in the frontmatter below.
#   3. Write the article under the closing --- . It is plain Markdown.
#
# Files starting with "_" are ignored, so this template never gets a page.

title: '无人生还'
date: 2025-05-09
summary: 'My book review.'

# Which series this belongs to. Must be one of the ids in `blogSeries`
# in src/data/site.ts — currently: tech | research | life
# A typo here fails the build and names this file.
series: 'books and movies'

tags: ['Books', 'Detective']

# Optional cover image. Put the file in src/assets/blogs/ first.
# cover: ../../assets/blogs/your-image.png
# coverAlt: 'What the image shows, for screen readers.'

# true = keeps the file but publishes nothing, not even the URL.
draft: false
---

Write the article here in Markdown.

## A heading

Paragraphs, **bold**, *italic*, [links](https://example.com), `inline code`,
lists, tables, block quotes and fenced code blocks all render.

```python
print("code blocks work too")
```
