---
name: qf-create-courses-from-sheet
description: Reads a Google Sheet of course definitions, compares each row with existing QuizFactor courses and categories using the AI routes, and creates missing categories and courses via dedicated QuizFactor endpoints. Use when bulk-creating or syncing courses from a spreadsheet into QuizFactor.
metadata: {"clawdbot":{"emoji":"📊"}}
---

# qf-create-courses-from-sheet

Use a **Google Sheet** as the source of truth for courses, and sync it into QuizFactor by creating any missing categories and courses. The sheet must have a **Status** column: the skill sets it to `created` or `skipped` after each row. On re-runs, **only rows with empty Status** are processed, so you can safely add new rows and run again.

## Prerequisites

- **Google Sheets / Drive**
  - Service account or OAuth credentials with read access to the spreadsheet.
  - Configuration:
    ```bash
    mkdir -p ~/.config/quizfactor
    echo "/absolute/path/to/google-service-account.json" > ~/.config/quizfactor/google_drive_credentials
    echo "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit" > ~/.config/quizfactor/sheet_url
    echo "Sheet1!A2:G9999" > ~/.config/quizfactor/course_sheet_range
    ```
  - **Sheet URL**: The Google Sheet is configured by **URL** in `~/.config/quizfactor/sheet_url` (not by sheet ID). For Sheets API calls, extract the **spreadsheet ID** from the URL: it is the segment between `/d/` and the next `/` (e.g. `https://docs.google.com/spreadsheets/d/abc123xyz/edit` → spreadsheet ID `abc123xyz`).
  - **Write access** to the spreadsheet is required so the skill can update the **Status** column after each row is processed.
  - Required columns (per row):
    - **Course Name** (or Course Title)
    - **Status** – updated by the skill: leave **empty** for rows to process; the skill sets it to `created` or `skipped` after processing. On re-runs, **only rows with empty Status** are processed.
  - Other recommended columns: `Description`, `Level`, `Duration`, `Category`, `Tag`. The exact column order/names depend on your sheet; the agent must know which column index or header is **Status** (e.g. second column = Status) so it can write back.

- **QuizFactor API**
  - Shared base URL config:
    ```bash
    QF_BASE_URL=$(cat ~/.config/quizfactor/base_url)
    ```
  - Existing AI route:
    - `GET /api/ai/courses` – returns `courseCategories` and `courses`.

- **QuizFactor AI routes (in Postman collection)**
  - `POST /api/ai/create-course-category` – body: `tagName`, `type`, `order`, `translations` (array of `languageCode`, `name`, `description`). See **Create Course Category** in `QuizeFactor AI Routes.postman_collection.json`.
  - `POST /api/ai/create-course` – body: `categoryUuid`, `level`, `duration`, `imageUrl`, `translations` (array of `languageCode`, `title`, `description`). See **Create Course** in the same collection.

## High-level Workflow

1. **Read all existing courses and categories**
   - Call:
     ```bash
     curl -X GET "$QF_BASE_URL/api/ai/courses"
     ```
   - Cache:
     - `courseCategories[]` keyed by normalized `name` and `tagName`.
     - `courses[]` keyed by normalized `title` and `slug`.

2. **Read the Google Sheet**
   - Read `~/.config/quizfactor/sheet_url` and extract the spreadsheet ID from the URL (the segment between `/d/` and the next `/`). Read `course_sheet_range` from config (e.g. `~/.config/quizfactor/course_sheet_range`).
   - Use Google Sheets API `spreadsheets.values.get` with that `spreadsheetId` and the configured `range`.
   - Parse the header row to identify columns (e.g. Course Name, Status, Description, Level, Duration, Category, Tag).
   - **Only process rows where the Status column is empty** (blank or missing). Rows that already have `created` or `skipped` in Status must be left untouched for idempotency.
   - For each row with empty Status, build an object that includes the row index (for writing back):
     ```json
     {
       "rowIndex": 2,
       "title": "Course Name from sheet",
       "description": "...",
       "level": "intermediate",
       "duration": 30,
       "categoryName": "Cloud Computing",
       "tag": "...",
       "statusColumnLetter": "B"
     }
     ```
   - Record which column is Status (e.g. B) and the sheet name so you can update the correct cell after processing.

3. **Check if the course already exists**
   - Normalize both sheet and QuizFactor values:
     - Lowercase, strip punctuation, map spaces to `-`.
   - Consider a course **existing** if:
     - Normalized title matches an existing course title, or
     - Provided `tag` equals an existing `slug`.
   - If a course exists:
     - Skip creation (optionally log that it was already present).

4. **Find or create a category**
   - Attempt to match `categoryName` against:
     - `courseCategories[].name`
     - `courseCategories[].tagName`
   - If no category fits “well enough”:
     - Create a new category using **Create Course Category** from the Postman collection (body: `tagName`, `type`, `order`, `translations` with `languageCode`, `name`, `description`). Use the returned `data.category.uuid` as `categoryUuid` for course creation.

5. **Create the course**

   - When a course is missing and a `categoryUuid` is known, call **Create Course** from the Postman collection (payload uses `translations`, not top-level title/description):
     ```bash
     curl -X POST "$QF_BASE_URL/api/ai/create-course" \
       -H "Content-Type: application/json" \
       -d '{
         "categoryUuid": "CATEGORY_UUID",
         "level": "intermediate",
         "duration": 30,
         "imageUrl": "https://example.com/images/placeholder.jpg",
         "translations": [
           {"languageCode": "en", "title": "Course Title", "description": "Course description from sheet"}
         ]
       }'
     ```
   - Map sheet columns: Course Title → `translations[].title`, Description → `translations[].description`. Default `level` to `"intermediate"` and `duration` to `30` when missing. Use `imageUrl` from sheet or omit/null. Response returns `data.course.uuid`.

6. **Update the Status column in the sheet**
   - After processing each row (create or skip), **write back** to the Google Sheet so the next run ignores that row:
     - If the course was **created** (create-course API was called successfully): set the row’s **Status** cell to **`created`**.
     - If the course was **skipped** (already existed in QuizFactor): set the row’s **Status** cell to **`skipped`**.
   - Use Google Sheets API `spreadsheets.values.update` with:
     - `spreadsheetId` (derived from `sheet_url` as above), `range` (e.g. `Sheet1!B2` for row 2 Status column), `valueInputOption`: `USER_ENTERED`, and `values`: `[["created"]]` or `[["skipped"]]`.
   - Update one row at a time, or batch updates for multiple rows in one request if the API allows. Ensure the range matches the Status column (e.g. column B = Status → range `Sheet1!B{rowIndex}`).

7. **Idempotency**
   - Re-runs only process rows where **Status is empty**. Rows with `created` or `skipped` are never processed again.
   - Always re-fetch QuizFactor `courses` and `courseCategories` before each batch.
   - Only call `create-course` when the course is not already present; only call `create-course-category` when no existing category matches.

## Agent Checklist

- [ ] Load QuizFactor base URL, Google credentials, and **sheet URL** from `~/.config/quizfactor`; derive spreadsheet ID from `sheet_url` for Sheets API calls.
- [ ] Fetch current `courses` and `courseCategories` from `GET /api/ai/courses`.
- [ ] Read the sheet and identify the **Status** column. Process **only rows where Status is empty**.
- [ ] For each row with empty Status:
  - [ ] Build a normalized course object (title, description, level, duration, categoryName, tag).
  - [ ] Check if the course already exists in QuizFactor; if yes, set Status to **`skipped`** in the sheet and continue.
  - [ ] If not present: find or create a category, then call `create-course`; on success, set Status to **`created`** in the sheet.
  - [ ] Use `spreadsheets.values.update` to write `created` or `skipped` to the Status cell for that row.
- [ ] Log any rows that could not be imported (e.g. invalid data) for human review; optionally set their Status to a value like `error` or leave empty.

