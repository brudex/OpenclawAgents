---
name: auto-image-generation
description: Full creative briefs for static assets—social, ads, thumbnails, blog heroes—with aspect ratio matrix, layered prompts, negative prompts, brand constraints, A/B variant grid, and optional safe-zone notes; live pixels via Gemini API (native image or Imagen) when GEMINI_API_KEY is set.
metadata: {"clawdbot":{"emoji":"🖼️"},"openclaw":{"emoji":"🖼️"}}
---

# auto-image-generation

Deliver **designer-ready** image specs: not a single vague prompt, but **placement**, **ratio**, **prompt + negative**, **text overlay rules**, and **A/B variants**—equivalent detail to how `qf-course-researcher` specifies Notion property types (Select vs rich_text) so downstream work does not degrade.

## Prerequisites

- **Workspace context:** `USER.md`, `SOUL.md`; optional brand hex codes from human.
- **Output root:**
  ```text
  workspace/drafts/images/<YYYY-MM-DD>-<slug>/
  ```
- **Brief:** use case (feed post, story, Meta ad 1:1, display 1200×628, YT thumbnail), **must-win message**, **legal** (no competitor logos, no fake badges).
- **Tools:** When generating **real files**, use **Gemini API** (this workspace’s default). OpenClaw **`image_generate`** may wrap the same API if configured. Otherwise output **briefs only** and state that in README.

## Credentials & API (qf-style)

- **Briefs-only:** No keys; deliver prompts and `README` under `workspace/drafts/images/...`.
- **Render (default: Gemini):** Store **`GEMINI_API_KEY`** in **`~/.openclaw/.env`** or **`~/.config/gemini/api_key`**. Send **`x-goog-api-key`** (not Bearer) to `generativelanguage.googleapis.com` — see **`workspace/INTEGRATIONS.md`**.
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
   - Single detailed prompt: subject, style (flat vector, photoreal, 3D), lighting, palette, **composition** (rule of thirds, center subject).

4. **Negative prompt (`negative-prompt.txt`)**
   - Always include: `watermark`, `lowres`, `blurry`, `extra fingers`, **competitor logos**, **fake App Store badge**, **gore**, **photorealistic named celebrity** (unless rights cleared).
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
- [ ] User told folder path; clarified **Gemini** pixels vs **brief-only** (no `GEMINI_API_KEY`).
- [ ] If chaining to `adverts-creator`, list which variant maps to which ad headline in README.
