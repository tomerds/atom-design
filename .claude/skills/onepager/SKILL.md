---
name: onepager
description: Build Atom Grants one-pagers (single-page Letter sheets — product/module overviews, comparison sheets, leave-behinds, flyers) in the house "soft-card" UX style. Trigger when the user asks to "make a one-pager", "comparison sheet", "X vs Y one-pager", "product one-pager", "module overview", "leave-behind", or any single-page marketing sheet. Encodes the card system, soft dividers, highlighted-column comparison table, proof/scenario cards, vertical-balance and fit-check rules so every one-pager reads as one product. Canonical reference: `references/Atom_vs_GrantAI.html`.
---

# Atom Grants One-Pagers

A single Letter-portrait sheet (read on-screen or printed) that makes one argument: what a product/module does, how it compares, or why someone should care. The house style is **soft UX cards on white** — rounded, **flat** cards with a hairline border, separated by hairline gray, never hard black rules. One-pagers are printed and read as PDFs, so they carry **no shadows at all** (see "Banned: shadows on documents" in `CLAUDE.md`).

**Canonical reference (copy from this):** `references/Atom_vs_GrantAI.html` — a comparison one-pager that exercises every component in the system (positioning cards, the highlighted-column comparison table, scenario cards, the proof card). Start by reading it; reuse its CSS tokens and component blocks. The comparison layout is one *application* of the system — the **style** (cards, dividers, accent discipline, balance) is the part that's fixed.

> ⚠️ **Do NOT copy `Proposals_Module_Onepager/`.** It's the retired style: hard black hairlines, square corners, a left-accent-bar proof box. That's exactly what this skill replaces.

## Page setup

- Letter **portrait**, `.poster` = `816 × 1056px` (8.5×11in at 96dpi), fixed height, `padding: 34px 48px 28px`.
- Page background a warm off-white (`#eceae6`); the `.poster` itself is plain white. **No outer shadow and no page border** — the white sheet reads against the warm background on its own, and the exported PDF has no edge line.
- Include the `@page` + `@media print` block (size `8.5in 11in`, margin 0) so it exports clean. See the reference `<style>`.
- One self-contained HTML file. Brand tokens (`--accent #ff4227`, grays, Cal Sans titles / DM Sans body, DM Mono for eyebrows) come straight from `CLAUDE.md` — load them as CSS variables; the reference already does.
- Always set `font-weight: 400` on any Cal Sans heading element — `<h1>`/`<h2>`/`<h3>` default to `font-weight: bold` in browsers, which synthetic-bolds Cal Sans and makes it heavier than intended.

## The soft-card system (this is the style)

Everything that groups content is a **card**, and every card obeys the same rules:

- **Rounded corners:** `14px` (cards) / `12px` (the ends of the comparison-table accent band).
- **Borders:** `1px solid var(--gray-hair)` (`#e8e8e8`). Never a black border.
- **No shadows.** Cards are flat: border + radius + fill, nothing else. No `box-shadow`, no `filter: drop-shadow`, no accent glow. If a card isn't reading as a card, strengthen the border, don't add elevation.
- **Inner hairlines:** `#f1efec` or `--gray-hair` for row/cell dividers. **Structural rules** (top strip, hero underline, the thin line beside a section header) use `--gray-light` (`#d9d9d9`). **No black `var(--text)` dividers anywhere, ever.**

### Accent discipline

One accent (`#ff4227`), used sparingly: the **highlighted card**, status checks, and the one or two words that carry the punch. The highlighted card (the Atom side, the recommended option) gets:

- border `1.5px solid var(--accent)` and tint `background: #fff5f3`. **No accent glow** — the border and tint carry it.

**Keep the highlighted side consistent.** If Atom is the recommended/winning column, put it on the **same side in every section** of the sheet (the reference keeps Atom on the **right** in the positioning cards, the comparison table, and the scenario cards). The reader's eye should land on Atom in the same place every time. Use CSS `order` to place it without reordering the DOM.

### Section headers

Cal Sans `h2` (~19px) + a `flex: 1` rule line in `--gray-light`. That's the only divider style for sectioning.

## Component recipes (all in the reference)

- **Positioning cards** (`.pos-card`) — two side-by-side cards introducing the things being compared; the highlighted one tinted + accent-bordered. Title (Cal Sans) + mono category tag + a plain-language line + a mono meta footer.
- **Comparison table** (`.ctable`): **no outer card**, the table sits flush on the page. Left column = capability labels, middle = the muted product, right = the highlighted product as a **full-height accent band** (continuous `#fff5f3` fill, `1.5px` accent left/right borders, rounded **top corners on the header cell** and **bottom corners on the last row**). The band **lines up exactly with the highlighted cards above and below it**: grid `minmax(0,1.1fr) minmax(0,1fr) calc(50% + 8px)` with `margin-left: 16px` on the band cells, paired with a `16px` gap on every two-card grid (`.pos`, `.fits-grid`). **Row dividers run straight across**: a `#f1efec` line (`.crow + .crow::before`) spans the two left columns and the gap and stops at the band's border; inside the band a tinted `#f5ddd7` line (`.cell.atom::before`, `left: 0; right: 0`) continues between the borders, so the accent outline is never cut. Header carries a small accent **pill badge** (e.g. "Full platform"). Status icons: accent **filled circle check** (flat, no glow) for yes, **muted gray ✕** (`#ededed` bg, `#b4b4b4` mark) for no, **hollow ring `~`** for partial. The losing column stays muted gray text so the accent column reads as the answer.
- **Scenario / "when each fits" cards** — two cards, mono uppercase label + one plain sentence each; highlighted card tinted to match.
- **Proof card** (`.proof`) — a rounded `#fafafa` card with a small **accent status dot** before a mono label, then the named-customers line. **Not** a hard left-accent bar.

## Layout & balance (don't skip)

1. **Fill the page top-to-bottom.** Distribute vertical space so the content reaches near the bottom margin — no dead band at the foot, no clipped content at the head. If you remove a section, re-space the rest; don't leave the hole.
2. **Always run the fit-check before exporting.** Measure the rendered height — the `.poster` must not exceed 1056px:

   ```python
   # /tmp/measure.py
   from playwright.sync_api import sync_playwright
   import pathlib, sys
   url = pathlib.Path(sys.argv[1]).resolve().as_uri()
   with sync_playwright() as p:
       b = p.chromium.launch(); pg = b.new_page(viewport={"width":900,"height":1100})
       pg.goto(url); pg.wait_for_timeout(400)  # let web fonts load
       h = pg.eval_on_selector(".poster", "el => el.scrollHeight")
       print("scrollHeight:", h, "overflow:", h-1056); b.close()
   ```
   `overflow ≤ 0` = fits (the fixed-height `.poster` floors scrollHeight at 1056). `> 0` = trim.

3. **Levers to reclaim space, in order:**
   - **Comparison-table column widths.** This is the #1 culprit. The highlighted column is fixed (it must align with the cards), so balance the two left columns against each other: a too-narrow *label* column wraps labels to two lines, a too-narrow *muted* column wraps its descriptions. Shorten labels or muted cells before touching the band. Short cells (mostly "None") can live in the narrow column.
   - Table cell padding (`.crow .cell` / `.feat` vertical padding).
   - Section-header `padding-top`, card paddings, the hero padding.
   - Last resort: trim copy by a line (one-pagers reward terseness).

## Copy register

- **Plain language, no marketing voice** (per `CLAUDE.md`). Simplest word that works. Make the argument with structure (which card is highlighted, which icons are checks), not adjectives.
- **No em dashes.** Use commas, colons, or semicolons. (House preference.)
- Reserve real text for what carries meaning: card titles, the capability labels, the one-line scenario sentences, the punch word. Eyebrows/labels in DM Mono uppercase.

## Render

Default to **vector PDF** (read on-screen, selectable text, real links):

```bash
python3 .claude/skills/html-to-pdf/export.py <Project>/<Project>.html
```

Also keep a 2× PNG for previews / decks:

```bash
python3 .claude/skills/html-screenshot/shoot.py <Project>/<Project>.html
```

Use `html-screenshot` + `png-to-pdf` only for a pure poster/brand-art sheet with no links where pixel-fidelity beats selectable text.

## Build checklist

- [ ] White `.poster` on warm bg, `@page`/print CSS present.
- [ ] Every group is a rounded, **flat** bordered card; **zero `box-shadow` / `drop-shadow` in the file**; no black dividers (structural = `--gray-light`, inner = `#f1efec`).
- [ ] One accent; highlighted card tinted + accent-bordered (no glow); highlighted side **consistent across all sections**.
- [ ] Comparison table = no outer border; accent band aligned with the highlighted cards; row lines run through without cutting the band's outline; badge and the three icon states.
- [ ] Proof = soft gray card with accent dot (no left bar).
- [ ] Plain copy, no em dashes.
- [ ] **Fit-check passes** (`overflow ≤ 0`) and the page is balanced top-to-bottom.
- [ ] Exported to vector PDF.
