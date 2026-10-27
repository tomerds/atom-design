#!/usr/bin/env python3
"""
Wrap a tweet / X post screenshot in the Atom tweet frame (full black canvas,
thick translucent glass ring) and render it to a PNG.

Usage:
    python3 .claude/skills/tweet-screenshot/build.py <source_image> <slug> [--out-dir DIR] [--no-render]

    <source_image>  Path to the raw tweet screenshot (PNG/JPG).
    <slug>          Kebab-case name, e.g. "alpoge-tweet".

Options:
    --out-dir DIR   Folder to write into (default: Tweet_Screenshots/ at repo root).
    --no-render     Only write the HTML; skip the PNG render.

Produces, in <out-dir>:
    <slug>-raw.png     the tweet, trimmed then re-padded evenly in its own bg color
    <slug>.html        the framed composition (references the raw copy)
    <slug>@2x.png      the rendered image (unless --no-render)
"""
import argparse
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageOps

SKILL_DIR = Path(__file__).resolve().parent
TEMPLATE = SKILL_DIR / "references" / "template.html"
REPO_ROOT = SKILL_DIR.parents[2]  # .claude/skills/tweet-screenshot -> repo root
SHOOT = REPO_ROOT / ".claude" / "skills" / "html-screenshot" / "shoot.py"

# Layout constants (CSS px; the render is 2x).
TARGET_LONG = 1040   # longest side of the tweet on the canvas (never upscaled)
PAD = 120            # even black space around the glass ring on every side
GLASS = 13           # glass ring per side (12px pad + 1px edge in the template)
INNER_PAD = 40       # tweet-bg margin re-added inside the shot after trimming (source px)


def prepare(src: Path, dst: Path):
    """Trim the tweet's uneven capture margin, then re-pad it evenly in the
    tweet's own background color so the text never runs into the glass ring."""
    im = Image.open(src).convert("RGB")
    bg_color = im.getpixel((0, 0))
    diff = ImageChops.difference(im, Image.new("RGB", im.size, bg_color)).convert("L")
    bbox = diff.point(lambda p: 255 if p > 12 else 0).getbbox()
    if bbox:
        im = im.crop(bbox)
    im = ImageOps.expand(im, border=INNER_PAD, fill=bg_color)
    im.save(dst)
    return im.size


def main():
    ap = argparse.ArgumentParser(description="Frame a tweet screenshot for Atom.")
    ap.add_argument("source", help="path to the raw tweet screenshot")
    ap.add_argument("slug", help="kebab-case deliverable name, e.g. alpoge-tweet")
    ap.add_argument("--out-dir", default=str(REPO_ROOT / "Tweet_Screenshots"),
                    help="output folder (default: Tweet_Screenshots/)")
    ap.add_argument("--no-render", action="store_true", help="write HTML only, skip PNG")
    args = ap.parse_args()

    src = Path(args.source).expanduser()
    if not src.exists():
        sys.exit(f"error: source image not found: {src}")

    out_dir = Path(args.out_dir).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)

    raw_name = f"{args.slug}-raw.png"
    sw, sh = prepare(src, out_dir / raw_name)

    scale = min(TARGET_LONG / max(sw, sh), 1.0)
    shot_w = round(sw * scale)
    shot_h = round(sh * scale)
    canvas_w = shot_w + 2 * (GLASS + PAD)
    canvas_h = shot_h + 2 * (GLASS + PAD)

    html = (TEMPLATE.read_text()
            .replace("__CANVAS_W__", str(canvas_w))
            .replace("__CANVAS_H__", str(canvas_h))
            .replace("__SHOT_W__", str(shot_w))
            .replace("__IMAGE_SRC__", raw_name))
    html_path = out_dir / f"{args.slug}.html"
    html_path.write_text(html)
    print(f"wrote {html_path}  (canvas {canvas_w}x{canvas_h}, shot {shot_w}x{shot_h})")

    if args.no_render:
        return

    png_path = out_dir / f"{args.slug}@2x.png"
    subprocess.run(["python3", str(SHOOT), str(html_path),
                    "--selector", ".canvas", "-o", str(png_path)], check=True)


if __name__ == "__main__":
    main()
