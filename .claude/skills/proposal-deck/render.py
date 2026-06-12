#!/usr/bin/env python3
"""
Render an Atom Grants proposal deck to a 3:2 (12x8 in) PDF.

The proposal deck is a landscape deck of full-viewport slides. Like the
intro-call deck, it is ALWAYS exported via screenshot-and-stitch (never
html-to-pdf): each slide is captured at a 1620x1080 (3:2) viewport so the
16:9-authored slides reflow into a laptop-friendly, less-wide frame, then the
PNGs are stitched into a 12x8 in PDF.

Usage:
    python3 .claude/skills/proposal-deck/render.py <Deck>/<Deck>.html
    python3 .claude/skills/proposal-deck/render.py <Deck>/<Deck>.html -o out.pdf

Navigation contract the deck must honor (the finalized template already does):
  - one `.slide` section per slide, one shown at a time via `.slide.active`
  - `location.hash = '#N'` deep-links to slide N (fires the deck's own show()).
"""
import argparse
import subprocess
import sys
from pathlib import Path

VIEWPORT_W, VIEWPORT_H = 1620, 1080          # 3:2 capture viewport (CSS px)
PAGE_SIZE = "12x8"                            # 3:2 page, inches
SKILL_DIR = Path(__file__).resolve().parent
MERGE = SKILL_DIR.parent / "png-to-pdf" / "merge.py"       # .claude/skills/png-to-pdf/merge.py


def ensure_playwright():
    try:
        import playwright  # noqa: F401
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "playwright"])
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        try:
            p.chromium.launch().close()
        except Exception:
            subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])


def main():
    ap = argparse.ArgumentParser(description="Render a proposal deck to a 12x8 (3:2) PDF.")
    ap.add_argument("html", help="Path to the deck HTML")
    ap.add_argument("-o", "--out", help="Output PDF path (default: alongside the HTML)")
    ap.add_argument("--title", default="Atom Grants: Partnership Proposal", help="PDF title")
    args = ap.parse_args()

    html = Path(args.html).resolve()
    if not html.exists():
        sys.exit(f"HTML not found: {html}")
    pdf = Path(args.out).resolve() if args.out else html.with_suffix(".pdf")

    ensure_playwright()
    from playwright.sync_api import sync_playwright

    pngs = []
    with sync_playwright() as p:
        ctx = p.chromium.launch().new_context(
            viewport={"width": VIEWPORT_W, "height": VIEWPORT_H}, device_scale_factor=2.0)
        page = ctx.new_page()
        page.goto(f"file://{html}")
        page.wait_for_load_state("networkidle")
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(1000)
        total = page.evaluate("document.querySelectorAll('.slide').length")
        for i in range(total):
            page.evaluate("(n) => { location.hash = '#' + n; }", i + 1)
            page.wait_for_timeout(350)
            out = html.with_name(f"{html.stem}_slide_{i + 1:02d}@2x.png")
            page.locator(".slide.active").screenshot(path=str(out), type="png")
            pngs.append(out)
        ctx.browser.close()

    subprocess.run([sys.executable, str(MERGE), *map(str, pngs),
                    "-o", str(pdf), "--size", PAGE_SIZE, "--title", args.title], check=True)
    for png in pngs:
        png.unlink(missing_ok=True)
    print(f"Rendered {total} slides -> {pdf}")


if __name__ == "__main__":
    main()
