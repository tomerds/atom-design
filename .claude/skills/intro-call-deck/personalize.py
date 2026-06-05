#!/usr/bin/env python3
"""
Personalize the finalized Atom Grants intro call deck for one prospect.

Only the cover and the close slide change between prospects, so this script
swaps five placeholder tokens in the template, drops the partner's logo into
the cover co-brand lockup (--logo, required), writes a per-prospect HTML next
to the template (so the relative img/ and ../assets paths still resolve), and
optionally renders a print-ready PDF.

The partner logo is copied into Intro_Call_Deck/tempimg/ (NOT img/) and
referenced from there. tempimg/ is git-ignored (the .gitignore tracks only the
template HTML + img/ inside Intro_Call_Deck/), so the per-prospect logo never
gets committed.

The PDF is always produced with the screenshot-and-stitch method: each slide is
captured as a 2x PNG (by stepping the deck through its .active states) and the
PNGs are merged into a 12x8 in (3:2) PDF. We render at a 3:2 viewport (1620x1080)
so the full-viewport slides reflow into a laptop-friendly, less-wide frame rather
than the wide 16:9 default. We never use html-to-pdf for this deck — its print
renderer mis-paginates these full-viewport slides.

Usage:
  python3 .claude/skills/intro-call-deck/personalize.py \
      --institution "University of Iowa" \
      --name "Tomer du Sautoy" \
      --email "tomer@atomgrants.com" \
      --date "June 2026" \
      --logo ~/Downloads/iowa-logo.png

Optional:
  --title "Atom Grants"     # the ", <Title>" after the presenter name on the cover
  --out   <path.html>       # default: <template dir>/Intro_Call_Deck_<Slug>.html
  --no-pdf                  # skip PDF render (HTML only)
"""
import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
REPO_ROOT = SKILL_DIR.parents[2]                      # .../Design
TEMPLATE = REPO_ROOT / "Intro_Call_Deck" / "Intro_Call_Deck.html"
MERGE = SKILL_DIR.parents[0] / "png-to-pdf" / "merge.py"
# 3:2 (laptop-friendly) is the default: capture at a 3:2 viewport so the
# full-viewport slides reflow into a less-wide frame, then stitch to a 12x8 page.
VIEWPORT_W, VIEWPORT_H = 1620, 1080                    # 3:2 capture viewport (CSS px)
PAGE_SIZE = "12x8"                                     # 3:2 page, in inches

# Token in template  ->  argparse attribute holding the replacement
TOKENS = {
    "[Your name]": "name",
    "[Title]": "title",
    "[Month YYYY]": "date",
    "[Institution name]": "institution",
    "[your.email@atomgrants.com]": "email",
}

# Cover co-brand lockup placeholder (swapped for an <img> using --logo)
PARTNER_PLACEHOLDER = '<span class="partner-logo">[Partner logo]</span>'

# Git-ignored folder the partner logo is copied into (kept out of the committed img/)
TEMPIMG_DIRNAME = "tempimg"
ALLOWED_LOGO_EXTS = {".png", ".jpg", ".jpeg", ".svg", ".webp", ".gif"}


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
    """Capture each slide as a 2x PNG, then stitch into a 12x8 in (3:2) PDF.

    Slides are full-viewport sections shown one at a time. We navigate via
    the deck's own hash deep-link (#N), which fires its hashchange listener and
    runs show() — so the .active slide AND the page-number counter both update.
    (Toggling .active directly would leave the counter stuck on 1/N.)
    """
    ensure_playwright()
    from playwright.sync_api import sync_playwright

    html_path = Path(html_path).resolve()
    pngs = []
    with sync_playwright() as p:
        ctx = p.chromium.launch().new_context(
            viewport={"width": VIEWPORT_W, "height": VIEWPORT_H},
            device_scale_factor=2.0,
        )
        page = ctx.new_page()
        page.goto(f"file://{html_path}")
        page.wait_for_load_state("networkidle")
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(1000)
        total = page.evaluate("document.querySelectorAll('.slide').length")
        for i in range(total):
            page.evaluate("(n) => { location.hash = '#' + n; }", i + 1)
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
    ap.add_argument("--logo", required=True, help="Partner logo image for the cover co-brand lockup (png/svg/jpg); inlined as a data URI, not copied into the repo")
    ap.add_argument("--out", help="Output HTML path (default: alongside the template)")
    ap.add_argument("--no-pdf", action="store_true", help="Skip the PDF render")
    args = ap.parse_args()

    if not TEMPLATE.exists():
        sys.exit(f"Template not found: {TEMPLATE}")

    html = TEMPLATE.read_text(encoding="utf-8")
    missing = [tok for tok in TOKENS if tok not in html]
    if missing:
        sys.exit("Template is missing expected placeholder(s): " + ", ".join(missing) +
                 "\nIs Intro_Call_Deck/Intro_Call_Deck.html still the clean template?")

    for tok, attr in TOKENS.items():
        html = html.replace(tok, getattr(args, attr))

    # Partner logo: copy into the git-ignored tempimg/ and point the lockup at it.
    src = Path(args.logo).expanduser()
    if not src.exists():
        sys.exit(f"Logo file not found: {src}")
    if src.suffix.lower() not in ALLOWED_LOGO_EXTS:
        sys.exit(f"Unsupported logo type '{src.suffix}'. Use one of: "
                 + ", ".join(sorted(ALLOWED_LOGO_EXTS)))
    if PARTNER_PLACEHOLDER not in html:
        sys.exit("Template is missing the partner-logo placeholder "
                 f"({PARTNER_PLACEHOLDER}). Is the cover lockup intact?")
    tempimg = TEMPLATE.parent / TEMPIMG_DIRNAME
    tempimg.mkdir(exist_ok=True)
    dest = tempimg / f"{slug(args.institution).lower()}{src.suffix.lower()}"
    shutil.copyfile(src, dest)
    img_tag = (f'<img class="partner-logo-img" src="{TEMPIMG_DIRNAME}/{dest.name}" '
               f'alt="{args.institution}">')
    html = html.replace(PARTNER_PLACEHOLDER, img_tag)
    print(f"Logo:  {dest}  (git-ignored)")

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
