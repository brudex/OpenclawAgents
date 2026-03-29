---
name: tiktok-video-ads-creator
description: TikTok organic and paid packages—hook library, beat-level retention map, caption/hashtag sets, ad hook variants, and Spark Ads / landing-message match notes—under workspace/drafts/tiktok/; consumes auto-video-generation beat sheets when provided.
metadata: {"clawdbot":{"emoji":"🎵"},"openclaw":{"emoji":"🎵"}}
---

# tiktok-video-ads-creator

**TikTok-specific** layer on top of generic video planning—like `qf-course-researcher` maps certifications to categories, this maps **beats** to **retention tactics** and **ads** to **conversion angles**.

## Prerequisites

- Optional input: `auto-video-generation` folder path (`beat-sheet.md`).
- `USER.md` + trend file from `social-trend-monitor` optional.
- Output:
  ```text
  workspace/drafts/tiktok/<YYYY-MM-DD>-<slug>/
  ```

## Credentials & API (qf-style)

- **Draft-only:** No TikTok credentials; hooks, captions, and ad notes live under `workspace/drafts/tiktok/...`.
- **Live ads / upload (optional):** TikTok for Business APIs need app + token setup. Use **`workspace/INTEGRATIONS.md`** for `TIKTOK_ACCESS_TOKEN` / `~/.config/tiktok/` guidance. Prefer **OpenClaw channel** integration for TikTok when available instead of embedding tokens in prompts.

## High-level Workflow

1. **Mode select (`mode.md`)**
   - `organic` | `ads` | `both`.

2. **Organic — hook library (`hooks-organic.md`)**
   - **10 hooks** categorized: pattern interrupt, controversy (safe), story, stat (sourced), challenge.

3. **Organic — retention map (`retention-map.md`)**
   - Rows: Second window | Goal (hold) | Tactic (text pop, jump cut, question) | Sound note.

4. **Organic — caption package (`caption.md`)**
   - Primary caption + **CTA** + **3–6 hashtags** + **pin comment** suggestion.

5. **Ads — hook variants (`hooks-ads.md`)**
   - **5 hooks** focused on **benefit + CTA**; label A–E.

6. **Ads — primary text (`ad-primary.md`)**
   - One block per variant; **message match** to landing H1 noted.

7. **Sound / legal (`audio-legal.md`)**
   - Trending audio: **rights warning**; default recommend original VO + royalty-free bed.

8. **Handoff**
   - Link `auto-video-generation` files if merged; else note “script-only, no beat sheet.”

9. **Scheduling**
   - **Trend jacking:** date slug required; do not reuse stale hooks without refresh note.

## Outputs (required)

- `mode.md`, and either `hooks-organic.md` + `caption.md` **or** `hooks-ads.md` + `ad-primary.md`, plus `audio-legal.md`.

## Agent Checklist

- [ ] 10 organic hooks OR 5 ad hooks per mode; both if `both`.
- [ ] Retention map covers 0–15s minimum for organic.
- [ ] Hashtag count within policy; no banned/gambling tags unless brand allows.
- [ ] Audio legal section present.
- [ ] Stats in hooks sourced or removed.
- [ ] Paths returned; human handles upload/ads manager.
