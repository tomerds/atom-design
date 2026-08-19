---
name: blog-graphics
description: Build Atom Grants inline blog feature graphics — the framed product-concept illustration cards embedded inside articles on atomgrants.com/blog (e.g. the "Introducing Projects" post). Trigger when the user asks to "make a blog graphic", "blog image", "blog illustration", "feature card for the blog", "turn this screenshot into a blog image", or wants a product-concept illustration (proposals pipeline, discovery feed, auto-built profile, collaborator flow, etc.) rendered in the house frame. NOT the same as OG/social share tiles — those are the `og-tile` skill.
---

# Atom Grants Blog Graphics

Inline **feature-illustration cards** that sit inside blog articles (not the social OG tile — that's `og-tile`). Each one is a small, idealized product mock (a pipeline, a feed, a profile being built) wrapped in the house **crosshair frame**, rendered to a 2× PNG and dropped into the post body. Reference article: `atomgrants.com/blog/introducing-projects`.

## Where it lives

- **Master file (source of truth):** `Atom3_Blog_Graphics/Atom3_Blog_Graphics.html`
- One file holds **all** frames as stacked `<section class="frame" id="frame-N">` blocks. Add a new graphic = add a new `#frame-N` section; you don't spin up a new HTML file per graphic.
- Rendered PNGs live beside it, named for the concept: `proposals_pipeline@2x.png`, `personalized_feed@2x.png`, `building_profile@2x.png`, etc.

## The frame (house style)

Every graphic uses the same shell so they read as one system:

- **Canvas:** `.frame` = **1200 × 860 px**, white background, `overflow:hidden`.
- **Outer outline:** `.outer` — 1px `#ebedf0` rounded rectangle inset 16px (barely-there page edge).
- **Crosshair frame:** `.xframe` — a thin **`#d1d5db`** rectangle offset around the centered card (`top:-54 bottom:66 left:-50 right:-30`), with **exactly two crosshair "+" marks on the diagonal — top-left and bottom-right only** (`.x.tr` and `.x.bl` are `display:none`). This two-crosshair treatment is the current standard; do not restore all four.
- **Card:** centered via `.center` (flex). The real content is a soft-card (white, `#e5e7eb` border, `border-radius:20px`, subtle shadow).
- **Font:** DM Sans only (loaded via Google Fonts). No Cal Sans in these graphics.
- **Accent:** `#ff4227`, applied as tinted chip/pill fills (`--r05/--r10/--r15`), the accent eyebrow/label, and score pills. Green `#10b981` is allowed only for verified/done checkmarks. Amber `#fbbf24` only for an "in review" status dot.

### Crosshair gotcha (important)

The crosshair corner classes are `tl/tr/bl/br`. **`.tl` collides with frame-2's timeline container class `.tl`** (which sets `margin-left`, `margin-top`, and a dashed `border-left`). Without a guard, those leak onto the top-left crosshair and shove it ~22px right / ~16px down and draw a stray dashed line. The guard that prevents this is already in place:

```css
.x{width:34px;height:34px;}
.xframe .x{position:absolute;margin:0;padding:0;border:0;}   /* resets the .tl leak */
.x.tl{left:-17px;top:-17px;}      /* -17 = half of 34, centers the box on the corner */
.x.br{right:-17px;bottom:-17px;}
```

Center each 34px crosshair box on the corner with **explicit `-17px` offsets**, not `transform: translate(-50%,-50%)` (the percentage transform collapsed to 0 in this context). If you add or rename frames, keep the `.xframe .x{margin:0;padding:0;border:0}` reset — it is what keeps the corners aligned.

## Existing frames (component library)

Reuse these before inventing new components; they share the tinted-chip / soft-row vocabulary.

| id | concept | reusable classes |
|----|---------|------------------|
| `#frame-1` | Discovery: researcher profile → match → "For You" feed (neuroinflammation) | `.disc*` |
| `#frame-2` | Finding collaborators: limited-submission stepped timeline | `.cl*`, `.tl*` |
| `#frame-3` | Proposals pipeline CRM (Drafting / In Review / Submitted kanban) | `.pp*` |
| `#frame-4` | Personalized feed (maternal-health variant of the discovery pattern) | `.disc*` |
| `#frame-5` | Build profile: public signals (dir/PubMed/ORCID/RePORTER) → auto-built researcher card | `.bp*` |

- The **discovery/feed** pattern (`.disc*`): profile-chips card → `&darr; Match` connector → feed rows with agency pill + title + accent `%` score. Swap the chips + rows for a new topic (that's all frame-4 is).
- The **profile** pattern (`.bp*`): source-check grid → `&darr; Building profile` connector → profile card with monogram avatar, topic tags, and a 3-up stat grid, plus a sparkle foot line.

## Copy + brand rules

- Plain, direct copy — no marketing voice (house register).
- **Avatars for demo people are grayscale square-rounded monograms** (e.g. "MP"), matching the timeline avatars (`.tl-av`) and the headshot rule in CLAUDE.md. Do not drop in a color face photo for a fictional persona.
- Never add the banned colored left-rule accent bar. Emphasis comes from the accent eyebrow, an accent word, chips, or score pills.
- Keep the two-crosshair frame and `#d1d5db` rectangle consistent across every frame.

## Turning a screenshot into a blog graphic

When the user hands over a raw product screenshot / mock:
1. Identify which existing pattern it maps to (feed, pipeline, profile, timeline). Reuse that frame's classes; only build new CSS for genuinely new components.
2. Reproduce the content faithfully, but in the house component vocabulary (tinted chips, soft rows, monogram avatars) — not a pixel-copy of raw product UI.
3. Add it as a new `#frame-N` section in the master file.

## Render

Each frame exports to a 2× PNG via the `html-screenshot` skill, scoped to the frame id:

```bash
python3 .claude/skills/html-screenshot/shoot.py \
  Atom3_Blog_Graphics/Atom3_Blog_Graphics.html \
  --selector "#frame-5" -o Atom3_Blog_Graphics/building_profile@2x.png
```

Output is 2400 × 1720 (1200 × 860 @ 2×). These are illustrations with no live links, so PNG (not vector PDF) is correct.

### Verifying crosshair alignment (optional)

Because the `.tl` collision is easy to reintroduce, alignment is measurable from the pixels — find the dark cross centroid vs. the grey rectangle corner; they should agree within ~1px:

```python
from PIL import Image; import numpy as np
im = np.asarray(Image.open('Atom3_Blog_Graphics/building_profile@2x.png').convert('RGB')).astype(int)
sub = im[150:430, 400:700]                      # top-left region (adjust per card size)
dark = (sub[:,:,0]<120)&(sub[:,:,1]<120)&(sub[:,:,2]<120)
ys,xs = np.where(dark)
grey = (abs(sub[:,:,0]-209)<18)&(abs(sub[:,:,1]-213)<18)&(abs(sub[:,:,2]-219)<18)
vx = int(np.argmax(grey.sum(axis=0)))+400; hy = int(np.argmax(grey.sum(axis=1)))+150
print('offset', (int(xs.mean())+400-vx, int(ys.mean())+150-hy))   # want ~(1,1)
```
