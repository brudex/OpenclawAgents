# Logo usage — generated social & article images

## Files

- **`logo-primary.png`** — Primary lockup (wordmark + icon if applicable), **32-bit PNG with alpha** (transparent pixels where there is no artwork—**no** full-bleed square “card” behind the mark unless intentionally part of the design).
- **`logo-mark.png`** — Square **icon** asset; same rule: **real transparency** so the **hero navy** shows through—**not** a lighter navy JPEG/PNG rectangle.

**Export checks:** In Figma/Illustrator/Photoshop, export **PNG**, enable **transparency**, delete any background layer. **Never** use **JPEG** for marks. If the file is a **flat square** with a fill behind the circle/mark, strip that fill or crop to the circle—otherwise composites will always show a **visible box** on generated images.

Replace placeholders with your real exports; do **not** hotlink URLs (e.g. LinkedIn `media.licdn.com`) in API calls—**download** the asset once, **fix alpha** if needed, sync to the server under `brand-images/`.

### No “text as logo”

Image models often spell **QuizFactor** (or your name) in a **font** in the corner. **That is not your logo** if you have **`logo-*.png`**. **`auto-image-generation`** expects **pixel-accurate** marks: **composite** the PNG after generation or pass it as a **reference image**—never accept styled text as a substitute unless this file says **typeset-only** is allowed and no PNG exists yet.

## Placement on AI-generated heroes (default)

| Rule | Value |
|------|--------|
| **Position** | **Top-left** corner of the final raster (feed post, article hero, teaser). |
| **Inset** | **~2.5–4%** of canvas width from top and left edges (not flush to the frame). |
| **Width** | **~8–14%** of total image width for **logo-primary**; **~6–10%** for **logo-mark**. |
| **Aspect ratio** | **Never** stretch or squish; scale uniformly. |
| **Background** | The **illustration** can reserve a calm corner so the mark reads; the **logo file itself** must **not** introduce a second rectangle of different navy—only **alpha** + artwork. |
| **Effects** | **No** redraw, **no** “AI interpretation” of the logo. Optional **subtle** shadow only if brand allows. |

## Campaign overrides

If **`visual-dna.md`** or creative brief specifies another corner or bottom placement, follow that file for **that campaign only**; otherwise use **top-left** above.

## Clear space

Maintain at least **0.5× logo height** clear space around the mark (no competing line art or high-contrast clutter touching the bounding box).

## Compositing (preserve alpha)

Final delivery should be **PNG** (or another format that keeps transparency for upload if your pipeline allows). Overlay the mark so the **source alpha** is respected—for example ImageMagick:

`magick generated-hero.png logo-mark.png -geometry +X+Y -compose over -composite post-image.png`

Replace **`+X+Y`** with inset pixels from **`logo-usage.md`**. If the composite still shows a box, the problem is almost always **opaque pixels in `logo-mark.png`**—fix the file, not the hero.
