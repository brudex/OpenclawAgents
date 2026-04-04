---
name: multi-agent-orchestrator
description: Defines DAG-style multi-skill runs with explicit input/output paths, approval gates between steps, failure rollback notes, and a run log markdown—writes to workspace/drafts/orchestration/; complements social-media-manager for cross-domain chains.
metadata: {"clawdbot":{"emoji":"🧩"},"openclaw":{"emoji":"🧩"}}
---

# multi-agent-orchestrator

**Meta-orchestration** for **SkillsToAdd.md** chains: explicit **DAG**, **files in / files out**, **gates**—same clarity as `qf-course-researcher` step list (web → API → Notion rows).

**Execution note:** Skills are **not** auto-invoked by the filesystem. “Wiring” = **shared paths** (`README-handoff.md`, `calendar.md`, `pipeline-state.md`, `APPROVAL.md`) + **you** (or **OpenClaw cron**) running the next skill. The canonical social DAG lives in **`chain-templates/social-feed-pipeline.md`**; **`social-media-manager`** lists the same order in **`pipeline-state.md`**.

## Automatic handoffs — what OpenClaw can (and cannot) do

| Mechanism | What it does | Feels like “auto handoff”? |
|-----------|----------------|----------------------------|
| **Built-in skill chaining** | None. Finishing `marketer-agent` does **not** enqueue `social-media-manager`. | No |
| **Cron** (`openclaw cron add`) | Gateway wakes on a schedule and runs an **isolated** or **main** session with your **`--message`**. That message can say: *read `pipeline-state.md`, run the next incomplete step, update the file.* | **Yes** — if you encode “next step” in the prompt |
| **Webhooks** (`hooks` in config) | `POST /hooks/agent` or `/hooks/wake` starts a turn (e.g. CI or n8n after a file lands in Drive). | **Yes** — event-driven |
| **Custom session** (`--session session:social-pipeline`) | Same session id across recurring cron runs so the agent **remembers** prior RUNLOG / pipeline state (within retention). | **Yes** — for multi-day chains |
| **One giant cron message** | “Do steps 3→4→5 in one turn.” | Possible but **fragile** (timeouts, gates, token limits); prefer **one step per job** or explicit checklist in one message |

**Practical pattern for your social pipeline**

1. **Cron job A (e.g. weekly):** `--message` = *Open `workspace/drafts/social/<campaign>/pipeline-state.md`. If `calendar` is incomplete, run social-media-manager + social-content-planning; else if `post_bodies` incomplete, run writers for missing rows; append RUNLOG.*  
2. **Cron job B + C (AM/PM):** *Only* publish approved rows via **`hype-engine`** (already in **`social-media-manager`** examples).  
3. Keep **`APPROVAL.md`** as the **human gate** so cron does not post without approved rows.

**Docs:** [Scheduled tasks (cron)](https://docs.openclaw.ai/automation/cron-jobs) · [Webhooks](https://docs.openclaw.ai/automation/cron-jobs#webhooks) (same page) · `openclaw cron list` / `openclaw cron add --help`

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
   - `chain-research-pm.md` — `auto-research-agent` → `product-manager-agent` (or `product-manager`)
   - `chain-research-marketer.md` — `auto-research-agent` → `marketer-agent`
   - `chain-marketer-social.md` — `marketer-agent` → `social-media-manager` → optional `adverts-creator`
   - `chain-pm-marketer.md` — `product-manager-agent` → `marketer-agent` (launch messaging after PRD)
   - `chain-agency-marketing-execution.md` — `agency-marketing` (persona) → `marketer-agent` → `social-media-manager`
   - `chain-agency-pm-delivery.md` — `agency-project-management` (shepherd or senior PM) → `product-manager-agent` (PRD) as needed
   - `chain-trend-tiktok.md` — `social-trend-monitor` → `tiktok-video-ads-creator`
   - `chain-image-ads.md` — `auto-image-generation` → `adverts-creator`
   - `chain-li-social.md` — `linkedin-article-writer` → `social-media-manager`
   - `chain-social-feed-full.md` — `marketer-agent` → `social-media-manager` (calendar) → post bodies (`linkedin-article-writer` / `x-post-writer` / `social-content-writer` / `agency-marketing`) → *optional* `social-caption-writer` → `hype-engine` (after approval). Concrete file: **`chain-templates/social-feed-pipeline.md`**.
   - `chain-video-tiktok.md` — `auto-video-generation` → `tiktok-video-ads-creator`
   - **QuizFactor:** reference existing `qf-*` instead of duplicating.

5. **Run log (`RUNLOG.md`)**
   - Append-only: timestamp, step, status, output path, errors.

6. **Rollback (`rollback.md`)**
   - If step K fails: which files are **stale**; what to **re-run**.

7. **Completion message**
   - User: start at `steps/01-...` and follow order; **stop at gates**.

8. **Scheduling**
   - **Cron-style** note in charter if daily/weekly — use **`openclaw cron add`** (see **Automatic handoffs** above), not a fictional built-in chain.

## Outputs (required)

- `00-charter.md`, `dag.md`, `steps/` directory with ≥1 step file, `RUNLOG.md`, `README-handoff.md`

## Agent Checklist

- [ ] Every step has readable inputs (not vague “data”).
- [ ] Every output path is under `workspace/drafts/...` or explicit tool destination.
- [ ] Gates labeled; destructive steps flagged.
- [ ] qf-* chains not re-specified in full—point to existing skills.
- [ ] RUNLOG template initialized with run id.
- [ ] User instructed to execute steps sequentially unless parallel safe.
