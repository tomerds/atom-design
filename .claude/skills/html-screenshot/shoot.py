#!/usr/bin/env python3
"""
Render a local HTML file to a high-res PNG using headless Chromium.

Typical use: screenshot poster / deck / one-pager HTML deliverables at 2× or 3×
retina scale. Waits for web fonts to load before capturing.
"""
import argparse
import subprocess
import sys
from pathlib import Path


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


def main():
    parser = argparse.ArgumentParser(description="Screenshot an HTML file with headless Chromium.")
    parser.add_argument("html", help="Path to HTML file")
    parser.add_argument("-o", "--output", help="Output PNG path (default: <name>@<scale>x.png)")
    parser.add_argument("-s", "--scale", type=float, default=2.0, help="Device scale factor (default: 2)")
    parser.add_argument("--selector", default=".poster", help="CSS selector to capture (default: .poster)")
    parser.add_argument("--full-page", action="store_true", help="Capture entire page (overrides --selector)")
    parser.add_argument("--wait", type=int, default=1200, help="Extra ms to wait after fonts/network idle")
    args = parser.parse_args()

    ensure_playwright()
    from playwright.sync_api import sync_playwright

    html_path = Path(args.html).resolve()
    if not html_path.exists():
        sys.exit(f"HTML file not found: {html_path}")

    scale_str = f"{int(args.scale)}" if args.scale.is_integer() else str(args.scale).replace(".", "_")
    output = Path(args.output).resolve() if args.output else html_path.with_name(f"{html_path.stem}@{scale_str}x.png")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=args.scale,
        )
        page = ctx.new_page()
        page.goto(f"file://{html_path}")
        page.wait_for_load_state("networkidle")
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(args.wait)

        if args.full_page:
            dims = page.evaluate(
                "({w: document.documentElement.scrollWidth, h: document.documentElement.scrollHeight})"
            )
            page.set_viewport_size({"width": int(dims["w"]), "height": int(dims["h"])})
            page.wait_for_timeout(200)
            page.screenshot(path=str(output), full_page=True, type="png")
        else:
            locator = page.locator(args.selector)
            try:
                box = locator.bounding_box(timeout=3000)
            except Exception:
                box = None
            if box is None:
                sys.exit(
                    f"Selector '{args.selector}' not found. "
                    f"Try --full-page or pass a different --selector."
                )
            page.set_viewport_size(
                {"width": int(box["width"] + 100), "height": int(box["height"] + 100)}
            )
            page.wait_for_timeout(200)
            locator.screenshot(path=str(output), type="png")

        browser.close()

    kb = output.stat().st_size // 1024
    print(f"Saved: {output}  ({kb:,} KB)")


if __name__ == "__main__":
    main()
