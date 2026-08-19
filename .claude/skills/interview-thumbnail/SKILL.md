---
name: interview-thumbnail
description: Build an Atom Grants two-up interview / collaboration thumbnail for a LinkedIn post (or video/recording) that features a host and a guest, or two collaborators. Two color photos side by side, a name label on each, an accent "×" seam badge, and the content title with one accent word. Trigger when the user asks for an "interview thumbnail", "guest thumbnail", "collab post", "podcast thumbnail", "LinkedIn post with a guest/collaborator", or a thumbnail promoting an interview/conversation between two people. Not the same as an OG tile (see og-tile) — this is the two-face promo layout with color photos.
---

# Atom Grants Interview Thumbnail

A two-up promo image for a piece of content featuring **two people** — a host + guest interview, a customer conversation, or two collaborators. Two photos side by side (host/left, guest/right), a name label on each, an accent `×` "in conversation" badge at the seam, and the content title in a bottom band. Built as one self-contained HTML file, rendered to PNG.

**This is a distinct deliverable from [og-tile].** The OG tile is a single-title card with an optional grayscale collab strip. This is the two-face layout, and — unlike every other Atom people-photo — **the photos stay in full color** (see "Color exception" below).

## Inputs (ask for what's missing — don't invent)

1. **Two photos** — one per person. See "Getting the photos onto disk" — this is the step that trips up every run.
2. **Two names + roles** — host is usually `Raphaël Bernier · Atom Grants` unless told otherwise; guest name, role, and organization come from the content piece (confirm, don't guess).
3. **The title** — the headline of the content piece being promoted. If the piece is a published blog/webinar, pull the real title from `atomgrants.com` (see og-tile's blog/webinar fetch workflow). Otherwise ask.
4. **Eyebrow label** — defaults to `INTERVIEW`. Swap to `IN CONVERSATION`, `PODCAST`, `WEBINAR`, or `Q&A` if it fits the piece better. **No date** by default (we removed it — it dates the post).

## Format

Default **1200 × 1200 square** — the Atom house format for a LinkedIn *feed* post (fills the most feed real estate). Render at 2× → 2400 × 2400.

Two other sizes on request (same layout, only frame + scale change):

| Use | Size (@1×) | Notes |
|---|---|---|
| **LinkedIn feed post** (default) | 1200 × 1200 | Square. What you build unless told otherwise. |
| **Link preview / OG** | 1200 × 630 | If the post shares a *link* (LinkedIn renders link previews in landscape, not square). Shorten the band, photos row ~430px. |
| **YouTube / recording thumb** | 1280 × 720 | 16:9 for the recording. Photos row ~500px. |

## Brand system (shared with the rest of the repo)

| Token | Value |
|---|---|
| Accent | `#ff4227` (only brand color) |
| Band background | `#F9FAFB` (cool light gray — the bottom title band; page bg stays white) |
| Text | `#000000`, secondary `#666` |
| Title font | Cal Sans (`https://fonts.cdnfonts.com/css/cal-sans`) — always `font-weight: 400` on `.title` (browsers bold `<h1>` by default and synth-bold Cal Sans) |
| Body font | DM Sans 400/500/600/700 (Google Fonts) |
| Logo | `../../assets/newredlogowordmarkhighres.png` from a deliverable folder (`../assets/...`) — height 42–44px in the band |

### Color exception (important)

The repo rule is that **all people photos are grayscale** (headshots, speaker portraits, og-tile collab strips). **The interview thumbnail is the one deliverable that keeps photos in full color** — the two large faces are the hero and read better in color, and the guest's clothing/tones often play off the accent. Do not grayscale them unless the user asks. Everything else (accent discipline, Cal Sans/DM Sans, single accent color) still applies.

## Layout

```
┌───────────────────────────────────────────────┐
│                        │                       │  ← photo row (color, full-bleed)
│      HOST photo        │      GUEST photo       │
│        (left)      ┌───┴───┐    (right)         │  ← accent "×" badge at the seam
│                    │   ×   │                     │
│                    └───┬───┘                     │
│  Host Name             │   Guest Name           │  ← name label + role over dark scrim
│  Role/Org              │   Role, Organization   │
├────────────────────────┴───────────────────────┤
│  ● INTERVIEW                      [Atom logo]   │  ← bottom band on #F9FAFB
│  Content Title Line One                         │  ← Cal Sans 62px, last phrase accent
│  Line Two With AI                               │
└───────────────────────────────────────────────┘
```

Key rules (square 1200×1200 values):

- **Photo row** `height: 740px`, two `.photo` halves at `50%` width each, `background-size: cover`. Because the slot is portrait and the source frames are 16:9, `cover` fills the height exactly and center-crops the sides — so **horizontal centering is what matters**; `background-position` Y only bites once you zoom past cover.
- **Color, no grayscale filter** (the exception above).
- **Name label** bottom-left of each photo, white text over a `linear-gradient(to top, rgba(0,0,0,.74), transparent)` scrim (~190px tall) so names stay legible over any frame. Name = Cal Sans 32px; role = DM Sans 500 16px at 85% white.
- **Seam badge**: `#ff4227` circle (84px) centered on the seam at the photo-row's vertical middle, with a `box-shadow: 0 0 0 7px #F9FAFB` ring so it punches off the photos. Contains a white Cal Sans `×` (`&times;`). This is the "in conversation" cue and the tile's signature.
- **Bottom band** `flex: 1` on `#F9FAFB`, `padding: 0 64px`. Top sub-row = `● INTERVIEW` eyebrow (accent dot + accent label, DM Sans 700, `0.2em` tracking) on the left, Atom wordmark on the right. Below it the **title**: Cal Sans 62px, `line-height: 1.03`, with the **last word or short phrase wrapped in `<span class="accent">`** (e.g. "…Understandable **With AI**"). Use `<br>` to control line breaks; drop to 54–56px if the title runs 3 lines.

### Crop tuning

After the first render, look at both faces:
- Too much headroom or a clipped chin → zoom in by setting `background-size` larger than cover (e.g. `background-size: auto 130%`) and then nudge `background-position` Y.
- Face off to one side → adjust `background-position` X (e.g. `center` → `40% 26%`).
Match the two crops so both heads sit at roughly the same scale and height (the guest frame often has more headroom than a tight host frame).

## Getting the photos onto disk (the step that always snags)

Images **pasted into chat are visible to Claude but are NOT written to the filesystem**, and the renderer can only use real files. So a paste is not enough. Get each photo onto disk one of these ways, in order:

1. **Newest Desktop screenshot** — ask the user to screenshot the frame (`⌘⇧4`), which saves to `~/Desktop`. Then grab the most recent one. **Gotcha:** macOS screenshot filenames contain a narrow no-break space (U+202F) before `AM`/`PM`, so a literal `cp` of the printed name fails — **always copy via a glob**:
   ```bash
   cp ~/Desktop/Screenshot\ 2026-07-01*10.27.33*.png <deliverable>/guest.png
   ```
   Find the newest with:
   ```bash
   ls -dt ~/Desktop/Screenshot*.png | head -3 | while read f; do echo "$(stat -f '%Sm' -t '%H:%M:%S' "$f")  $f"; done
   ```
2. **Clipboard** — if they copied the image, pull it with AppleScript:
   ```bash
   osascript -e 'set d to the clipboard as «class PNGf»' \
             -e 'set f to open for access POSIX file "/abs/path/guest.png" with write permission' \
             -e 'set eof f to 0' -e 'write d to f' -e 'close access f'
   ```
   (Errors with "Can't make some data into the expected type" when there's no image on the clipboard — that just means fall back to a screenshot.)
3. **A real file** the user drops at `<deliverable>/host.png` / `guest.png`, or a path they give you.
4. **For a published piece**, the guest headshot may already be hosted — see og-tile's `api.atomgrants.com/storage/...` shortcut and institution-bio sourcing. But for interview thumbnails the photos are usually **video-call stills** the user captures, so screenshots are the norm.

Name the files `host.png` (left) and `guest.png` (right) inside the deliverable folder so the template's `url()`s resolve.

## Workflow

1. Make the deliverable folder: `<Piece_Name>_Thumbnail/`.
2. Copy the template `references/Interview_Thumbnail_Template.html` in as `<Piece_Name>_Thumbnail.html`.
3. Get both photos onto disk as `host.png` / `guest.png` (section above).
4. Fill the tokens: names + roles, eyebrow, and the title (split the last phrase into `<span class="accent">`).
5. Render at 2× and **look at it** (Read the PNG) to check the crops:
   ```bash
   python3 .claude/skills/html-screenshot/shoot.py \
     <Piece_Name>_Thumbnail/<Piece_Name>_Thumbnail.html \
     --selector "#tile-01" \
     -o <Piece_Name>_Thumbnail/<Piece_Name>_Thumbnail@2x.png
   ```
6. Tune crops (`background-position` / `background-size`) and re-render until both faces sit well. Then `open` it for the user.

## File layout

```
<Piece_Name>_Thumbnail/
├── <Piece_Name>_Thumbnail.html   ← one self-contained file
├── host.png                       ← left photo (usually Raphaël)
├── guest.png                      ← right photo (the guest/collaborator)
└── <Piece_Name>_Thumbnail@2x.png  ← rendered export (2400×2400)
```

Reference implementation / template: `references/Interview_Thumbnail_Template.html`. Real example shipped: the Kim Weeks interview ("Making Clinical Research Understandable With AI").

## Don't

- Don't grayscale the two photos — this is the color exception. (Everywhere else in the repo, people photos are B&W.)
- Don't add a date to the eyebrow by default (it dates the post). Add one only if asked.
- Don't add gradients on type, secondary colors, or off-brand fonts. One accent (`#ff4227`): the eyebrow dot/label, the `×` badge, and one word/phrase in the title. That's the whole color load.
- Don't rely on a chat-pasted image being on disk — it isn't. Always get a real file first.
- Don't let the title synth-bold: keep `font-weight: 400` on `.title`.
- Don't forget to visually check the render — face crops are the thing that goes wrong, and only a look catches it.
