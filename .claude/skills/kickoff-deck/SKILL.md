---
name: kickoff-deck
description: Create and personalize the Atom Grants onboarding kickoff-call deck for a newly signed partner institution. This is the first call AFTER signing (day 1 of onboarding), not a sales call. Trigger when the user asks to "make a kickoff deck", "kickoff call deck", "onboarding deck for [institution]", "welcome deck", "spin up a kickoff for [University]", or to render that deck to PDF. The finalized 10-slide template lives at Kickoff_Deck/Kickoff_Deck.html.
---

# Kickoff Call Deck

The finalized template for Atom Grants' **onboarding kickoff call**: the first call with a new partner once they have **signed**. Welcome them, recap why they chose Atom, walk the platform and onboarding timeline, align on success metrics, set next steps.

## Where it sits in the lifecycle

`intro-call-deck` (first call) → demo → `proposal-deck` (pricing) → `quote` → **signed** → **`kickoff-deck` (you are here)** → `checkin-deck` (30/60/90/180-day) → `upsell-deck` (renewal)

This deck is where the partner's **onboarding objectives get set**. `checkin-deck` later requires those objectives and forbids inventing them, so whatever lands on slide 03 and the success-metrics discussion here is the source of truth for every subsequent check-in.

## Where it lives

- **Template (source of truth):** `Kickoff_Deck/Kickoff_Deck.html` (tracked in git)
- **Personalizer:** `.claude/skills/kickoff-deck/personalize.py`
- **Shipped examples (local, git-ignored):** `Georgia_Southern_Kickoff/`, `VCU_Kickoff/`

Single self-contained HTML file, 13.333 × 7.5 in landscape. Navigate with arrow keys / Space / click; `f` fullscreen; `#N` deep-links to slide N.

## The 10 slides

| # | Slide | Changes per partner? |
|---|---|---|
| 01 | **Cover** — "Welcome to Atom." + co-brand lockup (Atom **×** partner) + presenter / date / institution | **yes** (5 tokens + logo) |
| 02 | Agenda — the four sections of the call | no |
| 03 | **Why Atom?** — the 3 reasons *this* partner chose Atom | **yes** (the only content slide) |
| 04 | Platform walkthrough (section divider) | no |
| 05 | Onboarding timeline — Day 1 → Week 1 → Week 2-4 → Day 30 | no |
| 06 | Success metrics (divider, "How do you define success?") | no |
| 07 | Success timeline — 30 / 90 / 180 / 365-day milestones | no |
| 08 | Q&A (divider) | no |
| 09 | Next steps — SSO + admin access / schedule training / send invites | no |
| 10 | Thank you | no |

Slides 04, 06 and 08 are dividers that cue the live conversation; slide 06 in particular is a prompt to **ask** the partner how they define success, not to tell them.

## Slide 03 is the whole job

Everything else is fixed template. The three reason cards are the deck, and they must be **the partner's own stated reasons**, pulled from the kickoff/partnership call transcript. **Never invent them.** A kickoff deck that reflects back what the partner actually said is the entire point; a generic one is worse than none.

Sources, in order of preference:
1. **Granola** — query the partner's calls (`query_granola_meetings`, e.g. *"[Institution] — why did they choose Atom, pain points, current tools"*). Ask the user before assuming Granola has the calls; not every call is captured.
2. The user pastes the pain points / transcript directly.
3. The `proposal-deck` or `quote` built for the same partner (their "sized to your institute" and recommendation slides came from the same transcript).

Writing the cards:
- **Title:** 3 to 6 words, Cal Sans, sentence case, no trailing period.
- **Body:** one or two sentences, 35 to 45 words, in the partner's own framing. Address them as "you."
- Keep the three bodies within a line of each other so the cards balance. Six lines is the practical ceiling at the default clamp sizes; if one card runs long, cut a clause rather than shrinking type.
- Name their specifics: the incumbent tool they are leaving, the system they want it wired into, the ranking they are chasing. Specificity is the proof you listened.
- No em dashes (`personalize.py` rejects them). No marketing voice.

Shipped examples:

| Partner | Reason titles |
|---|---|
| Georgia Southern | A real upgrade from Grant Forward · Automated faculty matching, at speed · Built into your InfoReady workflow |
| VCU Health | Building out research development · Do more, without more FTEs · Opportunities that reach the right faculty |

## Personalizing

Cover tokens: `[Partner logo]`, `[Your name]`, `[Title]`, `[Month YYYY]`, `[Institution name]`.

Write the three reasons to a JSON file, then run the personalizer. It copies the template into `<Slug>_Kickoff/`, inlines the logo, swaps the tokens, fills slide 03, and exports the PDF:

```bash
cat > /tmp/reasons.json <<'JSON'
[
  {"title": "Building out research development",
   "body":  "You are standing up an RD function and recruiting a Director of Research Development. Atom covers the whole path from search to proposal development, backing proposal quality, young investigators, and collaboration across clinical and basic science."},
  {"title": "Do more, without more FTEs",
   "body":  "A fast-growing research enterprise should not need headcount to grow with it. Atom automates the manual work an RD team would otherwise absorb, so you can do more with less and plan resources against real capacity."},
  {"title": "Opportunities that reach the right faculty",
   "body":  "Library services and self-driven PI searches bury faculty in opportunities they never read. Personalized profiles and curated recommendations land in individual inboxes instead, lifting engagement and the conversion from opportunity to submission."}
]
JSON

python3 .claude/skills/kickoff-deck/personalize.py \
    --institution "VCU Health" \
    --logo ~/Downloads/vcu-health.png \
    --date "July 2026" \
    --reasons /tmp/reasons.json
```

Output: `VCU_Kickoff/VCU_Kickoff.html` + `.pdf`, with the logo at `VCU_Kickoff/img/`.

Flags: `--institution` and `--logo` are **required**; `--name` (default `Tomer du Sautoy`), `--title` (default `CEO and Co-Founder`), `--date` (default current month), `--reasons`, `--out`, `--no-pdf`.

Guardrails the script enforces:
- `--reasons` must hold **exactly 3** `{title, body}` objects, all non-empty.
- Em/en dashes in reason copy are a hard error.
- Omitting `--reasons` leaves the `[Reason N ...]` placeholders in and prints a warning. It will not make anything up.

**Keep each partner's deck in its own top-level `<Slug>_Kickoff/` folder** (a sibling of `assets/`), so the template's `../assets/...` logo paths resolve. `.gitignore` tracks only `Kickoff_Deck/Kickoff_Deck.html`; per-partner decks and partner logos stay local and are never committed.

## Partner logo

The cover lockup is the Atom wordmark, a thin gray `×`, then the partner's logo. Prefer a **full-color** logo on a transparent or white background. `personalize.py` picks the CSS height from the logo's aspect ratio, since a wide wordmark and a tall crest need different heights to carry the same visual weight next to the Atom wordmark:

| Logo shape | Example | CSS applied |
|---|---|---|
| Wide wordmark (ratio > 2.5) | VCU Health, 3.17:1 | `height: clamp(52px, 4.6vw, 68px); max-width: 300px` |
| Crest / squarish (ratio ≤ 2.5) | Georgia Southern, 1.65:1 | `height: clamp(64px, 5.6vw, 88px); max-width: 260px` |

SVG logos skip the aspect check (Pillow cannot read them) and fall through to the crest sizing. Eyeball the cover and adjust `.partner-logo-img` by hand if it looks off.

> Check which entity actually signed. VCU Health and Virginia Commonwealth University are different logos.

## Rendering the PDF — `html-to-pdf` works here

Unlike `intro-call-deck` (whose full-viewport slides mis-paginate and must be screenshot-and-stitched), this deck's print CSS paginates correctly. Verified: 10 pages at exactly 13.333 × 7.5 in, vector, selectable text.

```bash
python3 .claude/skills/html-to-pdf/export.py VCU_Kickoff/VCU_Kickoff.html --size 13.333x7.5
```

`personalize.py` runs this for you unless you pass `--no-pdf`.

To screenshot a single slide for review, load it via its hash deep-link so the deck's own `show()` runs (toggling `.active` directly leaves the page counter stuck at 1/N):

```python
page.goto(f"file://{html}#3"); page.wait_for_timeout(2500)
page.query_selector('[data-slide="3"]').screenshot(path="s3.png")
```

## When editing the template itself

- Edit `Kickoff_Deck/Kickoff_Deck.html`, then regenerate partner copies from it. Do not hand-edit per-partner decks.
- Keep the five cover tokens and the six `[Reason N ...]` placeholders intact, and keep the `.partner-logo-img` rule on one line — `personalize.py` matches all of them textually.
- Brand: single accent `#ff4227`, white bg, black text; Cal Sans titles, DM Sans body. Load Cal Sans from **Google Fonts** (`family=Cal+Sans`), not the retired cdnfonts CDN. **Flat — no shadows:** this deck exports to PDF, so no `box-shadow` with blur or offset, no `filter: drop-shadow`, no glow; cards read from their border, radius, and fill (see "Banned: shadows on documents" in `CLAUDE.md`). Zero-blur rings (`0 0 0 1px`) used as hairline borders are fine.
- Cal Sans ships one weight. Always set `font-weight: 400` on heading elements, since browsers synthetic-bold `<h1>`/`<h2>`/`<h3>` into an off-brand smear.
- **Never** put a colored left rule (`border-left: 3px solid var(--accent)`) on a panel or text block. Emphasize with an accent eyebrow, a single accent word, or a chip.
- No em dashes anywhere in copy. Plain language over marketing voice.
