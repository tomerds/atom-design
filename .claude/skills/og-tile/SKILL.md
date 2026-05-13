---
name: og-tile
description: Build Atom Grants Open Graph (OG) social-share images at 1200×630 for two deliverable families — downloadable resources and webinars. Trigger when the user asks for "OG image", "og card", "social tile", "share image", "Twitter card", or wants a thumbnail for a resource on atomgrants.com/resources or a webinar on atomgrants.com/webinars. Encodes layout, copy treatment, headshot sourcing & grayscale workflow so output stays consistent across runs and conversations.
---

# Atom Grants OG Tiles

Two layouts, same brand system. **Resource** tiles (downloadable resources) and **Webinar** tiles (event share cards) both render at **1200 × 630 px** (OG standard) on white, exported via the `html-screenshot` skill at 2× retina.

## When to use which

- **Resource OG** — downloadable assets from `atomgrants.com/resources` (playbooks, guides, templates, calculators, brochures). Single hero title, no people.
- **Webinar OG** — events from `atomgrants.com/webinars` (upcoming or past). Title + grayscale presenter portraits.

## Shared brand system (must match in both)

| Token | Value |
|---|---|
| Accent | `#ff4227` (the only brand color — no gradients, no secondary red) |
| Background | `#ffffff` |
| Text | `#000000`, secondary `#333`, tertiary `#666` |
| Title font | Cal Sans (loaded from `https://fonts.cdnfonts.com/css/cal-sans`) |
| Body font | DM Sans 400/500/600/700 (Google Fonts) |
| Logo | `../assets/newredlogowordmarkhighres.png` (height: 44–52px in tiles) |
| Bottom accent bar | 10px solid `#ff4227`, full-width — **resource tiles only** |

Wrap in a `:root` CSS-variables block so both layouts share tokens. Always set `width: 1200px; height: 630px;` on the `.tile` element so the screenshot crop is exact.

## Layout 1 — Resource OG

```
┌─────────────────────────────────────────────┐
│  [LOGO]                       [CATEGORY]    │  ← header row
│                                             │
│                                             │
│                                             │
│  Title Word One                             │  ← Cal Sans 88px (sm 76, xs 64)
│  Title Word Two (accent)                    │     bottom-left, hero treatment
│                                             │
└─────────────────────────────────────────────┘
  ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔   ← 10px accent bar
```

Key rules:
- Padding: `64px 72px`. Title sits in `.tile-body` with `margin-top: auto` so it anchors to bottom-left.
- **One word in the title is highlighted in `#ff4227`** — usually the most distinctive noun (e.g. "Library", "Newsletter", "AI-Readiness"). Wrap in `<span class="accent">…</span>`.
- **No subtitle, no description.** Title only — meant to be readable in a small social preview.
- Category pill top-right: outlined `#ff4227`, uppercase 16px DM Sans 600, letter-spacing `0.18em`, padding `10px 20px`, border-radius `999px`.
- Use size variants `.title.sm` (76px) and `.title.xs` (64px) for longer titles to keep them on 2–3 lines.
- The 10px accent bar at the bottom is the visual signature of resource tiles.

Reference implementation: `Resource_Tiles/Resource_Tiles.html` (12 tiles, all variants).

## Layout 2 — Webinar OG

```
┌─────────────────────────────────────────────┐
│  [LOGO]                  ● WEBINAR · DATE   │  ← header row
│                                             │
│  Title Line One                             │  ← Cal Sans 78px (sm 66, xs 56)
│  Title Line Two (accent)                    │     middle, anchored vertically
│  Subtitle line in gray                      │  ← DM Sans 500 22px gray
│                                             │
│  ─────────────────────────────────────────  │  ← 1px gray divider
│  [▢] Name 1       [▢] Name 2                │  ← presenter row
│       Role             Role                 │     square rounded photos
│       Org              Org                  │
└─────────────────────────────────────────────┘
```

Key rules:
- Padding: `56px 64px`. Three-row grid: header / title (1fr, vertically centered) / presenter footer.
- Header right side: small `#ff4227` dot + `WEBINAR` (accent) + `·` separator + date (e.g. `MAY 19, 2026`). All uppercase, DM Sans 700, 18px, letter-spacing `0.18em`. **No pill** — that's the resource tile's treatment.
- **Subtitle is required** (event tagline). Gray `#666`, DM Sans 500, 22px.
- Presenter row sits above a 1px `#d9d9d9` top border. 24px top padding inside the border.
- Presenter avatars: square with **`border-radius: 18px`** (not circles), 96 × 96px. `background-size: cover; background-position: center top` so the face anchors high.
- Presenter name: Cal Sans 600 22px, role: DM Sans 400 14px gray, org: DM Sans 600 14px black (use `<span class="org">` to bold the affiliation).
- **No bottom accent bar** on webinar tiles (that's resource-only).

### Speaker count variants

| Speakers | Class on `.presenters` | Avatar size | Notes |
|---|---|---|---|
| 1 | `.presenters` (single column) | 96 × 96 | Use `grid-template-columns: 1fr` override; pad title space |
| 2 | `.presenters` (default) | 96 × 96 | 2-column grid, 32px gap |
| 3 | `.presenters.three` | 78 × 78 | 3-column grid, 22px gap, smaller avatar + name (18px) + role (12px) |
| 4+ | use `.three` and shrink further or stack as 2×2 grid | — | Rare — only seen on past panel webinars |

Reference implementation: `Webinar_Tiles/Webinar_Tiles.html`.

## Workflow — building a webinar tile end-to-end

This is the trickier of the two. Resources are pure layout work; webinars need speaker-headshot sourcing. Follow the order below.

### 1. Get the webinar metadata

Fetch the detail page on `atomgrants.com/webinars/<slug>` and extract:
- Full title + subtitle/tagline
- Date (format header as `MONTH DD, YYYY`, e.g. `MAY 19, 2026`)
- Every speaker's full name, title, and affiliation

```bash
# Example via WebFetch (in Claude); for shell, just visit the URL.
```

### 2. Find each speaker's headshot

Try sources in this order — stop at the first that yields a clean front-facing portrait:

1. **Institution bio page** (best). Search `"<full name>" <institution> <role> headshot` — university and company sites usually expose 200–400px JPEGs at predictable paths (`/images/people/<slug>.jpg`, `/about/leadership/<slug>.jpg`).
2. **LinkedIn profile photo**. Use the public profile-displayphoto URL pattern: `https://media.licdn.com/dms/image/v2/.../profile-displayphoto-scale_200_200/...`. The user can paste this from a LinkedIn profile if Claude can't reach it directly.
3. **Conference / news article photo** featuring the person.
4. **Existing Atom Grants composite** (`hyawonmbxjlliwyracul.supabase.co/storage/v1/object/public/app/<webinar-slug>-*.png`). Last resort — small embedded faces, low quality.
5. **Ask the user** for a direct image URL or local file path. Faster than chasing dead ends.

**Many institution sites (especially `*.okstate.edu`, `*.mtech.edu`) sit behind Cloudflare** and reject `curl`/`WebFetch` with 403 or a JS challenge. Use Playwright with a real UA and a parent-page warm-up to bypass:

```python
from playwright.sync_api import sync_playwright
from PIL import Image, ImageOps

UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 ' \
     '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

def fetch_image(image_url, parent_url, out_path):
    with sync_playwright() as p:
        b = p.chromium.launch()
        ctx = b.new_context(user_agent=UA)
        page = ctx.new_page()
        page.goto(parent_url, wait_until='domcontentloaded', timeout=30000)  # warm CF
        resp = page.goto(image_url, wait_until='domcontentloaded', timeout=30000)
        with open(out_path, 'wb') as f:
            f.write(resp.body())
        b.close()
```

To find image URLs on a Cloudflare-blocked page, also use Playwright:

```python
page.goto(bio_page_url, wait_until='domcontentloaded')
srcs = page.eval_on_selector_all('img', 'els => els.map(e => e.currentSrc || e.src)')
# filter for likely-headshot URLs (matches name slug, /people/, /headshot/, etc.)
```

### 3. Grayscale + crop to square

Every webinar headshot is a center-cropped square, grayscale, anchored slightly above center to keep the face high. Use this helper:

```python
from PIL import Image, ImageOps

def to_square_gray(src, dst):
    img = Image.open(src)
    w, h = img.size
    s = min(w, h)
    left = (w - s) // 2
    top = max(0, (h - s) // 2 - int(0.05 * h))   # bias toward top for face framing
    img = img.crop((left, top, left + s, top + s))
    gs = ImageOps.grayscale(img).convert('RGB')
    gs.save(dst, quality=92)
```

Save as `Webinar_Tiles/<lastname>_gray.jpg`. 200–500px square is plenty — the OG card displays them at 96px.

If the source photo has a tilted/composite frame (e.g. polaroid mockup), prefer to source a different photo rather than try to de-rotate. If you must, rotate first with `Image.rotate(-angle, expand=True, fillcolor=(0,0,0))` and visually verify before cropping.

### 4. Render

Add a new `<section class="tile" id="tile-NN">` to `Webinar_Tiles/Webinar_Tiles.html` following the structure of existing tiles, then:

```bash
python3 .claude/skills/html-screenshot/shoot.py \
  Webinar_Tiles/Webinar_Tiles.html \
  --selector "#tile-NN" \
  -o Webinar_Tiles/tile_NN@2x.png
```

Output is 2400 × 1260 PNG (2× retina). The 1× equivalent is the OG-spec 1200 × 630.

## File layout

```
Resource_Tiles/
├── Resource_Tiles.html         ← all tiles in one file, one <section class="tile" id="tile-NN">
├── tile_01@2x.png … tile_NN@2x.png
Webinar_Tiles/
├── Webinar_Tiles.html
├── <speaker>_gray.jpg          ← grayscale square portraits, one per unique speaker
├── tile_01@2x.png … tile_NN@2x.png
```

Keep one master HTML per family — easier to keep typography and spacing consistent than separate files per tile.

## Don't

- Don't add gradients, drop shadows on type, secondary colors, or off-brand fonts.
- Don't add descriptions/subtitles to **resource** tiles. Title only.
- Don't use circular avatars in webinar tiles (resource tiles don't have avatars at all). Square + 18px radius is the signature.
- Don't add the bottom accent bar to webinar tiles. It's a resource-tile signal.
- Don't use full-color speaker photos. Always grayscale — keeps the speaker row visually unified across webinars even when source photos vary in lighting/background.
- Don't invent a category for resources or a date format for webinars without checking the source page.
