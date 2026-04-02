---
name: x-post-writer
description: X (Twitter) only—publish-ready post + hashtags + thread layout in posts/<post-id>/post-body.md; no LinkedIn. Draft-only; scheduling via social-media-manager and hype-engine.
metadata: {"clawdbot":{"emoji":"🐦"},"openclaw":{"emoji":"🐦"}}
---

# x-post-writer

**X/Twitter posts only.** Do **not** draft LinkedIn, Reddit, or other platforms here—use **`social-content-writer`** or **`linkedin-article-writer`** instead.

Each file must be **ready to paste or ship** after approval: **main text + hashtags** in one place so you normally **do not** need **`social-caption-writer`**.

## Prerequisites

- **`USER.md`**; no engagement-bait spam.
- **Input:** `calendar.md` row **or** brief (topic, CTA, tone, **post id**).
- **Campaign folder:** `workspace/drafts/social/<YYYY-MM-DD>-<campaign-slug>/`

## Credentials & API (qf-style)

- **Draft-only.** Live post: **`social-media-manager`** → **`hype-engine`** after **`APPROVAL.md`**, **or** employees copy from a shared **Google Doc** listed in **`drive-handoff.md`** (see **`INTEGRATIONS.md`** — social posting folder).

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
4. **Handoff:** update **`pipeline-state.md`**; next is **`social-media-manager`** (bundle)—**not** caption writer unless the human asks for a polish pass.

## Outputs (required)

- `posts/<post-id>/post-body.md` per slot.

## Agent Checklist

- [ ] **X only**—no other platforms in this file.
- [ ] Copy is publish-ready (hashtags included).
- [ ] Paths match calendar **Post id** / **Draft path**.
