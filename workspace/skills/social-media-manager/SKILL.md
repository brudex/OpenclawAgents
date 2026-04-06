---
name: social-media-manager
description: Social calendar, branded Gemini images (brand-images/ + post-image.png), bundles, HypeEngine POST /posts with date+time (scheduled auto-publish, UUID idempotency); cron AM/PM; Drive for LinkedIn articles only.
metadata: {"clawdbot":{"emoji":"📱"},"openclaw":{"emoji":"📱"}}
---

# social-media-manager

The **parent** social agent: owns **consistency** (voice, CTA ladder, disclosure) and **file-based handoffs** to sub-skills—mirroring how `qf-course-researcher` orchestrates web → API → Notion with explicit steps.

## Posting model (this workspace)

**HypeEngine is already connected** to **LinkedIn** and **Twitter/X**. For approved **feed** slots (`linkedin_feed`, `twitter_x`), send each row **once** via **`hype-engine`**: Media API + **POST `/posts`** with **`date` + `time`** from **`APPROVAL.md`**—HypeEngine **schedules and auto-publishes** (no separate “publish now” call). See **`hype-engine`** → *Scheduling — no separate “publish now”*.

**Pipeline order (how teams use it):**

1. **First — this skill + HypeEngine:** calendar → writers → **`auto-image-generation`** (per slot, **`brand-images/`** / **`BRAND_IMAGES_DIR`**) → bundles → **`APPROVAL.md`** → **`hype-engine`**: upload **`post-image.png`** / **`article-hero.png`**, **POST `/posts`** scheduled (**record `HypeEngine post UUID`**; never duplicate the same Post ID).
2. **Last — LinkedIn articles:** **`linkedin-article-writer`** produces **`article.md`** + **`article-hero.png`** + **`teaser.md`**. **Interns** publish the **article** body (composer / Drive). **`teaser.md`** **feed** row: same HypeEngine flow (**scheduled** **`POST /posts`** with hero image when approved).

## Operator summary (canonical playbook)

1. **Batch write (~2 weeks):** Using **`calendar.md`**, **`x-post-writer`** and **`social-content-writer`** (and **`linkedin-article-writer`** for article rows) generate copy **in advance**; then run **`auto-image-generation`** per slot so every **`twitter_x`** / **`linkedin_feed`** / article row has **`post-image.png`** or **`article-hero.png`** before bundling.
2. **Approve:** Fill **`APPROVAL.md`** with **Approved Y/N** and **go-live datetime** matching each row’s **Local time** (e.g. morning `09:00`, evening `18:00`).
3. **Cron (twice daily):** Two jobs (AM + PM) are **not** duplicates of each other: each must publish **only** rows whose **`calendar.md` `Local time`** matches that window (e.g. `09:00` vs `18:00`) **and** **`APPROVAL.md`** has **`HypeEngine post UUID` empty**. See **`hype-engine`** → *Idempotency*.
4. **Trends:** Before each publish run, optionally refresh or read **`social-trend-monitor`** and merge **0–2 vetted** trending hashtags into **X** and **LinkedIn feed** copy (see below).
5. **LinkedIn articles (last in the chain):** **`linkedin-article-writer`** on a **separate cadence** (~every 2 days). **Interns** post the **article** body (LinkedIn UI + optional Drive `04-articles/` per **`INTEGRATIONS.md`**). **HypeEngine** publishes **`teaser.md`** to the **LinkedIn feed** when approved—same connected account as other feed posts; it does **not** replace intern posting of the long-form article.

**OpenClaw:** [Cron documentation](https://docs.openclaw.ai/automation/cron-jobs) · jobs persist in **`~/.openclaw/cron/jobs.json`**. Finish skill setup first, then add cron so execution does not depend on manual chat triggers.

## Prerequisites

- Read `USER.md`, `SOUL.md`, `AGENTS.md` (group vs main session rules).
- **Google Drive (optional — articles + intake refs only):** If **`~/.config/social/drive_folder_id`** or **`SOCIAL_POSTING_DRIVE_FOLDER_ID`** is set (see **`workspace/INTEGRATIONS.md`** → *Google Drive — LinkedIn articles only*), then:
  - **Read:** At **intake**, you may pull **reference** files the team placed there (guidelines, notes) and summarize into **`00-intake.md`** with Drive paths.
  - **Do not** use this folder as the default export for **Twitter/LinkedIn feed** posts—those are **pushed** via **`hype-engine`** from **`post-bundle.md`** after approval.
  - **Articles:** **`linkedin-article-writer`** may export long-form copy to **`04-articles/`** for **interns**; link in **`publish-handoff.md`** / **`README-handoff.md`**. Routine social slots are **not** mirrored to Drive as “ready-to-post” Docs.
- **Default output root:**
  ```text
  workspace/drafts/social/<YYYY-MM-DD>-<campaign-slug>/
  ```
- **Publish policy:** default **draft-only**; auto-post only if human has documented allowlist in workspace (e.g. `TOOLS.md` or `USER.md`).

## Cadence: two-week batch + twice daily (AM / PM)

- **Planning:** Build **`calendar.md`** for the next **~14 days** from marketer + **`social-content-planning`**.
- **Writing + images:** **`social-content-writer`** / **`x-post-writer`** / **`linkedin-article-writer`** fill **`post-body.md`**, **`teaser.md`**, **`article.md`**; then **`auto-image-generation`** (Gemini, already configured) produces **`posts/<post-id>/post-image.png`** or **`workspace/drafts/linkedin/.../article-hero.png`**—**required** for this workspace unless a row is explicitly text-only in **`00-intake.md`**.
- **Calendar column:** add **Local time** (or **Slot**) per row, e.g. **`09:00`** and **`18:00`** for **morning** and **evening** posts. **`hype-engine`** `date` + `time` must match **`APPROVAL.md`**.
- **At publish time:** read the **approved** `post-bundle.md` for that slot only—do not improvise a different topic.

## Trending hashtags before X / LinkedIn feed posts

- When the human wants **live trends** in the copy: run or refresh **`social-trend-monitor`** (or read the latest file under `workspace/drafts/social/trends/`).
- **Merge rule:** add **0–2** hashtags or phrases that pass **brand fit** and **risk** from the trend brief—**no** spam-stacking; **no** unrelated viral tags.
- Record in **`post-bundle.md`** a line **`Trend source:`** + file path and which tags were added so publishes are auditable.

## Credentials & API (qf-style)

- **Draft-only:** No secrets; all bundles under `workspace/drafts/social/...` as above.
- **Twitter/X + LinkedIn feed (live post):** HypeEngine is **already connected** for these channels. When **`APPROVAL.md`** allows it, use **`hype-engine`**: Accounts API → Posts API with the correct account UUIDs (`~/.config/hype-engine/*`) to **push** the approved bundle—no assumption that OAuth setup happens inside this skill. Do not use raw LinkedIn or X API from this workflow unless HypeEngine is unavailable and **`TOOLS.md` / `USER.md`** explicitly allows a fallback.
- **Other live publish / analytics:** **OpenClaw channels** in `~/.openclaw/openclaw.json` when configured (Telegram, Discord, etc.) where the team uses them.
- **Per-platform API keys** (Meta, Google Ads, TikTok Marketing, Reddit, direct LinkedIn if fallback): use **`workspace/INTEGRATIONS.md`**. Sub-skills (`adverts-creator`, …) spell out which service each needs.

## High-level Workflow

1. **Intake (`00-intake.md`)**
   - Capture: goals, KPIs, platforms, **blacklist topics**, **legal/compliance** (region, disclaimers), **deadlines**, asset links.
   - **Images:** default **every** scheduled **`twitter_x`** / **`linkedin_feed`** / article row gets **`auto-image-generation`**. List **text-only** post IDs here if any row must ship without an image.
   - **Visual consistency:** optional campaign **`visual-dna.md`** (illustration style, banned motifs). **Product logo & colors:** always from **`workspace/brand-images/`** or **`BRAND_IMAGES_DIR`** (e.g. `/home/admin/.openclaw/workspace/brand-images`)—see **`auto-image-generation`** → *Brand kit* and **`workspace/brand-images/README.md`**.
   - Optional: path to **`marketer-agent`** output (`workspace/drafts/marketing/.../README-handoff.md` or `06-channel-plan.md`) to align pillars and CTAs.

2. **Trend pass (optional)**
   - Invoke or simulate `social-trend-monitor` → save `trends-in.md` reference in folder.

3. **Calendar (`calendar.md`)**
   - Produce or merge output from `social-content-planning`:
     - Columns: **Date** | **Local time** (e.g. `09:00` / `18:00` for twice daily) | **Platform** | **Format** | **Topic slug** | **CTA type** | **Asset needs** | **Owner** | **Post id** | **Draft path** | **Image path (TBD → filled)** — expect **`posts/<post-id>/post-image.png`** or LinkedIn folder **`article-hero.png`**.
   - Calendar rows are **schedule + intent** (“shadows”); they are **not** a substitute for full post copy.

4. **Per-slot production loop (order is mandatory)**
   For each calendar row:
   - **4a — Publish-ready copy first:** Use the **one** writer that matches the slot (writers include **hashtags / thread layout** in-file by default—**no separate caption step** unless the human opts in):
     - **LinkedIn article (long-form):** **`linkedin-article-writer`** only → **Draft path** → `workspace/drafts/linkedin/...` (`article.md` + **`teaser.md`** + **`article-hero.png`** per that skill).
     - **X only:** **`x-post-writer`** → `posts/<post-id>/post-body.md`.
     - **Short LinkedIn feed, Reddit, Facebook, mixed calendar:** **`social-content-writer`** → `posts/<post-id>/post-body.md` (or platform-specific notes inside file).
     - **Fallback:** `agency-marketing` persona if no dedicated skill fits—still require **`post-body.md`** with publish-ready sections.
   - **4b — Image (required unless intake marks row text-only):** Run **`auto-image-generation`** immediately after 4a for that slot. Write **`posts/<post-id>/post-image.png`** (+ **`image-alt.txt`**) or **`article-hero.png`** in the LinkedIn article folder per **`auto-image-generation`** → *Chaining from social posts & LinkedIn articles*. If Gemini refuses, document in bundle under **`## Image`** as `STATUS: missing — reason` and escalate in **`APPROVAL.md`**.
   - **4c — Optional caption polish:** Only if the human asks: `social-caption-writer` → `captions/<date>-<platform>-<slug>.md` (otherwise skip).
   - **4d — Video (optional):** `auto-video-generation` per `assets-needed.md` when applicable (separate from the static image default).
   - **4e — Bundle:** `posts/<post-id>/post-bundle.md` for **every** calendar row with a **Post id** (including LinkedIn **teaser** rows): final body + hashtags + suggested time + **disclosure line** + **`## Image`** block:

     ```markdown
     ## Image
     - File: posts/<post-id>/post-image.png  (or path to article-hero.png)
     - Alt: <from image-alt.txt or article>
     - HypeEngine: upload via Media API → save MEDIA_UUID in this file after upload
     ```

     Sources: **`post-body.md`**, **`teaser.md`**, optional caption from 4c.

5. **Engagement queue**
   - If community work requested: `social-community-engagement` outputs under `replies/`.

6. **Analytics loop**
   - When metrics provided: `social-analytics` → `analytics/<period>-summary.md`; feed **next calendar** adjustments.

7. **Approval package (`APPROVAL.md`)**
   - Table: Post ID | Platform | Preview link or file path | **Image path** | **Approved Y/N** | Publisher | **Go-live datetime** | **HypeEngine post UUID** (empty until published—**never** re-post if filled) | **Media UUID** (optional).

8. **HypeEngine handoff (X + LinkedIn feed only, after approval)**
   - For each row where Platform is **twitter_x** or **`linkedin_feed`** and **Approved Y/N** is yes: **if `HypeEngine post UUID` is already set** → **skip** (idempotent). Else **`hype-engine`**: upload media if needed, then **POST `/posts` once** with **`date` + `time`** from **`APPROVAL.md`**—HypeEngine **queues and auto-publishes** at that time (**no** separate “publish now” call). Record **post UUID** + **media UUID** in **`APPROVAL.md`**. If **no image** and row was not text-only, **do not** send without human OK. Trends: merge before POST. See **`hype-engine`** → *Scheduling — no separate “publish now”* and *Idempotency*.
   - **LinkedIn long-form articles:** **not** published as the article via HypeEngine—**interns** post **`article.md`** (Drive / LinkedIn composer). HypeEngine only handles the **`teaser.md`** **feed** promo when that calendar row is approved. See **`hype-engine`** → *LinkedIn: feed post vs long-form article*.
   - Other platforms: unchanged (drafts only, or channels/APIs per `INTEGRATIONS.md` / `TOOLS.md`).

9. **Close-out message to user**
   - List **exact paths** created; state **nothing was sent to HypeEngine** unless step 8 ran (scheduled posts still “go live” later via HypeEngine, not via a second agent step).

10. **Scheduling**
   - **Weekly** campaigns: one folder per week slug.
   - **Always-on:** date-prefix daily subfolders `day-YYYY-MM-DD/`.

## Sub-skills (explicit contracts)

| Skill | Delivers |
|--------|-----------|
| `marketer-agent` (optional upstream) | ICP, positioning, channel plan, `briefs/` for social |
| `social-content-planning` | `calendar.md` skeleton |
| `linkedin-article-writer` | LinkedIn **articles** + `teaser.md` (not short feed posts) |
| `x-post-writer` | X-only **`post-body.md`** (publish-ready, hashtags in-file) |
| `social-content-writer` | Multi-platform short posts **`post-body.md`** (LinkedIn feed, X, Reddit, etc.) |
| `agency-marketing` | Fallback personas into `posts/<id>/post-body.md` |
| `social-caption-writer` | **Optional** second pass on copy + hashtags |
| `social-community-engagement` | Reply drafts |
| `social-analytics` | Readout markdown |
| `social-trend-monitor` | Trend brief file |
| `auto-image-generation` | **`post-image.png`** / **`article-hero.png`** + alt text for every slot (Gemini) |
| `hype-engine` | Media **upload** + live **Twitter/X** and **LinkedIn feed** posts after approval (Accounts + Media + Posts API) |

## Job chain & “when done → next” (`pipeline-state.md`)

For multi-step automation, keep a **single status file** in the campaign folder (same directory as `calendar.md`):

```text
workspace/drafts/social/<campaign>/pipeline-state.md
```

**Template (copy and keep updated):**

| Step | Phase | Status | Gate (required artifact) | Next skill to run |
|------|--------|--------|---------------------------|-------------------|
| 1 | `strategy` | `pending` \| `complete` | `workspace/drafts/marketing/.../README-handoff.md` | `social-media-manager` (intake + calendar) |
| 2 | `calendar` | `pending` \| `complete` | `calendar.md` with Post id + Draft path columns | `linkedin-article-writer` / `x-post-writer` / `social-content-writer` (per row) |
| 3 | `post_bodies` | `pending` \| `complete` | Every slot: `post-body.md` **or** LinkedIn **`teaser.md` + `article.md`** **and** matching **`post-image.png`** or **`article-hero.png`** (+ `image-alt.txt` where applicable) | `auto-image-generation` (if images missing) → `social-media-manager` (bundles)—**or** optional `social-caption-writer` |
| 4 | `bundles` | `pending` \| `complete` | `posts/<id>/post-bundle.md` + `APPROVAL.md` table filled for review | Human approval |
| 5 | `publish` | `pending` \| `complete` | Approved rows in `APPROVAL.md` with **empty** HypeEngine post UUID | `hype-engine` (POST `/posts` + **date/time**; record UUID) |

**Rules**

- Whoever finishes a phase **updates** `pipeline-state.md`: set **Status** to `complete`, set **Last updated** (ISO date) in a line under the table, and optionally add **`NEXT_PROMPT`** for the operator (one sentence: what to invoke next).
- **Immediate focus when the calendar already exists:** set step 2 → `complete`; run step 3 until every slot has copy **and** **`post-image.png`** / **`article-hero.png`** (unless text-only flagged in intake); then step 4 (bundles)—**skip** caption writer unless requested.
- **Host automation:** use **OpenClaw cron** (Gateway scheduler) so jobs persist across restarts. Official docs: [Scheduled tasks (cron)](https://docs.openclaw.ai/automation/cron-jobs). Jobs are stored at **`~/.openclaw/cron/jobs.json`**. For **what counts as “auto handoff”** (cron vs webhooks vs custom sessions), see **`multi-agent-orchestrator`** → **Automatic handoffs — what OpenClaw can (and cannot) do**.
- **CLI examples (isolated session = full agent turn with your prompt):**

```bash
# Morning: post due slots + optional trend merge (adjust tz and message)
openclaw cron add \
  --name "Social AM publish" \
  --cron "0 9 * * *" \
  --tz "America/New_York" \
  --session isolated \
  --message "Open workspace/drafts/social/<campaign>/calendar.md and APPROVAL.md. Today’s date only. Rows: Local time 09:00 (or morning slot), Approved Y, HypeEngine post UUID EMPTY. hype-engine: upload media if needed, POST /posts once per row with date+time from APPROVAL (scheduled—no separate publish-now). Skip if UUID set. Trends: 0-2 hashtags if USER.md allows."

openclaw cron add \
  --name "Social PM publish" \
  --cron "0 18 * * *" \
  --tz "America/New_York" \
  --session isolated \
  --message "Open workspace/drafts/social/<campaign>/calendar.md and APPROVAL.md. Today’s date only. Rows: Local time 18:00 (evening), Approved Y, HypeEngine UUID EMPTY. hype-engine: POST /posts once per row with date+time from APPROVAL (scheduled auto-publish). Skip if UUID set. Do not touch morning slots."

# Optional: draft a new LinkedIn article on a fixed interval (does not publish the article body via HypeEngine)
openclaw cron add \
  --name "LinkedIn article draft every 2d" \
  --every "48h" \
  --session isolated \
  --message "Run linkedin-article-writer: one new article from marketer brief + calendar themes; save under workspace/drafts/linkedin/; update publish-handoff.md if using Google Drive."

openclaw cron list
```

- **Main session** (lighter): `openclaw cron add --session main --system-event "..." --wake now` — good for reminders; **isolated** is better for end-to-end post + API work.
- Until cron is configured, use **`multi-agent-orchestrator`** templates or chat: *“Read `pipeline-state.md` in `<campaign path>` and execute the next incomplete step.”*

## Outputs (required per campaign folder)

- `00-intake.md`, `calendar.md`, `APPROVAL.md`, `README-handoff.md`
- **`pipeline-state.md`** — required when running the marketer→publish chain (so the next session knows what to do).
- Optional: **`publish-handoff.md`** / article links only — long-form **LinkedIn articles** handed to interns via Drive (`04-articles/`); feed posts do not require a Drive row.

## Agent Checklist

- [ ] Intake captured goals, platforms, compliance, deadlines.
- [ ] Every post has a unique `post id` and file path.
- [ ] **`post-body.md`** (or linked **`teaser.md`**) exists with **publish-ready** copy before bundling (or explicit defer).
- [ ] **`post-image.png`** / **`article-hero.png`** exists for each non-text-only row, or **`APPROVAL.md`** notes an explicit exception.
- [ ] If **`social-caption-writer`** was skipped: **`post-bundle.md`** still reflects final copy from the writer files.
- [ ] If caption polish was used: `captions/*.md` merged; else note “caption pass skipped.”
- [ ] Disclosure / AI-assisted / sponsored lines present when applicable.
- [ ] `APPROVAL.md` present; human sign-off assumed empty until filled.
- [ ] User told no live publish unless tools + approval satisfied; X/LinkedIn use **`hype-engine`** when posting live.
- [ ] Sub-skill outputs referenced by path, not vague “see above.”
- [ ] If using trends: **`Trend source:`** line in bundles; hashtags brand-safe and sparse.
- [ ] Cron (if used): user has **`openclaw cron list`** and Gateway running; timezone matches **Local time** on calendar; cron **message** filters by **Local time** + **empty HypeEngine post UUID** (see **`hype-engine`** idempotency).
- [ ] No duplicate HypeEngine publishes: **`HypeEngine post UUID`** filled in **`APPROVAL.md`** after each successful post.
- [ ] If **`social/drive_folder_id`** (or env) is set: used for **article** handoff (`04-articles/`) per **`INTEGRATIONS.md`**, **not** for exporting every feed **`post-bundle`** to Drive.
