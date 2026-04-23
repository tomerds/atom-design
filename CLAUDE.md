# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

Design repository for **Atom Grants** marketing and company materials: decks, one-pagers, posters, mockups, animations, etc. Most deliverables are assembled as **HTML** (self-contained pages that can be exported to PDF/PNG or presented directly).

## Repository Layout

```
Design/
├── assets/                                    # shared brand assets (logo, etc.)
│   ├── newredlogowordmarkhighres.png          # CURRENT — logo + wordmark for light bgs
│   └── newredlogowordmarkwhitehighres.png     # CURRENT — logo + wordmark for dark/colored bgs
├── <Project_Name>/               # one folder per deliverable
│   ├── <Project_Name>.html       # the design (self-contained)
│   └── <Project_Name>@2x.png     # rendered export (gitignore if git is ever added)
├── .claude/
│   └── skills/
│       ├── html-screenshot/      # HTML → PNG, see "Rendering to PNG" below
│       ├── html-to-pdf/          # HTML → vector PDF (default), see "Rendering to PDF" below
│       └── png-to-pdf/           # PNGs → raster PDF, see "Rendering to PDF" below
└── CLAUDE.md
```

Always use the `newredlogowordmark*` files. Older `atom-logo*.png` and `atom-wordmark*.png` files may still exist in `assets/` from the previous brand (orange→red gradient) and should not be used in new work.

Each deliverable lives in its own folder. Reference shared assets with relative paths, e.g. `url("../assets/atom-logo.png")`.

## Brand System

Apply these consistently across every material unless the user explicitly overrides.

### Colors
- **Accent:** `#ff4227` — the single brand accent, used for headlines, highlights, CTAs, and colored fills.
- **Background:** white (`#ffffff`)
- **Text:** black (`#000000`)
- **Dark gray:** `#333333`
- **Light gray:** `#d9d9d9`

Use `#ff4227` as the only brand color. No gradients, no secondary red/orange — one accent, applied as a solid fill. Avoid introducing off-brand colors; if a chart or diagram needs more hues, derive tints/shades of the accent first, then fall back to grayscale.

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
  --accent: #ff4227;
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
- **Downloadable resources / playbooks / ebooks:** multi-page HTML sized as Letter portrait (`816 x 1056px` per page at 96dpi). Each page is a `.page` section with a sequential id (`#page-1`, `#page-2`, ...). Include the `@page` + `@media print` boilerplate from the "Rendering to PDF" section so the HTML can be exported directly via `html-to-pdf` (the default). Keep a consistent running header/footer across interior pages. Example: `Newsletter_Playbook/`.
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

## Rendering to PDF

There are two ways to produce a PDF from an HTML deliverable. **Default to `html-to-pdf`** — `html-screenshot` + `png-to-pdf` is a fallback for pixel-perfect raster output.

| | `html-to-pdf` (default) | `html-screenshot` + `png-to-pdf` |
|---|---|---|
| Links | native, clickable | broken (image) |
| Text | selectable, searchable | not |
| File size | small (vector) | large (raster, 2–5× bigger) |
| Crispness | any zoom | fixed at capture resolution |
| Visual fidelity | 99% — print renderer differs slightly | 100% pixel-match |

**Use `html-to-pdf` for** decks, one-pagers, playbooks, self-assessments, collaborator docs — anything read on-screen or anything with links.

**Use `html-screenshot` + `png-to-pdf` for** posters, mockups, and brand-art deliverables where visual fidelity above all else matters and there are no hyperlinks.

### Option A — HTML → PDF directly (vector, clickable links)

```bash
python3 .claude/skills/html-to-pdf/export.py <Project>/<Project>.html
```

The HTML must include `@page` + `@media print` CSS so Chromium paginates correctly. Drop this into every multi-page deliverable's `<style>` block:

```css
@page { size: 8.5in 11in; margin: 0; }
@media print {
  html, body { background: #fff; margin: 0; padding: 0; }
  .page {
    margin: 0 !important;
    box-shadow: none !important;
    page-break-after: always;
    break-after: page;
  }
  .page:last-child { page-break-after: auto; break-after: auto; }
}
```

Wrap clickable cards in `<a href="...">` — they become real PDF link annotations. After export the script prints which URLs it wired up, so you can verify at a glance.

See `.claude/skills/html-to-pdf/SKILL.md` for all flags (`--size`, `--margin`, etc.).

### Option B — screenshot per page, then stitch (raster)

```bash
# 1) Build HTML with N numbered .page sections (#page-1 ... #page-N)
# 2) Screenshot each page at 2× retina
for i in 01 02 03 04 05 06 07 08 09; do
  python3 .claude/skills/html-screenshot/shoot.py <Project>/<Project>.html \
    --selector "#page-$i" -o <Project>/page_$i@2x.png
done
# 3) Merge into one PDF
python3 .claude/skills/png-to-pdf/merge.py \
    <Project>/page_*@2x.png -o <Project>/<Project>.pdf --title "<Title>"
```

- Supports `letter`, `letter-landscape`, `a4`, `a4-landscape`, `tabloid`, `legal`, or a custom `WxH` in inches (e.g. `6x9`).
- DPI is auto-computed from image width so any retina scale works; override with `--dpi`.
- Output is image-backed (not text-searchable, no live links).
- See `.claude/skills/png-to-pdf/SKILL.md` for all flags.

## Working Style

- Ask what the deliverable is for (audience, format, export target) before designing if it's not obvious from the request.
- When the user says "make a deck/poster/etc.", produce a complete, openable HTML file rather than fragments.
- Don't invent additional brand rules (new colors, new fonts, taglines) without checking — flag and ask.
