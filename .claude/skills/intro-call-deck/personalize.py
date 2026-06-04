#!/usr/bin/env python3
"""
Personalize the finalized Atom Grants intro call deck for one prospect.

Only the cover and the close slide change between prospects, so this script
just swaps five placeholder tokens in the template, writes a per-prospect HTML
next to the template (so the relative img/ and ../../assets paths still
resolve), and optionally renders a print-ready PDF.

The PDF is always produced with the screenshot-and-stitch method: each slide is
captured as a 2x PNG (by stepping the deck through its .active states) and the
PNGs are merged into a 13.333x7.5 PDF. We never use html-to-pdf for this deck —
its print renderer mis-paginates these full-viewport 16:9 slides.

Usage:
  python3 .claude/skills/intro-call-deck/personalize.py \
      --institution "University of Iowa" \
      --name "Tomer du Sautoy" \
      --email "tomer@atomgrants.com" \
      --date "June 2026"

Optional:
  --title "Atom Grants"     # the ", <Title>" after the presenter name on the cover
  --out   <path.html>       # default: <template dir>/Intro_Call_Deck_<Slug>.html
  --no-pdf                  # skip PDF render (HTML only)
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
REPO_ROOT = SKILL_DIR.parents[2]                      # .../Design
TEMPLATE = REPO_ROOT / "Intro_Call_Deck" / "v4" / "Intro_Call_Deck.html"
MERGE = SKILL_DIR.parents[0] / "png-to-pdf" / "merge.py"
PAGE_SIZE = "13.333x7.5"                               # 16:9 slide, in inches

# Token in template  ->  argparse attribute holding the replacement
TOKENS = {
    "[Your name]": "name",
    "[Title]": "title",
    "[Month YYYY]": "date",
    "[Institution name]": "institution",
    "[your.email@atomgrants.com]": "email",
}


def slug(text):
    return re.sub(r"_+", "_", re.sub(r"[^A-Za-z0-9]+", "_", text)).strip("_")


def ensure_playwright():
    try:
        import playwright  # noqa: F401
    except ImportError:
        print("Installing playwright...", file=sys.stderr)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "playwright"])
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            try:
                p.chromium.launch().close()
            except Exception:
                print("Installing chromium...", file=sys.stderr)
                subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])
    except Exception:
        subprocess.check_call([sys.executable, "-m", "playwright", "install", "chromium"])


def render_pdf(html_path, pdf_path, title):
    """Capture each slide as a 2x PNG, then stitch into a 13.333x7.5 PDF.

    Slides are full-viewport 16:9 sections toggled by an .active class, so we
    step through them by toggling that class on the DOM directly (the deck's
    show() helper is module-scoped and not reachable from page.evaluate).
    """
    ensure_playwright()
    from playwright.sync_api import sync_playwright

    html_path = Path(html_path).resolve()
    pngs = []
    with sync_playwright() as p:
        ctx = p.chromium.launch().new_context(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=2.0,
        )
        page = ctx.new_page()
        page.goto(f"file://{html_path}")
        page.wait_for_load_state("networkidle")
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(1000)
        total = page.evaluate("document.querySelectorAll('.slide').length")
        for i in range(total):
            page.evaluate(
                "(idx) => document.querySelectorAll('.slide')"
                ".forEach((s,k)=>s.classList.toggle('active',k===idx))",
                i,
            )
            page.wait_for_timeout(350)
            out = html_path.with_name(f"{html_path.stem}_slide_{i+1:02d}@2x.png")
            page.locator(".slide.active").screenshot(path=str(out), type="png")
            pngs.append(out)
        ctx.browser.close()

    cmd = [sys.executable, str(MERGE), *map(str, pngs),
           "-o", str(pdf_path), "--size", PAGE_SIZE, "--title", title]
    subprocess.run(cmd, check=True)
    for png in pngs:                       # tidy up the intermediate frames
        png.unlink(missing_ok=True)


def main():
    ap = argparse.ArgumentParser(description="Personalize the intro call deck for a prospect.")
    ap.add_argument("--institution", required=True, help='e.g. "University of Iowa"')
    ap.add_argument("--name", required=True, help="Presenter name (cover + contact)")
    ap.add_argument("--email", required=True, help="Presenter email")
    ap.add_argument("--date", required=True, help='e.g. "June 2026"')
    ap.add_argument("--title", default="Atom Grants", help='Presenter title/org on the cover (default: "Atom Grants")')
    ap.add_argument("--out", help="Output HTML path (default: alongside the template)")
    ap.add_argument("--no-pdf", action="store_true", help="Skip the PDF render")
    args = ap.parse_args()

    if not TEMPLATE.exists():
        sys.exit(f"Template not found: {TEMPLATE}")

    html = TEMPLATE.read_text(encoding="utf-8")
    missing = [tok for tok in TOKENS if tok not in html]
    if missing:
        sys.exit("Template is missing expected placeholder(s): " + ", ".join(missing) +
                 "\nIs Intro_Call_Deck/v4/Intro_Call_Deck.html still the clean template?")

    for tok, attr in TOKENS.items():
        html = html.replace(tok, getattr(args, attr))

    out = Path(args.out) if args.out else TEMPLATE.with_name(f"Intro_Call_Deck_{slug(args.institution)}.html")
    if out.parent.resolve() != TEMPLATE.parent.resolve() and not args.out:
        out = TEMPLATE.with_name(out.name)
    out.write_text(html, encoding="utf-8")
    print(f"HTML:  {out}")
    if out.parent.resolve() != TEMPLATE.parent.resolve():
        print("WARNING: output is outside the template folder — relative image/asset paths may break.")

    if args.no_pdf:
        return
    pdf = out.with_suffix(".pdf")
    print("Rendering PDF (screenshot-and-stitch) ...")
    render_pdf(out, pdf, f"Atom Grants — {args.institution}")
    print(f"Saved: {pdf}")


if __name__ == "__main__":
    main()
