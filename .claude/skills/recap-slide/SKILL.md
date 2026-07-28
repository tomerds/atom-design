---
name: recap-slide
description: Build an Atom Grants single-slide conversation recap for a prospect institution — the "Our conversation so far" slide that summarizes the initial sales calls (intro + demo) in three prospect-facing columns. Pulls the content from Granola meeting notes for the contact. Trigger when the user asks for a "summary slide of our conversations", "recap slide", "conversation summary slide", "our conversation so far slide", or to summarize initial calls with a prospect into a slide. Not a check-in deck (see checkin-deck — that's for signed partners with usage data) and not a proposal deck (see proposal-deck — that's the pricing call itself; this slide often opens it).
---

# Atom Grants Conversation Recap Slide

One 16:9 slide, shown back to a **prospect** (usually at the top of the pricing/proposal call, or sent after the demo): "here's what we heard from you, here's what mattered, here's what landed." It proves we listened before we talk price.

Canonical reference: `references/Ohio_University_Summary.html`. Copy it and change only the topbar meta, the `<h1>` accent (keep "Our conversation *so far*" unless the user wants different), and the column content. Shipped examples: `Ohio_University_Summary/`, `SMU_Conversation_Summary/`.

## Step 1 — Pull the source material from Granola

The input is usually a contact email or institution name. Query Granola (`query_granola_meetings`) for all meetings with that contact: dates, attendees, what was discussed, their reactions and concerns. Also check whether any *booked* later call (pricing, follow-up) actually has notes — its absence is worth flagging.

- **Never invent content.** Everything on the slide must come from the meeting notes. If Granola has nothing, ask the user for the calls' content instead.
- If Granola detail is thin, pull the full transcript (`get_meeting_transcript`) of the intro call — column 1 lives or dies on specifics (tool names, team size, org context).

## Step 2 — Sort the material into the three columns

| Column | What goes in it | Bullets |
|---|---|---|
| **Your office today** | Their current state, in their words: office structure and bandwidth, current tooling and its failure ("Spin Plus is in place today, but faculty barely use it"), underserved populations, org changes in motion (VPR plans, new functions). | 4–5 |
| **What matters most** | Their priorities and buying criteria — what they said they need, including concerns we must satisfy (data privacy, adoption, timeline). Lead each bullet with a bold label where natural ("**Faculty adoption:** …"). | 4–5 |
| **What stood out** | The Atom features and moments that got a reaction on the calls — only things actually shown/discussed, ideally with the detail that landed ("AI review in **~90 seconds**", "which your colleague X had already flagged"). | 4–5 |

**Audience register — this slide is read by the prospect:**

- Address them as "you / your" ("Your office today", "your colleague Shazia").
- **Internal notes stay off the slide.** Pipeline status, "no notes exist for the July 7 call", next-step nudges, deal commentary — report those to the user in chat, never on the slide.
- Plain copy, no em dashes, no marketing voice. Their vocabulary, not ours (if they say "OSP", write "OSP").

## Step 3 — Accent discipline

- One accent word/phrase in the `<h1>` via `<em>` (kept: "so far").
- The topbar date gets the accent `<span>`.
- `class="hot"` turns a bullet's dot accent red. **Max 2 hot bullets per column**, on the items that matter most to the deal. Column 1 usually has zero (it's their status quo, nothing to highlight).
- Bold (`<strong>`) the load-bearing phrase in most bullets — the tool name, the number, the feature. One bold phrase per bullet, not whole sentences.

## Format

- `.poster` at **1280 × 720** (13.333 × 7.5 in at 96dpi), one self-contained HTML file in its own folder: `<Institution>_Summary/` or `<Institution>_Conversation_Summary/`.
- Three equal `.col` cards: `border: 1px solid #eeeeee`, `border-radius: 18px`, soft shadow — the house soft-card look, no hard rules, no colored left bars.
- Topbar: logo left (`../assets/newredlogowordmarkhighres.png`, height 30px), right meta `INSTITUTION · RECAP · MONTH YEAR` with the date in accent.
- Cal Sans `font-weight: 400` on `<h1>` and `.col h2`; DM Sans everywhere else.
- Keep the fit-to-window `<script>` from the reference so the HTML presents cleanly in a browser.

**Fit-check before export:** all bullets must sit inside their cards with breathing room at 1280 × 720. If a column overflows, cut or merge bullets — never shrink the font below 15px or the layout stops matching the family.

## Render

```bash
# PNG (2× retina) — default capture targets .poster
python3 .claude/skills/html-screenshot/shoot.py <Folder>/<File>.html -o <Folder>/<File>@2x.png

# PDF (single slide, 13.333 × 7.5 in)
python3 .claude/skills/png-to-pdf/merge.py <Folder>/<File>@2x.png \
    -o <Folder>/<File>.pdf --size 13.333x7.5 --title "<Institution> — Conversation Summary"
```

Deliver both the PNG and the PDF.
