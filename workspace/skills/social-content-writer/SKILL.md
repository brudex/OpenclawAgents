---
name: social-content-writer
description: Multi-platform short-form posts from the social calendar—LinkedIn feed, X, Reddit, Facebook, etc.—one publish-ready post-body per slot with hashtags; complements linkedin-article-writer (articles only) and x-post-writer (X only).
metadata: {"clawdbot":{"emoji":"📝"},"openclaw":{"emoji":"📝"}}
---

# social-content-writer

**Short-form social copy across platforms** from **`calendar.md`** rows. This is the workspace **“social content writer”** skill (distinct from **`agency-marketing`** personas—you may borrow voice patterns from references below).

**Not for:** long LinkedIn **articles** → **`linkedin-article-writer`**. **X-only** quick path → **`x-post-writer`**.

## When to use

- Calendar slots for **`linkedin_feed`** (short post, not article), **`twitter_x`**, **`reddit`**, **`facebook`**, **`instagram`** caption-style, etc.
- You want **one skill name** instead of picking an agency persona per platform.

## Prerequisites

- **`USER.md`**, campaign **`00-intake.md`** if present.
- **`calendar.md`** row(s): date, platform, topic slug, CTA, **Post id**.
- Output root: **`workspace/drafts/social/<campaign>/posts/<post-id>/post-body.md`**

## Credentials & API (qf-style)

- **Draft-only.** Reddit/Facebook live actions only after human approval and **`INTEGRATIONS.md`** / channel config. X/LinkedIn feed: **`hype-engine`** via **`social-media-manager`**.
- **Google Drive:** When the social campaign uses **`drive-handoff.md`**, the parent **`social-media-manager`** may export this skill’s **`post-body.md`** to a shared Doc for **employees** to paste live—same folder pattern as **`INTEGRATIONS.md`** (*social posting handoff*).

## Reference voices (optional, read—not copy fake stats)

| Platform tilt | Agency reference (under `agency-marketing/references/`) |
|---------------|--------------------------------------------------------|
| General multi-channel | `marketing-content-creator.md` |
| LinkedIn short post | `marketing-linkedin-content-creator.md` |
| X | `marketing-twitter-engager.md` |
| Reddit | `marketing-reddit-community-builder.md` |

## High-level Workflow

1. For each assigned row, read **Platform** enum and apply native constraints (length, tone, link rules).
2. Write **`post-body.md`** using the same section pattern as **`x-post-writer`**:

   ```markdown
   ## Publish-ready (<platform>)
   <copy-paste-ready body>

   ## Hashtags / formatting notes
   <platform-specific>

   ## Character / limit check
   <brief note>
   ```

3. **Reddit:** title + body if the slot is a post; note subreddit rules placeholder if unknown.
4. **Handoff:** update the campaign **`pipeline-state.md`** (set **`post_bodies`** progress); **`social-media-manager`** merges into **`post-bundle.md`**. **`social-caption-writer`** is **optional**—only if the human wants a second pass.

## Relationship to **social-community-engagement**

- **`social-content-writer`** = **outbound** scheduled posts from the calendar.
- **`social-community-engagement`** = **replies** to comments/DMs under `workspace/drafts/social/replies/`—do not mix into `post-body.md`.

## Outputs (required)

- One **`post-body.md`** per calendar slot you own.

## Agent Checklist

- [ ] Platform in filename or first heading matches calendar **Platform** column.
- [ ] Publish-ready copy + hashtags (or “no hashtags” note) in-file—no dependency on caption writer by default.
- [ ] No fabricated stats; sources only if brief provided.
