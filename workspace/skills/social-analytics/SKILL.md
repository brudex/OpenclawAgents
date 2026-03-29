---
name: social-analytics
description: Turns raw metrics exports or pasted numbers into normalized tables, period-over-period deltas, top/bottom content diagnosis, and a prioritized experiment backlog—writes analytics-<period>.md under workspace/drafts/social/analytics/ for social-media-manager.
metadata: {"clawdbot":{"emoji":"📊"},"openclaw":{"emoji":"📊"}}
---

# social-analytics

**Analytics** with **no hallucinated metrics**—same honesty standard as `qf-course-researcher` citing sources: every number traces to an input file or paste.

## Prerequisites

- **Input:** CSV path, screenshot list, or pasted table from human; **date range** and **platform**.
- If no data: output **template only** stating “insufficient data.”
- Output:
  ```text
  workspace/drafts/social/analytics/<YYYY-MM-DD>-<period-label>.md
  ```

## Credentials & API (qf-style)

- **Default:** Human supplies **exports or pasted tables** — no API keys.
- **Automated insights (optional):** Platform APIs (e.g. Meta **Insights**, LinkedIn **Organization** metrics) need app + tokens; align with **`workspace/INTEGRATIONS.md`** and prefer **OpenClaw**-connected channels when they can fetch metrics. Do not invent numbers — every value must trace to an export or API response documented in `data-sources.md`.

## High-level Workflow

1. **Data manifest (`data-sources.md`)**
   - List each file/snippet: platform, date range, metric definitions (reach vs impressions).

2. **Normalize (`metrics-normalized.csv`)**
   - Columns: date, platform, post_id, metric_name, value, unit.

3. **Period compare**
   - **WoW** or **MoM** table: Metric | Current | Previous | Δ% | Notes.

4. **Top / bottom (`content-leaders.md`)**
   - Top **5** and bottom **5** posts with **hypothesis** per row (hook, format, time, topic).

5. **Funnel / goals (if KPIs provided)**
   - Link posts to outcomes if UTM or conversion data exists; else **omit** section.

6. **Experiment backlog (`experiments.md`)**
   - Table: Idea | Hypothesis | Metric | Effort S/M/L | Priority P1–P3.

7. **Recommendations for planning**
   - 3 bullets for `social-content-planning` (pillar shift, format mix, CTA change).

8. **Scheduling**
   - **Weekly** default filename `week-YYYY-Www.md`; **monthly** `month-YYYY-MM.md`.

## Outputs (required)

- `analytics-<period>.md` containing embedded tables or links to `metrics-normalized.csv`, `experiments.md`.

## Agent Checklist

- [ ] Every numeric claim traceable to input manifest.
- [ ] Δ% uses same denominator rules; footnote if platforms changed definition.
- [ ] Top/bottom lists not empty when data has >5 posts; else explain.
- [ ] Experiments are testable (one variable preferred).
- [ ] Clear “no data” path without fabricating benchmarks.
