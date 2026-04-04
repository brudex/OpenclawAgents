---
name: social-media-manager
description: Social calendar (~2-week batches), AM/PM slots, optional trend hashtags before hype-engine publish; LinkedIn/X feed via HypeEngine; articles hand off to human/Drive. OpenClaw cron examples in skill body.
metadata: {"clawdbot":{"emoji":"📱"},"openclaw":{"emoji":"📱"}}
---

# social-media-manager

The **parent** social agent: owns **consistency** (voice, CTA ladder, disclosure) and **file-based handoffs** to sub-skills—mirroring how `qf-course-researcher` orchestrates web → API → Notion with explicit steps.

## Operator summary (canonical playbook)

1. **Batch write (~2 weeks):** Using **`calendar.md`**, **`x-post-writer`** and **`social-content-writer`** (LinkedIn **feed** slots) generate **all** scheduled posts **in advance** under the campaign folder—no “write at publish time” unless the human overrides.
2. **Approve:** Fill **`APPROVAL.md`** with **Approved Y/N** and **go-live datetime** matching each row’s **Local time** (e.g. morning `09:00`, evening `18:00`).
3. **Cron (twice daily):** OpenClaw **Cron jobs** (Gateway menu / `openclaw cron`) run **two** recurring jobs (AM + PM). Each run **only** selects the next due, **already-written** slot and publishes via **`hype-engine`**—it does **not** invent new topics.
4. **Trends:** Before each publish run, optionally refresh or read **`social-trend-monitor`** and merge **0–2 vetted** trending hashtags into **X** and **LinkedIn feed** copy (see below).
5. **LinkedIn articles:** Handled by **`linkedin-article-writer`** on a **separate cadence** (~every 2 days); long-form body is **saved** (workspace + optional **Google Drive** `04-articles/` per **`INTEGRATIONS.md`**). **HypeEngine** publishes **`teaser.md`** to the **feed**; **article** body → **employees** via Drive + LinkedIn UI until API support is explored.

**OpenClaw:** [Cron documentation](https://docs.openclaw.ai/automation/cron-jobs) · jobs persist in **`~/.openclaw/cron/jobs.json`**. Finish skill setup first, then add cron so execution does not depend on manual chat triggers.

## Prerequisites

- Read `USER.md`, `SOUL.md`, `AGENTS.md` (group vs main session rules).
- **Google Drive (optional — employee posting):** If **`~/.config/social/drive_folder_id`** or **`SOCIAL_POSTING_DRIVE_FOLDER_ID`** is set (see **`workspace/INTEGRATIONS.md`** → *Google Drive — social posting handoff*), then:
  - **Read:** At **intake**, pull any team files the folder allows (guidelines, spreadsheet calendar, approved edits) and summarize into **`00-intake.md`** with Drive paths.
  - **Save:** After **`post-bundle.md`** is ready for humans, **export** copy to **`03-ready-to-post/`** as Google Docs (host **`gws-docs-write`** / **`gws-drive-upload`** or manual upload) and add links to **`drive-handoff.md`** in the campaign folder so **employees** can post without hunting the repo. Auto-publish via **`hype-engine`** can still run in parallel when **`APPROVAL.md`** says so.
- **Default output root:**
  ```text
  workspace/drafts/social/<YYYY-MM-DD>-<campaign-slug>/
  ```
- **Publish policy:** default **draft-only**; auto-post only if human has documented allowlist in workspace (e.g. `TOOLS.md` or `USER.md`).

## Cadence: two-week batch + twice daily (AM / PM)

- **Planning:** Build **`calendar.md`** for the next **~14 days** from marketer + **`social-content-planning`**.
- **Writing:** **`social-content-writer`** / **`x-post-writer`** (and **`linkedin-article-writer`** for articles) fill **`post-body.md`** / LinkedIn draft paths **ahead** of publish—e.g. batch “week 1–2” copy in one pass.
- **Calendar column:** add **Local time** (or **Slot**) per row, e.g. **`09:00`** and **`18:00`** for **morning** and **evening** posts. **`hype-engine`** `date` + `time` must match **`APPROVAL.md`**.
- **At publish time:** read the **approved** `post-bundle.md` for that slot only—do not improvise a different topic.

## Trending hashtags before X / LinkedIn feed posts

- When the human wants **live trends** in the copy: run or refresh **`social-trend-monitor`** (or read the latest file under `workspace/drafts/social/trends/`).
- **Merge rule:** add **0–2** hashtags or phrases that pass **brand fit** and **risk** from the trend brief—**no** spam-stacking; **no** unrelated viral tags.
- Record in **`post-bundle.md`** a line **`Trend source:`** + file path and which tags were added so publishes are auditable.

## Credentials & API (qf-style)

- **Draft-only:** No secrets; all bundles under `workspace/drafts/social/...` as above.
- **Twitter/X + LinkedIn (live post):** When publishing approved slots for **`twitter_x`** or **`linkedin_feed`**, use the **`hype-engine`** skill: Accounts API → Posts API with the correct account UUIDs (`~/.config/hype-engine/*`). Do not use raw LinkedIn or X API from this workflow unless HypeEngine is unavailable and **`TOOLS.md` / `USER.md`** explicitly allows a fallback.
- **Other live publish / analytics:** **OpenClaw channels** in `~/.openclaw/openclaw.json` when configured (Telegram, Discord, etc.) where the team uses them.
- **Per-platform API keys** (Meta, Google Ads, TikTok Marketing, Reddit, direct LinkedIn if fallback): use **`workspace/INTEGRATIONS.md`**. Sub-skills (`adverts-creator`, …) spell out which service each needs.

## High-level Workflow

1. **Intake (`00-intake.md`)**
   - Capture: goals, KPIs, platforms, **blacklist topics**, **legal/compliance** (region, disclaimers), **deadlines**, asset links.
   - Optional: path to **`marketer-agent`** output (`workspace/drafts/marketing/.../README-handoff.md` or `06-channel-plan.md`) to align pillars and CTAs.

2. **Trend pass (optional)**
   - Invoke or simulate `social-trend-monitor` → save `trends-in.md` reference in folder.

3. **Calendar (`calendar.md`)**
   - Produce or merge output from `social-content-planning`:
     - Columns: **Date** | **Local time** (e.g. `09:00` / `18:00` for twice daily) | **Platform** | **Format** | **Topic slug** | **CTA type** | **Asset needs** | **Owner** | **Post id** | **Draft path** (optional: where the feed writer will save `post-body.md`).
   - Calendar rows are **schedule + intent** (“shadows”); they are **not** a substitute for full post copy.

4. **Per-slot production loop (order is mandatory)**
   For each calendar row:
   - **4a — Publish-ready copy first:** Use the **one** writer that matches the slot (writers include **hashtags / thread layout** in-file by default—**no separate caption step** unless the human opts in):
     - **LinkedIn article (long-form):** **`linkedin-article-writer`** only → **Draft path** → `workspace/drafts/linkedin/...` (`article.md` + **`teaser.md`** for feed promo).
     - **X only:** **`x-post-writer`** → `posts/<post-id>/post-body.md`.
     - **Short LinkedIn feed, Reddit, Facebook, mixed calendar:** **`social-content-writer`** → `posts/<post-id>/post-body.md` (or platform-specific notes inside file).
     - **Fallback:** `agency-marketing` persona if no dedicated skill fits—still require **`post-body.md`** with publish-ready sections.
   - **4b — Optional caption polish:** Only if the human asks: `social-caption-writer` → `captions/<date>-<platform>-<slug>.md` (otherwise skip).
   - **4c — Visuals:** `auto-image-generation` or `auto-video-generation` per `assets-needed.md` when applicable.
   - **4d — Bundle:** `posts/<post-id>/post-bundle.md`: final body + hashtags + suggested time + **disclosure line** — source = **`post-body.md`** and/or **`teaser.md`**, plus optional caption file if 4b ran.

5. **Engagement queue**
   - If community work requested: `social-community-engagement` outputs under `replies/`.

6. **Analytics loop**
   - When metrics provided: `social-analytics` → `analytics/<period>-summary.md`; feed **next calendar** adjustments.

7. **Approval package (`APPROVAL.md`)**
   - Table: Post ID | Platform | Preview link or file path | **Approved Y/N** | Publisher | **Go-live datetime** (empty until human fills).

8. **Live publish (X + LinkedIn feed only, after approval)**
   - For rows where Platform is **twitter_x** or **linkedin_feed** and **Approved Y/N** is yes: run **`hype-engine`** — list accounts, map UUIDs, create draft/scheduled/published post per `APPROVAL.md` datetime (AM/PM slots). If **trend hashtags** are enabled, merge vetted tags from **`social-trend-monitor`** output into the HTML body **before** the API call. Log HypeEngine **post UUID** (or id returned by API) back into `APPROVAL.md` or `publish-log.md`.
   - **LinkedIn long-form articles** are **not** assumed to publish through HypeEngine; see **`hype-engine`** → *LinkedIn: feed post vs long-form article*.
   - Other platforms: unchanged (drafts only, or channels/APIs per `INTEGRATIONS.md` / `TOOLS.md`).

9. **Close-out message to user**
   - List **exact paths** created; state **nothing was published** unless step 8 ran or another approved tool executed.

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
| `hype-engine` | Live **Twitter/X** and **LinkedIn feed** posts after approval (Accounts + Posts API) |

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
| 3 | `post_bodies` | `pending` \| `complete` | Every slot: `posts/<id>/post-body.md` **or** LinkedIn folder with **`teaser.md`** | `social-media-manager` (bundles)—**or** optional `social-caption-writer` if human wants polish |
| 4 | `bundles` | `pending` \| `complete` | `posts/<id>/post-bundle.md` + `APPROVAL.md` table filled for review | Human approval |
| 5 | `publish` | `pending` \| `complete` | Approved rows in `APPROVAL.md` | `hype-engine` |

**Rules**

- Whoever finishes a phase **updates** `pipeline-state.md`: set **Status** to `complete`, set **Last updated** (ISO date) in a line under the table, and optionally add **`NEXT_PROMPT`** for the operator (one sentence: what to invoke next).
- **Immediate focus when the calendar already exists:** set step 2 → `complete`; run step 3 until all slots have publish-ready **`post-body.md`** or **`teaser.md`**; then step 4 (bundles)—**skip** caption writer unless requested.
- **Host automation:** use **OpenClaw cron** (Gateway scheduler) so jobs persist across restarts. Official docs: [Scheduled tasks (cron)](https://docs.openclaw.ai/automation/cron-jobs). Jobs are stored at **`~/.openclaw/cron/jobs.json`**. For **what counts as “auto handoff”** (cron vs webhooks vs custom sessions), see **`multi-agent-orchestrator`** → **Automatic handoffs — what OpenClaw can (and cannot) do**.
- **CLI examples (isolated session = full agent turn with your prompt):**

```bash
# Morning: post due slots + optional trend merge (adjust tz and message)
openclaw cron add \
  --name "Social AM publish" \
  --cron "0 9 * * *" \
  --tz "America/New_York" \
  --session isolated \
  --message "Open workspace/drafts/social/<campaign>/APPROVAL.md. For rows with today's date and morning time approved, run hype-engine. If USER.md allows trends, read latest social-trend-monitor file and merge 0-2 vetted hashtags into X/LinkedIn body only."

openclaw cron add \
  --name "Social PM publish" \
  --cron "0 18 * * *" \
  --tz "America/New_York" \
  --session isolated \
  --message "Same as morning job but evening slots in APPROVAL.md for today."

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
- Optional: **`drive-handoff.md`** — table: Post ID | Platform | Local time | **Google Doc link** (employee copy-paste) | HypeEngine status (if any).

## Agent Checklist

- [ ] Intake captured goals, platforms, compliance, deadlines.
- [ ] Every post has a unique `post id` and file path.
- [ ] **`post-body.md`** (or linked **`teaser.md`**) exists with **publish-ready** copy (hashtags in-file or documented) before bundling (or explicit defer).
- [ ] If **`social-caption-writer`** was skipped: **`post-bundle.md`** still reflects final copy from the writer files.
- [ ] If caption polish was used: `captions/*.md` merged; else note “caption pass skipped.”
- [ ] Disclosure / AI-assisted / sponsored lines present when applicable.
- [ ] `APPROVAL.md` present; human sign-off assumed empty until filled.
- [ ] User told no live publish unless tools + approval satisfied; X/LinkedIn use **`hype-engine`** when posting live.
- [ ] Sub-skill outputs referenced by path, not vague “see above.”
- [ ] If using trends: **`Trend source:`** line in bundles; hashtags brand-safe and sparse.
- [ ] Cron (if used): user has **`openclaw cron list`** and Gateway running; timezone matches **Local time** on calendar.
- [ ] If **`social/drive_folder_id`** (or env) is set: **`drive-handoff.md`** updated with Doc links for employee posting **or** note “HypeEngine-only, no Drive export.”
