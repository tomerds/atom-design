# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

Design repository for **Atom Grants** marketing and company materials: decks, one-pagers, posters, mockups, animations, etc. Most deliverables are assembled as **HTML** (self-contained pages that can be exported to PDF/PNG or presented directly).

## Repository Layout

```
Design/
├── assets/                       # shared brand assets (logo, etc.)
│   ├── atom-logo.png             # primary logo mark (for light backgrounds)
│   ├── atom-logo-white.png       # white logo mark (for dark/colored backgrounds)
│   ├── atom-wordmark.png         # logo + wordmark, high-res (for light backgrounds)
│   └── atom-wordmark-white.png   # logo + wordmark, white (for dark/colored backgrounds)
├── <Project_Name>/               # one folder per deliverable
│   ├── <Project_Name>.html       # the design (self-contained)
│   └── <Project_Name>@2x.png     # rendered export (gitignore if git is ever added)
├── .claude/
│   └── skills/
│       └── html-screenshot/      # see "Rendering to PNG" below
└── CLAUDE.md
```

Each deliverable lives in its own folder. Reference shared assets with relative paths, e.g. `url("../assets/atom-logo.png")`.

## Brand System

Apply these consistently across every material unless the user explicitly overrides.

### Colors
- **Primary red:** `#ff3338`
- **Primary orange:** `#fe6400`
- **Background:** white (`#ffffff`)
- **Text:** black (`#000000`)
- **Dark gray:** `#333333`
- **Light gray:** `#d9d9d9`

Use red and orange as accent/brand colors (headlines, highlights, CTAs, gradients between the two). Avoid introducing off-brand colors; if a chart or diagram needs more hues, derive tints/shades of the two brand colors first, then fall back to grayscale.

### Typography
- **Titles / display:** Cal Sans
- **Body / everything else:** DM Sans

Load both via Google Fonts (DM Sans) and the Cal Sans CDN, e.g.:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">
<link href="https://fonts.cdnfonts.com/css/cal-sans" rel="stylesheet">
```

CSS variables to prefer:

```css
:root {
  --atom-red: #ff3338;
  --atom-orange: #fe6400;
  --bg: #ffffff;
  --text: #000000;
  --gray-dark: #333333;
  --gray-light: #d9d9d9;
  --font-title: "Cal Sans", system-ui, sans-serif;
  --font-body: "DM Sans", system-ui, sans-serif;
}
```

## Conventions for New Materials

- **One HTML file per deliverable** by default (easier to share/export). Inline CSS or a single `<style>` block is fine — don't introduce a build step unless asked.
- **Decks:** each slide is a full-viewport section (`width: 100vw; height: 100vh;`) so it exports cleanly to PDF at 16:9. Keep one idea per slide.
- **One-pagers / posters:** design to a fixed page size (Letter or A4) and make it print-ready (`@page` rules, no clipped content).
- **Animations:** prefer CSS keyframes or lightweight JS; avoid pulling in heavy animation libraries unless the brief calls for it.
- **Mockups:** when showing product UI, keep it consistent with the real Atom Grants product styling if reference is available.

## Rendering to PNG

Use the `html-screenshot` skill (in `.claude/skills/html-screenshot/`) to export any HTML deliverable to a high-res PNG. Default invocation from the repo root:

```bash
python3 .claude/skills/html-screenshot/shoot.py <Project>/<Project>.html
```

- Defaults: captures the `.poster` element at 2× retina scale.
- For decks / one-pagers without a `.poster` wrapper, pass `--full-page` or `--selector "<css>"`.
- See `.claude/skills/html-screenshot/SKILL.md` for all flags.

## Working Style

- Ask what the deliverable is for (audience, format, export target) before designing if it's not obvious from the request.
- When the user says "make a deck/poster/etc.", produce a complete, openable HTML file rather than fragments.
- Don't invent additional brand rules (new colors, new fonts, taglines) without checking — flag and ask.
