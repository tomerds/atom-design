#!/usr/bin/env python3
"""
Personalize the Atom Grants renewal-upsell deck for one existing partner.

This swaps the mechanical text tokens in the template, drops the partner's logo
into the cover co-brand lockup (--logo, required), writes a per-partner HTML next
to the template (so the relative img/ and ../assets paths still resolve), and
optionally renders a print-ready PDF.

WHAT THIS DOES NOT DO: the slide-02 metric cells and the slide-06 dashboard KPI
values are DATA, fed from the partner's actual usage. They ship as grey skeleton
bars and must be filled in by hand once the numbers are in. personalize.py never
touches them. (See the upsell-deck SKILL "The data slide" section.)

The partner logo is copied into Upsell_Deck/tempimg/ (NOT img/) and referenced
from there. tempimg/ is git-ignored, so the per-partner logo never gets committed.

The PDF is always produced with the screenshot-and-stitch method: each slide is
captured as a 2x PNG (by stepping the deck through its .active states) and the
PNGs are merged into a 12x8 in (3:2) PDF. We render at a 3:2 viewport (1620x1080)
so the full-viewport slides reflow into a laptop-friendly frame. We never use
html-to-pdf for this deck — its print renderer mis-paginates the full-viewport
slides.

Usage:
  python3 .claude/skills/upsell-deck/personalize.py \
      --institution "Youngstown State University" \
      --short "Youngstown State" \
      --name "Tomer du Sautoy" \
      --email "tomer@atomgrants.com" \
      --date "June 2026" \
      --logo Upsell_Deck/img/logos/youngstown-state.png \
      --renewal-decision "Aug 1 auto-renewal" \
      --renewal-date "Sep 1, 2026"

Optional:
  --title "Atom Grants"        # the ", <Title>" after the presenter name on the cover
  --short "<name>"             # conversational name in prose (default: --institution)
  --renewal-decision "<text>"  # slide 8 "Decision by" value (default: leaves the [token] visible)
  --renewal-date "<text>"      # slide 8 "Renews" value      (default: leaves the [token] visible)
  --out   <path.html>          # default: <template dir>/Upsell_Deck_<Slug>.html
  --no-pdf                     # skip PDF render (HTML only)
"""
import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent
REPO_ROOT = SKILL_DIR.parents[2]                      # .../Design
TEMPLATE = REPO_ROOT / "Upsell_Deck" / "Upsell_Deck.html"
MERGE = SKILL_DIR.parents[0] / "png-to-pdf" / "merge.py"
# 3:2 (laptop-friendly): capture at a 3:2 viewport so the full-viewport slides
# reflow into a less-wide frame, then stitch to a 12x8 page.
VIEWPORT_W, VIEWPORT_H = 1620, 1080                    # 3:2 capture viewport (CSS px)
PAGE_SIZE = "12x8"                                     # 3:2 page, in inches

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

    Slides are full-viewport sections shown one at a time. We navigate via the
    deck's own hash deep-link (#N), which fires its hashchange listener and runs
    show() — so the .active slide AND the page-number counter both update.
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
    ap = argparse.ArgumentParser(description="Personalize the renewal-upsell deck for an existing partner.")
    ap.add_argument("--institution", required=True, help='Formal name, e.g. "Youngstown State University"')
    ap.add_argument("--short", help='Conversational name used in prose (default: --institution), e.g. "Youngstown State"')
    ap.add_argument("--name", required=True, help="Presenter name (cover + contact)")
    ap.add_argument("--email", required=True, help="Presenter email")
    ap.add_argument("--date", required=True, help='e.g. "June 2026"')
    ap.add_argument("--title", default="Atom Grants", help='Presenter title/org on the cover (default: "Atom Grants")')
    ap.add_argument("--renewal-decision", help='Slide 8 "Decision by" value, e.g. "Aug 1 auto-renewal" (default: leaves the [token] visible)')
    ap.add_argument("--renewal-date", help='Slide 8 "Renews" value, e.g. "Sep 1, 2026" (default: leaves the [token] visible)')
    ap.add_argument("--logo", required=True, help="Partner logo image for the cover co-brand lockup (png/svg/jpg/webp)")
    ap.add_argument("--out", help="Output HTML path (default: alongside the template)")
    ap.add_argument("--no-pdf", action="store_true", help="Skip the PDF render")
    args = ap.parse_args()

    if not TEMPLATE.exists():
        sys.exit(f"Template not found: {TEMPLATE}")

    html = TEMPLATE.read_text(encoding="utf-8")

    # [Institution full] MUST be replaced before [Institution] (substring).
    short = args.short or args.institution
    ordered = [
        ("[Institution full]", args.institution),
        ("[Institution]", short),
        ("[Your name]", args.name),
        ("[Title]", args.title),
        ("[Month YYYY]", args.date),
        ("[your.email@atomgrants.com]", args.email),
    ]
    if args.renewal_decision:
        ordered.append(("[Renewal decision]", args.renewal_decision))
    if args.renewal_date:
        ordered.append(("[Renewal date]", args.renewal_date))
    for tok, val in ordered:
        html = html.replace(tok, val)

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

    out = Path(args.out) if args.out else TEMPLATE.with_name(f"Upsell_Deck_{slug(args.institution)}.html")
    if out.parent.resolve() != TEMPLATE.parent.resolve() and not args.out:
        out = TEMPLATE.with_name(out.name)
    out.write_text(html, encoding="utf-8")
    print(f"HTML:  {out}")
    if out.parent.resolve() != TEMPLATE.parent.resolve():
        print("WARNING: output is outside the template folder — relative image/asset paths may break.")

    # Surface anything still unresolved so it gets filled by hand.
    leftovers = sorted(set(re.findall(r"\[(?:Institution|Your name|Title|Month YYYY|Renewal[^\]]*|your\.email[^\]]*)\]", html)))
    if leftovers:
        print("NOTE: tokens still in the deck (fill by hand): " + ", ".join(leftovers))
    if 'class="skel' in html:
        print("NOTE: slide-02 metrics + slide-06 KPIs are still SKELETON — fill from the partner's usage data.")

    if args.no_pdf:
        return
    pdf = out.with_suffix(".pdf")
    print("Rendering PDF (screenshot-and-stitch) ...")
    render_pdf(out, pdf, f"Atom Grants — {args.institution}")
    print(f"Saved: {pdf}")


if __name__ == "__main__":
    main()
