---
name: marketer-agent
description: Marketing strategy and GTM—ICP, positioning, messaging pillars, offer and funnel map, campaign briefs, channel plan, and handoff paths to social-media-manager, adverts-creator, and linkedin-article-writer; dated packs under workspace/drafts/marketing/.
metadata: {"clawdbot":{"emoji":"📈"},"openclaw":{"emoji":"📈"}}
---

# marketer-agent

Turn **business goals** into **market-facing clarity**: who we sell to, what we say, where we show up, and how success is measured—then **hand off** executable briefs to content and ads skills.

## Prerequisites

- Inputs from human: **product** or initiative name, **goal** (awareness, leads, activation, retention), **geo**, **budget band** (optional), **constraints** (compliance, taboo claims).
- Read **`USER.md`**, **`SOUL.md`** for brand voice and claims policy.
- Optional: `auto-research-agent` **`report.md`** path for category/competitor context.
- Output root:
  ```text
  workspace/drafts/marketing/<YYYY-MM-DD>-<campaign-or-initiative-slug>/
  ```

## Credentials & API (qf-style)

- **Draft-only:** No keys; all artifacts under `workspace/drafts/marketing/...`.
- **Optional:** Sync summaries to **Notion** via **`notion`** skill; paid ad **live** execution via **`adverts-creator`** + **`INTEGRATIONS.md`**; social calendar via **`social-media-manager`**.

## High-level Workflow

1. **Brief lock (`00-brief.md`)**
   - Goal, primary **CTA**, timeline, **success metrics** (e.g. signups, trials, MQLs), non-goals.

2. **ICP (`01-icp.md`)**
   - Segments, **jobs-to-be-done**, pains, objections, buying triggers; **anti-ICP** (who not to target).

3. **Positioning (`02-positioning.md`)**
   - Category, **differentiation** (vs status quo + 1–2 named competitor archetypes if research provided), **one-line positioning**, proof types needed (data, logos, demos).

4. **Messaging pillars (`03-messaging-pillars.md`)**
   - 3–4 pillars: **headline**, proof point, example use in copy; **words to use / avoid** per `USER.md`.

5. **Offer & funnel (`04-offer-funnel.md`)**
   - Offer stack (lead magnet, trial, demo), **funnel stages**, suggested next asset per stage; alignment with product **if** `product-manager` outputs exist.

6. **Campaign concept (`05-campaign-concept.md`)**
   - Named campaign angle, **hero hook**, 2–3 supporting angles, **creative guardrails** (legal, brand).

7. **Channel plan (`06-channel-plan.md`)**
   - Table: Channel | Role (reach / nurture / convert) | Format | Cadence suggestion | **Handoff skill** (e.g. `linkedin-article-writer`, `social-media-manager`, `adverts-creator`, `tiktok-video-ads-creator`).

8. **Creative & copy briefs (`briefs/`)**
   - One file per major deliverable type: `linkedin-thought-leadership-brief.md`, `social-week-brief.md`, `paid-ads-brief.md` — each with objective, audience, **must-say**, **never-say**, CTA, **approval gate** note.

9. **Measurement (`07-metrics.md`)**
   - North star + **leading indicators**; UTM / campaign naming convention; what to report weekly.

10. **Handoff index (`README-handoff.md`)**
    - Ordered list: which skill to run next, **input paths** from this folder, expected **output paths** under `workspace/drafts/...`.

## Coordination (explicit)

| Downstream skill | Typical input from this folder |
|------------------|--------------------------------|
| `social-media-manager` | `06-channel-plan.md`, `briefs/social-week-brief.md` |
| `social-content-planning` | Pillars + calendar hints from channel plan |
| `adverts-creator` | `briefs/paid-ads-brief.md`, offer + UTM from `04` / `07` |
| `linkedin-article-writer` | `briefs/linkedin-thought-leadership-brief.md` |
| `agency-marketing` | Deep persona execution (e.g. SEO, TikTok specialist) using `references/` after strategy is set |
| `auto-research-agent` | Optional upstream; marketer consumes `report.md` |

## Outputs (required)

- `00-brief.md`, `02-positioning.md`, `03-messaging-pillars.md`, `06-channel-plan.md`, `README-handoff.md`
- At least **one** file under `briefs/`

## Agent Checklist

- [ ] ICP and positioning are **specific** (not “everyone” / “best platform”).
- [ ] Claims match evidence or are framed as opinion; no fabricated stats.
- [ ] Channel plan names **handoff skills** and file paths.
- [ ] Compliance / disclosure called out where promos or paid social apply.
- [ ] User given folder path and suggested order: brief → positioning → briefs → handoffs.
