---
name: auto-research-agent
description: Deep research runs with explicit source policy, comparison tables, confidence levels, Q&A appendix, and gap analysis—outputs a dated research pack under workspace/drafts/research/. Karpathy-style: one primary artifact per run, clear done criteria.
metadata: {"clawdbot":{"emoji":"🔎"},"openclaw":{"emoji":"🔎"}}
---

# auto-research-agent

Run **autonomous research** with **traceability**: every non-obvious claim should tie to a **source note** (URL, doc title + date, or “model inference—low confidence”). Output is a **single primary markdown report** per run (plus optional CSV), same “one dated artifact” discipline as `qf-course-researcher` uses for Notion.

## Prerequisites

- **Workspace:** read `USER.md` / `SOUL.md`; write under:
  ```text
  workspace/drafts/research/<YYYY-MM-DD>-<slug>/
  ```
- **Tools:** web search / browse when available. If **unavailable**, entire report must be labeled **INFERENCE-ONLY** in H1 banner and **no** factual “trending” or stats claims.
- **Scope:** timebox (e.g. 45 min equivalent depth), geography, language from human.

## Credentials & API (qf-style)

- **Browse / web search only:** No files required if the gateway exposes search tools (same class as `qf-course-researcher` “Web access”).
- **Optional structured search:** If you add SerpAPI, Brave Search API, etc., put keys in **`~/.openclaw/.env`** and document the variable names in **`workspace/INTEGRATIONS.md`** (add a row to the table there when you introduce one).
- **QuizFactor cross-check:** If the brief needs live course data, reuse **`qf-course-researcher`** patterns: `QF_BASE_URL` from `~/.config/quizfactor/base_url` and `GET /api/ai/courses` with Bearer if your API requires it — see **`workspace/INTEGRATIONS.md`** and `qf-course-researcher` Prerequisites.

## High-level Workflow

1. **Scope contract (`00-scope.md`)**
   - Questions answered, **out of scope**, success criteria, **stakeholder** (who uses this).

2. **Source plan**
   - List **source types** you will use: official docs, filings, academic, news (with dates), forums (low weight).
   - Set **minimum source count** (e.g. ≥8 for deep dive, ≥3 for quick brief).

3. **Gather — structured notes (`notes-raw.md`)**
   - Bullet per source: `Source:` URL or citation, `Date accessed:`, `Claim supported:`, `Confidence: high/med/low`.

4. **Synthesize — executive summary (`report.md`)**
   - **TL;DR** (5 bullets max).
   - **Key findings** with inline source markers `[S1]`, `[S2]` mapping to a **Sources** section at bottom (numbered list).

5. **Comparison tables**
   - When comparing options (tools, vendors, courses), add `comparison.csv` or markdown table:
     - Columns: Name, Pros, Cons, Cost signal, Risk, Source.

6. **Q&A appendix**
   - `qa.md`: anticipated stakeholder questions → **short answer** + pointer to section in `report.md`.

7. **Gaps and contradictions**
   - Section **Gaps:** unknowns, conflicting sources, what would change conclusion if known.

8. **Recommendations**
   - **Next steps** numbered; each **actionable** (who/what/when style, no vague “monitor”).

9. **Handoff**
   - `README-handoff.md`: which downstream skill consumes this (`product-manager-agent`, `social-trend-monitor`, `qf-course-researcher`-style workflows).

10. **Scheduling**
    - **Daily pulse** research: short slug `daily-<topic>`.
    - **Deep dive:** slug `deep-<topic>`; do not overwrite prior dated folders.

## Outputs (required)

- `workspace/drafts/research/<YYYY-MM-DD>-<slug>/report.md` (primary)
- `00-scope.md`, `notes-raw.md`, `README-handoff.md`

Optional: `comparison.csv`, `qa.md`

## Agent Checklist

- [ ] Scope file created first; stuck to scope or documented deviation.
- [ ] INFERENCE-ONLY banner if no web/tools access.
- [ ] No fabricated statistics, dates, or rankings.
- [ ] Source list numbered; report references match.
- [ ] Gaps section non-empty when data is incomplete.
- [ ] Folder path communicated to user.
- [ ] Recommendations tie to business/product/social next actions.
