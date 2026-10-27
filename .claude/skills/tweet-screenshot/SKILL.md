---
name: tweet-screenshot
description: Frame a tweet / X post screenshot for Atom Grants use (blog posts, newsletters, LinkedIn). Full black canvas with the tweet centered inside a thick translucent glass ring. No offset box, no crop marks. Trigger when the user asks to "wrap this tweet", "frame a tweet", "tweet screenshot", "put this X post in our border", or hands over a screenshot of a tweet to dress up. Not the blog-screenshot blueprint frame (that is for Atom product UI).
---

# Tweet Screenshot Framer

Turns a raw screenshot of a tweet (X post) into a clean framed image. Every output
reads the same: a **full black canvas** with the tweet centered inside the house
**thick glass ring**, and nothing else.

## What it produces

- **Canvas:** solid `#000000`, sized around the shot with an even 120px margin on
  every side (output dimensions vary per tweet, which is fine).
- **Glass ring:** 12px translucent white ring (`rgba(255,255,255,0.22 → 0.10)`
  gradient), 1px `rgba(255,255,255,0.28)` edge, 24px outer radius. Same geometry as
  the blog-screenshot glass, re-tinted for a dark canvas.
- **Tweet:** 12px rounded corners, flat, longest side fit to 1040px (never
  upscaled). The capture margin is trimmed, then **re-padded evenly (40px) in the
  tweet's own background color**, so the text never runs into the ring and uneven
  captures come out balanced.
- **No** offset frame rectangle, **no** `+` crop marks, no logo, no URL, no accent.

Canonical output: `references/Example_Alpoge_Tweet@2x.png`.

## Usage

```bash
python3 .claude/skills/tweet-screenshot/build.py <source_image> <slug>
```

Writes `Tweet_Screenshots/<slug>-raw.png`, `<slug>.html`, and `<slug>@2x.png`.
Flags: `--out-dir DIR`, `--no-render`. Naming: `<handle>-tweet`, e.g. `alpoge-tweet`.

**Always Read the rendered PNG back** before handing it over.

## Getting the screenshot onto disk

- **Pasted into the chat:** the message usually carries the source path (a
  `/var/folders/.../pasted-image-*.png`); pass it directly. Otherwise check the newest
  file in the session image-cache.
- **A macOS screenshot just taken:** `ls -t ~/Desktop/Screenshot*.png | head -1`
  (filenames contain a U+202F narrow space, so glob).

## Notes

- Built for dark-mode tweets (black on black blends seamlessly into the canvas). A
  light-mode tweet still works: it shows as a white card in the ring on black.
- Crop browser chrome, reply threads, or engagement rows out of the source first if
  they aren't wanted; trim only removes a solid one-color margin.
- Tuning lives in `build.py` (`TARGET_LONG`, `PAD`, `INNER_PAD`) and the template's
  `.glass` rule. If you change the ring thickness, update `GLASS` to match.
- Re-render after hand-editing the HTML:
  `python3 .claude/skills/html-screenshot/shoot.py Tweet_Screenshots/<slug>.html --selector ".canvas" -o Tweet_Screenshots/<slug>@2x.png`
- Raster deliverable; PNG is the final form.
