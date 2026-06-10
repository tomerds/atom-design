---
name: og-tile
description: Build Atom Grants Open Graph (OG) social-share images at 1200×630 for three deliverable families — downloadable resources, webinars, and blog posts. Trigger when the user asks for "OG image", "og card", "social tile", "share image", "Twitter card", or wants a thumbnail for a resource on atomgrants.com/resources, a webinar on atomgrants.com/webinars, or a blog post on atomgrants.com/blog. Encodes layout, copy treatment, headshot sourcing & grayscale workflow so output stays consistent across runs and conversations.
---

# Atom Grants OG Tiles

Three layouts, same brand system. **Resource** tiles (downloadable resources), **Webinar** tiles (event share cards), and **Blog** tiles (article share cards) all render at **1200 × 630 px** (OG standard — aspect ratio 40/21 ≈ 1.905, which matches the card frame on atomgrants.com exactly, so no content is cropped on the website). Exported via the `html-screenshot` skill at 2× retina (final image: 2400 × 1260).

## When to use which

- **Resource OG** — downloadable assets from `atomgrants.com/resources` (playbooks, guides, templates, calculators, brochures). Single hero title, no people.
- **Webinar OG** — events from `atomgrants.com/webinars` (upcoming or past). Title + subtitle + grayscale presenter portraits.
- **Blog OG** — articles from `atomgrants.com/blog`. Two variants: **featured** (external interviewee/guest writer — bottom collab strip with grayscale headshot) and **general** (Atom-authored — title only, no footer).

## Shared brand system (must match in all three)

| Token | Value |
|---|---|
| Accent | `#ff4227` (the only brand color — no gradients, no secondary red) |
| **Tile background** | **`#F9FAFB`** (cool light gray — applied to all three families; page background stays `#ffffff`) |
| Text | `#000000`, secondary `#333`, tertiary `#666` |
| Title font | Cal Sans (loaded from `https://fonts.cdnfonts.com/css/cal-sans`) — always set `font-weight: 400` on `.title`; `<h1>` has a browser default of `font-weight: bold` which causes synthetic bolding on top of Cal Sans |
| Body font | DM Sans 400/500/600/700 (Google Fonts) |
| Logo | `../assets/newredlogowordmarkhighres.png` (height: 44–52px in tiles) |
| **Tile padding** | **`64px 144px`** (universal — matches the website card padding) |
| Headshot frame | Square + `border-radius: 18px` + grayscale + `box-shadow: 0 0 0 1px rgba(0,0,0,0.04)` (the inset shadow keeps the avatar legible against the gray tile bg) |

Wrap in a `:root` CSS-variables block so all three layouts share tokens (`--accent`, `--tile-bg`, `--text`, `--gray-light`, `--font-title`, `--font-body`). Always set `width: 1200px; height: 630px;` on the `.tile` element so the screenshot crop is exact.

The `#F9FAFB` tile-on-white treatment matches how cards appear on the live atomgrants.com pages — keeps the tiles visually unified across the three families and consistent with the website chrome. The website card frame matches the 1200 × 630 (40/21) OG aspect, so the full canvas is visible on-site within the universal `64px 144px` safe padding.

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
```

Key rules:
- Padding: `64px 144px` (the universal tile padding). Title sits in `.tile-body` with `margin-top: auto` so it anchors to bottom-left.
- **One word in the title is highlighted in `#ff4227`** — usually the most distinctive noun (e.g. "Library", "Newsletter", "AI-Readiness"). Wrap in `<span class="accent">…</span>`.
- **No subtitle, no description.** Title only — meant to be readable in a small social preview.
- Category pill top-right: outlined `#ff4227`, uppercase 16px DM Sans 600, letter-spacing `0.18em`, padding `10px 20px`, border-radius `999px`.
- Use size variants `.title.sm` (76px) and `.title.xs` (64px) for longer titles to keep them on 2–3 lines.
- **No bottom bar.** The tile ends flush; the accent word in the title is the only color hit besides the logo and category pill.

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
- Padding: `64px 144px`. Three-row grid: header / title (1fr, vertically centered) / presenter footer. The Webinar listing page on atomgrants.com doesn't crop OG images to 4:3, so the wider content band is fine here.
- Header right side: small `#ff4227` dot + `WEBINAR` (accent) + `·` separator + date (e.g. `MAY 19, 2026`). All uppercase, DM Sans 700, 18px, letter-spacing `0.18em`. **No pill** — that's the resource tile's treatment.
- **Subtitle is required** (event tagline). Gray `#666`, DM Sans 500, 22px.
- Presenter row sits above a 1px `#d9d9d9` top border. 24px top padding inside the border.
- Presenter avatars: square with **`border-radius: 18px`** (not circles), 96 × 96px. `background-size: cover; background-position: center top` so the face anchors high.
- Presenter name: Cal Sans 600 22px, role: DM Sans 400 14px gray, org: DM Sans 600 14px black (use `<span class="org">` to bold the affiliation).
- **No bottom accent bar.** None of the tile families carry one anymore (see "Don't" section).

### Speaker count variants

| Speakers | Class on `.presenters` | Avatar size | Notes |
|---|---|---|---|
| 1 | `.presenters` (single column) | 96 × 96 | Use `grid-template-columns: 1fr` override; pad title space |
| 2 | `.presenters` (default) | 96 × 96 | 2-column grid, 32px gap |
| 3 | `.presenters.three` | 78 × 78 | 3-column grid, 22px gap, smaller avatar + name (18px) + role (12px) |
| 4+ | use `.three` and shrink further or stack as 2×2 grid | — | Rare — only seen on past panel webinars |

Reference implementation: `Webinar_Tiles/Webinar_Tiles.html`.

### YouTube version — ALWAYS generate alongside the webinar OG

**Rule: every webinar tile ships in two sizes.** Whenever you create or update a webinar OG tile (1200 × 630), you must also produce a **YouTube** version of the same webinar. Webinars become recordings, and the recording's thumbnail needs the 16:9 frame. Never hand off a webinar OG without its YouTube twin.

- **Dimensions:** `1280 × 720` (16:9 — the YouTube thumbnail standard). Render at 2× → `2560 × 1440`.
- **Same everything else:** identical copy, date tag, accent split, speakers, and grayscale square-rounded headshots. Only the frame ratio and the type/spacing scale change (the OG is wider; 16:9 is taller, so the layout breathes into the extra height and the title grows for small-thumbnail legibility).

**Canonical method — a `.yt` twin in the master file.** For each `#tile-NN` add a sibling `<section class="tile yt" id="tile-NN-yt">` with the *same inner markup*, then render it to `tile_NN_yt@2x.png`. The `.tile.yt` modifier overrides only dimensions, padding, and scale:

> **Note:** all deliverable folders (`Webinar_Tiles/`, etc.) are gitignored — deliverables stay local. So **this skill is the source of truth**, not any local HTML. When you open or recreate `Webinar_Tiles.html`, paste the `.tile.yt` block below into its `<style>` if it isn't already there.

| Element | OG (1200×630) | YouTube (`.yt`, 1280×720) |
|---|---|---|
| `.tile` | `padding: 64px 144px; gap: 28px` | `padding: 72px 128px; gap: 32px` |
| `.logo` | 44px | 52px |
| `.date-tag` / dot | 18px / 10px | 20px / 11px |
| `.title` (default / `.sm` / `.xs`) | 78 / 66 / 56px | 96 / 80 / 68px |
| `.subtitle` | 22px | 26px |
| `.avatar` (2-up) | 96px, radius 18 | 110px, radius 20 |
| `.presenter-name` / `.role` | 22 / 14px | 26 / 16px |
| `.avatar` (`.three`) | 78px | 92px, radius 16 |
| `.three` name / role | 18 / 12px | 21 / 14px |

Paste-ready block (drop into the webinar master file's `<style>`):

```css
/* ── YouTube twin: 1280×720 (16:9). Same copy/speakers/accent as the OG;
   only frame + scale change. Duplicate a tile as <section class="tile yt"
   id="tile-NN-yt"> and render to tile_NN_yt@2x.png. ── */
.tile.yt { width: 1280px; height: 720px; gap: 32px; padding: 72px 128px; }
.tile.yt .logo { height: 52px; }
.tile.yt .date-tag { font-size: 20px; }
.tile.yt .date-tag::before { width: 11px; height: 11px; }
.tile.yt .title { font-size: 96px; margin-bottom: 22px; }
.tile.yt .title.sm { font-size: 80px; }
.tile.yt .title.xs { font-size: 68px; }
.tile.yt .subtitle { font-size: 26px; }
.tile.yt .presenters { gap: 36px; padding-top: 28px; }
.tile.yt .presenter { grid-template-columns: 110px 1fr; gap: 20px; }
.tile.yt .avatar { width: 110px; height: 110px; border-radius: 20px; }
.tile.yt .presenter-name { font-size: 26px; }
.tile.yt .presenter-role { font-size: 16px; }
.tile.yt .presenters.three .presenter { grid-template-columns: 92px 1fr; gap: 16px; }
.tile.yt .presenters.three .avatar { width: 92px; height: 92px; border-radius: 16px; }
.tile.yt .presenters.three .presenter-name { font-size: 21px; }
.tile.yt .presenters.three .presenter-role { font-size: 14px; }
```

```bash
# render both sizes of the same webinar
python3 .claude/skills/html-screenshot/shoot.py Webinar_Tiles/Webinar_Tiles.html --selector "#tile-NN"    -o Webinar_Tiles/tile_NN@2x.png
python3 .claude/skills/html-screenshot/shoot.py Webinar_Tiles/Webinar_Tiles.html --selector "#tile-NN-yt" -o Webinar_Tiles/tile_NN_yt@2x.png
```

For a standalone, hand-off-ready deliverable (its own folder with copied speaker crops), see the reference implementation `BuildingTrust_YouTube/` — same spec, written as one self-contained file.

## Layout 3 — Blog OG

Two variants share the same shell and header signature. Pick **featured** when the post has an external interviewee or guest writer; **general** otherwise.

### Shared shell (both variants)

```
┌─────────────────────────────────────────────┐
│  [LOGO]                  ● BLOG · DATE      │  ← header row
│                                             │
│                                             │
│  Title Line One                             │  ← Cal Sans 88px (sm 76, xs 64)
│  Title Line Two (accent)                    │     anchored above the footer
│                                             │
│  ─ footer (variant-specific) ─              │
└─────────────────────────────────────────────┘
```

Key shell rules:
- **Tile background:** `#F9FAFB` (universal — shared with resource & webinar tiles). Page background stays white; the cool light gray fills the 1200×630 card.
- **Padding:** `64px 144px`. The Blog listing page doesn't crop OG images to 4:3, so no safe-zone constraint applies here.
- **Header right side:** small `#ff4227` dot + `BLOG` (accent) + `·` separator + uppercase date (`APR 22, 2026` — month abbreviated to 3 letters, no leading zero on day). Same DM Sans 700 18px / `0.18em` tracking as webinar tiles. Reuse the `.date-tag` pattern.
- **Title split:** find the word boundary closest to the character midpoint; first half stays black on line 1, second half goes to accent on line 2. For 1-word titles, accent the whole word; for 2-word titles, accent the second word.
- **Size variants** (length-based):
  - Featured: 88px default, `.sm` (76px) if `len > 20`, `.xs` (64px) if `len > 28`.
  - General: 88px default, `.sm` (76px) if `len > 22`, `.xs` (64px) if `len > 32`.
- **No subtitle** — title only, like resource tiles. The only thing that can sit under the headline is the featured variant's collab strip; the general variant is title-only.

### Featured variant

```
│  ─────────────────────────────────────────  │  ← 1px gray divider
│  [▢] IN COLLABORATION WITH                  │  ← collab strip
│      Person Name                            │     square rounded headshot (96px)
│      Role, Organization                     │
└─────────────────────────────────────────────┘
```

- Bottom collab strip sits above a `1px #d9d9d9` top border, 22px top padding.
- 96 × 96 grayscale **square with `border-radius: 18px`** headshot — same crop/grayscale rules as webinar speakers (`object-fit: cover; object-position: center 18%` for portrait sources, plus an inset shadow `0 0 0 1px rgba(0,0,0,0.04)` since the headshot sits on the gray tile).
- Eyebrow: `IN COLLABORATION WITH` — DM Sans 700, 13px, `0.22em` tracking, `#666`.
- Name: Cal Sans 600 26px black. Role/org line: DM Sans 500 16px gray with `<span class="org">` wrapping the organization in black 600.
- **Collab strip is the only footer.** No accent bar under it.

### General variant

```
│                                             │
│  (title-only — no footer, no bar)           │
└─────────────────────────────────────────────┘
```

- No collab strip, no bottom bar. Title block uses `align-self: end;` so the headline sits anchored near the bottom of the tile padding, with the lower half of the card empty for breathing room.
- The accent word in the title is the only color hit besides the header eyebrow and logo.

### Workflow — fetching blog metadata + featured headshots

Atom Grants blog pages embed their content in Next.js RSC chunks (`self.__next_f.push([N, "..."])`). The reference parser is `/tmp/parse_blog.py` in this repo's working set, but the algorithm is:

1. **Slug list** — fetch `atomgrants.com/blog` with a Chrome UA and grep `/blog/<slug>` from the raw HTML. Drop strict-prefix truncations (e.g. `research-grant-finder-acad` when `research-grant-finder-academic-...` is also present).
2. **Per-post page** — fetch `atomgrants.com/blog/<slug>` and:
   - Title: `<h1>...</h1>` or `"h1"…"children":"..."` in the decoded chunks.
   - Date: `<p class="text-center">Mon DD, YYYY</p>` above the title.
3. **Featured detection** — scan markdown image references at `https://api.atomgrants.com/storage/v1/object/public/app/...`. Two alt-text patterns mark a featured author:
   - `![A Picture of <Name>](url)`
   - `![*This article was written by <Name>.*](url)`
   Skip if the name matches the Atom Grants in-house roster (`raphaël/raphael bernier`, `tomer dicturel`, `matteus pan`, `brian evans`, `mathilde bernier`).
4. **Bio extraction** — try in order:
   - Bold-name block: `**<FirstToken>...**\n<bio line>` (allow up to 40 trailing chars to absorb credentials like `, M.Ed., CRA`).
   - Prose: `<FirstToken> is the/a <role> at <org>.`
   - Trim trailing relative clauses with `re.split(r'\s+(?:who|which|that|where|whose)\s+', first, maxsplit=1)[0]` so bios like "...at Northwestern University who specializes in..." don't pollute the org.
5. **Mojibake** — RSC chunks ship as Latin-1-mis-decoded UTF-8. Round-trip with `s.encode('latin-1').decode('utf-8')` and `codecs.decode(body, 'unicode_escape')` on the chunk body.

For headshot crops, **prefer the post's own `api.atomgrants.com/storage/...` URL** — the blog already hosts the right image. Apply the same grayscale + square crop as webinar speakers (see "Grayscale + crop to square" below). For banner-style sources (wide composite images, e.g. Cristina Flowerday's 6868×970 banner), find the dark-pixel centroid in the left third and crop a square around it rather than centering naively.

Reference implementation: `Blog_Tiles/Blog_Tiles.html` (67 tiles).

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

**Then render the YouTube twin** (required — see "YouTube version" above): add a `<section class="tile yt" id="tile-NN-yt">` with the same inner markup and screenshot it to `Webinar_Tiles/tile_NN_yt@2x.png` (2560 × 1440 = 1280 × 720 at 2×).

## File layout

```
Resource_Tiles/
├── Resource_Tiles.html         ← all tiles in one file, one <section class="tile" id="tile-NN">
├── tile_01@2x.png … tile_NN@2x.png
Webinar_Tiles/
├── Webinar_Tiles.html         ← each webinar = an OG `#tile-NN` + a YouTube `#tile-NN-yt` twin
├── <speaker>_gray.jpg          ← grayscale square portraits, one per unique speaker
├── tile_01@2x.png … tile_NN@2x.png       ← OG 1200×630 (@2x)
├── tile_01_yt@2x.png … tile_NN_yt@2x.png ← YouTube 1280×720 (@2x), one per webinar
```

Keep one master HTML per family — easier to keep typography and spacing consistent than separate files per tile.

## Don't

- Don't add gradients, drop shadows on type, secondary colors, or off-brand fonts.
- **Don't let `<h1>` bold-synthesize Cal Sans.** Always set `font-weight: 400` on `.title` — browsers default `<h1>` to `font-weight: bold`, which renders Cal Sans heavier than intended.
- Don't add descriptions/subtitles to **resource** tiles. Title only.
- Don't use circular avatars in webinar tiles (resource tiles don't have avatars at all). Square + 18px radius is the signature.
- **Don't add a bottom accent bar to any tile.** The 10px `#ff4227` bottom-bar treatment is retired across all three families — resources, blogs, webinars. The accent word in the title (and the category pill / blog eyebrow / collab strip where applicable) is the only color load.
- Don't use full-color speaker photos. Always grayscale — keeps the speaker row visually unified across webinars even when source photos vary in lighting/background.
- Don't invent a category for resources or a date format for webinars without checking the source page.
