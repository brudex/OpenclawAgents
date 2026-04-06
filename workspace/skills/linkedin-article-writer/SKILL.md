---
name: linkedin-article-writer
description: LinkedIn long-form articles only—~one every 2 days; article.md + teaser.md; interns post article (Drive/UI); HypeEngine (already connected) pushes teaser to LinkedIn feed after approval via social-media-manager.
metadata: {"clawdbot":{"emoji":"💼"},"openclaw":{"emoji":"💼"}}
---

# linkedin-article-writer

## Scope (read first)

- **In scope:** LinkedIn **article** editorials—`article.md`, **`teaser.md`** to promote that article on the feed, outline, sources.  
- **Out of scope:** Short **LinkedIn feed posts** that are not tied to a long article → **`social-content-writer`** (or **`x-post-writer`** / **`social-content-writer`** for other platforms). This skill is **not** a generic “LinkedIn post writer.”

**Where this sits in the pipeline:** **`social-media-manager`** + **`hype-engine`** handle **routine LinkedIn + Twitter feed** posting first (approved bundles). **This skill is the long-form tail:** produce **`article.md`**; **interns** publish the **article** in LinkedIn (and/or copy from **Google Drive** per **`publish-handoff.md`**). **`teaser.md`** is a **feed** post—after approval, it is **pushed** through the same **already-connected** HypeEngine path as other LinkedIn feed rows.

**Thought leadership** artifacts with **structure** comparable to `qf-course-researcher` (numbered workflow, explicit deliverables per step): outline → draft → teaser → optional carousel → references.

## Prerequisites

- Audience: **founder**, **exec**, **brand**, or **hiring** mode from human.
- `USER.md` tone; **no** engagement-bait (“Comment YES”, “Agree?” spam).
- Optional: `auto-research-agent` `report.md` path for citations.
- Output:
  ```text
  workspace/drafts/linkedin/<YYYY-MM-DD>-<slug>/
  ```

## Credentials & API (qf-style)

- **Draft-only:** No credentials; write `article.md`, `teaser.md`, etc. under the path above.
- **Long-form article publish (interns):** The **article** body is **not** pushed through HypeEngine. **Interns** post via **LinkedIn’s article composer** (and/or paste from a **Google Drive** Doc in **`04-articles/`**). Add **`publish-handoff.md`**: Doc link, **who publishes**, cadence (e.g. **every ~2 days**). See **`workspace/INTEGRATIONS.md`** → *Google Drive — LinkedIn articles only* (Drive is **not** used for routine feed posts—only long-form article handoff).
- **Live LinkedIn feed teaser:** **HypeEngine is already connected** to LinkedIn. After **`APPROVAL.md`** sign-off, **`social-media-manager`** runs **`hype-engine`** to **push** **`teaser.md`** as a normal **`linkedin_feed`** post (Accounts + Posts API)—same as other approved feed slots.
- **Fallback:** **OpenClaw LinkedIn channel** if documented in **`TOOLS.md`**, or **`INTEGRATIONS.md`** when HypeEngine is unavailable and humans allow it.

## Cadence (example: one article every two days)

- Base each article on **existing strategy**: **`marketer-agent`** outputs, **`calendar.md`** themes, and **`briefs/`**—do not drift off-brand.
- When the human sets a **bi-daily article** rhythm, name folders with date slugs and note the next due date in **`README-handoff.md`**.
- **Save:** always persist **`article.md`** (and assets) under `workspace/drafts/linkedin/...`; if using **Google Drive**, record the Doc link + owner in **`publish-handoff.md`** (optional **`gws-*`** skills per **`INTEGRATIONS.md`** / host tools).
- Schedule generation with OpenClaw cron: see **`social-media-manager`** → example **`LinkedIn article draft every 2d`** job (`--every 48h`).

## High-level Workflow

1. **Thesis (`00-thesis.md`)**
   - One sentence **claim** + **who it helps** + **what reader will do differently**.

2. **Outline (`outline.md`)**
   - `##` H2 list (5–9 sections); each with 3 bullet **support points**.

3. **Draft article (`article.md`)**
   - Full markdown body; **short paragraphs**; **data** only with footnote-style source links.

4. **TL;DR box**
   - Top of `article.md` after title: 3–5 bullets.

5. **Teaser post (`teaser.md`)**
   - **≤ ~700 characters**; hook + value + CTA (“link in comments” strategy if used).

6. **Carousel optional (`carousel.md`)**
   - 8–12 slides: `Slide N:` headline + 1–2 lines body.

7. **Sources (`sources.md`)**
   - Numbered list matching in-text markers if used.

8. **Compliance (`compliance.md`)**
   - **No** misleading job promises; **no** confidential employer data.

9. **Handoff**
   - **Article:** interns → LinkedIn article UI (or Drive Doc). **Teaser:** after approval, **`social-media-manager`** → **`hype-engine`** **push** (no extra LinkedIn OAuth work—connection is already in place).
   - When this run backs a **calendar slot**, put **`Draft path`** in **`calendar.md`** to `workspace/drafts/linkedin/...`. **`teaser.md`** is **publish-ready** for the feed—**`social-media-manager`** bundles and **`hype-engine`** posts it like any other **`linkedin_feed`** row. **`social-caption-writer`** is **optional** only if the human wants a separate caption pass.

10. **Scheduling**
    - Series: `part-1`, `part-2` slugs; cross-link in article foot.

## Outputs (required)

- `article.md`, `teaser.md`, `outline.md`, `README-handoff.md`
- Optional: **`publish-handoff.md`** — Drive/Docs link, owner, and “article every ~2 days” cadence when humans publish the long-form piece outside HypeEngine.

## Agent Checklist

- [ ] Thesis and outline exist before long draft.
- [ ] Teaser within length guide; matches article promise.
- [ ] Sources file if factual claims beyond common knowledge.
- [ ] No engagement bait structure.
- [ ] Carousel file only if requested.
- [ ] User given path; **article** = intern/human publish; **teaser** = HypeEngine feed push after approval (via manager).
