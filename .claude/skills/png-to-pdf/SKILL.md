---
name: png-to-pdf
description: Combine a sequence of page-sized PNGs into a single print-ready PDF at the correct physical dimensions (Letter, A4, custom). Trigger when the user asks for a "downloadable PDF", "PDF resource", "print-ready PDF", "combine images into PDF", "playbook PDF", or any time multi-page HTML has been rendered to PNGs that need to be stitched into a single deliverable.
---

# png-to-pdf

Stitch a set of page PNGs (typically produced by the `html-screenshot` skill) into one multi-page PDF sized for print.

## Prerequisites

```bash
pip3 install Pillow
```

Pillow ships with macOS Python, so usually nothing to install. No system dependencies.

## Usage

From the repository root:

```bash
python3 .claude/skills/png-to-pdf/merge.py <input PNGs...> -o <output.pdf> [flags]
```

Common flags:

| Flag | Default | Purpose |
|---|---|---|
| `-o, --output <path>` | required | Output PDF path |
| `--size <preset \| WxH>` | `letter` | `letter`, `letter-landscape`, `a4`, `a4-landscape`, `tabloid`, `legal`, or custom `WxH` in inches (e.g. `6x9`) |
| `--dpi <n>` | auto | Force a DPI. By default DPI is computed from image width / page width so each page sits at the target physical size. |
| `--title <str>` | none | PDF title metadata |
| `--author <str>` | none | PDF author metadata |
| `--no-sort` | off | Preserve argv order. Default sorts filenames alphabetically. |

## How DPI is chosen

The default assumes PNGs are rendered at a consistent retina scale against a fixed page size:

- Letter portrait at 2× = 1632 px wide → 192 DPI
- Letter portrait at 3× = 2448 px wide → 288 DPI
- A4 portrait at 2× = ~1654 px wide → ~200 DPI

Because the merge script computes DPI from `image_width / page_width_inches`, it "just works" as long as the PNGs were captured against the same logical page size.

## Examples

```bash
# Typical: Letter portrait playbook, 2x PNGs named page_01@2x.png ... page_09@2x.png
python3 .claude/skills/png-to-pdf/merge.py \
    Newsletter_Playbook/page_*@2x.png \
    -o Newsletter_Playbook/The_Playbook.pdf \
    --title "The AI-Powered Research Newsletter Playbook" \
    --author "Atom Grants"

# A4 portrait
python3 .claude/skills/png-to-pdf/merge.py \
    Report/page_*.png -o Report/Report.pdf --size a4

# Custom square format (e.g. 8x8 in) at 3x retina
python3 .claude/skills/png-to-pdf/merge.py \
    Lookbook/slide_*@3x.png -o Lookbook/Lookbook.pdf --size 8x8

# Tabloid landscape, with explicit DPI override
python3 .claude/skills/png-to-pdf/merge.py \
    Deck/slide_*.png -o Deck/Deck.pdf --size tabloid --dpi 150
```

## Typical pipeline

```bash
# 1) Build HTML with N numbered page sections (e.g. #page-1 ... #page-N)
# 2) Render each page to a 2x PNG
for i in 01 02 03 04 05 06 07 08 09; do
  python3 .claude/skills/html-screenshot/shoot.py Project/Project.html \
    --selector "#page-$i" -o Project/page_$i@2x.png
done

# 3) Merge into one PDF
python3 .claude/skills/png-to-pdf/merge.py \
    Project/page_*@2x.png -o Project/Project.pdf --title "Project"
```

## Notes

- Pages keep their true aspect ratio; if an image is shorter/taller than the target page size, it will still render at the correct width but with height proportional to the source (usually you want all pages rendered at the same size up front).
- Output is a standard image-backed PDF (each page is a full-page bitmap). This is perfect for print and reliable across viewers; it's not text-searchable. If you need selectable text, export the HTML to PDF directly (e.g. Chrome "Print to PDF") instead.
