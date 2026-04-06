---
name: social-caption-writer
description: Optional polish pass—hooks, hashtag variants, thread layout—from existing post-body.md or teaser.md; default pipeline skips this when x-post-writer/social-content-writer already ship publish-ready copy.
metadata: {"clawdbot":{"emoji":"✍️"},"openclaw":{"emoji":"✍️"}}
---

# social-caption-writer

**Optional** skill. **`x-post-writer`**, **`social-content-writer`**, and **`linkedin-article-writer`** (`teaser.md`) are expected to deliver **publish-ready** text (including hashtags) so **`social-media-manager`** can bundle **without** this step.

Use **`social-caption-writer`** when the human wants **extra hook variants**, **hashtag refresh**, **thread re-split**, or **platform-specific polish** on top of an existing draft.

**Copy-only** execution: you **do not invent the post from a one-line calendar row alone** when a full draft already exists. Prefer **post body in → caption package out**. Same rigor as `qf-course-researcher` (explicit rules, character math, not vibes).

## Pipeline position (when used)

1. **`marketer-agent`** → … → **`calendar.md`**.  
2. **`x-post-writer`** / **`social-content-writer`** / **`linkedin-article-writer`** → **`post-body.md`** or **`teaser.md`**; **`auto-image-generation`** → **`post-image.png`** / **`article-hero.png`** + **`image-alt.txt`**.  
3. ***(Optional)* `social-caption-writer`** → `captions/*.md` (may reference **`image-alt.txt`** for consistency).  
4. **`social-media-manager`** → `post-bundle.md`, **`APPROVAL.md`**, **`hype-engine`**.

When the human says “captions for the April calendar” **without** opting into this skill, prefer **re-running the content writer** to refresh in-file copy instead.

If step 2 is skipped, you may still run from a **full brief** (see below)—but when batching, **first confirm** each slot has a **`post-body.md`**, **`teaser.md`**, or equivalent; if missing, **stop that row** with a defer note instead of hallucinating the post.

## Prerequisites

- **Primary input:** path to **existing post text** — e.g. `workspace/drafts/social/<campaign>/posts/<post-id>/post-body.md`, or `workspace/drafts/linkedin/<date>-<slug>/teaser.md` / excerpt from `article.md` linked from the calendar row.  
- **Secondary:** the matching **`calendar.md`** row (date, platform, slug, CTA type, asset flags).  
- **Fallback brief** (only when no draft exists): `topic_id` or slug, **platform** (enum: instagram, twitter_x, facebook, tiktok_caption, linkedin_feed, youtube_community), **tone**, **CTA**, **link policy**, **banned phrases** — and note in the output that the post body is still **TODO** for the feed writer.  
- Read `USER.md` for brand.  
- Output (per slot, under the **same campaign folder** as `calendar.md` unless the human specifies otherwise):
  ```text
  workspace/drafts/social/<campaign>/captions/<YYYY-MM-DD>-<topic>-<platform>.md
  ```

## Batch mode (e.g. one month / April)

1. Open the campaign folder (e.g. `workspace/drafts/social/2026-04-01-acme-launch/`).  
2. Read **`calendar.md`**; for **each row** in the target month (e.g. April = dates `2026-04-*`):  
   - Resolve **`post-id`** or file path from a **Post file** / **Draft path** column if present, else `posts/<date>-<slug>/post-body.md`.  
   - If the post file exists → write one caption `.md` as below.  
   - If missing → append a row to `captions/DEFERRED.md` with date, slug, reason.  
3. Summarize counts: written vs deferred.

## Credentials & API (qf-style)

- **None:** Copy-only artifacts. **Posting** for **`twitter_x`** and **`linkedin_feed`** goes **`social-media-manager`** → **`hype-engine`** (HypeEngine Posts API; config `~/.config/hype-engine/`). Other platforms: **`INTEGRATIONS.md`** or OpenClaw channels per **`TOOLS.md`**.

## High-level Workflow

1. **Platform constraint sheet (top of file)**
   - Paste relevant row:

     | Platform | Body limit (guide) | Hashtags | Link placement |
     |----------|-------------------|----------|----------------|
     | X | 280 or thread | 0–2 inline | often end |
     | IG | ~125 chars “above fold” | 3–12 end | bio CTA |
     | TikTok | short + line break | 3–6 | phrase + link in bio |
     | LinkedIn feed | first ~210 chars hook | 3–5 professional | comment strategy note |
     | Facebook | 1–3 short paragraphs | optional | mid or end |

2. **Hook variants**
   - **3 options** labeled A/B/C; each ≤ **12 words** for short-form first line.

3. **Body**
   - **Chosen hook** expanded; paragraphs for long platforms; single block for short.

4. **Hashtag block**
   - On new line; research-style mix: **broad + niche**; **no** banned/spam tags.

5. **Thread plan (X only)**
   - If >280: `Thread 1/…` sections with **character count estimate** per tweet.

6. **Accessibility**
   - Note: avoid emoji-only meaning; **alt text suggestion** for paired image (one line).

7. **Compliance footer**
   - `#ad`, `#sponsored`, AI disclosure line if `USER.md` requires.

8. **Handoff section**
   - “Merged by: social-media-manager into post-bundle `<id>`.”

## Outputs (required)

- One `.md` per (date, topic, platform) with sections above.

## Agent Checklist

- [ ] **Upstream:** caption reflects an existing **post body** or **`teaser.md`**, or output flags **TODO** for the feed writer.
- [ ] Batch runs: **DEFERRED.md** updated for slots with no draft file.
- [ ] Constraint table present for chosen platform.
- [ ] 3 hooks + one selected path clear (or manager picks).
- [ ] Character estimates for X threads.
- [ ] Hashtags vetted for relevance and spam risk.
- [ ] Compliance lines when applicable.
- [ ] No unverifiable claims; stats only if brief or post body provided source.
