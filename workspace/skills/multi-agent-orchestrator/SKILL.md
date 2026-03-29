---
name: multi-agent-orchestrator
description: Defines DAG-style multi-skill runs with explicit input/output paths, approval gates between steps, failure rollback notes, and a run log markdown—writes to workspace/drafts/orchestration/; complements social-media-manager for cross-domain chains.
metadata: {"clawdbot":{"emoji":"🧩"},"openclaw":{"emoji":"🧩"}}
---

# multi-agent-orchestrator

**Meta-orchestration** for **SkillsToAdd.md** chains: explicit **DAG**, **files in / files out**, **gates**—same clarity as `qf-course-researcher` step list (web → API → Notion rows).

## Prerequisites

- Human: **goal**, **deadline**, **risk tolerance** (can any step auto-execute?).
- List of **available skills** in workspace `skills/` (read names from folders).
- Output:
  ```text
  workspace/drafts/orchestration/<YYYY-MM-DD>-<run-slug>/
  ```

## Credentials & API (qf-style)

- **Orchestration docs only:** The DAG does not require secrets by itself.
- **Per-step needs:** When a step lists “Tool/API”, resolve credentials via **`workspace/INTEGRATIONS.md`** and the **target skill’s** “Credentials & API” section (`qf-course-researcher`, `notion`, `adverts-creator`, etc.).

## High-level Workflow

1. **Run charter (`00-charter.md`)**
   - Objective, success metric, **out of scope**, **owner** human.

2. **DAG (`dag.mmd` or `dag.md`)**
   - Mermaid or numbered list: `Step N: skill → reads → writes`.

3. **Step specs (`steps/`)**
   - One file per step `01-<skill>.md`:
     - **Inputs:** exact paths or “TO BE PRODUCED BY STEP N-1”
     - **Outputs:** exact paths
     - **Tool/API** needs
     - **Approval gate:** `none` | `human` | `human+legal`

4. **Recommended chains (templates)**
   - `chain-research-pm.md` — `auto-research-agent` → `product-manager-agent`
   - `chain-trend-tiktok.md` — `social-trend-monitor` → `tiktok-video-ads-creator`
   - `chain-image-ads.md` — `auto-image-generation` → `adverts-creator`
   - `chain-li-social.md` — `linkedin-article-writer` → `social-media-manager`
   - `chain-video-tiktok.md` — `auto-video-generation` → `tiktok-video-ads-creator`
   - **QuizFactor:** reference existing `qf-*` instead of duplicating.

5. **Run log (`RUNLOG.md`)**
   - Append-only: timestamp, step, status, output path, errors.

6. **Rollback (`rollback.md`)**
   - If step K fails: which files are **stale**; what to **re-run**.

7. **Completion message**
   - User: start at `steps/01-...` and follow order; **stop at gates**.

8. **Scheduling**
   - **Cron-style** note in charter if daily/weekly (human configures OpenClaw cron).

## Outputs (required)

- `00-charter.md`, `dag.md`, `steps/` directory with ≥1 step file, `RUNLOG.md`, `README-handoff.md`

## Agent Checklist

- [ ] Every step has readable inputs (not vague “data”).
- [ ] Every output path is under `workspace/drafts/...` or explicit tool destination.
- [ ] Gates labeled; destructive steps flagged.
- [ ] qf-* chains not re-specified in full—point to existing skills.
- [ ] RUNLOG template initialized with run id.
- [ ] User instructed to execute steps sequentially unless parallel safe.
