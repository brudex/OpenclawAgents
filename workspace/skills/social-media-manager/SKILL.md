---
name: social-media-manager
description: End-to-end social orchestration—intake, calendar integration with social-content-planning, copy via social-caption-writer, engagement drafts via social-community-engagement, performance readouts via social-analytics, and trend injection via social-trend-monitor. Outputs dated bundles under workspace/drafts/social/ with explicit approval gates before any publish.
metadata: {"clawdbot":{"emoji":"📱"},"openclaw":{"emoji":"📱"}}
---

# social-media-manager

The **parent** social agent: owns **consistency** (voice, CTA ladder, disclosure) and **file-based handoffs** to sub-skills—mirroring how `qf-course-researcher` orchestrates web → API → Notion with explicit steps.

## Prerequisites

- Read `USER.md`, `SOUL.md`, `AGENTS.md` (group vs main session rules).
- **Default output root:**
  ```text
  workspace/drafts/social/<YYYY-MM-DD>-<campaign-slug>/
  ```
- **Publish policy:** default **draft-only**; auto-post only if human has documented allowlist in workspace (e.g. `TOOLS.md` or `USER.md`).

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
     - Columns: Date | Platform | Format | Topic slug | CTA type | Asset needs | Owner.

4. **Per-slot production loop**
   For each calendar row:
   - **Brief** → `social-caption-writer` (save `captions/<date>-<platform>-<slug>.md`).
   - **Visual** → `auto-image-generation` or `auto-video-generation` brief paths in `assets-needed.md`.
   - **Bundle** → `posts/<id>/post-bundle.md`: hook, body, hashtags, suggested time, **disclosure line**, link placeholders.

5. **Engagement queue**
   - If community work requested: `social-community-engagement` outputs under `replies/`.

6. **Analytics loop**
   - When metrics provided: `social-analytics` → `analytics/<period>-summary.md`; feed **next calendar** adjustments.

7. **Approval package (`APPROVAL.md`)**
   - Table: Post ID | Platform | Preview link or file path | **Approved Y/N** | Publisher | **Go-live datetime** (empty until human fills).

8. **Live publish (X + LinkedIn only, after approval)**
   - For rows where Platform is **twitter_x** or **linkedin_feed** and **Approved Y/N** is yes: run **`hype-engine`** — list accounts, map UUIDs, create draft/scheduled/published post per `APPROVAL.md` datetime. Log HypeEngine **post UUID** (or id returned by API) back into `APPROVAL.md` or `publish-log.md` in the same campaign folder.
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
| `social-caption-writer` | Raw copy per slot |
| `social-community-engagement` | Reply drafts |
| `social-analytics` | Readout markdown |
| `social-trend-monitor` | Trend brief file |
| `hype-engine` | Live **Twitter/X** and **LinkedIn feed** posts after approval (Accounts + Posts API) |

## Outputs (required per campaign folder)

- `00-intake.md`, `calendar.md`, `APPROVAL.md`, `README-handoff.md`

## Agent Checklist

- [ ] Intake captured goals, platforms, compliance, deadlines.
- [ ] Every post has a unique `post id` and file path.
- [ ] Caption files exist for each scheduled slot (or explicit “defer” note).
- [ ] Disclosure / AI-assisted / sponsored lines present when applicable.
- [ ] `APPROVAL.md` present; human sign-off assumed empty until filled.
- [ ] User told no live publish unless tools + approval satisfied; X/LinkedIn use **`hype-engine`** when posting live.
- [ ] Sub-skill outputs referenced by path, not vague “see above.”
