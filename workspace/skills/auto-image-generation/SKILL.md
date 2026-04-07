---
name: auto-image-generation
description: Briefs + Gemini-rendered images using workspace brand-images/ (or BRAND_IMAGES_DIR) for QuizFactor/product logo & palette, merged with post copy and marketer/Drive context; copies to post-image.png / article-hero.png for HypeEngine.
metadata: {"clawdbot":{"emoji":"🖼️"},"openclaw":{"emoji":"🖼️"}}
---

# auto-image-generation

Deliver **designer-ready** image specs: not a single vague prompt, but **placement**, **ratio**, **prompt + negative**, **text overlay rules**, and **A/B variants**—equivalent detail to how `qf-course-researcher` specifies Notion property types (Select vs rich_text) so downstream work does not degrade.

## When Gemini is available (this workspace — default)

If **OpenClaw already has Gemini** (API key in **`~/.openclaw/.env`** / **`~/.config/gemini/api_key`** and/or host **`image_generate`** / equivalent tool), treat **pixel generation as the default outcome**, not optional:

1. Write the brief artifacts (`concept.md`, `prompt-master.txt`, etc.) as today.
2. **Then** call Gemini (**prefer host `image_generate` if exposed**; else **`generateContent`** with an image-capable model per [Gemini image docs](https://ai.google.dev/gemini-api/docs/image-generation)) and save **at least one** real file (e.g. **`generated-1.png`**) into the same draft folder.
3. Record model id, time, and output filenames in **`gemini-render.md`**.

Only skip the render step if the human explicitly asked **briefs only**, the tool/key is missing after checking, or the API refuses (document in `gemini-render.md`).

## Chaining from social posts & LinkedIn articles (canonical paths)

When **`social-media-manager`** (or a writer) asks for a **slot image**, use this workspace contract so bundles and **HypeEngine** always know where to look:

| Context | Where to save the **primary** raster | Notes |
|---------|--------------------------------------|--------|
| Social campaign slot | **`workspace/drafts/social/<campaign>/posts/<post-id>/post-image.png`** (or `.jpg`) | Still write full brief + `generated-*` under `workspace/drafts/images/<date>-<slug>/`, then **copy or symlink** the chosen asset to **`post-image.png`**. Add **`posts/<post-id>/image-alt.txt`** (one line, ≤125 chars) for accessibility / HypeEngine. |
| LinkedIn long-form article | **`workspace/drafts/linkedin/<date>-<slug>/article-hero.png`** (or `.jpg`) | Hero for the article body + intern handoff; reference in **`article.md`** (e.g. `![Hero](article-hero.png)` after title) and in **`README-handoff.md`**. |
| Teaser row (same article) | Reuse **`article-hero.png`** for the **feed** bundle when the calendar row points at the LinkedIn folder—**or** generate **`teaser-image.png`** in that folder if the teaser needs a distinct crop. |

**Inputs for the image run:** first line / hook from **`post-body.md`** or article **thesis + title**; **platform** from **`calendar.md`** (map to aspect ratio: X/LinkedIn feed often **1.91:1** or **1:1** per `social-content-planning` matrix).

## End-to-end flow (this workspace)

**Write post → generate image → attach → HypeEngine → schedule/publish.**

1. **`post-body.md` / `teaser.md` / `article.md`** exists first (copy is source of truth for *what* to illustrate).  
2. This skill produces **`post-image.png`** / **`article-hero.png`** + **`image-alt.txt`**.  
3. **`social-media-manager`** puts paths + alt into **`post-bundle.md`**; on publish, **`hype-engine`** **uploads** the file (Media API) and sets **`content[].media`** so the post is **not text-only**.  
4. HypeEngine: **one** POST `/posts` with **`date` + `time`** from **`APPROVAL.md`**—the product **schedules and publishes** at that time; **no extra “publish now”** step (see **`hype-engine`**).

## Brand kit (`brand-images/`) — QuizFactor logo & product look

Generated images must **match the product** and **use your real brand**, not a model-invented mark.

### Where the folder lives (resolve in this order)

1. Env **`BRAND_IMAGES_DIR`** (e.g. `/home/admin/.openclaw/workspace/brand-images` on the OpenClaw server).  
2. Else **`workspace/brand-images/`** relative to this workspace root (same filenames as on server).  
3. If neither exists or is empty: **stop** before claiming a branded image—write `gemini-render.md` with `BRAND_KIT_MISSING` and ask the human to add assets (see **`workspace/brand-images/README.md`**).

**On every run:** `list_dir` / read **`palette.md`**, **`logo-usage.md`**, **`product-context.md`** (if present), and note available rasters (`logo-primary.png`, `logo-mark.png`, …).

### How the QuizFactor / product logo gets into the image (not “magic prompt only”)

| Method | When to use |
|--------|-------------|
| **Reference image (preferred if host/API supports it)** | Pass **`logo-primary.png`** / **`logo-mark.png`** as **multimodal** input alongside text (e.g. `generateContent` with image `inline_data`, or OpenClaw tool that accepts reference images). Instruction: *“Composite or place this exact brand mark per logo-usage.md; match colors from palette.md.”* |
| **Text-only fallback** | If the pipeline cannot send bytes: paste **verbatim** hex + short **logo description** from **`palette.md`** + **`logo-usage.md`** into `prompt-master.txt`. State *“Official QuizFactor mark only—no generic quiz icons, no other wordmarks.”* |
| **Never** | Do not describe a logo from memory. Do not substitute a different product name or icon set. |

### Merging **post copy** + **product truth** + **brand kit**

Build the final generation brief in this order:

1. **Scene / story** from **`post-body.md`** (or article title + TL;DR)—this is what the **illustration is about**.  
2. **Product facts** (if available): path from campaign **`00-intake.md`** to **`marketer-agent`** outputs (`00-brief.md`, `02-positioning.md`) or **`USER.md`**—same source as the **content creator**; **Google Drive** (when used) is the long-form product source for **`marketer-agent`** / writers, **not** a substitute for renders. **`prompt-master.txt` always layers three things:** ***Style benchmark*** (canonical block in this skill), **`brand-images/`** (logo + palette), and **copy-derived subject**—Drive-backed docs only add **extra product truth** for `concept.md` / positioning lines, not “brand instead of benchmark.”  
3. **Brand lock** from **`brand-images/`**: colors, logo rules, placement.  
4. **`visual-dna.md`** (campaign) for illustration style across the batch.  
5. **Style benchmark** (*Canonical visual system* below): fold into **`prompt-master.txt`** on every run unless **`visual-dna.md`** explicitly replaces the illustration mode for that campaign.

**First post of a campaign:** identical pipeline. If **`marketer-agent`** has not run yet, use **post copy** + **`product-context.md`** + **`brand-images/`** + ***Style benchmark***; after marketing pack exists, prefer **`00-brief.md`** excerpts in `concept.md`.

### Optional host script

If you keep **`image-generation.ts`** (or similar) under `brand-images/` on the server, the **skill still treats this folder as the asset source**; wire execution through OpenClaw tools if you add a wrapper—the markdown workflow does not depend on TypeScript.

## Style benchmark (flat vector educational)

**Default illustration system** for social slots and LinkedIn article heroes: fixed **composition + vector grammar** below, merged with **`post-body.md`** / **`article.md`** so pixels match copy—not generic stock. **This block is not optional** when using the default pipeline: you use **both** the benchmark (hand/phone/couch/tablet/floating icons + vector look) **and** **`brand-images/`**—Drive-only marketing docs never replace them.

**Hard requirement for OpenClaw / any agent:** Updating this `SKILL.md` does **nothing** to the image API by itself. Whoever calls **`image_generate`** / Gemini **must read this skill** and **paste** the **STYLE LOCK** + **Canonical visual system** into the **actual** `prompt-master.txt` (or equivalent single string). Improvising “IT certification hero art” from post copy alone will drift to sci‑fi/anime/holographic stock—**that is a failure mode**, not an acceptable shortcut.

### STYLE LOCK — mandatory first lines (anti-drift)

**The first paragraph of every `prompt-master.txt`** (before the quoted canonical block) **must** be a short imperative block, verbatim in spirit—**do not skip** because the topic is “technical” or “IT certs”:

```text
STYLE LOCK — NON-NEGOTIABLE: Flat 2D vector illustration only (clean corporate editorial / app-marketing vector), like Figma or Illustrator flats — NOT anime, NOT manga, NOT cinematic digital painting, NOT semi-realistic character art, NOT 3D render. NO holographic or floating sci-fi UI, NO cyberpunk, NO server room or data center, NO futuristic city skyline, NO cyan/teal neon glow as the dominant look, NO “tech command center” or tactical jumpsuit characters. NO large hero faces in painterly style. REQUIRED COMPOSITION: hand holding smartphone in foreground with simple quiz/lesson UI; person relaxing on couch with tablet in mid-background; small floating minimalist line icons (books, brain-in-lightbulb, checkmark, graduation cap) plus 1–2 topic icons from the post copy. REQUIRED PALETTE unless brand kit overrides: deep navy background, bright yellow accents, white linework. The ONLY “tech” is the phone/tablet screens — flat UI mockups, not glowing Blade Runner panels.
```

Then immediately follow with the **Canonical visual system** quote below (tokens permitting). If the API has a length limit, **shorten the quote last**—never delete the **STYLE LOCK** paragraph.

### Canonical visual system (structure & style)

Use this block as the **stable backbone** of every `prompt-master.txt` (trim for token limits only; keep structure; **never trim the STYLE LOCK paragraph**):

> **Professional flat vector illustration** for an educational quiz / learning product. **Composition:** A **hand holding a smartphone** in the foreground; the phone screen shows a **quiz or lesson UI** with **multiple-choice-style buttons or clear lesson steps** (not illegible micro-text). In the **mid/background**, a person **relaxes on a couch** using a **tablet** that echoes the same learning theme. **Floating around the scene**, cute **minimalist** icons (same line weight): **open books**, **lightbulbs with simple brain shapes**, **checkmarks**, and a **graduation cap**—plus **one or two extra icons** tied to the **post/article topic** (see *Content from copy* below). **Default color scheme:** **deep navy blue** background, **bright yellow** accents, **white** linework and key highlights. **Quality:** clean, modern, **corporate educational** aesthetic, **high resolution**, **2D vector art** (not photorealistic), generous negative space, crisp edges.

### Content from copy (mandatory)

The benchmark is **not** a generic scene. **Derive scene meaning from the source document:**

| Source | Minimum extraction |
|--------|-------------------|
| Social **`post-body.md`** | First **hook line** + **must-win message** + any **named topic, course, or outcome** in the `## Publish-ready` block (or equivalent). |
| LinkedIn **`article.md`** | **Title** + **TL;DR** or lede + **first H2 theme** (or strongest concrete example in the opening sections). |

**On-screen text (phone / tablet):** Where the model can render short UI text, use a **paraphrase** of the hook or thesis (**≤8 words per line**, **≤3 lines** on the phone; **no lorem ipsum**). Examples: “Cut study time in half”, “CompTIA Security+ in 20 min/day”—tuned to **this** post. If the API cannot place text reliably, state in `text-overlay.md` and keep the **visual metaphor** (icons, scene) tightly aligned with the same nouns.

**Floating icons:** Keep the **benchmark set** (books, brain-lightbulb, checkmark, cap). **Add or emphasize** 1–2 motifs that mirror the copy (e.g. shield for security, cloud for cloud certs, chart for analytics).

**Anti-generic check:** If the image could apply to **any** edtech post without reading the copy, the prompt is **too weak**—inject specific nouns from the post into `prompt-master.txt`.

### Brand kit precedence (vs. benchmark defaults)

If **`brand-images/`** (or **`BRAND_IMAGES_DIR`**) has **`palette.md`** / **`logo-usage.md`**:

- **Logo** and **wordmark** rules always win (reference image or verbatim description per *Brand kit* above).
- **Colors:** Prefer **brand hex** for primary accents and logo surrounds; **preserve** the overall **flat vector + white linework** read unless the brand doc forbids white lines. **Navy + yellow** above is the **default only when** the brand kit does not specify alternatives.

### Negative prompt hints (benchmark-specific)

**Always** merge these into **`negative-prompt.txt`** (or the same user prompt string for APIs without a separate negative field) for default QuizFactor social/article runs—especially when post copy mentions **IT, AWS, security, coding, certifications**, which otherwise pull holographic/sci‑fi defaults:

`anime`, `manga`, `manhwa`, `cel shading`, `visual novel`, `cyberpunk`, `holographic interface`, `HUD`, `sci-fi control room`, `mission control room`, `server rack`, `data center`, `tactical suit`, `jumpsuit`, `futuristic city`, `skyline at night`, `neon cyan`, `electric blue glow`, `cinematic lighting`, `octane render`, `Unreal Engine`, `highly detailed face`, `semi-realistic portrait`, `digital painting`, `concept art`, `tech test evaluation`, `matrix code rain`, `Matrix-style`

Also as needed: photorealistic skin, wrong logo, unreadable tiny paragraphs, clutter competing with the phone hero, **celebrity likeness**, **watermarks**, **generic unrelated quiz topic** (if copy is about X, ban visual story about unrelated Y).

### Post-render visual QA (one retry)

After saving **`generated-1.png`**, **glance** at the output (or read a vision description). If you see **any** of: anime face, holographic/blue sci-fi UI as the main subject, server room, cyberpunk city, painterly detail skin, or **no smartphone-in-hand + couch + tablet** composition → **regenerate once** with the **STYLE LOCK** repeated twice (top + bottom of prompt) and **`negative-prompt.txt`** doubled; note **`REGENERATED_STYLE_DRIFT`** in **`gemini-render.md`**. Do **not** ship cyberpunk/holographic art as QuizFactor branded flats.

**Every run:**

1. Put the **STYLE LOCK** paragraph **first** in **`prompt-master.txt`**, then the **canonical visual system** block.
2. Apply **Content from copy**: phone/tablet hints and extra floating icons must reflect **specific** hooks, nouns, and outcomes from **`post-body.md`** / **`article.md`**.
3. **Then** apply **brand kit** (`palette.md`, `logo-usage.md`) so logo and colors stay compliant; brand colors **override** the benchmark default palette when they conflict; keep vector + white-linework **read** unless brand docs forbid it.
4. Merge benchmark **negative** list; run **Post-render visual QA** before copying to **`post-image.png`** / **`article-hero.png`**.

If a campaign **`visual-dna.md`** explicitly defines a **different** illustration mode, follow **`visual-dna.md`** for that campaign—but still tie subject matter to the same copy rules above.

## Aligning images with copy (style & quality)

Generic “nice illustration” prompts drift. For **every** social-slot run:

1. **Read the actual post text** — at minimum the **`## Publish-ready`** block (or article **title + TL;DR + first H2 theme**). The image must reflect **specific nouns, metaphors, or outcomes** in that copy—not an unrelated category stock scene. **Use *Style benchmark*** above for composition and vector grammar **while** injecting those specifics into **on-device UI hints** and **scene metaphors** (*Content from copy*).
2. **Campaign visual DNA (optional but recommended):** If **`workspace/drafts/social/<campaign>/visual-dna.md`** exists, **append** its locked lines to every `prompt-master.txt`. **Always merge after** the **brand kit** block from **`brand-images/`** (`palette.md` / `logo-usage.md`) so colors and logo rules are not contradicted. If `visual-dna.md` is missing, derive 3–5 **style rules** from **`USER.md`**, **`SOUL.md`**, and **`marketer-agent`** `03-messaging-pillars.md` / `00-brief.md` once per campaign and **reuse** them for all slots in that folder.
3. **Same model + ratio within a batch:** Use **one** image model id for all posts in the same **`calendar.md`** week unless the human asks otherwise; keep **`aspectRatio`** aligned to **`social-content-planning`** / calendar row so crops match HypeEngine/LinkedIn/X expectations.
4. **Prompt structure:** `prompt-master.txt` = **[style DNA] + [subject tied to post] + [composition] + [lighting] + [what to avoid]`. Fold **`negative-prompt.txt`** into the same generation call as today.
5. **Quality bar (words in prompt):** e.g. *sharp focus, clean edges, professional marketing asset, no watermark, no clutter*—adjust to brand; avoid vague “high quality” alone.
6. **Alt text = alignment check:** **`image-alt.txt`** must describe **what’s in the image** and **why it fits the post** in one line; if you can’t write that, the image probably doesn’t match—regenerate with a tighter prompt.
7. **Optional spot-check:** When generating slot N, skim **`posts/<earlier-post-id>/image-alt.txt`** (not necessarily the binary) to keep **tone and illustration mode** consistent across the batch.

## Prerequisites

- **Workspace context:** `USER.md`, `SOUL.md`; **`brand-images/`** per **Brand kit** section (env **`BRAND_IMAGES_DIR`** or `workspace/brand-images/`).
- **Output root:**
  ```text
  workspace/drafts/images/<YYYY-MM-DD>-<slug>/
  ```
- **Brief:** use case (feed post, story, Meta ad 1:1, display 1200×628, YT thumbnail), **must-win message**, **legal** (no competitor logos, no fake badges).
- **Tools:** **Gemini** produces **actual image files** in this setup. **Order:** try OpenClaw **`image_generate`** (or other host image tool) first if available; else **`generateContent`** with **`x-goog-api-key`** — see **`workspace/INTEGRATIONS.md`**.

## Credentials & API (qf-style)

- **Briefs-only (exception):** Only when the human asked no render, or no Gemini key/tool is available after checking — state that in **`README-handoff.md`**.
- **Render (default when Gemini exists):** **`GEMINI_API_KEY`** in **`~/.openclaw/.env`** or **`~/.config/gemini/api_key`**. Send **`x-goog-api-key`** (not Bearer) to `generativelanguage.googleapis.com` — see **`workspace/INTEGRATIONS.md`**.
- **Native image model (`generateContent`):** Map `prompt-master.txt` + aspect ratio from `brief.json` / matrix into `generationConfig.imageConfig.aspectRatio` (`"1:1"`, `"16:9"`, `"9:16"`, etc.—use values supported by the model you choose). Parse the response for **inline image bytes** (base64) and write **`generated-1.png`** (or `.jpg` per MIME) under the same draft folder. **Model IDs change** — pick the current image-capable model from [Gemini image generation docs](https://ai.google.dev/gemini-api/docs/image-generation).
- **Imagen (`predict`):** Optional batch-style generation via e.g. `imagen-4.0-generate-001:predict` with `instances[].prompt` and `parameters.sampleCount` if your project uses Imagen instead of native image output.
- **Negatives / brand:** Fold `negative-prompt.txt` into the **user text prompt** (Gemini image prompts are text-first); keep `text-overlay.md` as post-edit guidance if the API cannot place text reliably.

## High-level Workflow

1. **Use case → aspect ratio matrix**
   - Map explicitly:

     | Placement | Ratio | Min resolution (guide) |
     |-----------|-------|-------------------------|
     | IG feed | 4:5 or 1:1 | 1080 wide min |
     | Stories/Reels cover | 9:16 | 1080×1920 |
     | Meta feed ad | 1:1 / 4:5 | per Ads Manager |
     | YT thumbnail | 16:9 | 1280×720 min |
     | LinkedIn link post | 1.91:1 | 1200×627 typical |

2. **Concept sheet (`concept.md`)**
   - 1–2 sentences **creative idea** + **audience** + **emotion** (trust, urgency, curiosity).

3. **Master prompt (`prompt-master.txt`)**
   - Single detailed prompt: ***Style benchmark* (this skill)** + **subject tied to post/article copy** + composition, lighting, palette (brand kit where present). Default style = **flat 2D vector** per benchmark unless campaign **`visual-dna.md`** overrides.

4. **Negative prompt (`negative-prompt.txt`)**
   - Always include: `watermark`, `lowres`, `blurry`, `extra fingers`, **competitor logos**, **fake App Store badge**, **gore**, **photorealistic named celebrity** (unless rights cleared).
   - **Always include** the ***Negative prompt hints (benchmark-specific)*** list from *Style benchmark* (anime, holographic UI, server room, cyberpunk, etc.) unless **`visual-dna.md`** explicitly defines a different illustration mode.
   - Add use-case negatives (e.g. “cluttered UI” for app mockups).

5. **Text-on-image policy (`text-overlay.md`)**
   - If text required: **≤5 words** for thumb/story; font style note; **contrast** (WCAG-style: light on dark band).
   - If no text: state “clean image; caption carries copy.”

6. **Safe zones (`safe-zones.md`)**
   - For 9:16: top/bottom UI overlay avoidance; for YT thumb: **right third** often occluded by timestamp—keep face/keyword left.

7. **A/B variants (`variants.md`)**
   - Table: `Variant` | `What changed` | `Hypothesis` | `Prompt delta summary`.
   - Minimum **2** variants for ads; **3** for social tests when requested.

8. **Brand compliance block**
   - In `README-handoff.md`: checklist against `USER.md` (colors, banned motifs, disclosure if sponsored creative).

9. **Optional `brief.json`**
   - Keys: `aspect_ratio`, `width`, `height`, `prompt`, `negative_prompt`, `variants[]`.

10. **Optional pixel pass (`gemini-render.md`)**
    - If keys exist: document model id, request timestamp, output filenames, and any **safety filter** or refusal in `gemini-render.md` next to the images.

11. **Scheduling**
    - Campaign assets: date-prefix folders; **retain** previous days for audit.

## Outputs (required)

- `workspace/drafts/images/<YYYY-MM-DD>-<slug>/concept.md`
- `prompt-master.txt`, `negative-prompt.txt`, `text-overlay.md`, `safe-zones.md`, `variants.md`, `README-handoff.md`

## Agent Checklist

- [ ] Aspect ratio matches placement table; resolution guidance included.
- [ ] Negative prompt covers legal/safety brand items.
- [ ] A/B table present when use case is ads or declared test.
- [ ] No invented awards, rankings, or “official” marks.
- [ ] User told folder path; if Gemini/OpenClaw image tools were available, **at least one `generated-*` file** exists **or** failure/refusal documented in **`gemini-render.md`**.
- [ ] If chaining to `adverts-creator`, list which variant maps to which ad headline in README.
- [ ] **STYLE LOCK** paragraph is **first** in **`prompt-master.txt`**; full benchmark negatives included; ***Style benchmark*** reflected unless **`visual-dna.md`** overrides; subject + on-screen hints tied to **specific** post/article copy; **Post-render visual QA** passed (or one regenerate logged in **`gemini-render.md`**).
- [ ] **`visual-dna.md`** or equivalent style block **reused** across the campaign batch when present (and still copy-grounded).
- [ ] **`image-alt.txt`** reads true to the raster and to the post intent.
- [ ] **`brand-images/`** loaded (`BRAND_IMAGES_DIR` or default); logo rules applied; no invented wordmark.
