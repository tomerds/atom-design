---
name: webinar-deck
description: Build the Atom Grants live webinar deck — the 6-slide shell shown on screen while hosting a webinar (cover, agenda, speakers, talk handover, Q&A, thank you + QR to the next sessions). Trigger when the user asks to "make a webinar deck", "deck for the webinar", "slides for [webinar title]", "webinar template", or wants the presenting deck for a session that already has an OG tile. Not the OG share tile (see og-tile) and not the launch deck (that is a one-off content deck).
---

# Webinar Deck

The presenting shell for any Atom Grants webinar. It is deliberately **thin**: six slides that top-and-tail the session. The substance belongs to the speakers, who present their own material between slides 04 and 05.

Derived from the Atom 3.0 launch deck (`Atom_3_Launch_Webinar_Deck/`), which is a one-off *content* deck and not the template.

## Where it lives

- **Template (source of truth):** `Webinar_Deck/Webinar_Deck.html`
- **QR:** `Webinar_Deck/webinars_qr.png` (points at `https://atomgrants.com/webinars/` — stable, reuse it)

One self-contained HTML file. 13.333 × 7.5 in landscape. Presented in-browser (arrow keys / Space / click to advance, `f` fullscreen, `#N` deep-link) or exported to PDF.

## The 6 slides

| # | Slide | What it carries |
|---|---|---|
| 01 | **Cover** | logo + "Webinar · Live" tag, accent eyebrow, title, subtitle, all speakers, then When / Format / Questions |
| 02 | **Agenda** | "The next 60 minutes" + a numbered list, one line per item, with who and how long |
| 03 | **Speakers** | "Who you are hearing from" + the speakers in a row |
| 04 | **Handover** | the talk title, full size. Left up while you hand over to the speakers |
| 05 | **Q&A** | "Ask the panel anything." + one line on where to put questions |
| 06 | **Thank you** | "See you at the next one." + `atomgrants.com/webinars` + QR card + footer row |

Slides 04 and 05 are separated by however long the speakers present. Nothing else goes in this deck: if the host has content, it is a different deck.

## Building one for a webinar

The webinar almost always has an **OG tile already built** (`og-tile` skill, `Webinar_Tiles/Webinar_Tiles.html`). **Pull the title, subtitle, date, and the full speaker list straight from that tile** rather than rewriting them — the deck and the tile must say the same thing. The tile's `_gray.jpg` headshots are the deck's headshots.

Swap these and nothing else:

| Token | Where | Notes |
|---|---|---|
| title | 01 cover headline, 04 handover, page `<title>` | one word in `<span class="accent">`, same word in both places |
| subtitle | 01, 04 | the tile's subtitle verbatim on 01; 04 can expand it slightly |
| when | 01 meta | `Wednesday 26 August · 11am ET`. **Confirm the start time**, do not assume 12pm ET |
| speakers | 01 `.presenter` rows, 03 `.sp` blocks | headshots at `../Webinar_Tiles/<lastname>_gray.jpg` |
| agenda | 02 `.agenda-list` | see below |

### Speaker blocks — order is fixed

Both slide 01 and slide 03 run **name → organization → role**, in that order:

```
Dr. Lulu Jiang                                  ← Cal Sans (03) / DM Sans 600 (01), black
Morgan State University                         ← DM Sans 600, black
Program Administrator, NTC & SMARTER Center     ← DM Sans 400, gray
```

Organization before role, always. The org is reliably one line and the role is not, so putting the org second keeps lines one and two on a shared baseline across every column and lets only the role rag at the bottom. Role last also stops a long title from shoving the org out of alignment. Do not "fix" the rag with a `min-height` — that was tried and it just pads out the short roles.

Slide 03 is **uncarded**: no border, no shadow, no padding box. Portraits are ~124px squares at `border-radius: 18px` with a hairline ring, grayscale, `object-position: center 18%`. Nothing sits below the row — no summary line.

Slide 01 presenter rows are top-aligned (`align-items: flex-start`), so a speaker whose title wraps to two lines does not push their name off the shared line.

### Agenda — one line for the talk

The talk gets **exactly one agenda line, carrying its real title**, matching slide 04. Do not break the talk into per-speaker segments:

```
01  Welcome and introductions                          Tomer · 5 min
02  Building a Smart Research Administration Ecosystem  The panel · 40 min
03  Q&A                                                All · 15 min
```

**Ask for the run of show.** Timings and the host name are the two things most often invented here. If the user has not given them, put a placeholder in and say so explicitly.

## Copy and accent rules

- One accent word in the title, the same word on 01 and 04. On 06 the accent lands on the closing phrase and the URL.
- Slide 05 is the headline plus one line. It previously carried three "nothing is too basic" style notes; they were cut and should stay cut.
- The QR card is **white with a hairline border and no shadow**. It reads as a card against the white page from the border alone.
- **Nothing in this deck carries a shadow.** It exports to PDF, so no `box-shadow` with blur or offset, no `filter: drop-shadow`, no glow anywhere (see "Banned: shadows on documents" in `CLAUDE.md`). The only `box-shadow` in the file is the zero-blur `0 0 0 1px rgba(0,0,0,0.08)` hairline ring on the speaker portraits, which is a border.
- Plain copy, no em dashes, no colored left-rule bars, Cal Sans at weight 400 only.

## Render

Print CSS paginates correctly, so this deck exports **vector** (selectable text, live links):

```bash
python3 .claude/skills/html-to-pdf/export.py Webinar_Deck/Webinar_Deck.html
```

To eyeball a single slide while iterating, rasterize the PDF rather than screenshotting the HTML — slides are `position: absolute` and hidden unless `.active`, so `html-screenshot` only ever sees slide 01:

```bash
pdftoppm -png -r 100 -f 3 -l 3 Webinar_Deck/Webinar_Deck.pdf /tmp/chk
```

## Related

- `og-tile` — the 1200 × 630 share tile + 1280 × 720 YouTube twin for the same webinar. Build that first; this deck inherits its copy.
- The `.byline` speaker strips (see `CLAUDE.md`) reuse the same `_gray.jpg` headshots.
