---
name: social-caption-writer
description: Platform-native captions with hook variants, character-limit tables, hashtag policy, first-line preview notes, and optional thread numbering for X—writes to workspace/drafts/social/captions/ for social-media-manager to merge into post bundles.
metadata: {"clawdbot":{"emoji":"✍️"},"openclaw":{"emoji":"✍️"}}
---

# social-caption-writer

**Copy-only** execution: given a **brief**, output **multiple hook options** and **final caption blocks** per platform rules—as detailed as `qf-course-researcher` is on matching heuristics (explicit rules, not vibes).

## Prerequisites

- Brief includes: `topic_id` or slug, **platform** (enum: instagram, twitter_x, facebook, tiktok_caption, linkedin_feed, youtube_community), **tone**, **CTA**, **link policy**, **banned phrases**.
- Read `USER.md` for brand.
- Output:
  ```text
  workspace/drafts/social/captions/<YYYY-MM-DD>-<topic>-<platform>.md
  ```

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

- [ ] Constraint table present for chosen platform.
- [ ] 3 hooks + one selected path clear (or manager picks).
- [ ] Character estimates for X threads.
- [ ] Hashtags vetted for relevance and spam risk.
- [ ] Compliance lines when applicable.
- [ ] No unverifiable claims; stats only if brief provided source.
