# Logo usage — generated social & article images

## Files

- **`logo-primary.png`** — Primary lockup (wordmark + icon if applicable), transparent PNG.
- **`logo-mark.png`** — Square icon / avatar-style mark only (use when the hero is busy or space is tight).

Replace placeholders with your real exports; do **not** hotlink URLs (e.g. LinkedIn `media.licdn.com`) in API calls—**download** the asset once, optimize, commit or sync to the server under `brand-images/`.

### No “text as logo”

Image models often spell **QuizFactor** (or your name) in a **font** in the corner. **That is not your logo** if you have **`logo-*.png`**. **`auto-image-generation`** expects **pixel-accurate** marks: **composite** the PNG after generation or pass it as a **reference image**—never accept styled text as a substitute unless this file says **typeset-only** is allowed and no PNG exists yet.

## Placement on AI-generated heroes (default)

| Rule | Value |
|------|--------|
| **Position** | **Top-left** corner of the final raster (feed post, article hero, teaser). |
| **Inset** | **~2.5–4%** of canvas width from top and left edges (not flush to the frame). |
| **Width** | **~8–14%** of total image width for **logo-primary**; **~6–10%** for **logo-mark**. |
| **Aspect ratio** | **Never** stretch or squish; scale uniformly. |
| **Background** | Prefer **unobstructed** corner: reserve a calm navy (or solid) patch so the mark stays readable; illustration must **not** run through the logo. |
| **Effects** | **No** redraw, **no** “AI interpretation” of the logo. Optional **subtle** shadow only if brand allows. |

## Campaign overrides

If **`visual-dna.md`** or creative brief specifies another corner or bottom placement, follow that file for **that campaign only**; otherwise use **top-left** above.

## Clear space

Maintain at least **0.5× logo height** clear space around the mark (no competing line art or high-contrast clutter touching the bounding box).
