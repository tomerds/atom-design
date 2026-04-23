---
name: html-to-pdf
description: Export an HTML deliverable directly to a vector PDF via headless Chromium (Playwright). Preserves <a> tags as native clickable link annotations and keeps text selectable. Trigger when the user asks for a "PDF with working links", "clickable PDF", "selectable text PDF", "vector PDF", or is producing a deck/one-pager/playbook meant to be read on-screen.
---

# html-to-pdf

Export any HTML design file directly to a **vector** PDF through Chromium's print pipeline. Anchors become native PDF link annotations, text stays selectable, and files are much smaller than raster equivalents.

## When to use this vs `html-screenshot` + `png-to-pdf`

| | `html-to-pdf` (this skill) | `html-screenshot` + `png-to-pdf` |
|---|---|---|
| Links | native, clickable | broken — image |
| Text | selectable, searchable | not |
| File size | small (vector) | large (raster, ~2-5× bigger) |
| Crispness | infinite zoom | fixed at capture resolution |
| Visual fidelity | 99% — print renderer differs very slightly from screen | 100% pixel-match |

**Default to `html-to-pdf`** for anything with links or anything people read on-screen: decks, one-pagers, playbooks, self-assessments, collaborator docs.

**Use `html-screenshot` + `png-to-pdf`** only when visual fidelity above all else matters AND there are no hyperlinks: posters, mockups, brand-art deliverables, anything where a CSS effect or pixel detail that the print renderer drops would be a regression.

## Required HTML boilerplate

The HTML must tell Chromium how to paginate. Add this once to the document's `<style>`:

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

Swap `.page` for whatever class wraps each page section and `8.5in 11in` for the target paper size. Without these rules Chromium will paginate based on its own heuristics and you'll get misaligned or split pages.

Any `<a href="https://...">` in the HTML automatically becomes a clickable annotation — wrap whole cards in `<a>` if you want the whole card to be clickable.

## Prerequisites

```bash
pip3 install playwright pypdf
python3 -m playwright install chromium
```

`pypdf` is optional — it only powers the post-export "Links detected" report. The export itself needs only `playwright`.

## Usage

From the repository root:

```bash
python3 .claude/skills/html-to-pdf/export.py <path/to/file.html>
```

Common flags:

| Flag | Default | Purpose |
|---|---|---|
| `-o, --output <path>` | `<name>.pdf` next to the HTML | Custom output path |
| `--size <preset \| WxH>` | `letter` | `letter`, `letter-landscape`, `a4`, `a4-landscape`, `tabloid`, `legal`, or custom `WxH` (e.g. `8.5x11`, `210mmx297mm`) |
| `--margin <len>` | `0` | Page margin applied to all sides. Usually leave 0 and control margins via the HTML's `@page` rule. |
| `--wait <ms>` | `1500` | Extra settle time after fonts/network idle |

## Examples

```bash
# Typical: Letter portrait deliverable with clickable links
python3 .claude/skills/html-to-pdf/export.py \
    Content_Collaborator_Overview/Content_Collaborator_Overview.html

# A4 portrait, custom output path
python3 .claude/skills/html-to-pdf/export.py \
    Report/Report.html --size a4 -o dist/report_v3.pdf

# Slide deck (Letter landscape)
python3 .claude/skills/html-to-pdf/export.py \
    Deck/Deck.html --size letter-landscape

# Custom square format
python3 .claude/skills/html-to-pdf/export.py \
    Lookbook/Lookbook.html --size 8x8
```

After export the script prints detected link annotations so you can verify the URLs wired up correctly:

```
Saved: .../Content_Collaborator_Overview.pdf  (663 KB)
Links detected (4):
  p3  https://atomgrants.com/webinars/ai-adoption-in-research-administration
  p4  https://atomgrants.com/blog/consistency-over-chaos
  p5  https://atomgrants.com/resources/the-ai-powered-research-newsletter-playbook
  p5  https://atomgrants.com/resources/the-ai-readiness-self-assessment-for-research-leaders
```

## Notes

- The script uses `page.emulate_media(media="print")` so `@media print` rules apply during export.
- `prefer_css_page_size=True` means the HTML's `@page` rule wins over the `--size` flag if both are set — that's usually what you want.
- Web fonts load correctly because the script waits for `networkidle` + `document.fonts.ready` before printing.
- Background colors and images print by default (`print_background=True`). Pass `--no-background` if you want a pure-text printout.
- Chromium's print renderer handles almost all modern CSS, but a few effects (some filters, fixed-position elements spanning pages) can render differently than screen. If you hit a visual regression, fall back to `html-screenshot` for that specific deliverable.
