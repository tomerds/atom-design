---
name: checkin-deck
description: Build periodic check-in decks for Atom Grants partner institutions (30/60/90/180/270-day reviews, annual QBRs, renewal-conversation decks). Encodes the slide order, comparison framing, copy register, chart conventions, brand system, and data-interpretation gotchas so every check-in deck across every customer reads as one consistent product. Trigger when the user asks for a "check-in deck", "QBR", "90-day / 180-day / 270-day review", "renewal deck", "customer review deck", or any periodic metrics review for a partner institution. The reference implementation lives at `NYULH_180_Day_Checkin/v1/`.
---

# Atom Grants Partner Check-In Decks

Decks reviewing a partner institution's engagement with Atom over a defined period. Used in renewal conversations, internal QBRs, and milestone reviews with the customer's research-development leadership. Reference: `NYULH_180_Day_Checkin/v1/`.

## When to use

- **Milestone check-ins** at 30 / 60 / 90 / 180 / 270 days from onboarding
- **Annual QBRs** with the partner sponsor (typically Office of Sponsored Programs, VP Research)
- **Renewal-conversation decks** when contract end is 60-90 days out
- **Internal account reviews** preparing the team for a customer call

Skip this skill for: one-off pitch decks (use `Intro_Call_Deck` patterns), webinar recaps, marketing reports.

## Output format

- **One self-contained HTML file** per deck. Single `<style>` block. No build step.
- Each slide is `100vw × 100vh`, deck navigates with arrow keys / space / click. Deep-link via `?slide=N`.
- **Always produce three artifacts:** the HTML, a 13.333×7.5in vector PDF (via `html-to-pdf`), and 1920×1080 @2x PNGs per slide (via Playwright + `?slide=N`).
- Version each iteration: `v1/`, `v2/`, etc. Move the working version into its own subfolder; never overwrite a prior version.

## File layout

```
<Partner>_<N>_Day_Checkin/
└── v1/                                      # shipped version (canonical)
    ├── <Partner>_<N>_Day_Checkin.html
    ├── <Partner>_<N>_Day_Checkin.pdf
    ├── <partner-logo>.png                   # at v1/ root for sibling-relative paths
    └── slide_NN@2x.png
```

**Asset paths.** Inside a `vN/` folder, the deck is two levels deep relative to `/Design/`. Reference shared assets with `../../assets/...` (not `../assets/...`). The partner logo sits *inside* the `vN/` folder and is referenced as a sibling (`nyulogo.png`).

## Slide order (canonical sequence)

**Default 12 slides** for a 180-day check-in. Drop slides 11-12 if there's no module/renewal story to tell yet. Always keep the relative order — never reshuffle.

| # | Slide | One-line job |
|---|---|---|
| 01 | **Cover** | Logo lockup + "{N}-Day Check-In" + period meta block |
| 02 | **All-time headlines** | 4 big stat tiles: total volume metrics (page views, AI chats, favorites, searches) |
| 03 | **Activation** | Donut showing engaged-vs-roster, plus 3 supporting numbers (engaged / active recent / yet to activate) |
| 04 | **Period comparison** | 4 stat tiles: before vs since the prior check-in, with daily rates |
| 05 | **Weekly engagement trend** | Bar chart, full timeline, dashed accent marker at the prior check-in date |
| 06 | **Cohort flow** | Three numbers — retained / new / lapsed — with a takeaway line |
| 07 | **Top departments** | Table: department, active users, page visits, engagement bar, growth % vs prior period. **Does the volume *and* growth job in one slide** — don't add a separate "fastest-growing" slide, it duplicates this one |
| 08 | **Funder mix shift** | Horizontal bars of top 12 funders since the check-in, with `NEW` pills on first-time funders. Right column = "what's changing" commentary + one big callout (e.g. "+910 views across industry/foundation funders") |
| 09 | **Channels** | Stacked bar lists (P1 vs P2) showing where visits originate (email, dashboard, search, direct) + a takeaway headline |
| 10 | **Top active researchers** | Ranked table of top 10: #, name, department, page views, AI chats, searches, favorites. No accent on rows — table speaks for itself. Eyebrow does the framing |
| 11 | **Next steps** | 3 priorities for the next quarter — number, headline, paragraph. Point 03 = renewal conversation when contract end is within 90-120 days |
| 12 | **Modules / what's coming** | 2 cards teasing roadmap (currently Researcher Search + Proposals), only when there's a real renewal story |

**Slide 03 (Activation) is non-negotiable** even on early check-ins — it sets the context for every other metric.

**Don't add a separate "fastest-growing departments" slide.** It feels duplicative with slide 07 because slide 07 already accent-highlights the >50% growth rows in its growth column. We removed it from the canonical sequence after the first NYULH iteration.

## Cover slide (slide 01)

Format:

```
[Atom Grants logo]   ×   [Partner logo]

{N}-Day            ← "{N}-Day" in accent
Check-In.          ← black

PERIOD                COMPARED TO              PREPARED
Oct 2025 — May 2026   90-day check-in (Jan 21) May 13, 2026
```

- Both logos at the same height. The `×` is a Cal Sans glyph, vertically centered, in `--rule-mid` gray. Use `align-items: center` on the cover-row, *not* `flex-end`.
- Headline: `clamp(72px, 9vw, 148px)` Cal Sans, line-height 0.96. The `{N}-Day` word is accent; `Check-In.` is black.
- Keep meta block short: Period · Compared to · Prepared.
- **No subhead.** No "found its audience" tagline — the user asked us to remove flowery framing on the cover.
- **Partner logo** lives inside the deck's `vN/` folder (e.g. `nyulogo.png`). Reference as a sibling: `src="nyulogo.png"`. Use the partner's published wordmark logo — do not recreate or stylize.

## Brand system

| Token | Value | Use |
|---|---|---|
| `--accent` | `#ff4227` | The **only** accent. Used sparingly — see "accent discipline" below |
| `--bg` | `#ffffff` | Slide background |
| `--text` | `#000000` | Body text and most numbers |
| `--text-muted` | `#6b6b6b` | Eyebrows, supporting copy, axis labels |
| `--rule-soft` | `#e6e6e6` | Table row dividers, soft borders |
| `--rule-mid` | `#d9d9d9` | Cover `×`, separators |
| `--rule-strong` | `#333333` | Stat-tile top rules (when not accent) |
| Title font | Cal Sans (via `fonts.cdnfonts.com/css/cal-sans`) | All headlines, big numbers |
| Body font | DM Sans 400/500/700 (Google Fonts) | All copy, labels, axis text |
| Logo | `../../assets/newredlogowordmarkhighres.png` | Brand bar, top-left of every slide (path assumes deck lives in `<project>/vN/`) |

**CSS variables block** (always at the top of `<style>`):

```css
:root {
  --accent: #ff4227;
  --accent-soft: #ffe7e3;
  --bg: #ffffff;
  --bg-alt: #fafafa;
  --text: #000000;
  --text-muted: #6b6b6b;
  --rule-soft: #e6e6e6;
  --rule-mid:  #d9d9d9;
  --rule-strong: #333333;
  --font-title: "Cal Sans", "DM Sans", system-ui, sans-serif;
  --font-body: "DM Sans", system-ui, sans-serif;
  --pad-x: clamp(56px, 6.5vw, 112px);
  --pad-y: clamp(48px, 5.5vw, 88px);
}
```

## Accent discipline (most important visual rule)

**One focal accent moment per slide.** When everything is highlighted, nothing is. Default everything to black / muted gray and earn the accent.

What deserves accent on a slide:
- One word in the headline (the punchline)
- "Now / since" data in a P1-vs-P2 comparison (legend-driven)
- One row in a table where the data demands attention (e.g. growth >50%)
- "NEW" tags / pills (semantic — first appearance)
- The single hero number on a callout slide

What should **not** be accent:
- Eyebrows (use muted gray)
- Stat-tile top rules (use thin gray by default)
- Every numeral on a power-users card (just the headline number)
- Every bar in a table chart (only the rows you want the eye to land on)
- 01 / 02 / 03 sequence numerals on the next-steps slide *unless* they're the lone accent moment

When in doubt, run the deck and ask: "What is my eye drawn to first on this slide?" If the answer is more than one thing, prune.

## Copy register

- **Direct, not flowery.** "Favorites" not "save-for-later actions." "Active users" not "engaged community members."
- **Sentence-case headlines** with title-case proper nouns. No em-dashes-as-stage-pauses except for separating clauses.
- **No taglines or framing copy** on the cover ("A platform that has found its audience" was removed for being too marketing-y).
- **Headlines fit on one line where possible.** If a headline runs to two lines naturally, fine — but never let a key line break in the middle of a phrase. Use `white-space: nowrap` + reduced font for one-liners that should stay together (e.g., "Email is now 73% of all grant traffic — up from 55%.").
- **No single-word orphan lines.** Always set `text-wrap: balance` on the `.headline` class so multi-line headlines distribute evenly. `text-wrap: pretty` is too weak for these display sizes — Chromium leaves single-word last lines (e.g. "researchers." alone) even with `pretty`. `balance` fixes them. Spot-check every slide's rendered PNG after writing copy; if a one-word line survives, reword or widen `max-width` on that slide's headline by 4-6ch.
- **Period labels are absolute dates, not codenames.** Use "Through Jan 21" and "Since Jan 21" in copy. "P1 / P2" is OK inside chart legends or short axis labels only.
- **Footers are uppercase, tracked.** Format: `PARTNER NAME · ATOM GRANTS` on the left, slide counter `NN / TT` on the right with the current number in accent.

## Period comparison framing

**Periods are rarely equal in length.** A 180-day check-in compared to a 90-day check-in has 146 days of P1 data and 112 days of P2 data (the prior cycle had a ramp-up). Be honest about this:

- **Show both absolute totals and daily rates.** On the period-comparison slide (typically 04), label each tile with both: `9,401 / Through Jan 21 / 64 / day` next to `10,893 / Since Jan 21 / 97 / day`.
- **Lead the headline with the daily rate** — that's the fair comparison. "Daily engagement up 51%" beats "Visits up 16%."
- **Disclose period lengths in the legend** of every period-comparison chart: `Through Jan 21 (146 days)` vs `Since Jan 21 (112 days)`.
- **Don't compute "%" deltas on absolute totals when the periods differ.** It silently undersells real growth and a sharp reader will catch it.

## Chart conventions

### Color
- **Gray bars** = before / through-period. Use `var(--rule-mid)` (#d9d9d9) or `#bfbfbf`.
- **Accent bars** = since / current period. `var(--accent)`.
- **In growth/sorted-by-delta charts:** accent only the rows where the data merits emphasis (e.g. >50% growth). Everything else dark gray.

### Type
- Axis labels: DM Sans 11-12px, `var(--text-muted)`.
- Big stat numbers: Cal Sans, `clamp(48px, 5vw, 84px)`, letter-spacing -0.02em.
- Numerals in tables: tabular nums, right-aligned.

### Weekly trend (slide 05)
- Vertical bars, one per week. ~37 weeks total for a 180-day check-in.
- **Dashed accent vertical line** marking the previous check-in date (Jan 21), labeled inline.
- Gray bars before the line, accent bars after.
- Y-axis: 0, 250, 500, 750, 1000 with dashed soft gridlines.
- Three callouts beneath the chart: avg-per-day current, % change vs prior, weeks above floor.

### Funder mix (slide 08)
- Two-column layout: left = list of top 12 funders (since the check-in), right = commentary panel + one big callout box.
- `NEW` pill in accent-soft background for funders with zero pre-check-in views.
- Numbers in tabular DM Mono / DM Sans, right-aligned. Current-period number bold; prior number muted.

### Top active researchers (slide 10)
- **Ranked table, not cards.** Cards were the first iteration but the user replaced them with a table to show a fuller activity profile per person.
- Columns: `#`, `Name`, `Department`, `Page views`, `AI chats`, `Searches`, `Favorites`.
- Sort descending by page views, top 10.
- No accent on rows — let the numbers do the work. The eyebrow ("Most active researchers · all-time") and the headline ("The 10 most active researchers on Atom.") frame the slide; no editorial claim like "X researchers drove Y% of traffic" since that ties the slide to a single message instead of letting the reader read.
- Department names: trim long lists. Use the first or most relevant department; replace ", " separator with " · " when keeping two.

## Data-interpretation gotchas

These are lessons from the NYULH deck — verify these explicitly when pulling data for a new institution:

1. **A "user count" file may be the roster, not the active base.** NYU's roster CSV had 2,567 rows but only 1,645 had loaded any page. Always check: how many rows have nonzero engagement? Don't conflate "addressable population" with "active users" in copy.
2. **Verify unique counts across CSVs.** The visits, searches, favorites, page-views, and chats exports each give a different "user count." Document which denominator you're using in each tile's `note` line.
3. **Cross-check totals against an independent source before publishing.** The first NYULH chats export was reported as 5,851 chats across 733 chatters; the corrected export was 207 chats across 92 chatters — a >25× difference. If a metric seems unusually large relative to the rest of the deck (e.g. ~3.6 chats per active researcher when the product is new), ask for a re-pull *before* shipping the deck.
4. **Event count ≠ distinct items.** "1,308 favorites" is 1,308 favoriting events across 780 distinct grants. Label both when relevant.
5. **Convert all relative dates to absolute** when writing copy ("Aug 31" not "renewal date").
6. **Per-day rates beat raw totals** when comparing unequal-length periods. See "Period comparison framing" above.

## Render / export

From the repo root:

```bash
# 1. Screen PNGs (one per slide, via Playwright deep-linking)
python3 - <<'EOF'
from playwright.sync_api import sync_playwright
from pathlib import Path
html = Path("<Partner>_<N>_Day_Checkin/<Partner>_<N>_Day_Checkin.html").resolve()
out = html.parent
with sync_playwright() as p:
    b = p.chromium.launch()
    for i in range(1, 13):  # adjust to your slide count
        c = b.new_context(viewport={"width": 1920, "height": 1080}, device_scale_factor=2.0)
        page = c.new_page(); page.goto(f"file://{html}?slide={i}")
        page.wait_for_load_state("networkidle"); page.evaluate("document.fonts.ready")
        page.wait_for_timeout(700)
        page.screenshot(path=str(out / f"slide_{i:02d}@2x.png"), clip={"x":0,"y":0,"width":1920,"height":1080})
        c.close()
    b.close()
EOF

# 2. Vector PDF with clickable links
python3 .claude/skills/html-to-pdf/export.py <Partner>_<N>_Day_Checkin/<Partner>_<N>_Day_Checkin.html --size 13.333x7.5
```

The `?slide=N` deep-link relies on the navigation `<script>` reading `URLSearchParams`. Include it in every deck.

## Print rules (critical — the v1 deck regressed twice on this)

The Playwright print viewport is `1280 × 720` (13.333×7.5in at 96 dpi), **not** `1920 × 1080`. `vw`-based `clamp()` values collapse to their middle values, breaking layouts tuned to the screen viewport. Always include print-specific overrides:

```css
@media print {
  :root { --pad-x: 60px; --pad-y: 56px; }
  .brand { top: 28px; height: 22px; }
  .counter, .footer-meta { bottom: 28px; }

  html, body {
    background: #fff; margin: 0; padding: 0; overflow: visible;
    width: 13.333in; height: auto;
  }
  .deck { position: static; width: 13.333in; height: auto; }
  .slide {
    display: flex !important;
    position: relative !important;
    inset: auto !important;
    width: 13.333in !important;
    height: 7.5in !important;
    page-break-after: always; break-after: page;
    overflow: hidden;
  }
  .slide:last-child { page-break-after: auto; break-after: auto; }
  .nav-hint { display: none; }

  /* Per-slide overrides for content-heavy slides — fixed pixel sizes appropriate
     for the 1280×720 viewport. See v1 deck for the full set. */
  .slide[data-slide="3"] .headline { font-size: 36px; max-width: 30ch; }
  /* ... etc per slide ... */
}
@page { size: 13.333in 7.5in; margin: 0; }
```

**Always render the PDF after editing** and rasterize a few pages (`pdftoppm -r 100 deck.pdf check -png`) to verify content doesn't overflow. The screen render is necessary but not sufficient evidence the deck is shippable.

## Slide skeleton (boilerplate)

Copy this scaffolding to start a new deck. Fill in headline, eyebrow, content body. The cover and counter scripts are turnkey.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{Partner}: {N}-Day Check-In</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&display=swap" rel="stylesheet">
  <link href="https://fonts.cdnfonts.com/css/cal-sans" rel="stylesheet">
  <style>
    :root { /* tokens — see Brand system above */ }
    * { box-sizing: border-box; }
    html, body { margin: 0; padding: 0; background: var(--bg); color: var(--text);
                 font-family: var(--font-body); font-size: 16px; overflow: hidden; }
    .deck { position: relative; width: 100vw; height: 100vh; }
    .slide { position: absolute; inset: 0; width: 100vw; height: 100vh;
             padding: var(--pad-y) var(--pad-x); display: none;
             flex-direction: column; background: var(--bg); }
    .slide.active { display: flex; }
    .brand { position: absolute; top: clamp(28px, 3.2vw, 48px); left: var(--pad-x);
             height: clamp(28px, 2.4vw, 36px); }
    .brand img { height: 100%; width: auto; display: block; }
    .counter { position: absolute; bottom: clamp(28px, 3.2vw, 48px); right: var(--pad-x);
               font-size: clamp(12px, 0.95vw, 14px); color: var(--text-muted);
               letter-spacing: 0.08em; text-transform: uppercase; }
    .counter .now { color: var(--accent); font-weight: 500; }
    .counter .sep { color: var(--rule-mid); margin: 0 6px; }
    .footer-meta { position: absolute; bottom: clamp(28px, 3.2vw, 48px); left: var(--pad-x);
                   font-size: clamp(11px, 0.85vw, 13px); color: var(--text-muted);
                   letter-spacing: 0.14em; text-transform: uppercase; }
    .eyebrow { font-size: clamp(12px, 0.95vw, 14px); font-weight: 500; letter-spacing: 0.18em;
               text-transform: uppercase; color: var(--text-muted);
               margin-bottom: clamp(20px, 1.6vw, 28px); }
    h1, h2 { font-family: var(--font-title); font-weight: 400; margin: 0;
             line-height: 1.04; letter-spacing: -0.015em; }
    .headline { font-size: clamp(44px, 5vw, 80px); max-width: 22ch; text-wrap: balance; }
    .headline .accent { color: var(--accent); }
    @media print { /* see Print rules above */ }
    @page { size: 13.333in 7.5in; margin: 0; }
  </style>
</head>
<body>
<div class="deck">

  <section class="slide active" data-slide="1">
    <!-- Cover: logo lockup + {N}-Day Check-In + period meta -->
    <div class="counter"><span class="now">01</span><span class="sep">/</span>NN</div>
  </section>

  <section class="slide" data-slide="2">
    <div class="brand"><img src="../../assets/newredlogowordmarkhighres.png" alt="Atom Grants"></div>
    <div class="content-wrap">
      <div class="eyebrow">All-time · since launch</div>
      <h2 class="headline">{headline}</h2>
      <!-- 4 big-stat tiles -->
    </div>
    <div class="footer-meta">{Partner} · Atom Grants</div>
    <div class="counter"><span class="now">02</span><span class="sep">/</span>NN</div>
  </section>

  <!-- … remaining slides per canonical sequence … -->

</div>
<script>
  const slides = Array.from(document.querySelectorAll('.slide'));
  let idx = 0;
  function go(n) { idx = Math.max(0, Math.min(slides.length - 1, n));
    slides.forEach((s, i) => s.classList.toggle('active', i === idx)); }
  const m = new URLSearchParams(location.search).get('slide');
  if (m) { const n = parseInt(m, 10); if (!isNaN(n)) go(n - 1); }
  document.addEventListener('keydown', e => {
    if (e.key === 'ArrowRight' || (e.key === ' ' && !e.shiftKey)) { e.preventDefault(); go(idx + 1); }
    else if (e.key === 'ArrowLeft' || (e.key === ' ' && e.shiftKey)) { e.preventDefault(); go(idx - 1); }
    else if (e.key === 'f' || e.key === 'F') { document.documentElement.requestFullscreen?.(); }
    else if (e.key === 'Escape') { document.exitFullscreen?.(); }
  });
  document.addEventListener('click', e => { if (!e.target.closest('a')) go(idx + 1); });
</script>
</body>
</html>
```

For component-specific markup (donut, stat tiles, sankey, weekly-trend chart, power-user cards, etc.), copy directly from `NYULH_180_Day_Checkin/v1/NYULH_180_Day_Checkin.html` — that file is the canonical reference.

## When the user iterates

Common feedback patterns and how to handle them:

- **"Too much accent."** Audit every red element in the deck. Default to black/gray. Earn each accent. See "Accent discipline" above.
- **"Make this fit on one line."** Add `white-space: nowrap`, reduce font slightly, remove `max-width` constraints. See slide-9 v1 channels-headline treatment.
- **"This can be on two lines."** A 3-line headline often happens when `max-width: 22ch` is too narrow for the copy. Override on that specific slide: `.slide[data-slide="N"] .headline { max-width: 34ch; }` (or similar — pick the width that produces an even 2-line break). See slide-6 v1 cohort headline.
- **"No new lines with just one word."** Add `text-wrap: balance` to the base `.headline` class (already in the boilerplate). If a single-word orphan survives `balance`, reword or widen `max-width` on that slide.
- **"This data doesn't match what I expect."** Re-check denominators. The roster-vs-active distinction is the most common trap. If the metric is dramatically off, the export itself may be wrong — ask for a re-pull. Investigate before adjusting copy.
- **"Be direct, not flowery."** Strip euphemisms ("save-for-later actions" → "favorites"). Lead with the noun, not the verb-phrase. Headlines should be observations, not slogans.
- **"This slide feels duplicative."** Don't run two slides of the same chart form back-to-back (two tables, two donuts) unless they answer truly different questions. Merge or cut. We removed a "Fastest-growing departments" slide for this reason.
- **"Change the cards to a table."** When the user asks for a table replacing cards/tiles, expect: more columns (broader activity profile), no per-item accent emphasis, headline reframed as an observation rather than a punchline.
- **"Add a graph for X."** Default to: horizontal bars (rankings), grouped vertical bars (P1 vs P2), donut (share / activation), sankey (cohort flow). Slope charts only work when value ranges are similar — otherwise the small lines crush together. Tried-and-rejected: dense slope chart of funder volume P1→P2 (small values crushed into unreadable cluster).

## Versioning convention

When the user says "scrap that, v1 is better" — delete the new folder entirely; do not leave broken iterations around. When the user says "try a v2 version" — copy the canonical version into `v1/` *first* if it isn't already there, then start `v2/` fresh. Never edit a `vN/` folder once a later version exists.

**When you delete or insert a slide mid-deck**, do all three of these in one pass — never leave the deck in a half-renumbered state:
1. Update every `data-slide="N"` attribute and every `.slide[data-slide="N"]` selector in both screen and print CSS.
2. Update the counter denominator (`<span class="sep">/</span>NN`) on every slide.
3. Update the displayed slide number (`<span class="now">NN</span>`) on every slide that shifted.

A short Python script with two ordered loops (one descending for inserts, one ascending for deletes) handles this safely. After the renumber, grep for orphan `.slide[data-slide="N"]` overrides that targeted the removed slide and delete them too.
