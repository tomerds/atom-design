---
name: quote
description: Build an Atom Grants formal quotation (single-page Letter-portrait PDF) for a prospect institution, working from the partnership-call transcript plus the agreed package and price. Traditional quote document — masthead, from/prepared-for, ruled line-item table, totals anchored on the annual license fee, license-includes and terms blocks. Trigger when the user asks to "make a quote", "formal quote", "quotation", "order quote", "put together a quote for [institution]", or pastes a transcript and asks for a quote. Reference implementation: references/MPFI_Quote.html.
---

# Atom Grants Formal Quote

A single-page formal quotation a prospect can take to their team. It follows the partnership proposal deck (see `proposal-deck`): the deck sells the options, the quote prices the chosen one. The separate contract / order form is sent later, so the quote has **no signature block**.

## Input

Primary input is the **partnership-call transcript** plus the **agreed package and price**. Read the transcript for the parties; get the commercial terms from the user.

**Extract from the transcript:** institution name and type, the billing/attention contacts and roles, and which package/tier they are moving forward with (if decided on the call).

## Ask before building

Use `AskUserQuestion` for the commercial details. Confirm:
- **Institution** name and the **Attn:** contacts.
- **Package** being quoted and the **annual license fee** $ (this is the headline number).
- **One-time implementation fee** $ (and what it covers, e.g. "Platform set up and Trainings").
- **License includes** — the short capability list (reference uses: 4 Training sessions, SSO, Discovery, Collaborators, Proposals, Admin Dashboard, Ongoing support).
- **Terms** — license term, start date, seats, payment terms, quote validity.
- **Quote number** and **dates** (issued, valid until). Offer sensible defaults (e.g. `AG-YYYY-MMDD`, issued today, valid 30 days) and proceed; flag them.

Do not invent the price. The reference numbers (`$15,000` annual + `$5,000` implementation) are an example, not a default.

## Output format

- **One self-contained HTML file**, single `<style>` block. **Letter portrait: `816 × 1056px`** (`.page`).
- Export to a **vector PDF via `html-to-pdf`** (selectable text, live email/site links) — not screenshot. A quote benefits from selectable text and clickable links.
- Must fit **one page**. The `.page` is a fixed-height flex column with `.page > * { flex-shrink: 0; }` so children never collapse; keep the natural content height **≤ 1056px** (measure before export — see "Fit"). The footer uses `margin-top: auto` to sit at the bottom.

## File layout

Build in its own top-level folder (sibling of `assets/`):

```
<Institution>_Quote/
├── MPFI_Quote.html      # rename to <Institution>_Quote.html
└── <Institution>_Quote.pdf
```

Copy `references/MPFI_Quote.html` and adapt. Logo: the masthead wordmark is **rebuilt from the icon + text**, not the combined image — `../assets/newlogo.png` (atom icon) + "Atom Grants" set in Cal Sans at the same size as the "Quote" title (the icon a touch larger so it extends just beyond the text height).

## Structure (top to bottom)

1. **Masthead** — left: the rebuilt wordmark lockup + contact lines (email, site). Right: "Quote" (Cal Sans, sized to the wordmark) + a small meta table (Quote No. / Date Issued / Valid Until).
2. **Accent rule** — a 3px `#ff4227` divider under the masthead.
3. **From / Prepared for** — two columns split by a vertical hairline with even spacing on each side. From = Atom + presenter; Prepared for = institution + Attn contacts.
4. **Line-item table** — ruled table, light-gray header row (`DESCRIPTION / TERM / AMOUNT`) with a 2px dark bottom divider; tabular figures. Rows: the annual license (12 months) and the one-time implementation & onboarding.
5. **Totals** — right-aligned, **anchored on the annual license fee** (the hero figure in the gray box). Below it, smaller secondary lines for the one-time implementation fee and the Year-1 total, then a renewal note (renews at $X/yr; implementation is Year-1 only; USD, excl. tax).
6. **License includes** + **Terms** — two columns. Includes = accent-bulleted capability list. Terms = dotted key/value rows (term, start, seats, payment, validity).
7. **Footer** — `margin-top: auto`, a top rule, contact line with live `mailto:`/site links. No "thank you" line, no signature block.

## Formal-quote style (not the soft-card UX style)

This deliverable is a **traditional business document**, the one place that intentionally departs from the soft-card one-pager house style:

- **Ruled tables and square corners**, tabular numbers (`font-variant-numeric: tabular-nums`).
- **Restraint on accent and dark fills.** One accent (`#ff4227`) on the masthead rule, section labels, and includes bullets. No heavy near-black fills — the table header is light gray with dark text; the total box is light gray with a dark top rule (not an accent or black block). No tinted left-rule callouts (banned in `CLAUDE.md`).
- **Cal Sans** for the "Quote" title, totals figure, and item titles; **DM Sans** for everything else. **No em dashes.**

### Line / text alignment (important)

The line-item table **bleeds ~16px wider than the text guides on each side** (the gray fill extends past the text); all *text* aligns to inner left/right guides. Then **every horizontal rule reaches the table's edges** while its text stays on the guide: full-width rules (accent rule, footer) span the whole table width; column-level rules (the From/Prepared-for underlines, section headers, terms dividers) extend to the table edge on their outer side. The totals box is sized so its left edge **aligns with the Terms column below it** — a clean right column, not bleeding further left than the divider/terms. When adapting, re-check these alignments by measuring element `x` edges.

## Fit

Before exporting, measure the natural content height and trim spacing until it is **≤ 1056px**:

```python
# headless Chromium: set .page to display:block / min-height:0, read getBoundingClientRect().height
```

If it overflows, compress section margins and row padding (the reference is already tuned tight). Then export:

```bash
python3 .claude/skills/html-to-pdf/export.py <Institution>_Quote/<Institution>_Quote.html
```

The exporter prints the links it wired up (the `mailto:` and site) — verify at a glance.
