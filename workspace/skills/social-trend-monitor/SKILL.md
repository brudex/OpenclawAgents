---
name: social-trend-monitor
description: Produces dated trend briefs with source URLs, confidence and recency notes, audience fit scores, and risk flags—feeds social-media-manager and tiktok-video-ads-creator. No posting; research-only artifact under workspace/drafts/social/trends/.
metadata: {"clawdbot":{"emoji":"📡"},"openclaw":{"emoji":"📡"}}
---

# social-trend-monitor

**Trend intelligence** as a **standalone dated report**, parallel to how `qf-course-researcher` produces a **dated** research page—each run is **self-contained** and citable.

## Scope boundary (do not duplicate course research)

- **`qf-course-researcher`** / QuizFactor course work = **category, curriculum, competitor courses**, evidence for product decisions.  
- **`social-trend-monitor`** = **what is surfacing on social platforms now** — trending **hashtags**, **topics**, **formats**, **memes**, breakout sounds (short-video), and **conversation spikes** on X, Instagram, TikTok, LinkedIn, etc., scoped to the human’s **niche + geo**.  
- Goal: give **`social-media-manager`** and creatives **tags and angles to ride the feed**, not to redo deep course-market research.

## Prerequisites

- Web search / news tools when available; else **INFERENCE-ONLY** banner at top.
- Human: **niche**, **geo**, **languages**, **competitors to watch**, **topics to avoid**.
- Output:
  ```text
  workspace/drafts/social/trends/<YYYY-MM-DD>-<niche-slug>.md
  ```

## Credentials & API (qf-style)

- **Web search / browse:** Same expectation as `qf-course-researcher` — gateway must expose search tools, or mark output **INFERENCE-ONLY**.
- **Optional paid SERP:** If configured, document env vars in **`workspace/INTEGRATIONS.md`** (see **`auto-research-agent`**).

## High-level Workflow

1. **Query plan (`queries.md`)**
   - List 5–10 search queries you will run (or would run); **date** of run.

2. **Raw hits table (`raw-hits.md`)**
   - Columns: Topic | Source URL | Publisher | **Published date** | **Snippet** | Angle.

3. **Scoring (`scored-topics.md`)**
   - For each consolidated topic (5–15 rows):
     - **Recency** (hours/days since peak).
     - **Relevance** to niche (0–10).
     - **Brand fit** (0–10) per `USER.md`.
     - **Risk** (misinfo, controversy) — `low/med/high`.

4. **Angles (`angles.md`)**
   - 3 **content angles** per **high-fit** topic: hook idea, format suggestion, **avoid** notes.

5. **Declined topics (`declined.md`)**
   - Trends **rejected** and why (off-brand, high risk, stale).

6. **Handoff**
   - “Consume by: `social-media-manager` (calendar), `tiktok-video-ads-creator` (hooks).”
   - **Before `hype-engine` publish:** `social-media-manager` may copy **0–2 vetted** hashtags/topics from this file into **X** and **LinkedIn feed** payloads only (see that skill’s *Trending hashtags* section).

7. **Scheduling**
   - **Daily** slug `daily-<niche>`; do not overwrite—new date file each run.

## Outputs (required)

- `trends-<YYYY-MM-DD>-<niche-slug>.md` as master (can embed or link child sections).

## Agent Checklist

- [ ] INFERENCE-ONLY if no live search.
- [ ] Published dates on raw hits where visible; unknown marked unknown.
- [ ] No “viral” claim without describing evidence (velocity, volume).
- [ ] Risk column populated; high-risk not recommended without human OK.
- [ ] Declined list non-empty when many hits were filtered (shows rigor).
- [ ] File path returned to user and parent skills.
