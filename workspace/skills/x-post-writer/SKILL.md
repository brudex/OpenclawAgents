---
name: x-post-writer
description: X (Twitter) only—publish-ready post + hashtags + thread layout in posts/<post-id>/post-body.md; no LinkedIn. Draft-only; scheduling via social-media-manager and hype-engine.
metadata: {"clawdbot":{"emoji":"🐦"},"openclaw":{"emoji":"🐦"}}
---

# x-post-writer

**X/Twitter posts only.** Do **not** draft LinkedIn, Reddit, or other platforms here—use **`social-content-writer`** or **`linkedin-article-writer`** instead.

Each file must be **ready to paste or ship** after approval: **main text + hashtags** in one place so you normally **do not** need **`social-caption-writer`**.

**Images (workspace default):** After this file exists, **`auto-image-generation`** produces **`posts/<post-id>/post-image.png`** and **`image-alt.txt`** in the same folder (see **`social-media-manager`**). You may add a stub line under **`post-body.md`**: `## Image brief` (1–2 sentences for the art director) to steer the generator.

## Prerequisites

- **`USER.md`**; no engagement-bait spam.
- **Input:** `calendar.md` row **or** brief (topic, CTA, tone, **post id**).
- **Campaign folder:** `workspace/drafts/social/<YYYY-MM-DD>-<campaign-slug>/`

## Credentials & API (qf-style)

- **Draft-only.** Live post: **`social-media-manager`** → **`hype-engine`** after **`APPROVAL.md`** (push approved copy—HypeEngine already connected). **Google Drive** in this workspace is for **LinkedIn articles**, not routine X posts.

## High-level Workflow

1. Read row/brief; respect intake **blacklist** and compliance.
2. Write **`posts/<post-id>/post-body.md`** with this structure:

   ```markdown
   ## Publish-ready (X)
   <single tweet or thread; numbers for thread order>

   ## Hashtags
   <0–2 inline or end line; platform-appropriate>

   ## Character check
   <note counts per tweet if thread>
   ```

3. Optional tone: skim **`workspace/skills/agency-marketing/references/marketing-twitter-engager.md`** (do not copy fake metrics).
4. **Handoff:** update **`pipeline-state.md`**; next is **`auto-image-generation`** (slot image) → **`social-media-manager`** (bundle)—**not** caption writer unless the human asks for a polish pass.

## Outputs (required)

- `posts/<post-id>/post-body.md` per slot.

## Agent Checklist

- [ ] **X only**—no other platforms in this file.
- [ ] Copy is publish-ready (hashtags included).
- [ ] Paths match calendar **Post id** / **Draft path**.
- [ ] **`post-image.png`** will be produced by **`auto-image-generation`** before bundle (unless campaign intake marks this row text-only).
