---
name: product-manager
description: Product manager — PRDs, MVP scope, user stories, acceptance criteria, roadmaps, and release-note skeletons; same workflow and outputs as product-manager-agent under workspace/drafts/product/.
metadata: {"clawdbot":{"emoji":"🧭"},"openclaw":{"emoji":"🧭"}}
---

# product-manager

**Role:** Product manager for planning, documentation, and engineering handoff.

## Execution

1. Open **`workspace/skills/product-manager-agent/SKILL.md`** and follow it **exactly**: Prerequisites, High-level Workflow, Outputs, and Agent Checklist.
2. Use the same output root:
   ```text
   workspace/drafts/product/<YYYY-MM-DD>-<feature-slug>/
   ```

## Credentials & API (qf-style)

Same as **`product-manager-agent`**: markdown-only by default; optional **Notion** / **Linear** / **Jira** per **`workspace/INTEGRATIONS.md`** and that skill’s Credentials section.

## Note

This entry exists so chat and subagent labels can say **“product manager”** while logic stays **single-sourced** in **`product-manager-agent`**. If sibling `SKILL.md` is unreadable, still produce the **required** artifacts named there (`PRD.md`, `01-problem.md`, `03-mvp-scope.md`, `acceptance.md`, `README-handoff.md`).
