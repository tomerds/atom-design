---
name: intro-call-deck
description: Create and personalize the Atom Grants intro / first-call sales deck for a specific prospect institution. Trigger when the user asks to "make an intro deck", "first call deck", "demo deck for [institution]", "customize the intro call deck", "spin up a deck for [University]", or render that deck to PDF. The finalized 8-slide template lives at Intro_Call_Deck/v4/Intro_Call_Deck.html.
---

# Intro Call Deck

The finalized template for Atom Grants' **first-call** deck. This is the deck used live on the initial ~30-minute call (discovery + intro), **not** the full demo — the in-depth, customized product demo happens on call 2.

## Where it lives

- **Template (source of truth):** `Intro_Call_Deck/v4/Intro_Call_Deck.html`
- **Worked example:** `Intro_Call_Deck/v4/Intro_Call_Deck_University_of_Iowa.html` (+ `.pdf`)
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

> Keep personalized copies **inside `Intro_Call_Deck/v4/`** so the relative `img/` and `../../assets` paths resolve. The script defaults there.

## Rendering manually

```bash
python3 .claude/skills/html-to-pdf/export.py Intro_Call_Deck/v4/<file>.html --size 13.333x7.5
```

The deck's print CSS sets `@page` to 13.333in × 7.5in with one slide per page; always pass `--size 13.333x7.5`.

## When editing the deck itself (not just personalizing)

- Edit the **template** (`Intro_Call_Deck/v4/Intro_Call_Deck.html`), then regenerate any prospect copies from it — don't hand-edit per-prospect files.
- Keep the five placeholder tokens intact in the template.
- Brand: single accent `#ff4227`, white bg, black text; Cal Sans titles, DM Sans body; headshots grayscale + square-rounded; no em dashes; no "modules" language (sell as one package).
- Content-heavy slides must fit a 7.5in page in print — preview the PDF after layout changes (the case-study stats and the leadership dashboard are the tight ones).
- To screenshot a single slide for review, temporarily set the bootstrap call `show(0)` to `show(N-1)` (or load with `#N` in a real browser), capture `[data-slide="N"]`, then revert.
