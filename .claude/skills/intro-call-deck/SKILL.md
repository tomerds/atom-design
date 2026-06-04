---
name: intro-call-deck
description: Create and personalize the Atom Grants intro / first-call sales deck for a specific prospect institution. Trigger when the user asks to "make an intro deck", "first call deck", "demo deck for [institution]", "customize the intro call deck", "spin up a deck for [University]", or render that deck to PDF. The finalized 8-slide template lives at Intro_Call_Deck/Intro_Call_Deck.html.
---

# Intro Call Deck

The finalized template for Atom Grants' **first-call** deck. This is the deck used live on the initial ~30-minute call (discovery + intro), **not** the full demo — the in-depth, customized product demo happens on call 2.

## Where it lives

- **Template (source of truth):** `Intro_Call_Deck/Intro_Call_Deck.html`
- **Personalizer:** `.claude/skills/intro-call-deck/personalize.py`

Single self-contained HTML file. 16:9 slides, presented in-browser or exported to PDF. Navigate with arrow keys / Space / click; `f` fullscreen; `#N` deep-links to slide N.

## The 8 slides

1. **Cover** — hero line + presenter / date / institution
2. **Why now** — the squeeze: rising workload, flat budgets, less funding visibility
3. **A different category** — "a teammate, not a search tool," with a partner quote
4. **How it works** — the six-step research-development workflow (sold as one package — never "modules")
5. **Case study** — University of Memphis, dark slide, quote + stats
6. **Partners** — full-color logo strip + customer quote cards + "and 45+ more"
7. **For leadership** — analytics dashboard (show when leadership is on the call)
8. **Next steps & Q&A** — steer to the full demo, focused on what they care about most

## Personalizing for a prospect

**Only two slides change per prospect: the cover and the close slide.** Five placeholder tokens:

| Token | Where | Example |
|---|---|---|
| `[Your name]` | cover "Presented by" + contact | `Tomer du Sautoy` |
| `[Title]` | cover, after the name | `Atom Grants` |
| `[Month YYYY]` | cover "Date" | `June 2026` |
| `[Institution name]` | cover "For" | `University of Iowa` |
| `[your.email@atomgrants.com]` | contact line | `tomer@atomgrants.com` |

Run the personalizer (copies the template, swaps the tokens, renders the PDF):

```bash
python3 .claude/skills/intro-call-deck/personalize.py \
    --institution "University of Iowa" \
    --name "Tomer du Sautoy" \
    --email "tomer@atomgrants.com" \
    --date "June 2026"
```

Output lands next to the template as `Intro_Call_Deck_<Slug>.html` + `.pdf`. Flags: `--title` (cover org/title, default "Atom Grants"), `--out`, `--no-pdf`.

> Keep personalized copies **inside `Intro_Call_Deck/`** so the relative `img/` and `../assets` paths resolve. The script defaults there.

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
    page = p.chromium.launch().new_context(
        viewport={"width":1920,"height":1080}, device_scale_factor=2.0).new_page()
    page.goto(f"file://{html}"); page.wait_for_load_state("networkidle")
    page.evaluate("document.fonts.ready"); page.wait_for_timeout(1000)
    for i in range(page.evaluate("document.querySelectorAll('.slide').length")):
        page.evaluate("(n)=>{location.hash='#'+n;}", i+1)
        page.wait_for_timeout(350)
        page.locator(".slide.active").screenshot(
            path=str(html.with_name(f"{html.stem}_slide_{i+1:02d}@2x.png")), type="png")
PY

# 2) Stitch into a 13.333×7.5 (16:9) PDF.
python3 .claude/skills/png-to-pdf/merge.py \
    Intro_Call_Deck/<file>_slide_*@2x.png \
    -o Intro_Call_Deck/<file>.pdf --size 13.333x7.5 --title "<Title>"
```

The PDF is raster: pixel-perfect to the HTML, but text isn't selectable and links aren't clickable. That tradeoff is intentional and accepted for this deck.

## When editing the deck itself (not just personalizing)

- Edit the **template** (`Intro_Call_Deck/Intro_Call_Deck.html`), then regenerate any prospect copies from it — don't hand-edit per-prospect files.
- Keep the five placeholder tokens intact in the template.
- Brand: single accent `#ff4227`, white bg, black text; Cal Sans titles, DM Sans body; headshots grayscale + square-rounded; no em dashes; no "modules" language (sell as one package).
- Content-heavy slides must fit a 7.5in page in print — preview the PDF after layout changes (the case-study stats and the leadership dashboard are the tight ones).
- To screenshot a single slide for review, temporarily set the bootstrap call `show(0)` to `show(N-1)` (or load with `#N` in a real browser), capture `[data-slide="N"]`, then revert.
