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
│       ├── png-to-pdf/           # PNGs → raster PDF, see "Rendering to PDF" below
│       └── og-tile/              # Resource + Webinar OG image conventions, see "OG Tiles" below
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
- **Titles / display:** Cal Sans — **single weight only.** Cal Sans ships just `font-weight: 400`; always set `font-weight: 400` on every Cal Sans element. Asking for 500/600/700 makes the browser synthetic-bold it (an off-brand smeared look). `<h1>`–`<h3>` default to bold, so override them explicitly.
- **Body / everything else:** DM Sans (has real 400–700 weights — use those for any bold text)

Load both via Google Fonts, e.g.:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">
<link href="https://fonts.googleapis.com/css2?family=Cal+Sans&display=swap" rel="stylesheet">
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

### Banned: colored left-rule accent bar

**Never** put a colored left rule (vertical accent bar) on a panel or block of text — e.g. `border-left: 3px solid var(--accent)` on a callout. That left-bar treatment reads as generic AI-generated "admonition/alert box" boilerplate and is off-brand. Soft panels and tinted fills are fine on their own; it's the colored vertical rule on the edge that's banned. To emphasize a point, use the house typographic tools instead: an accent eyebrow/label, a single accent word or phrase inside otherwise-plain body text, a soft-card (the one-pager card system), or a chip.

### Headshots

All headshots of people — author cards, speaker portraits, team bios, testimonial avatars, anywhere a real person's face appears — must be **black-and-white** and **square with rounded corners**. No full circles, no color photos. Crop so the full head is visible with a small margin of headroom above; if the source photo is portrait-oriented, bias the crop upward (`object-position: center ~15-20%`) rather than centering.

Apply via CSS:

```css
.avatar {
  width: 200px; height: 200px;
  border-radius: 24px;
  overflow: hidden;
}
.avatar img {
  width: 100%; height: 100%;
  object-fit: cover;
  object-position: center 18%;
  filter: grayscale(100%);
}
```

This matches the webinar speaker portrait convention already used in `og-tile`.

## Conventions for New Materials

- **One HTML file per deliverable** by default (easier to share/export). Inline CSS or a single `<style>` block is fine — don't introduce a build step unless asked.
- **Decks:** each slide is a full-viewport section (`width: 100vw; height: 100vh;`) so it exports cleanly to PDF at 16:9. Keep one idea per slide.
- **One-pagers** (product/module overviews, comparison sheets, leave-behinds, single-page sheets read on-screen or printed): always the house **soft-card** style — rounded, lightly-shadowed cards on white, separated by hairline gray, **never hard black rules**. One accent (`#ff4227`) on the highlighted card + status checks + the punch word; if one side "wins," keep it on the same side in every section. Comparison sheets use the elevated-table-with-highlighted-column pattern. Letter portrait (`816 × 1056px`), and the content must fill the page top-to-bottom and pass a fit-check (`.poster` ≤ 1056px) before export. The full spec — card system, divider rules, accent discipline, the comparison-table recipe, vertical-balance/fit-check workflow, copy register (plain language, no em dashes), and render commands — lives in the `onepager` skill (`.claude/skills/onepager/SKILL.md`). Read it before building any one-pager. Canonical reference: `.claude/skills/onepager/references/Atom_vs_GrantAI.html`. **Do not copy the retired `Proposals_Module_Onepager/` style (hard black hairlines, square corners, no shadows).**
- **Posters / brand-art sheets:** design to a fixed page size (Letter or A4) and make it print-ready (`@page` rules, no clipped content). These favor visual fidelity over links — render via `html-screenshot` + `png-to-pdf`.
- **Downloadable resources / playbooks / ebooks:** multi-page HTML sized as Letter portrait (`816 x 1056px` per page at 96dpi). Each page is a `.page` section with a sequential id (`#page-1`, `#page-2`, ...). Include the `@page` + `@media print` boilerplate from the "Rendering to PDF" section so the HTML can be exported directly via `html-to-pdf` (the default). Keep a consistent running header/footer across interior pages. Example: `Newsletter_Playbook/`.
- **Animations:** prefer CSS keyframes or lightweight JS; avoid pulling in heavy animation libraries unless the brief calls for it.
- **Mockups:** when showing product UI, keep it consistent with the real Atom Grants product styling if reference is available.
- **OG / social tiles** for resources (`atomgrants.com/resources/...`), webinars (`atomgrants.com/webinars/...`), and blog posts (`atomgrants.com/blog/...`): always 1200 × 630 (40/21 ratio — the website cards on atomgrants.com are sized to match), cool light-gray `#F9FAFB` tile on white page bg, with universal `64px 144px` padding across all three families. **No tile family uses a bottom accent bar** — that 10px `#ff4227` strip is retired; the accent word in the title is the only color load. Resource tiles = title + category pill. Webinar tiles = title + subtitle + dated header + grayscale square-rounded speaker portraits — and **every webinar tile must also be exported as a 1280 × 720 YouTube twin** (16:9, for the recording thumbnail; see the skill's "YouTube version" rule). Blog tiles = `● BLOG · DATE` header + split-accent title, with two variants — **featured** (external author: bottom collab strip with grayscale headshot, name, role/org) and **general** (Atom-authored: title only, no footer). The complete spec, layout grids, copy rules, headshot-sourcing playbook (incl. Cloudflare-blocked institution sites and the `api.atomgrants.com/storage/...` shortcut for blog headshots), and the grayscale/crop helper live in `.claude/skills/og-tile/SKILL.md` — read that before designing or extending any family. Examples: `Resource_Tiles/`, `Webinar_Tiles/`, `Blog_Tiles/`.
- **Partner check-in decks** (30/60/90/180/270-day reviews, QBRs, renewal-conversation decks): always 13.333 × 7.5 in landscape, one HTML file. Every deck is **agenda-driven** and follows the canonical ~14-slide sequence: cover → **agenda** → all-time headlines → activation → **your objectives** → period comparison → weekly trend → cohort flow (or engagement funnel on a first check-in) → top departments → funder mix → search themes → channels → top researchers → **feedback** → next 60 days. Four slides are **required on every deck**: agenda, objectives (ask the user for the partner's onboarding objectives — never invent them), activation, and feedback. The complete spec — agenda structure, required slides, first-check-in swaps, accent discipline, copy register, chart conventions, data-interpretation gotchas, print-CSS overrides, render commands, and the boilerplate skeleton — lives in `.claude/skills/checkin-deck/SKILL.md`. Read that before starting or extending any check-in deck. The reference component library lives inside the skill at `.claude/skills/checkin-deck/references/`: `SUNY_Cortland_30_Day_Checkin.html` (agenda + objectives + feedback, first check-in) and `NYULH_180_Day_Checkin.html` (period-comparison / cohort / funder-shift components).
- **Intro / first-call decks** (the initial ~30-min discovery + intro call, *not* the full demo): always 13.333 × 7.5 in landscape, one self-contained HTML file. The finalized 8-slide template lives at `Intro_Call_Deck/Intro_Call_Deck.html` (cover → partners → why now → a different category → how it works → admin backend → case study → next steps). To make a prospect-specific version, **only the cover and the close slide change** (five placeholder tokens). Use the `intro-call-deck` skill (`.claude/skills/intro-call-deck/`) — its `personalize.py` swaps the tokens and renders the PDF (always via screenshot-and-stitch, never html-to-pdf). Read `.claude/skills/intro-call-deck/SKILL.md` before editing the template itself.
- **Partnership proposal decks** (the pricing / quotes call, after the intro call and demo): 13.333 × 7.5 in landscape, one self-contained HTML file, **built from the partnership-call transcript**. The 9-slide sequence reframes from cost to outcome: cover → what you'd be licensing → sized to your institute → two licensing options (pricing table) → projected ROI → recommendation → a path to a better price → onboarding timeline → next steps. The "sized to your institute," ROI, and recommendation slides come from the transcript (never invent metrics or objectives); ask for the institution/logo, pricing tiers, and the implementation fee. Always export to a **3:2 (12×8 in) PDF via screenshot-and-stitch** using the skill's `render.py` (never html-to-pdf). The complete spec — transcript extraction, info to request, slide-by-slide structure, accent/copy rules, render command — lives in `.claude/skills/proposal-deck/SKILL.md`. Canonical reference: `.claude/skills/proposal-deck/references/MPFI_Partnership_Proposal.html`.
- **Formal quotes** (the single-page quotation a prospect takes to their team): Letter portrait (`816 × 1056px`), one self-contained HTML file, exported to a **vector PDF via `html-to-pdf`** (selectable text, live links). This is the **one deliverable that intentionally departs from the soft-card house style** — it is a traditional business document: ruled line-item table, tabular figures, restrained accent, light-gray total box anchored on the annual license fee, no signature block (a separate contract/order form follows). Built from the transcript (parties) plus the agreed package and price (ask for these). The complete spec — sections, formal-quote style, line/text alignment rules, one-page fit-check — lives in `.claude/skills/quote/SKILL.md`. Canonical reference: `.claude/skills/quote/references/MPFI_Quote.html`.
- **LinkedIn / social concept posts:** 1200 × 1200 square on white. Lead with a **diagram or UX mockup**, not a typographic quote — show the concept, don't write it. For "X vs Y" posts (the most common kind), use a two-column comparison with stark asymmetry: the worse paradigm gets a long list of dim/low-relevance items, the better one a short list of dark/high-relevance items. Represent UI text with **skeleton bars** (gray `<div>` rectangles of varying width — `w-90`, `w-70`, etc.) so the viewer reads the shape of the UI, not the words. Reserve real text for: column labels (small caps, gray), one short Cal Sans title per column, the input mock (search bar query, profile name + context chips), and a single bottom takeaway line in Cal Sans. Brand frame: small logo top-left (~38px), URL top-right (16px gray). Use accent red only for the "good" side's signals — match meters, why-it-matches tags, the takeaway punch word. Example: `LinkedIn_Knows_Me/`.

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
- **Default to a diagram or product mock** when the post explains a concept (how something works, before-vs-after, a paradigm shift). Reserve typographic-hero / pull-quote designs for quote or voice posts where the words *are* the point. If you're unsure which the brief calls for, ask before designing.
- **Use skeleton bars for UI text.** When mocking product surfaces in a diagram, fill non-essential text with light-gray rectangles of varying width. Reserve real copy for the elements that carry meaning (search query, profile chips, match labels, takeaway).
- **Plain copy, not marketing voice.** Direct phrasing in every deliverable. Use the simplest word that works ("favorites," not "save-for-later actions"). No flowery framing — in copy or in conversation.
