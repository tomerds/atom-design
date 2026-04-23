#!/usr/bin/env python3
"""
Merge one or more PNG pages into a single print-ready PDF.

Typical use: take the per-page PNGs rendered by the html-screenshot skill and
stitch them into a downloadable multi-page PDF (playbook, one-pager set, etc.)
at the correct physical page size.

The PNGs are assumed to be rendered at a consistent retina scale against a
fixed page size (Letter portrait by default). DPI is computed so the resulting
PDF page matches the physical size in inches.

Examples
--------
# Auto-detect: Letter portrait (8.5 x 11 in), 2x retina PNGs (1632 px wide)
python3 .claude/skills/png-to-pdf/merge.py Project/page_*@2x.png \
    -o Project/Project.pdf --title "My Playbook"

# Explicit DPI (e.g. 3x retina captures)
python3 .claude/skills/png-to-pdf/merge.py Project/page_*.png -o out.pdf --dpi 288

# A4 portrait
python3 .claude/skills/png-to-pdf/merge.py Project/page_*.png -o out.pdf --size a4
"""
import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Pillow is required. Install with: pip3 install Pillow", file=sys.stderr)
    sys.exit(1)


PRESETS = {
    "letter":          (8.5, 11.0),   # US Letter portrait
    "letter-landscape": (11.0, 8.5),
    "a4":              (8.27, 11.69), # A4 portrait
    "a4-landscape":    (11.69, 8.27),
    "tabloid":         (11.0, 17.0),
    "legal":           (8.5, 14.0),
}


def parse_size(s: str) -> tuple[float, float]:
    s = s.strip().lower()
    if s in PRESETS:
        return PRESETS[s]
    # Custom "WxH" in inches, e.g. "6x9"
    if "x" in s:
        w, h = s.split("x", 1)
        return float(w), float(h)
    raise argparse.ArgumentTypeError(
        f"Unknown size '{s}'. Use a preset ({', '.join(PRESETS)}) or WxH in inches (e.g. 6x9)."
    )


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("images", nargs="+", help="PNG files (glob expansion welcome)")
    p.add_argument("-o", "--output", required=True, help="Output PDF path")
    p.add_argument(
        "--size",
        default="letter",
        type=parse_size,
        help="Page size preset or WxH inches. Default: letter (8.5x11). "
             "Presets: " + ", ".join(PRESETS),
    )
    p.add_argument(
        "--dpi",
        type=float,
        default=None,
        help="Override DPI. By default DPI is computed so the image width equals the page width in inches.",
    )
    p.add_argument("--title", default=None, help="PDF title metadata")
    p.add_argument("--author", default=None, help="PDF author metadata")
    p.add_argument(
        "--no-sort",
        action="store_true",
        help="Preserve argv order. Default sorts filenames alphabetically for deterministic output.",
    )
    args = p.parse_args()

    paths = [Path(x).resolve() for x in args.images]
    missing = [str(x) for x in paths if not x.exists()]
    if missing:
        sys.exit("Missing files:\n  " + "\n  ".join(missing))

    if not args.no_sort:
        paths.sort(key=lambda x: x.name)

    page_w_in, page_h_in = args.size

    images: list[Image.Image] = []
    for path in paths:
        img = Image.open(path).convert("RGB")
        # Compute DPI so the image width matches the target page width.
        # Height follows automatically from the image's aspect ratio; pages
        # whose aspect doesn't match the target size will still render at
        # their true proportions (just sized to the correct width).
        dpi = args.dpi if args.dpi else img.width / page_w_in
        img.info["dpi"] = (dpi, dpi)
        images.append(img)

    out = Path(args.output).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    first, rest = images[0], images[1:]
    save_kwargs = {
        "format": "PDF",
        "resolution": first.info["dpi"][0],
        "save_all": True,
        "append_images": rest,
    }
    if args.title:
        save_kwargs["title"] = args.title
    if args.author:
        save_kwargs["author"] = args.author

    first.save(out, **save_kwargs)

    kb = out.stat().st_size // 1024
    print(
        f"Saved: {out}  ({kb:,} KB, {len(images)} page{'s' if len(images) != 1 else ''}, "
        f"{page_w_in}x{page_h_in} in @ {first.info['dpi'][0]:.0f} dpi)"
    )


if __name__ == "__main__":
    main()
