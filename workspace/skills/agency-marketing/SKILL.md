---
name: agency-marketing
description: Bundle of 29 agency-style marketing personas (SEO, growth, LinkedIn, TikTok, China/social, Reddit, ASO, etc.); pick one playbook under references/ and produce dated deliverables under workspace/drafts/agency-marketing/.
metadata: {"clawdbot":{"emoji":"🏷️"},"openclaw":{"emoji":"🏷️"}}
---

# agency-marketing

Use **one persona per run** from **`references/`** (imported agency agent definitions). Each file is a full role spec: capabilities, metrics, workflows—adapt outputs to **this workspace** and **QuizFactor / USER.md** context.

## Prerequisites

- Human names the **persona** (table below) **or** describes the task and you **choose** the closest `references/*.md` file.
- Read **`USER.md`**, **`SOUL.md`**; respect claims, compliance, and geography (some personas are China-specific—only use when relevant).
- **Output root** (all artifacts for this run):
  ```text
  workspace/drafts/agency-marketing/<YYYY-MM-DD>-<persona-slug>/
  ```
- **Tools:** Web search / browse when the reference expects research; file writes under the output root only unless human provides another path.

## Credentials & API (qf-style)

- **Draft-only by default:** Strategy docs, calendars, copy—no API keys.
- **Live publish / ads:** Hand off to **`social-media-manager`**, **`hype-engine`**, **`adverts-creator`**, or **`INTEGRATIONS.md`** after human approval—not from this skill alone.

## Persona catalog → reference file

| Persona focus | File in `references/` |
|---------------|------------------------|
| AI citation / authority | `marketing-ai-citation-strategist.md` |
| Baidu SEO | `marketing-baidu-seo-specialist.md` |
| LinkedIn content | `marketing-linkedin-content-creator.md` |
| Twitter/X engagement | `marketing-twitter-engager.md` |
| TikTok | `marketing-tiktok-strategist.md` |
| General content | `marketing-content-creator.md` |
| Carousel growth | `marketing-carousel-growth-engine.md` |
| Weibo | `marketing-weibo-strategist.md` |
| Livestream commerce | `marketing-livestream-commerce-coach.md` |
| China market localization | `marketing-china-market-localization-strategist.md` |
| Growth hacking | `marketing-growth-hacker.md` |
| SEO | `marketing-seo-specialist.md` |
| Bilibili | `marketing-bilibili-content-strategist.md` |
| Xiaohongshu (Little Red Book) | `marketing-xiaohongshu-specialist.md` |
| Social media strategy | `marketing-social-media-strategist.md` |
| Instagram | `marketing-instagram-curator.md` |
| Kuaishou | `marketing-kuaishou-strategist.md` |
| Douyin | `marketing-douyin-strategist.md` |
| Video optimization | `marketing-video-optimization-specialist.md` |
| Reddit | `marketing-reddit-community-builder.md` |
| Book co-author | `marketing-book-co-author.md` |
| App Store | `marketing-app-store-optimizer.md` |
| Zhihu | `marketing-zhihu-strategist.md` |
| Podcast | `marketing-podcast-strategist.md` |
| Private domain / CRM ops | `marketing-private-domain-operator.md` |
| WeChat official account | `marketing-wechat-official-account.md` |
| China ecommerce | `marketing-china-ecommerce-operator.md` |
| Short-video editing coach | `marketing-short-video-editing-coach.md` |
| Cross-border ecommerce | `marketing-cross-border-ecommerce.md` |

## High-level Workflow

1. **Select persona**
   - Open **`workspace/skills/agency-marketing/references/<file>.md`** for the chosen row.

2. **Ingest**
   - Internalize Role, Core Capabilities, Decision Framework, and Success Metrics from that file—**do not** copy vendor-specific tool lists as mandatory (map to OpenClaw tools available).

3. **Context lock (`00-brief.md`)**
   - Goal, audience, geo, constraints, **which reference file** governs this run.

4. **Deliver**
   - Produce the concrete artifacts implied by the persona (strategy doc, calendar, thread plan, SEO outline, etc.) as markdown under the output root. Name files clearly (`strategy.md`, `calendar.md`, `hooks.md`, …).

5. **Handoff (`README-handoff.md`)**
   - What was produced, **recommended next skills** (`marketer-agent`, `social-media-manager`, `reddit-trend-poster`, `linkedin-article-writer`, …), and **approval** note before any live post.

6. **Integration with existing suite**
   - Prefer **`marketer-agent`** for cross-channel GTM + **`social-media-manager`** for execution rather than duplicating their folders—link paths in README-handoff.

## Outputs (required)

- `00-brief.md`, `README-handoff.md`, and **≥1** substantive deliverable matching the persona (e.g. `strategy.md`, `content-plan.md`).

## Agent Checklist

- [ ] Exactly **one** primary `references/*.md` file drove the run (named in `00-brief.md`).
- [ ] Outputs live under `workspace/drafts/agency-marketing/<date>-<persona-slug>/`.
- [ ] No fabricated stats; cite sources when reference expects metrics.
- [ ] China-specific playbooks used only when audience/geo fits.
- [ ] User told live publish requires approval + downstream skills/APIs.
