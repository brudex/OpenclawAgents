---
name: linkedin-article-writer
description: Long-form LinkedIn articles with H2 outline, TL;DR, teaser post under ~700 chars, optional carousel slide list, and source bibliography—saved under workspace/drafts/linkedin/; no publishing without human action.
metadata: {"clawdbot":{"emoji":"💼"},"openclaw":{"emoji":"💼"}}
---

# linkedin-article-writer

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

- **Draft-only:** No credentials; write `article.md`, `teaser.md`, etc. under the path above. Human publishes.
- **Live (optional):** Prefer an **OpenClaw LinkedIn channel** if configured. Otherwise store a long-lived token securely, e.g. `~/.config/linkedin/access_token` or `LINKEDIN_ACCESS_TOKEN` in `~/.openclaw/.env` — see **`workspace/INTEGRATIONS.md`**. UGC / Marketing API payloads follow [LinkedIn’s current API docs](https://learn.microsoft.com/en-us/linkedin/); do not commit tokens or paste them into skill files.

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
   - “Publish via LinkedIn UI; scheduling optional.”

10. **Scheduling**
    - Series: `part-1`, `part-2` slugs; cross-link in article foot.

## Outputs (required)

- `article.md`, `teaser.md`, `outline.md`, `README-handoff.md`

## Agent Checklist

- [ ] Thesis and outline exist before long draft.
- [ ] Teaser within length guide; matches article promise.
- [ ] Sources file if factual claims beyond common knowledge.
- [ ] No engagement bait structure.
- [ ] Carousel file only if requested.
- [ ] User given path; publish explicitly human.
