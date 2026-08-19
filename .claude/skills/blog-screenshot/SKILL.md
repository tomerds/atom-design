---
name: blog-screenshot
description: Wrap a raw product screengrab from the Atom Grants app in the house "technical blueprint frame" for use as an in-article blog image. The frame is an offset light-gray rectangle peeking out top-left and right, two crop-mark crosshairs on its exposed corners, and the screenshot on top (rounded corners, flat, auto-trimmed to the UI edges). Trigger when the user asks to "frame a screenshot", "make a blog image", "blog screenshot", "wrap this screengrab", "put this UI shot in the frame", or hands over a product screenshot to dress up for the blog. Not an OG/social tile (see og-tile) — this is the in-article framed product shot.
---

# Blog Screenshot Framer

Turns a plain product screengrab into a polished in-article blog image by dropping
it into a fixed "technical blueprint frame." Every output reads as one consistent
family so screenshots across the atomgrants.com blog look designed, not pasted.

## What it produces

A white canvas (rendered at 2× → PNG) containing:

- The screenshot **on top** — rounded corners (12px), flat (no drop shadow), sitting
  inside a **thick glass border**: a 12px frosted ring (translucent gray-white
  gradient fill, 1px hairline outer edge, 1px white inner highlight, 24px outer
  radius) that reads like a tablet-style bezel while staying flat and neutral. The
  shot's uniform outer margin is **auto-trimmed** so it crops to the UI edges, its
  longest side is fit to ~1040px (never upscaled past native), and the **canvas is
  sized around it** with fixed padding, so wide, square, or tall grabs all stay
  proportional and read as one family.
- An **auto edge border** only when the edge is genuinely absent: a single-surface UI
  that bleeds to a white edge (no border of its own) would blend into the white canvas
  and look sliced, so a 1px border derived from the UI's own tone closes it into a
  clean card. A UI that already has a border — even a faint one — is left alone, and
  multi-panel shots (kanban columns, side-by-side cards) are detected by their
  full-height background gutters and left borderless (a bounding border there would
  draw a stray line across the gaps).
- An **offset frame**: a 1px light-gray rectangle sitting *behind* the shot, shifted
  up-and-left so it peeks out past the screenshot's top-left and right edges while the
  screenshot spills below its bottom edge. This diagonal overlap is the signature move.
- Two **crop-mark crosshairs** (`+`) on the frame's two exposed corners
  (top-left, bottom-right) — medium gray, technical-drawing feel.

See `references/Example_Start_Proposal@2x.png` for the canonical output and
`references/template.html` for the exact composition.

## Usage

```bash
python3 .claude/skills/blog-screenshot/build.py <source_image> <slug>
```

- `<source_image>` — the raw screenshot, anywhere on disk (image-cache path, a fresh
  Desktop screenshot, etc.).
- `<slug>` — kebab-case deliverable name, e.g. `start-a-proposal`.

This copies the source into `Blog_Screenshots/<slug>-raw.<ext>`, writes
`Blog_Screenshots/<slug>.html` from the template, and renders
`Blog_Screenshots/<slug>@2x.png`.

Flags: `--out-dir DIR` (default `Blog_Screenshots/`), `--no-render` (HTML only).

**Always Read the rendered PNG back** and eyeball it against the example before
handing it over.

## Getting the screenshot onto disk

The screenshot is usually one the user just took or pasted. Pasted images are **not
on disk** — resolve a real path first:

- **Pasted into the chat:** look under the session image-cache
  (`/Users/<you>/.claude/image-cache/<session-id>/`) for the newest file and pass that.
- **A macOS screenshot they just took:** grab the newest file on the Desktop. These
  filenames contain a U+202F narrow no-break space (`Screenshot 2026-07-15 at
  3.24.01 PM.png`), so glob rather than typing the name:
  `ls -t ~/Desktop/Screenshot*.png | head -1`.

Pass that resolved path as `<source_image>`.

## Design notes / tuning

- **Works at any aspect ratio.** The canvas is derived from the fitted screenshot plus
  fixed padding (`TARGET_LONG` / `PAD_*` in `build.py`), so a wide dashboard, a
  near-square kanban board, and a tall panel all compose the same way — the shot stays
  large and the frame reveal stays proportional. Output pixel dimensions therefore
  vary per shot (that's fine for in-article images, which scale to column width). To
  make every shot bigger or smaller, change `TARGET_LONG`; to change the whitespace,
  change `PAD_X` / `PAD_TOP` / `PAD_BOTTOM`. Don't stretch the source.
- **Auto-trim + auto-border** need Pillow (fall back to no-trim / no-border if it's
  missing). Trim only crops a solid one-color margin — it won't remove browser chrome,
  toolbars, or a busy background; crop the source down to the UI first for those. The
  border only appears when a single-surface shot has a faint/cut edge; if the
  heuristic guesses wrong, hand-edit the `.shot { border: ... }` line in the generated
  HTML (set it to `none` or a color) and re-render.
- **Glass thickness** is set in the template's `.glass` rule (12px padding, 24px
  radius) with the matching `GLASS` constant in `build.py` (pad + 1px edge per side,
  used for canvas sizing). Change both together if the user wants a thicker or
  thinner ring.
- **Partial-scroll captures** (content visibly sliced mid-element at top/bottom):
  if the trim leaves the cut edges looking cramped or odd, pad the raw with a white
  margin on the **sides only** (`ImageOps.expand(im, border=(m, 0, m, 0), ...)`,
  m ≈ 5% of the long side) so the sliced edges run flush into the glass and read as
  intentional, then update the shot/canvas dimensions in the HTML and re-render.
- **Colors are locked** to the technical-neutral palette (`--frame #dcdcdc`,
  `--cross #8c8c8c`). No brand accent is added — the accent lives
  inside the product UI being shown. Do not add a logo, URL, or accent bar; this is a
  clean in-article image, not a social tile.
- The offset geometry (`.frame` insets and the two `.cross` corners) is calibrated to
  match the reference. Leave it unless the user wants a different look.

## Rendering

The build script calls `html-screenshot` with `--selector ".canvas"` at 2×. To
re-render after hand-editing the HTML:

```bash
python3 .claude/skills/html-screenshot/shoot.py \
  Blog_Screenshots/<slug>.html --selector ".canvas" -o Blog_Screenshots/<slug>@2x.png
```

This is a raster deliverable (no links, no text selection) — PNG is the final form;
there is no PDF step.
