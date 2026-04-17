---
name: html-screenshot
description: Render a local HTML file to a high-resolution PNG using headless Chromium via Playwright. Trigger when the user asks to "screenshot", "render", "export to PNG/image", "capture", or "take a picture of" any HTML design deliverable (poster, deck, one-pager, mockup). Supports retina scaling, element-scoped capture, and auto-fit viewport.
---

# html-screenshot

Render any HTML design file to a crisp PNG using headless Chromium (Playwright).

## Prerequisites

Run once per machine (the skill script installs lazily if missing, but doing it up front is faster):

```bash
pip3 install playwright
python3 -m playwright install chromium
```

## Usage

From the repository root:

```bash
python3 .claude/skills/html-screenshot/shoot.py <path/to/file.html>
```

Common flags:

| Flag | Default | Purpose |
|---|---|---|
| `-o, --output <path>` | `<name>@<scale>x.png` next to the HTML | Custom output path |
| `-s, --scale <n>` | `2` | Device scale factor (retina). Use `3` for extra-crisp print. |
| `--selector <css>` | `.poster` | CSS selector to crop to |
| `--full-page` | off | Capture the whole page (overrides `--selector`) |
| `--wait <ms>` | `1200` | Extra settle time after fonts/network idle |

## Examples

```bash
# Default: captures .poster element at 2× into MSU_Poster_2026@2x.png
python3 .claude/skills/html-screenshot/shoot.py MSU_Poster_2026/MSU_Poster_2026.html

# 3× retina, custom output
python3 .claude/skills/html-screenshot/shoot.py deck.html -s 3 -o deck_print.png

# Non-poster document: capture whole page
python3 .claude/skills/html-screenshot/shoot.py one_pager.html --full-page

# Capture a specific element (e.g. one slide)
python3 .claude/skills/html-screenshot/shoot.py deck.html --selector "#slide-3"
```

## Notes

- The script waits for `networkidle` + `document.fonts.ready` before shooting, so web fonts (Cal Sans, DM Sans) render correctly.
- Viewport is auto-sized to the target element's bounding box (plus margin) so nothing clips.
- Output is PNG with no transparency — ready for print, Slack, email, etc.
- For very large posters (e.g. 36×56 in at 2×) the PNG can be 5–10 MB. Use `-s 1` for preview renders.
