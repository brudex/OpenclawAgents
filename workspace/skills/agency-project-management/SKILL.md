---
name: agency-project-management
description: Six agency-style PM personas (senior PM task breakdown, project shepherd, Jira steward, experiment tracker, studio ops, studio producer); full playbooks in references/; outputs under workspace/drafts/agency-project-management/.
metadata: {"clawdbot":{"emoji":"📋"},"openclaw":{"emoji":"📋"}}
---

# agency-project-management

Use **one persona per run** from **`references/`**. Imported definitions may mention other repos (`ai/memory-bank`, Laravel, Jira)—**map paths** to this workspace and OpenClaw unless the human supplies a real project path.

## Prerequisites

- Human picks **persona** (table below) **or** you infer from the ask.
- Read **`USER.md`**, **`AGENTS.md`** when shaping comms and gates.
- **Output root:**
  ```text
  workspace/drafts/agency-project-management/<YYYY-MM-DD>-<persona-slug>/
  ```

## Path adaptation (critical)

- **`project-manager-senior.md`** references `ai/memory-bank/site-setup.md` and `ai/memory-bank/tasks/...` — treat as **templates**. Write task lists to:
  ```text
  workspace/drafts/agency-project-management/<run>/tasks/<project-slug>-tasklist.md
  ```
  If a real spec exists elsewhere, human must provide its path; **quote** requirements from that file, don’t invent scope.
- Ignore or generalize stack-specific lines (FluxUI, Playwright scripts, `&` background processes) unless the human’s project actually uses them—keep **realistic scope** and **checklist acceptance criteria** from the reference.

## Credentials & API (qf-style)

- **Markdown / planning:** No keys.
- **Jira / Linear / Notion:** If **`project-management-jira-workflow-steward`** flows need live APIs, use **`workspace/INTEGRATIONS.md`** and optional **`notion`** skill—only after human confirms.

## Persona catalog → reference file

| Persona | File in `references/` |
|---------|------------------------|
| Senior PM — spec → tasks, realistic scope | `project-manager-senior.md` |
| Cross-functional shepherd, charter, risks | `project-management-project-shepherd.md` |
| Jira workflow / board hygiene | `project-management-jira-workflow-steward.md` |
| Experiments, A/B tracking | `project-management-experiment-tracker.md` |
| Studio operations | `project-management-studio-operations.md` |
| Studio producer (delivery, timelines) | `project-management-studio-producer.md` |

## High-level Workflow

1. **Select persona** — Open the matching **`references/*.md`** file.

2. **Context (`00-charter.md` or `00-brief.md`)**
   - Problem, scope, stakeholders, **reference file name**, success criteria.

3. **Execute persona deliverables**
   - Examples: task breakdown + acceptance criteria (Senior PM); project charter + RAID log (Shepherd); Jira workflow doc (Steward); experiment log (Tracker); ops runbook (Studio Ops); milestone plan (Producer).

4. **Alignment with in-repo PM skill**
   - For **PRDs / user stories / roadmap** product work, prefer or hand off to **`product-manager-agent`** / **`product-manager`**; this skill keeps **agency PM personas** distinct.

5. **Handoff (`README-handoff.md`)**
   - Files produced, owners, next actions, **approval** gates.

## Outputs (required)

- `00-charter.md` **or** `00-brief.md`, `README-handoff.md`, and **≥1** core artifact (e.g. `tasks/<slug>-tasklist.md`, `charter.md`, `experiment-log.md`, `jira-workflow.md`).

## Agent Checklist

- [ ] One primary `references/*.md` identified in the brief.
- [ ] All paths under `workspace/drafts/agency-project-management/...` unless human overrode.
- [ ] No gold-plated scope; gaps called out explicitly.
- [ ] Jira/API steps only if configured and approved.
- [ ] User given folder path and suggested handoff to engineering or `product-manager-agent` when relevant.
