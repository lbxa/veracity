# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an Astro project named "content-trust-paper" configured as a research paper landing page for "A New Incentive Model For Content Trust" (`arXiv:2507.09972`). The project uses Bun as the package manager, MDX for content sections, and Tailwind CSS for styling. It is designed to present a concise academic summary with paper links, section navigation, citations, and figure slots.

## Common Commands

The project uses Bun as the package manager. All commands should be run from the root directory:

- `bun install` - Install dependencies
- `bun run dev` - Start development server at localhost:4321
- `bun run build` - Build production site to ./dist/
- `bun run preview` - Preview production build locally
- `bun astro check` - Run TypeScript and Astro checks
- `bun astro add <integration>` - Add Astro integrations

## Architecture

This is a research showcase website with the following structure:

### Content Management
- **src/content/sections/** - Ordered MDX files for each landing-page section
- **src/content.config.ts** - Content collections configuration
- **src/assets/images/** - Imported image assets for Astro optimization when official figures are added
- **public/files/** - Static downloadable paper files

### Components
- **src/pages/index.astro** - Main page shell, hero metadata, artifact links, TOC, and MDX rendering loop
- **src/components/Image.astro** - Image display with ThumbHash placeholders and Astro asset support
- **src/components/ImageTwoUp.astro** - Two-column figure layout
- **src/components/FigurePlaceholder.astro** - Temporary captioned figure slots until official images are added

### Styling
- **Tailwind CSS** with typography plugin for academic content
- **Responsive design** optimized for research paper presentation
- **Academic styling** inspired by research websites

## Content Structure

The landing-page content is organized into MDX sections:

1. **abstract.mdx** - Short summary and mechanism preview
2. **01-problem.mdx** - Misinformation and incentive problem
3. **02-core-idea.mdx** - Veracity bonds and contestable claims
4. **03-roles.mdx** - Creators, challengers, jurors, and viewers
5. **04-mechanics.mdx** - Challenge flow, jury resolution, evaluation, and queues
6. **05-incentive-model.mdx** - Payouts, reputation, and visibility
7. **06-trust-infrastructure.mdx** - Digital identity and provenance
8. **07-guarantees-limits.mdx** - Collusion and capacity analysis
9. **08-open-questions.mdx** - Future research questions
10. **09-citation.mdx** - BibTeX

## Key Features

- **MDX Content Collections** - Easy content management with frontmatter
- **Media Support** - Optimized image components and temporary figure placeholders
- **Responsive Navigation** - Smooth scrolling with active section highlighting
- **Academic Styling** - Clean, professional design for research presentation
- **Copy-Paste Friendly** - Designed for easy content transfer from Notion

## Development Workflow

1. **Content Updates** - Modify MDX files in `src/content/sections/`
2. **Media Assets** - Add official figure source assets to `src/assets/images/`, optimize to WebP, and wire them through `Image.astro`
3. **Styling Changes** - Modify component styles or Tailwind configuration
4. **Component Updates** - Edit components in `src/components/` for functionality changes

## Technical Stack

- **Astro 6.x** with TypeScript support
- **MDX integration** for rich content authoring
- **Tailwind CSS** with typography plugin
- **Bun** package manager
- **Content Collections** for structured content management
