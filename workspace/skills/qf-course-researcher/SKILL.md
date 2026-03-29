---
name: qf-course-researcher
description: Researches trending certification courses on the web, compares them with existing QuizFactor courses using the AI routes collection, and generates a Notion report for missing or inactive courses. Use for daily discovery of high-demand certifications to add to QuizFactor.
metadata: {"clawdbot":{"emoji":"🔎"},"openclaw":{"emoji":"🔎"}}
---

# qf-course-researcher

Discover **trending certification courses** (e.g. AWS, Azure, security, networking, DevOps) on a regular basis, compare them to what already exists in QuizFactor, and write the report to a **new dated page** under **QuizFactorA+** (e.g. **Course Research – 2026-03-14**), not to the QuizFactorA+ page itself. Each run creates its own page and database.

## Prerequisites

- **QuizFactor API**
  - Base URL config as used in other QuizFactor skills:
    ```bash
    QF_BASE_URL=$(cat ~/.config/quizfactor/base_url)
    ```
  - AI route used:
    - `GET /api/ai/courses` – for all course categories and courses.

- **Notion integration**
  - Use the existing `notion` skill.
  - Configure:
    - `~/.config/notion/api_key` – Notion API key.
    - **QuizFactorA+ parent page**: Resolve the top-level page **QuizFactorA+** (e.g. search `POST /v1/search` with `query: "QuizFactorA+"` and use the page id, or store it in `~/.config/quizfactor/notion_quizfactor_page_id`). All course research output goes under this page, not on it directly.

- **Web access**
  - The agent needs to be able to search the web (e.g. via a web search tool) for up-to-date certification trends.

- **Shared reference**
  - For a consolidated table of config paths, env vars, and curl patterns used across growth skills, see **`workspace/INTEGRATIONS.md`**.

## High-level Workflow

1. **Gather trending certification list**
   - Use web search to identify at least **20 trending certifications**, prioritizing:
     - Cloud (AWS, Azure, GCP).
     - Security (CISSP, CEH, CompTIA Security+).
     - Networking (CCNA, CCNP, etc.).
     - DevOps & automation (AWS/Azure DevOps, Kubernetes, Terraform).
   - Normalize into a list of objects:
     - `name` – e.g. `"AWS Certified Solutions Architect"`.
     - `provider` – e.g. `"AWS"`.
     - `categoryGuess` – e.g. `"Cloud Computing"`.

2. **Fetch QuizFactor courses**
   - Call:
     ```bash
     curl -X GET "$QF_BASE_URL/api/ai/courses"
     ```
   - Extract:
     - `data.courses[]` – `uuid`, `title`, `slug`, `categoryUuid`, `totalQuizzes`.
     - `data.courseCategories[]` – for mapping providers to categories.

3. **Match trending certifications to QuizFactor courses**
   - For each trending course:
     - Normalize both the trending name and QuizFactor `title` / `slug`:
       - Lowercase, strip punctuation, collapse spaces to `-`.
     - Matching heuristic:
       - Exact or near-exact match on normalized name vs. `title` or `slug`.
       - Fuzzy substring/keyword matching for cases like `"CISSP"` vs. `"Certified Information Systems Security Professional (CISSP)"`.
   - Determine status:
     - **Existing & active** – course found and appears to have quizzes (`totalQuizzes > 0`).
     - **Existing but underdeveloped** – course found but `totalQuizzes = 0`.
     - **Missing** – no reasonable match found.

4. **Map to QuizFactor categories**
   - For missing or underdeveloped certifications:
     - Map to a `courseCategories` entry using:
       - `name` or `tagName` containing or matching `categoryGuess`.
     - If no good match:
       - Mark `Category` as `"Unmapped"` but still report in Notion.

5. **Create a new report page under QuizFactorA+**
   - **Do not** write results directly to the top-level QuizFactorA+ page.
   - Resolve the **QuizFactorA+** page id (search Notion for `"QuizFactorA+"` or read from `~/.config/quizfactor/notion_quizfactor_page_id`).
   - Create a **new child page** under QuizFactorA+ with title:
     - **Course Research – {Today's Date}**
     - Use a clear date format, e.g. `Course Research – 2026-03-14` or `Course Research – March 14, 2026`.
   - Use `POST /v1/pages` with:
     - `parent`: `{"page_id": "QUIZFACTOR_A_PLUS_PAGE_ID"}`
     - `properties`: set the page title to the string above.
   - Save the new page’s `id` for the next step.

6. **Create the Course Research database and write rows**
   - **Colored tags in Notion** only appear when a property is **Select** or **Multi-select** and its options include a `color` in the schema. If Category or Provider are created as `rich_text` or as Select without predefined colored options, the table will show plain text with no coloring.
   - Create a **data source (database)** as a child of the new page from step 5:
     - `POST /v1/data_sources` with `parent`: `{"page_id": "NEW_PAGE_ID"}`.
     - Title the database (e.g. "Course Research" or use the same date).
     - **Use Select (with colored options) for Category and Provider** so Notion shows colored tags. Do **not** use `rich_text` for these, or tags will appear as plain text with no coloring. When defining the database, set `options` on each select property with a `color` for each option (Notion colors: `default`, `gray`, `brown`, `orange`, `yellow`, `green`, `blue`, `purple`, `pink`, `red`). Example: `"Category": {"select": {"options": [{"name": "Cloud Computing", "color": "blue"}, {"name": "Cybersecurity", "color": "orange"}, {"name": "DevOps & Automation", "color": "purple"}, {"name": "Networking & Infrastructure", "color": "purple"}, {"name": "Unmapped", "color": "gray"}]}}`, and `"Provider"` (or `"Source"`) as select with options for common vendors (e.g. AWS, Cisco, Docker, HashiCorp, CompTIA) each with a `color`. Other properties: `Name` (title), `Status` (select: Missing/Inactive/Existing), `Notes` (rich_text).
   - For each trending certification, create a **row** in this database:
     - `POST /v1/pages` with `parent`: `{"database_id": "NEW_DATABASE_ID"}`.
     - `Name` – certification name.
     - `Status` – `{"select": {"name": "Missing"}}` (or Inactive/Existing).
     - `Category` – `{"select": {"name": "Cloud Computing"}}` (or the matching category name from your predefined options).
     - `Provider` – `{"select": {"name": "Docker"}}` (or the matching provider; use the predefined option name so the tag gets the color).
     - `Notes` – rich text commentary.
   - After finishing, confirm in the user-facing message that the report was written to the **new page** “Course Research – {date}” under QuizFactorA+, not to QuizFactorA+ itself.

7. **Scheduling**
   - This skill is designed to run **daily** (or on a schedule). Each run creates a **new** dated page and database, so no deduplication of rows is required across runs; each run is self-contained on its own page.

## Agent Checklist

- [ ] Use web search to compile at least 20 trending certification names with basic metadata.
- [ ] Call `GET /api/ai/courses` to load all QuizFactor courses and categories.
- [ ] For each trending certification: match to a QuizFactor course, classify as `Existing` / `Inactive` / `Missing`, and map to a category where possible.
- [ ] Resolve the QuizFactorA+ page id (search or config).
- [ ] Create a **new** child page under QuizFactorA+ titled **Course Research – {Today's Date}** (e.g. `Course Research – 2026-03-14`).
- [ ] Create a Course Research data source with **Select** properties for Category and Provider that include **options with `color`** (so Notion shows colored tags), plus Name, Status, Notes.
- [ ] For each certification, add a row to that database with status and notes.
- [ ] Tell the user the report was written to the new page “Course Research – {date}” under QuizFactorA+, not to the top-level QuizFactorA+ page.

