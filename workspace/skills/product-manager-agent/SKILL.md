---
name: product-manager-agent
description: PRDs, MVP slicing, user stories with acceptance criteria, dependency maps, roadmap views, and release-note skeletons—saved as dated markdown under workspace/drafts/product/ for engineering and design handoff.
metadata: {"clawdbot":{"emoji":"🧭"},"openclaw":{"emoji":"🧭"}}
---

# product-manager-agent

Turn **fuzzy ideas** into **ship-ready product docs**, with the same rigor as `qf-course-researcher` uses for matching courses (clear heuristics, explicit states, no ambiguous “done”). Each engagement produces a **dated folder** under `drafts/product/`.

## Prerequisites

- Inputs: problem statement, users, constraints, metrics—or `auto-research-agent` / `report.md` path.
- **Workspace:** `USER.md` for product context; output:
  ```text
  workspace/drafts/product/<YYYY-MM-DD>-<feature-slug>/
  ```

## Credentials & API (qf-style)

- **Markdown-only:** No credentials; PRDs and stories under `workspace/drafts/product/...`.
- **Optional sync:** To push issues or roadmap rows to **Notion**, use the **`notion`** skill and `~/.config/notion/api_key` (same as `qf-course-researcher`). For **Linear / Jira**, add tokens only on the host and extend **`workspace/INTEGRATIONS.md`** with env var names when you wire them.

## High-level Workflow

1. **Problem framing (`01-problem.md`)**
   - User pain, **current workaround**, why now, **non-goals**.

2. **Users and stories (`02-personas-stories.md`)**
   - Primary/secondary personas (1 paragraph each).
   - **User stories:** “As a … I want … so that …” — **minimum 5** for M-sized feature, **3** for S.

3. **MVP vs later (`03-mvp-scope.md`)**
   - **Must ship** vs **Phase 2** vs **Won’t do (v1)** with rationale.
   - **MVP test:** “Can we validate value in <2 weeks engineering?” style gate.

4. **Detailed PRD (`PRD.md`)**
   - Sections: Overview, Goals / Non-goals, User flows (numbered steps), **Edge cases**, Analytics events (name + when fired), **Open questions**.

5. **Acceptance criteria (`acceptance.md`)**
   - Per story: **Given / When / Then**; **measurable** (no “works well”).

6. **Dependencies (`dependencies.md`)**
   - Table: Dependency | Owner | Type (design, API, legal) | Risk | Mitigation.

7. **Roadmap snippet (`roadmap.md`)**
   - Now / Next / Later with **outcome** labels not just feature names.

8. **Release notes draft (`release-notes-draft.md`)**
   - User-facing **What changed**, **Improvements**, **Fixes** (placeholders OK).

9. **Handoff (`README-handoff.md`)**
   - Links to Figma/engineering ticket expectations; **review meeting** ask.

10. **Scheduling**
    - One folder per feature initiative; **revise** with `v2` suffix if major PRD update same day (rare).

## Outputs (required)

- `workspace/drafts/product/<YYYY-MM-DD>-<slug>/PRD.md`
- `01-problem.md`, `03-mvp-scope.md`, `acceptance.md`, `README-handoff.md`

## Agent Checklist

- [ ] MVP explicitly smaller than full vision; Phase 2 captured.
- [ ] Every story has testable acceptance criteria.
- [ ] Edge cases and analytics named where relevant.
- [ ] Dependencies and risks visible; no hidden “someone else” assumptions.
- [ ] User given folder path and suggested review order (01 → PRD → acceptance).
