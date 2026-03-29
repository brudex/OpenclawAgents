---
name: reddit-trend-poster
description: Subreddit-aware trend scanning, sentiment tables, post and comment drafts with title/body/flair templates, rule-compliance checklist, and escalation for mod mail—artifacts under workspace/drafts/reddit/; human submits posts after verifying each sub's rules.
metadata: {"clawdbot":{"emoji":"🔶"},"openclaw":{"emoji":"🔶"}}
---

# reddit-trend-poster

**Reddit** workflow with **anti-spam** discipline: same class of rigor as `qf-course-researcher` (match heuristics, explicit statuses)—here statuses are **Safe to draft** / **Needs mod approval** / **Do not post**.

## Prerequisites

- **Target subreddit list** + **rules summary** (human paste or wiki bullets).
- `USER.md`: disclosure rules for **promotional** posts.
- Tools: browse/search when available for **recent megathreads** and **sidebar rules**.
- Output:
  ```text
  workspace/drafts/reddit/<YYYY-MM-DD>-<subreddit-or-batch>/
  ```

## Credentials & API (qf-style)

- **Draft-only (default):** No Reddit app needed; all drafts under `workspace/drafts/reddit/...`. Human submits in the Reddit UI.
- **Live / automation (optional):** Reddit requires **OAuth** for most posting flows. Recommended paths and env names: **`workspace/INTEGRATIONS.md`** (`~/.config/reddit/client_id`, `client_secret`, refresh token, or `REDDIT_*`). If **OpenClaw** exposes a Reddit channel, prefer that over raw `curl`.

## High-level Workflow

1. **Sub audit (`subreddit-audit.md`)**
   - Per sub: subscriber rough tier, **self-promo rule** quote (human-provided), **flair** requirement, **karma** notes if known.

2. **Trend scan (`trend-scan.md`)**
   - Table: Thread title | URL | Age | Upvotes snapshot | **Topic cluster** | Sentiment guess | **Promo risk**.

3. **Opportunity map (`opportunities.md`)**
   - Rows where brand can add **value** (answer question, share data) vs **shill** risk.

4. **Post drafts (`posts/`)**
   - Per draft file:
     - **Title** (≤300 chars; aim shorter).
     - **Body** markdown.
     - **Flair** suggestion.
     - **Disclosure** paragraph if promotional.
     - **Rule checklist** (checkboxes: read rules, no personal info, ratio of value:promo ≥ 3:1).

5. **Comment drafts (`comments/`)**
   - Parent link + **2 reply options** (helpful, brief).

6. **No-go list (`do-not-post.md`)**
   - Subs or threads where engagement is **toxic** or **rule-breaking**.

7. **Handoff**
   - Explicit: human posts via Reddit UI or approved tooling; **no** automation unless documented.

8. **Scheduling**
   - **Daily** scan: new folder per date; **do not** spam same sub (note **cooldown** table in `subreddit-audit.md`).

## Outputs (required)

- `subreddit-audit.md`, `trend-scan.md`, at least one of `posts/` or `comments/` or documented “no safe opportunities.”

## Agent Checklist

- [ ] Every target sub has audit section.
- [ ] Promotional drafts include disclosure matching sub + law.
- [ ] Rule checklist complete on each post draft.
- [ ] do-not-post list used when in doubt.
- [ ] No brigading language; no “upvote this.”
- [ ] User told paths; reminded human verifies rules day-of post.
