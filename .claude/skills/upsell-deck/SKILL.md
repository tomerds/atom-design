---
name: upsell-deck
description: Create and personalize the Atom Grants renewal-upsell deck for an existing partner institution. This is the deck for the renewal / expansion conversation — discovery is already working, now upsell Researcher Search + Proposal Development ahead of the renewal. Trigger when the user asks to "make an upsell deck", "renewal deck for [institution]", "expansion deck", "upsell [University]", "renewal upsell", or to render that deck to PDF. The finalized 8-slide template lives at Upsell_Deck/Upsell_Deck.html.
---

# Renewal Upsell Deck

The finalized template for Atom Grants' **renewal / expansion** deck. Used live with an **existing partner** where discovery is already working, to upsell **Researcher Search** and **Proposal Development** ahead of the renewal. It reframes from "what you license today" to "the next gain": you are finding more grants, now win more proposals.

This is the upsell cousin of the `intro-call-deck` (same chassis, CSS, render path). The difference is the narrative: it opens on the partner's own results, names the gap, then sells the new capabilities.

## Where it lives

- **Template (source of truth):** `Upsell_Deck/Upsell_Deck.html`
- **Personalizer:** `.claude/skills/upsell-deck/personalize.py`

Single self-contained HTML file. Full-viewport slides, presented in-browser or exported to a **3:2 (12×8 in) PDF**. Navigate with arrow keys / Space / click; `f` fullscreen; `#N` deep-links to slide N.

## The 8 slides

1. **Cover** — hero line ("You're finding more grants. Now let's win more proposals.") + co-brand lockup (Atom **×** partner logo) + presenter / date / institution
2. **Where you are now** — the partner's all-time usage recap, six metric cells (Active faculty, Monthly actives, Grants favorited, Faculty using AI chat, Still subscribed, Department reach). **This is the data slide — see below.**
3. **The gap** — what Atom already solved (getting the right grants in front of faculty) vs what's still on the team (turning a match into a winning submission)
4. **Already happening** — your faculty are already using AI to build proposals, with a customer quote (the next step is real tools + guardrails)
5. **What's new** — the upsell: Researcher Search (build the team), Proposal Guides (build the proposal), AI Proposal Review (win the proposal), each with a mini product mock
6. **The pipeline** — admin backend: engagement analytics + a proposal project board, so the office sees every submission in flight
7. **Case study** — University of Memphis, dark slide, quote + stats (reusable proof)
8. **Next steps & Q&A** — quick demo today, then a decision before the renewal auto-renews

> The numbered eyebrows (01–07) count the content slides after the cover.

## The data slide (slide 2) — fed per partner, ships as skeleton

Slide 2 is grounded in the partner's **actual usage** and is the one slide that is genuinely bespoke per partner. The same numbers reappear as the slide-6 dashboard KPIs. In the clean template **both are grey skeleton bars** (`.skel`) — `personalize.py` does **not** fill them. Once you have the partner's numbers:

- Slide 2: replace each `<span class="skel num"></span>` with the figure (e.g. `<div class="num">449</div>`) and each pair of `<span class="skel line ...">` with a one-line `<p>` description. Keep the six standard metric `<h3>` labels (swap a label only if a metric truly doesn't apply).
- Slide 6: replace the four `<span class="skel kv">` with the same figures as `<div class="v">…</div>` (the last one keeps `class="v accent"`).

Both spots are marked with `<!-- DATA PENDING -->` comments. Until filled, the deck reads as an honest work-in-progress draft — which is the intended state when a partner's data hasn't landed yet.

## Personalizing for a partner

Mechanical tokens (swapped by `personalize.py`):

| Token | Where | Example |
|---|---|---|
| `[Institution full]` | cover "For", logo alt | `Youngstown State University` |
| `[Institution]` | cover sub + headlines + prose (conversational) | `Youngstown State` |
| `[Your name]` | cover "Presented by" + contact | `Tomer du Sautoy` |
| `[Title]` | cover, after the name | `Atom Grants` |
| `[Month YYYY]` | cover "Date" | `June 2026` |
| `[your.email@atomgrants.com]` | contact line | `tomer@atomgrants.com` |
| `[Renewal decision]` | slide 8 "Decision by" | `Aug 1 auto-renewal` |
| `[Renewal date]` | slide 8 "Renews" | `Sep 1, 2026` |
| partner logo | cover co-brand lockup | `--logo youngstown-state.png` |

Run the personalizer (copies the template, swaps the tokens, drops in the partner logo, renders the PDF):

```bash
python3 .claude/skills/upsell-deck/personalize.py \
    --institution "Youngstown State University" \
    --short "Youngstown State" \
    --name "Tomer du Sautoy" \
    --email "tomer@atomgrants.com" \
    --date "June 2026" \
    --logo Upsell_Deck/img/logos/youngstown-state.png \
    --renewal-decision "Aug 1 auto-renewal" \
    --renewal-date "Sep 1, 2026"
```

Output lands next to the template as `Upsell_Deck_<Slug>.html` + `.pdf`. Flags: `--logo` (**required**), `--short` (conversational name, default = `--institution`), `--title` (default "Atom Grants"), `--renewal-decision` / `--renewal-date` (optional — omit to leave the bracket token visible and fill later), `--out`, `--no-pdf`.

The script prints a NOTE listing any tokens still unresolved and reminds you the slide-2 / slide-6 figures are still skeleton.

> Keep personalized copies **inside `Upsell_Deck/`** so the relative `img/` and `../assets` paths resolve. The script defaults there.

## Partner logo (cover co-brand lockup) — required

The cover shows a co-brand lockup: the Atom Grants wordmark, a thin gray **×**, then the partner's logo. In the clean template that partner slot is a dashed placeholder:

```html
<span class="partner-logo">[Partner logo]</span>
```

`--logo` is **required**. The script copies the file into `Upsell_Deck/tempimg/` and points the cover lockup at `tempimg/<institution-slug>.<ext>`. It does **not** put the logo in `img/`. `tempimg/` is git-ignored, so the per-partner logo never gets committed. PNG (transparent), SVG, JPG, WebP, or GIF all work.

Logo sourcing & prep:
- Prefer a **full-color** logo on a transparent or white background. The lockup sits on white, so it drops in cleanly. Avoid logos baked onto a colored tile.
- The `.partner-logo-img` CSS height-matches it to the Atom wordmark (`height: clamp(40px, 3.6vw, 54px)`, `max-width: 240px`, `object-fit: contain`) — sizing is automatic.

> Hand-editing (rare): if you skip the script, drop the logo in `Upsell_Deck/tempimg/` and swap the placeholder span for `<img class="partner-logo-img" src="tempimg/<partner>.png" alt="<Partner>">`. **Do not** add the logo under `img/` (that folder is committed).

## Rendering the PDF — always screenshot-and-stitch, never html-to-pdf

**Do not use `html-to-pdf` for this deck.** Its print renderer mis-paginates the full-viewport slides. Always render by capturing each slide as a 2× PNG and stitching them into the PDF — exactly what `personalize.py` does (at a 1620×1080 / 3:2 capture viewport, stitched to a 12×8 in page). To render an existing HTML manually, reuse the snippet from the `intro-call-deck` SKILL (identical mechanism) but point it at the `Upsell_Deck/` file.

The PDF is raster: pixel-perfect to the HTML, but text isn't selectable and links aren't clickable. That tradeoff is intentional for this deck.

## When editing the deck itself (not just personalizing)

- Edit the **template** (`Upsell_Deck/Upsell_Deck.html`), then regenerate partner copies — don't hand-edit per-partner files (except to fill the data slide, which is expected).
- Keep the placeholder tokens and the `.skel` skeleton spots intact in the template.
- Brand: single accent `#ff4227`, white bg, black text; Cal Sans titles, DM Sans body; headshots grayscale + square-rounded; **no em dashes**; sell the new capabilities as additions to one package, not "modules". Always set `font-weight: 400` on Cal Sans heading elements (browsers default `<h1>`/`<h2>`/`<h3>` to bold, which synthetic-bolds Cal Sans).
- **Never** put a colored left rule (vertical accent bar) on a panel or text block — that callout reads as AI "admonition box" boilerplate and is off-brand. Emphasize with an accent eyebrow/label, a single accent word, or a chip.
- Content-heavy slides must fit the 3:2 frame — preview the PDF after layout changes (slide 5's three product mocks and slide 6's dashboard are the tight ones).
- The case study (slide 7) and the customer quote (slide 4) are reusable proof; leave them unless the user supplies a better-matched reference.
