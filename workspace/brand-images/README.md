# Brand images (QuizFactor / product visuals)

This folder is the **canonical brand kit** for **`auto-image-generation`**. The OpenClaw agent **reads files here** (names, palette, optional reference PNGs/SVGs) so generated social/article images **match your real product identity**—not a hallucinated logo.

## Deploy path (your server)

On the gateway host this often lives at:

` /home/admin/.openclaw/workspace/brand-images `

Point the agent at it with env **`BRAND_IMAGES_DIR`** (see **`workspace/INTEGRATIONS.md`**). In git clones, use **`workspace/brand-images/`** in the repo root and keep the same filenames so skills behave the same locally and on the server.

## What to place here

| File (recommended) | Purpose |
|--------------------|--------|
| **`logo-primary.png`** | Full logo on transparent background (primary asset for “include our logo” prompts / reference). |
| **`logo-mark.png`** | Icon / mark only (square-friendly). |
| **`palette.md`** | Hex codes + primary/secondary/accent + “never use”. |
| **`logo-usage.md`** | Clear space, min size, **default top-left placement** on generated heroes, light/dark backgrounds, **do / don’t** (e.g. no stretch, no recolor except approved mono). |
| **`product-context.md`** | Short **static** product one-liner (optional); *detailed* product truth still comes from **Drive** via **`marketer-agent`** / campaign **`00-intake.md`**. |

Optional: host-specific **`image-generation.ts`** or scripts—skills treat this directory as **read-only assets + text**; execution stays in OpenClaw/Gemini unless you wire a custom tool.

### Using a LinkedIn-hosted image as your mark

If your only source is a **LinkedIn profile or company photo** (`media.licdn.com/…`):

1. **Download** it once in the browser or with `curl`, save locally as **`logo-mark.png`** (square) or **`logo-primary.png`** (full lockup), **PNG with transparency** where possible.
2. **Do not** pass the **URL** into Gemini—APIs need **file bytes** or paths; remote URLs expire, resize, or block hotlinking.
3. **`auto-image-generation`** default: place the logo in the **top-left** with inset and max width per **`logo-usage.md`** (reference image + prompt, or composite after generation).

## How this ties to posts (not “logo in a vacuum”)

1. **Copy first:** `post-body.md` / `teaser.md` / `article.md` defines **what the scene is about**.  
2. **Product truth:** **`marketer-agent`** ingests **Google Drive** (`product-info-drive`) → strategy/briefs; social **`00-intake.md`** can link `workspace/drafts/marketing/.../00-brief.md` for the campaign.  
3. **Brand kit:** This folder supplies **which logo, which colors, usage rules**.  
4. **Gemini:** The **prompt** merges (2) + (3); if the host/API supports **reference images**, pass **`logo-primary.png`** (and similar) as **multimodal** input so the model aligns marks with your real asset—otherwise use **`palette.md` + `logo-usage.md`** verbatim in text.

**First post in a campaign:** Same rules—there is no special case. If Drive/brief is not ready yet, use **`product-context.md`** + post copy only until **`marketer-agent`** output exists; still always load **`brand-images/`**.
