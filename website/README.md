# Content Trust Paper Landing Page

Astro landing page for the research paper "A New Incentive Model For Content Trust" (`arXiv:2507.09972`).

The site keeps the existing academic visual system and renders the paper summary from ordered MDX sections in `src/content/sections/`. Figures are currently represented by captioned placeholders so official paper images can be optimized and inserted later.

## Commands

```sh
bun install
bun run dev
bun run build
bun astro check
```

## Content

- `src/pages/index.astro` contains the hero metadata, artifact links, TOC, and MDX rendering loop.
- `src/content/sections/` contains the ordered paper narrative.
- `src/components/FigurePlaceholder.astro` marks image slots and final captions.
- `public/files/content-trust-paper.pdf` is the linked paper PDF.

When replacing placeholders with official images, keep imported image assets in `src/assets/images/` and use the local Astro image optimization skill to generate WebP files and ThumbHash placeholders.
