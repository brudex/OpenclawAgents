---
name: social-content-planning
description: Builds rolling content calendars with pillars, format mix per platform, CTA rotation rules, asset dependency flags, and conflict checks—outputs calendar.md plus pillar-rationale for social-media-manager.
metadata: {"clawdbot":{"emoji":"🗓️"},"openclaw":{"emoji":"🗓️"}}
---

# social-content-planning

Produces **calendar artifacts** that are **executable** by downstream agents (not vague “post more”). Same specificity bar as `qf-course-researcher` (normalized fields, explicit statuses).

## Prerequisites

- From `social-media-manager` or human: **horizon** (1 week / 2 weeks / month), **platforms**, **posts per week per platform** cap.
- Optional: `social-trend-monitor` file path for topic injection.
- Output:
  ```text
  workspace/drafts/social/<campaign>/planning/calendar-<YYYY-MM-DD>.md
  ```

## Credentials & API (qf-style)

- **None for planning:** Calendars are files only. Any **live scheduling** or **CMS publish** uses the parent **`social-media-manager`** flow and host config in **`workspace/INTEGRATIONS.md`** / OpenClaw channels.

## High-level Workflow

1. **Pillar definition (`pillars.md`)**
   - 3–5 pillars; each: name, **goal** (awareness / traffic / community), **% of slots** target (should sum ~100%).

2. **Format mix matrix (`format-matrix.md`)**
   - Rows: Platform | Allowed formats (carousel, reel, thread, poll) | **Max per week**.

3. **CTA rotation (`cta-rotation.md`)**
   - List CTAs (e.g. link in bio, newsletter, product page); **rule:** no same CTA **>2 consecutive** days on same platform unless campaign exception.

4. **Build master table (`calendar.md`)**
   - Columns:

     | Slot date | Local time | Platform | Pillar | Format | Topic slug | Hook theme | CTA id | Asset type | Depends on | Post id | Draft path |

   - **Post id:** stable id for `social-media-manager` folder `posts/<post-id>/`.  
   - **Draft path:** where **`social-content-writer`** / **`x-post-writer`** saves **`post-body.md`**, or link to **`linkedin-article-writer`** (`teaser.md` / `article.md`); leave **TBD** until written. Optional **`social-caption-writer`** reads the same paths only if the human requests a polish pass.  
   - **Conflict check:** two heavy asks (e.g. full video) not same day unless resourced.

5. **Asset dependency rollup (`assets-needed.md`)**
   - Table: Date | Asset | Owner | Skill (`auto-video-generation`, `auto-image-generation`) | Due **48h before** slot.

6. **Risk flags (`risks.md`)**
   - Sensitive dates (elections, tragedies), competitor launches, **quiet periods**.

7. **Handoff**
   - `README.md` in planning folder: how `social-media-manager` consumes `calendar.md` and routes rows to **`linkedin-article-writer`** (articles), **`x-post-writer`** (X), or **`social-content-writer`** (short/multi-platform)—**not** a separate caption step by default.

8. **Scheduling**
   - Version calendar filename when **replanning** same campaign: `calendar-<YYYY-MM-DD>-v2.md`.

## Outputs (required)

- `pillars.md`, `format-matrix.md`, `calendar.md`, `assets-needed.md`, `README.md`

## Agent Checklist

- [ ] Pillar percentages roughly balanced to goals.
- [ ] Format caps respected per platform.
- [ ] CTA rotation rule documented and visible in calendar (CTA id column filled).
- [ ] Asset due dates **before** post dates.
- [ ] Risks section non-empty for visible calendar weeks (holidays etc.).
- [ ] File paths communicated to parent manager.
