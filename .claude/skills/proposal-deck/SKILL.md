---
name: proposal-deck
description: Build an Atom Grants partnership proposal deck (the pricing / quotes call) for a prospect institution, working from the transcript of the partnership call(s). The 9-slide landscape deck reframes from cost to outcome and closes on next steps. Trigger when the user asks to "make a proposal deck", "pricing deck", "quotes-call deck", "partnership proposal deck", "put together a proposal for [institution]", or pastes a partnership-call transcript and asks for a proposal. Reference implementation: references/MPFI_Partnership_Proposal.html.
---

# Atom Grants Partnership Proposal Deck

The deck used on the **pricing / quotes call** (the call where you align on partnership terms and price), after the intro call and demo. It plays back what you heard, presents the licensing options, reframes the conversation from cost to outcome (ROI), recommends a tier, offers paths to a lower price, shows how onboarding works, and closes on the decision.

**This is not** the intro/first-call deck (use `intro-call-deck`) or a periodic review (use `checkin-deck`).

## Input

The primary input is the **transcript of the partnership call(s)**. Read it first and pull out everything below. Anything you cannot find in the transcript, ask the user for (see "Ask before building"). Do not invent institutional facts, pricing, or objectives.

**Extract from the transcript:**
- **Institution** name and type (R1, medical center, specialized institute, lab, etc.). Watch for telltale terminology (e.g. "research group leaders" → Max Planck).
- **Attendees and roles** (who is the economic buyer, who is the admin/end user).
- **Research metrics**, used on the "Sized to your institute" slide: number of PIs / faculty, annual funding ($), research expenditures, proposals submitted per year, any existing funding database / list they maintain by hand, current tools and manual workflows.
- **Pain points and interests** — which parts of Atom they leaned into (discovery, collaborator search, proposals project board, AI red-line review, etc.). The recommendation slide is built from these.
- **Budget signals** — any numbers floated, who controls budget, constraints.
- **Pricing discussed** — tiers and figures if mentioned.

## Ask before building

Use `AskUserQuestion` for anything not settled by the transcript. At minimum confirm:
- **Institution name** (confirm your inference) and **partner logo file** (for the cover lockup).
- **Pricing**: the two tiers and amounts (entry tier $ + name, full tier $ + name), and the **one-time implementation fee** $. The reference uses a `$5,000` Discovery tier and a `$15,000` Full Package + `$5,000` implementation fee — do not reuse those numbers blindly.
- **Which tier to anchor / recommend** (default: the full package, highlighted).
- **Presenter** name, title, email, and the **call date / month**.
- Whether to include the **"path to a better price"** slide and which levers (multiyear discount tiers, case-study commitment, etc.).

Recommend a sensible default in the question options and proceed; flag the assumptions you made in your summary.

## Output format

- **One self-contained HTML file**, single `<style>` block, no build step.
- Landscape deck: each slide is a `100vw × 100vh` `<section class="slide" data-slide="N">`, one shown at a time. Navigation: ArrowLeft/Right, Space, click to advance, `f` fullscreen, `#N` deep-link. Keep the nav `<script>` from the reference.
- **Always export to a 3:2 (12×8 in) PDF via screenshot-and-stitch** (never `html-to-pdf` — the print renderer mis-paginates these full-viewport slides). Use `render.py` (below).
- Authored at a 16:9 base but rendered at a 3:2 viewport, so slides sit a little top-weighted with whitespace toward the bottom — that is expected and consistent across the deck.

## File layout

Build each deck in its **own top-level folder** (sibling of `assets/`), so the reference's relative paths resolve:

```
<Institution>_Partnership_Proposal/
├── MPFI_Partnership_Proposal.html        # rename to <Institution>_Partnership_Proposal.html
├── <Institution>_Partnership_Proposal.pdf
└── img/<institution>-logo.png            # partner logo for the cover lockup
```

Start by copying `references/MPFI_Partnership_Proposal.html` into the new folder and adapting it. Asset paths in the reference: Atom logo `../assets/newredlogowordmarkhighres.png`, partner logo `img/<logo>.png`, customer-quote headshot `../Intro_Call_Deck/img/lydia.png` (reuse an existing grayscale headshot or swap for a more relevant one).

## The 9 slides

The eyebrow on each content slide is numbered (`01 / …` starts on slide 2; the cover is unnumbered). Keep the counter total in sync (`<span class="total">09</span>`).

1. **Cover** — "Partnership proposal." Co-brand lockup: Atom wordmark `×` partner logo. Eyebrow "For <Institution>". Presenter / date / "For <attendees>". *(Changes per prospect.)*
2. **What you'd be licensing** (`01`) — Atom in three parts: **Grant Discovery**, **Collaborator Search**, **Proposals**. Highlight (accent card) the part they cared about most on the call. *(Highlight changes; copy mostly fixed.)*
3. **Sized to your institute** (`02`) — four soft-card stats from the transcript (PIs, annual funding, proposals/yr, existing list), then one calm takeaway line tying their terminology/focus to the pricing. Keep accent to a single number. *(Fully prospect-specific.)*
4. **Two licensing options** (`03`) — the centerpiece comparison table. Two priced columns (entry vs full), the full column highlighted with a "Recommended" badge, grouped feature rows (Grant Discovery / Collaborator Search / Proposals) with check / dash per column. Footer: annual license + unlimited seats, plus the one-time implementation-fee line. *(Prices, tier names, and the highlighted tier change.)*
5. **Projected ROI** (`04`) — the cost→outcome reframe. Headline "Look at the outcome, not the cost." Three stat cards: the license as a fraction of their annual funding (e.g. `0.15%`, neutral), and two return multipliers (e.g. `~7×` on a 1% funding lift, `16×+` on one added award) in accent. **Always label it illustrative** and base the math on their figures; do not over-claim. *(Numbers derived from their funding.)*
6. **Our recommendation** (`05`) — why the full package, in 3 reasons tied to *their* workflow and pain points (from the transcript), plus a relevant customer quote card. *(Reasons are prospect-specific.)*
7. **A path to a better price** (`06`) — two concrete levers to lower the price: e.g. **multiyear commitment** (3-year / 5-year discount tiers) and a **case-study commitment** (on a successful 180-day check-in). Two neutral option cards. *(Optional; levers per deal.)*
8. **Getting started** (`07`) — onboarding timeline. A horizontal 3-phase stepper (subtle white circles on a full-width line): **Setup** (Weeks 1-2: kickoff, org structure, SSO, faculty list), **Launch** (Weeks 3-6: admin + faculty training, invites), **Partnership** (Ongoing · Year One: 30/90/180-day check-ins, end-of-year ROI review). *(Mostly fixed; timeframes adjustable.)*
9. **Next steps** (`08`) — numbered steps (decide on scope with the team in the room → we send the formal quote → countersign and onboard), an "options at a glance" card recapping the two prices + key terms, and the presenter's contact. *(Prices/contact change.)*

**Slides that change per prospect:** cover (1), sized-to-institute (3), pricing (4), ROI numbers (5), recommendation (6), the price-lever options (7), and the close (9). Slides 2 and 8 are largely fixed copy.

## Brand & copy rules

Follow the house brand system (see root `CLAUDE.md`): single accent `#ff4227` as a solid fill, white bg, black text; **Cal Sans** titles (`font-weight: 400`), **DM Sans** body. Headshots grayscale, square-rounded.

- **Plain language, no marketing voice.** Simplest word that works. **No em dashes** — use commas, colons, semicolons.
- **Accent discipline.** One accent load per slide. On the stats and ROI slides, keep accent to a single number; the rest stays black. Do not wrap copy in tinted callout/admonition panels (banned in `CLAUDE.md`) — emphasize with an accent eyebrow, a single accent word, a soft-card, or the highlighted comparison column.
- **Honesty on ROI.** Mark projections illustrative and anchor them to the prospect's own numbers. State the denominator if asked (annual license vs full Year-1 outlay).
- **Reflect, don't invent.** The "sized to your institute" and "recommendation" slides must come from the transcript. Ask if unsure.

## Render

```bash
# Build/adapt <Institution>_Partnership_Proposal/<...>.html, then:
python3 .claude/skills/proposal-deck/render.py <Institution>_Partnership_Proposal/<Institution>_Partnership_Proposal.html
```

`render.py` captures each `.slide` at a 1620×1080 (3:2) viewport at 2× and stitches a `12×8` in PDF next to the HTML. To preview a single slide while iterating, screenshot `.slide.active` after setting `location.hash = '#N'` at the same 1620×1080 viewport.
