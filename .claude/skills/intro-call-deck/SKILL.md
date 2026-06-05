---
name: intro-call-deck
description: Create and personalize the Atom Grants intro / first-call sales deck for a specific prospect institution. Trigger when the user asks to "make an intro deck", "first call deck", "demo deck for [institution]", "customize the intro call deck", "spin up a deck for [University]", or render that deck to PDF. The finalized 8-slide template lives at Intro_Call_Deck/Intro_Call_Deck.html.
---

# Intro Call Deck

The finalized template for Atom Grants' **first-call** deck. This is the deck used live on the initial ~30-minute call (discovery + intro), **not** the full demo — the in-depth, customized product demo happens on call 2.

## Where it lives

- **Template (source of truth):** `Intro_Call_Deck/Intro_Call_Deck.html`
- **Personalizer:** `.claude/skills/intro-call-deck/personalize.py`

Single self-contained HTML file. Full-viewport slides, presented in-browser (fills whatever window) or exported to a **3:2 (12×8 in) PDF** — a laptop-friendly, less-wide frame. Navigate with arrow keys / Space / click; `f` fullscreen; `#N` deep-links to slide N.

## The 8 slides

1. **Cover** — hero line + co-brand lockup (Atom **x** partner logo) + presenter / date / institution
2. **Partners** — full-color logo strip + customer quote cards + "and 45+ more"
3. **Why now** — the squeeze: rising workload, flat budgets, less funding visibility
4. **A different category** — "a teammate, not a search tool," with a partner quote
5. **How it works** — six product capabilities as website-style cards, each with a mini product mock (Automated Profiles, Grant Discovery, Eligibility Checks, Collaborator Identification, Proposal Guides, AI Proposal Review). Sold as one package — never "modules"
6. **Case study** — University of Memphis, dark slide, quote + stats
7. **The admin backend** — analytics + project-management board + faculty directory (show when leadership is on the call)
8. **Next steps & Q&A** — steer to the full demo, focused on what they care about most

> Slide order is set in the deck (Partners is slide 2, the admin backend is slide 7). The numbered eyebrows in the HTML count the content slides after the cover.

## Personalizing for a prospect

**Only two slides change per prospect: the cover and the close slide.** Five placeholder tokens, plus the partner logo (required — see below):

| Token | Where | Example |
|---|---|---|
| `[Your name]` | cover "Presented by" + contact | `Tomer du Sautoy` |
| `[Title]` | cover, after the name | `Atom Grants` |
| `[Month YYYY]` | cover "Date" | `June 2026` |
| `[Institution name]` | cover "For" | `University of Iowa` |
| `[your.email@atomgrants.com]` | contact line | `tomer@atomgrants.com` |
| partner logo | cover co-brand lockup | `--logo iowa-logo.png` |

Run the personalizer (copies the template, swaps the tokens, inlines the partner logo, renders the PDF):

```bash
python3 .claude/skills/intro-call-deck/personalize.py \
    --institution "University of Iowa" \
    --name "Tomer du Sautoy" \
    --email "tomer@atomgrants.com" \
    --date "June 2026" \
    --logo ~/Downloads/iowa-logo.png
```

Output lands next to the template as `Intro_Call_Deck_<Slug>.html` + `.pdf`. Flags: `--logo` (**required** — partner logo for the cover lockup, see below), `--title` (cover org/title, default "Atom Grants"), `--out`, `--no-pdf`.

> Keep personalized copies **inside `Intro_Call_Deck/`** so the relative `img/` and `../assets` paths resolve. The script defaults there.

## Partner logo (cover co-brand lockup) — required

The cover shows a co-brand lockup: the Atom Grants wordmark, a thin gray **×**, then the partner's logo. In the clean template that partner slot is a dashed placeholder:

```html
<span class="partner-logo">[Partner logo]</span>
```

`--logo` is **required**. The script copies the file into `Intro_Call_Deck/tempimg/` and points the cover lockup at `tempimg/<institution-slug>.<ext>`. It does **not** put the logo in `img/`. The `.gitignore` tracks only `Intro_Call_Deck.html` and `img/` inside `Intro_Call_Deck/`, so `tempimg/` (and the per-prospect HTML/PDF) are git-ignored — the partner logo never gets committed. PNG (transparent), SVG, JPG, WebP, or GIF all work.

So: just download the prospect's logo anywhere (e.g. `~/Downloads/`) and point `--logo` at it. The copy in `tempimg/` is local-only.

Logo sourcing & prep:
- Prefer a **full-color** logo on a transparent or white background (PNG or SVG). The lockup sits on white, so it drops in cleanly. Avoid logos baked onto a colored tile.
- The `.partner-logo-img` CSS height-matches it to the Atom wordmark (`height: clamp(40px, 3.6vw, 54px)`, `max-width: 240px`, `object-fit: contain`) — sizing is automatic.
- A wordmark-style logo (mark + institution name) or a bare icon mark both read well next to the Atom wordmark.

> Hand-editing (rare): if you skip the script, drop the logo in `Intro_Call_Deck/tempimg/` and swap the placeholder span for `<img class="partner-logo-img" src="tempimg/<partner>.png" alt="<Partner>">`. **Do not** add the logo under `img/`, since that folder is committed.

## Rendering the PDF — always screenshot-and-stitch, never html-to-pdf

**Do not use `html-to-pdf` for this deck.** Its print renderer mis-paginates the full-viewport 16:9 slides and the formatting comes out wrong. Always render by capturing each slide as a 2× PNG and stitching the PNGs into the PDF.

`personalize.py` does this for you (it's the only render path the script supports). To render an existing HTML manually, capture each slide then merge:

```bash
# 1) Step the deck through its 8 slides, capturing each at 2×.
#    Navigate via the deck's hash deep-link (#N) so its show() runs — this
#    updates BOTH the .active slide and the page-number counter. (Toggling the
#    .active class directly leaves every slide stuck on 1/N.)
python3 - "Intro_Call_Deck/<file>.html" << 'PY'
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
html = Path(sys.argv[1]).resolve()
with sync_playwright() as p:
    # 3:2 capture viewport (1620x1080) so the full-viewport slides reflow into
    # a laptop-friendly, less-wide frame rather than the wide 16:9 default.
    page = p.chromium.launch().new_context(
        viewport={"width":1620,"height":1080}, device_scale_factor=2.0).new_page()
    page.goto(f"file://{html}"); page.wait_for_load_state("networkidle")
    page.evaluate("document.fonts.ready"); page.wait_for_timeout(1000)
    for i in range(page.evaluate("document.querySelectorAll('.slide').length")):
        page.evaluate("(n)=>{location.hash='#'+n;}", i+1)
        page.wait_for_timeout(350)
        page.locator(".slide.active").screenshot(
            path=str(html.with_name(f"{html.stem}_slide_{i+1:02d}@2x.png")), type="png")
PY

# 2) Stitch into a 12×8 (3:2) PDF.
python3 .claude/skills/png-to-pdf/merge.py \
    Intro_Call_Deck/<file>_slide_*@2x.png \
    -o Intro_Call_Deck/<file>.pdf --size 12x8 --title "<Title>"
```

The PDF is raster: pixel-perfect to the HTML, but text isn't selectable and links aren't clickable. That tradeoff is intentional and accepted for this deck.

## When editing the deck itself (not just personalizing)

- Edit the **template** (`Intro_Call_Deck/Intro_Call_Deck.html`), then regenerate any prospect copies from it — don't hand-edit per-prospect files.
- Keep the five placeholder tokens intact in the template.
- Brand: single accent `#ff4227`, white bg, black text; Cal Sans titles, DM Sans body; headshots grayscale + square-rounded; no em dashes; no "modules" language (sell as one package).
- Content-heavy slides must fit the 3:2 frame (rendered at a 1620×1080 viewport, stitched to a 12×8in page) — preview the PDF after layout changes (the case-study stats and the admin-backend dashboard are the tight ones).
- To screenshot a single slide for review, temporarily set the bootstrap call `show(0)` to `show(N-1)` (or load with `#N` in a real browser), capture `[data-slide="N"]`, then revert.
