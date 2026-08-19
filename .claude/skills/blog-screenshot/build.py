#!/usr/bin/env python3
"""
Wrap a raw product screengrab in the Atom blog "technical blueprint frame" and
render it to a PNG.

Usage:
    python3 .claude/skills/blog-screenshot/build.py <source_image> <slug> [--out-dir DIR] [--no-render]

    <source_image>  Path to the raw screenshot (PNG/JPG). Can be anywhere, e.g. an
                    image-cache path or a fresh Desktop screenshot.
    <slug>          Kebab-case name for the deliverable, e.g. "start-a-proposal".

Options:
    --out-dir DIR   Folder to write into (default: Blog_Screenshots/ at repo root).
    --no-render     Only write the HTML; skip the PNG render.

Produces, in <out-dir>:
    <slug>-raw.<ext>   copy of the source screenshot
    <slug>.html        the framed composition (references the raw copy)
    <slug>@2x.png      the rendered blog image (unless --no-render)
"""
import argparse
import shutil
import struct
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
TEMPLATE = SKILL_DIR / "references" / "template.html"
REPO_ROOT = SKILL_DIR.parents[2]  # .claude/skills/blog-screenshot -> repo root
SHOOT = REPO_ROOT / ".claude" / "skills" / "html-screenshot" / "shoot.py"

# Layout constants. The canvas is derived from the fitted screenshot plus this
# padding, so the frame reveal + crop marks look proportional at any aspect ratio.
TARGET_LONG = 1040   # longest side of the screenshot on the canvas (never upscaled)
PAD_X = 240          # breathing room left/right of the shot
PAD_TOP = 210        # room above the shot (frame + crop mark peek up into this)
PAD_BOTTOM = 170     # room below the shot (it spills past the frame's bottom edge)
GLASS = 13           # glass ring per side (12px pad + 1px edge in the template)


def trim_border(src: Path, dst: Path):
    """Crop a uniform (usually white) margin off the screenshot so it hugs the UI.

    Uses Pillow if available; otherwise copies through untouched. Returns the
    (width, height) written to dst.
    """
    try:
        from PIL import Image, ImageChops
    except ImportError:
        shutil.copyfile(src, dst)
        return image_size(dst), "none"  # no pixel access → no trim, no border

    im = Image.open(src).convert("RGB")
    # background = the most common corner color (top-left is a safe default)
    bg_color = im.getpixel((0, 0))
    bg = Image.new("RGB", im.size, bg_color)
    diff = ImageChops.difference(im, bg).convert("L")
    mask = diff.point(lambda p: 255 if p > 12 else 0)  # tolerance for anti-aliasing
    bbox = mask.getbbox()
    if bbox and bbox != (0, 0, im.width, im.height):
        im = im.crop(bbox)
    im.save(dst)
    border = edge_border(im, bg_color)
    return im.size, border


def edge_border(im, bg_color):
    """Return a CSS border for the shot when it's a single surface with a faint edge.

    Now that the shot is flat (no shadow), a single-panel UI whose own border is
    faint — or whose edge was cut off in the capture — blends into the white canvas
    and looks sliced. In that case we add a 1px border derived from the UI's own edge
    tone (its average perimeter color, nudged darker) to close it into a clean card.

    We skip this for multi-panel shots (e.g. kanban columns): those have full-height
    background gutters between the panels, and a bounding border would draw a stray
    line across the empty gaps. Detecting a gutter is what tells the two apart.
    Returns "none" when no border should be added.
    """
    w, h = im.size
    px = im.load()

    def near_bg(c):
        return all(abs(c[i] - bg_color[i]) <= 12 for i in range(3))

    # Multi-panel? Look for a wide, near-full-height background column in the interior.
    margin = max(4, round(w * 0.03))
    col_bg = []  # fraction of each column that is background, top-to-bottom
    for x in range(w):
        col_bg.append(sum(near_bg(px[x, y]) for y in range(h)) / h)
    run = widest = 0
    for x in range(margin, w - margin):
        run = run + 1 if col_bg[x] >= 0.985 else 0
        widest = max(widest, run)
    min_gutter = max(6, round(w * 0.012))

    # Perimeter contrast: how visible is the shot's own edge against the canvas?
    ring = []
    for x in range(w):
        ring.append(px[x, 0]); ring.append(px[x, h - 1])
    for y in range(h):
        ring.append(px[0, y]); ring.append(px[w - 1, y])
    mean_contrast = sum(max(abs(c[i] - bg_color[i]) for i in range(3)) for c in ring) / len(ring)

    if widest >= min_gutter:
        print(f"  border: none (multi-panel — {widest}px gutter)")
        return "none"
    # Only add a border when the edge is genuinely ABSENT (the UI bleeds to a white
    # edge). A faint-but-present border still counts as having one — leave it alone.
    if mean_contrast >= 8:
        print(f"  border: none (edge present — contrast {mean_contrast:.0f})")
        return "none"
    n = len(ring)
    avg = tuple(sum(c[i] for c in ring) // n for i in range(3))
    bc = tuple(max(0, v - 26) for v in avg)  # nudge the UI tone darker
    css = f"1px solid rgb({bc[0]}, {bc[1]}, {bc[2]})"
    print(f"  border: added ({css}) — faint edge, contrast {mean_contrast:.0f}")
    return css


def image_size(path: Path):
    """Return (width, height) for a PNG/JPEG without needing Pillow."""
    with open(path, "rb") as f:
        head = f.read(26)
    # PNG
    if head[:8] == b"\x89PNG\r\n\x1a\n":
        w, h = struct.unpack(">II", head[16:24])
        return w, h
    # JPEG — walk the segments for the first SOF marker
    if head[:2] == b"\xff\xd8":
        with open(path, "rb") as f:
            f.read(2)
            while True:
                b = f.read(1)
                while b and b != b"\xff":
                    b = f.read(1)
                marker = f.read(1)
                while marker == b"\xff":
                    marker = f.read(1)
                if not marker:
                    break
                if 0xC0 <= marker[0] <= 0xCF and marker[0] not in (0xC4, 0xC8, 0xCC):
                    f.read(3)
                    h, w = struct.unpack(">HH", f.read(4))
                    return w, h
                seg_len = struct.unpack(">H", f.read(2))[0]
                f.seek(seg_len - 2, 1)
    raise ValueError(f"could not read image dimensions from {path}")


def main():
    ap = argparse.ArgumentParser(description="Frame a screengrab as an Atom blog image.")
    ap.add_argument("source", help="path to the raw screenshot")
    ap.add_argument("slug", help="kebab-case deliverable name, e.g. start-a-proposal")
    ap.add_argument("--out-dir", default=str(REPO_ROOT / "Blog_Screenshots"),
                    help="output folder (default: Blog_Screenshots/)")
    ap.add_argument("--no-render", action="store_true", help="write HTML only, skip PNG")
    args = ap.parse_args()

    src = Path(args.source).expanduser()
    if not src.exists():
        sys.exit(f"error: source image not found: {src}")

    out_dir = Path(args.out_dir).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)

    # PNG out (trim may drop an alpha/format; keep it simple and lossless).
    raw_name = f"{args.slug}-raw.png"
    raw_path = out_dir / raw_name
    # Trim the uniform margin so the shot crops to the UI edges, and decide whether
    # the shot needs its own border to read against the canvas.
    (sw, sh), shot_border = trim_border(src, raw_path)

    # Fit the screenshot to TARGET_LONG (never upscaled), then size the canvas
    # around it so the frame + crop marks stay proportional at any aspect ratio.
    scale = min(TARGET_LONG / max(sw, sh), 1.0)
    shot_w = round(sw * scale)
    shot_h = round(sh * scale)
    canvas_w = shot_w + 2 * PAD_X + 2 * GLASS
    canvas_h = shot_h + PAD_TOP + PAD_BOTTOM + 2 * GLASS

    html = (TEMPLATE.read_text()
            .replace("__CANVAS_W__", str(canvas_w))
            .replace("__CANVAS_H__", str(canvas_h))
            .replace("__WRAP_LEFT__", str(PAD_X))
            .replace("__WRAP_TOP__", str(PAD_TOP))
            .replace("__SHOT_W__", str(shot_w))
            .replace("__SHOT_BORDER__", shot_border)
            .replace("__IMAGE_SRC__", raw_name))
    html_path = out_dir / f"{args.slug}.html"
    html_path.write_text(html)
    print(f"wrote {html_path}  (canvas {canvas_w}x{canvas_h}, shot {shot_w}x{shot_h})")

    if args.no_render:
        return

    png_path = out_dir / f"{args.slug}@2x.png"
    cmd = ["python3", str(SHOOT), str(html_path),
           "--selector", ".canvas", "-o", str(png_path)]
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
