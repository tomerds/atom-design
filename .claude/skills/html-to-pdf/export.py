#!/usr/bin/env python3
"""
Export an HTML deliverable directly to a vector PDF via headless Chromium (Playwright).

Unlike the screenshot + stitch pipeline, this preserves:
  - <a href> tags as native clickable link annotations
  - text as selectable / searchable content
  - vector drawing at any zoom level
  - much smaller file size

Prerequisite: the HTML must include @page / @media print CSS that paginates
correctly. See SKILL.md for the boilerplate snippet.
"""
import argparse
import subprocess
import sys
from pathlib import Path


PAGE_PRESETS = {
    "letter":           ("8.5in", "11in"),
    "letter-landscape": ("11in",  "8.5in"),
    "a4":               ("210mm", "297mm"),
    "a4-landscape":     ("297mm", "210mm"),
    "tabloid":          ("11in",  "17in"),
    "legal":            ("8.5in", "14in"),
}


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


def parse_size(size: str):
    if size in PAGE_PRESETS:
        return PAGE_PRESETS[size]
    if "x" in size.lower():
        w, h = size.lower().split("x", 1)
        unit = "in" if not any(u in (w + h) for u in ("mm", "cm", "in", "px")) else ""
        return (f"{w}{unit}", f"{h}{unit}")
    raise ValueError(f"Unknown page size '{size}'. Use a preset or WxH (e.g. 8.5x11, 210mmx297mm).")


def report_links(pdf_path: Path):
    """Print the clickable URLs the PDF now contains, as a sanity check."""
    try:
        from pypdf import PdfReader
    except ImportError:
        return
    try:
        r = PdfReader(str(pdf_path))
    except Exception:
        return
    found = []
    for i, page in enumerate(r.pages, 1):
        anns = page.get("/Annots")
        if not anns:
            continue
        for a in anns:
            obj = a.get_object()
            if obj.get("/Subtype") == "/Link":
                action = obj.get("/A")
                if action and action.get("/URI"):
                    found.append((i, action.get("/URI")))
    if found:
        print(f"Links detected ({len(found)}):")
        for pg, uri in found:
            print(f"  p{pg}  {uri}")


def main():
    parser = argparse.ArgumentParser(description="Export an HTML file to a vector PDF with live links.")
    parser.add_argument("html", help="Path to HTML file")
    parser.add_argument("-o", "--output", help="Output PDF path (default: <name>.pdf)")
    parser.add_argument("--size", default="letter",
                        help="Page size: letter, letter-landscape, a4, a4-landscape, tabloid, legal, or WxH (default: letter)")
    parser.add_argument("--wait", type=int, default=1500, help="Extra ms to wait after fonts/network idle")
    parser.add_argument("--margin", default="0",
                        help="Page margin (CSS length, applies to all sides). Default 0 — rely on @page in the HTML.")
    parser.add_argument("--no-background", action="store_true",
                        help="Skip printing CSS backgrounds (Chromium default is to skip; this flag keeps that). By default this script prints backgrounds.")
    args = parser.parse_args()

    html_path = Path(args.html).resolve()
    if not html_path.exists():
        sys.exit(f"HTML file not found: {html_path}")

    output = Path(args.output).resolve() if args.output else html_path.with_suffix(".pdf")

    try:
        width, height = parse_size(args.size)
    except ValueError as e:
        sys.exit(str(e))

    ensure_playwright()
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file://{html_path}")
        page.wait_for_load_state("networkidle")
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(args.wait)
        page.emulate_media(media="print")
        page.pdf(
            path=str(output),
            width=width,
            height=height,
            margin={"top": args.margin, "right": args.margin, "bottom": args.margin, "left": args.margin},
            print_background=not args.no_background,
            prefer_css_page_size=True,
        )
        browser.close()

    kb = output.stat().st_size // 1024
    print(f"Saved: {output}  ({kb:,} KB)")
    report_links(output)


if __name__ == "__main__":
    main()
