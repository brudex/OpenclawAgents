---
name: auto-image-generation
description: Full creative briefs for static assets—social, ads, thumbnails, blog heroes—with aspect ratio matrix, layered prompts, negative prompts, brand constraints, A/B variant grid, and optional safe-zone diagram notes for designers or image_generate tools.
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
- **Tools:** `image_generate` or external API when enabled; otherwise output **briefs only** and state that in README.

## Credentials & API (qf-style)

- **Briefs-only:** No keys; deliver prompts and `README` under `workspace/drafts/images/...`.
- **Render / API:** Set provider keys on the gateway host — typically `OPENAI_API_KEY`, `FAL_KEY`, and/or `GEMINI_API_KEY` in **`~/.openclaw/.env`** (see **`workspace/INTEGRATIONS.md`**). Example OpenAI Images-style call (adjust model and endpoint per current docs):

  ```bash
  export OPENAI_API_KEY=$(cat ~/.config/openai/api_key)   # or .env only
  curl -sS https://api.openai.com/v1/images/generations \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"model":"gpt-image-1","prompt":"…","n":1,"size":"1024x1024"}'
  ```

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

10. **Scheduling**
    - Campaign assets: date-prefix folders; **retain** previous days for audit.

## Outputs (required)

- `workspace/drafts/images/<YYYY-MM-DD>-<slug>/concept.md`
- `prompt-master.txt`, `negative-prompt.txt`, `text-overlay.md`, `safe-zones.md`, `variants.md`, `README-handoff.md`

## Agent Checklist

- [ ] Aspect ratio matches placement table; resolution guidance included.
- [ ] Negative prompt covers legal/safety brand items.
- [ ] A/B table present when use case is ads or declared test.
- [ ] No invented awards, rankings, or “official” marks.
- [ ] User told folder path; clarified whether pixels were generated or brief-only.
- [ ] If chaining to `adverts-creator`, list which variant maps to which ad headline in README.
