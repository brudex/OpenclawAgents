---
name: qf-record-pending-uploads
description: Watches a Google Drive folder for new quiz files, maps them to QuizFactor courses or categories using the AI routes collection, and records pending quiz uploads in a dedicated QuizFactor backend table. Use when importing new quiz source files from Drive into QuizFactor.
metadata: {"clawdbot":{"emoji":"🧾"}}
---

# qf-record-pending-uploads

Monitor a Google Drive folder for new quiz files, infer the target QuizFactor course or category from the filename, and record each file as a **pending upload** in QuizFactor.

This skill focuses on **discovery and classification only** – it does **not** parse questions or create quizzes. That is handled by `qf-process-pending-uploads`.

## Prerequisites

- **Google Drive**
  - Google Cloud project with the Drive API enabled.
  - Service account or OAuth credentials with **read access** to the target folder.
  - **Not for marketing briefs:** The **`marketer-agent`** skill watches a **different** folder for the **full project brief** via `~/.config/openclaw/marketing_brief_drive_folder_id` (see **`INTEGRATIONS.md`**). Keep **quiz** folder IDs only in `drive_folder_ids` below — do not add the marketing brief folder here or pending-upload logic may treat brief PDFs/Docs as quiz sources.
  - Recommended config paths:
    ```bash
    mkdir -p ~/.config/quizfactor
    echo "/absolute/path/to/google-service-account.json" > ~/.config/quizfactor/google_drive_credentials
    # Provide Google Drive folder IDs one per line:
    #   GOOGLE_DRIVE_FOLDER_ID_1
    #   GOOGLE_DRIVE_FOLDER_ID_2
    # (Do not use JSON array syntax.)
    printf '%s\n' 'GOOGLE_DRIVE_FOLDER_ID_1' 'GOOGLE_DRIVE_FOLDER_ID_2' > ~/.config/quizfactor/drive_folder_ids
    ```

- **QuizFactor API**
  - Base URL from the Postman collection:
    ```bash
    mkdir -p ~/.config/quizfactor
    echo "https://quizefactor.cachetechs.com" > ~/.config/quizfactor/base_url
    ```
  - AI routes used in this skill (from `QuizeFactor AI Routes.postman_collection.json`):
    - `GET /api/ai/courses` – returns `courseCategories` and `courses`.

- **Pending uploads and course creation (in Postman collection)**
  - `POST /api/ai/pending-quiz-uploads` – create a pending upload (body: `courseUuid`, `courseName`, `filename`, `driveFileId`, `status`).
  - `GET /api/ai/pending-quiz-uploads` – list pending uploads.
  - `POST /api/ai/create-course` – create a course when a category exists but no course matches (body: `categoryUuid`, `level`, `duration`, `imageUrl`, `translations` with `languageCode`, `title`, `description`). See **Create Course** in `QuizeFactor AI Routes.postman_collection.json` for the exact payload and response.

## Configuration

Always derive config from files rather than hard-coding:

```bash
QF_BASE_URL=$(cat ~/.config/quizfactor/base_url)
QF_DRIVE_FOLDER_IDS=$(cat ~/.config/quizfactor/drive_folder_ids)
QF_GOOGLE_CREDS_PATH=$(cat ~/.config/quizfactor/google_drive_credentials)
```

The agent may use either Google client libraries (Python/Node) or raw HTTP with OAuth2, but must honor these paths.

`QF_DRIVE_FOLDER_IDS` is read as text and should be treated as an **array** of folder IDs, with one ID per line.

## High-level Workflow

1. **Iterate drive folder IDs**
   - Split `QF_DRIVE_FOLDER_IDS` by newline into an array of folder IDs.
   - For each folder id `FOLDER_ID` in the array, list files in that folder.

2. **List files in the current Google Drive folder**
   - Use Drive API `files.list` with:
     - `q` filtering by parent folder `FOLDER_ID` and `trashed = false`.
     - Fields including `id`, `name`, `mimeType`, and timestamps.

2. **Fetch QuizFactor course and category metadata**
   - Call:
     ```bash
     curl -X GET "$QF_BASE_URL/api/ai/courses"
     ```
   - Use:
     - `data.courseCategories[]` – `uuid`, `name`, `tagName`, `description`, `type`.
     - `data.courses[]` – `uuid`, `title`, `slug`, `categoryUuid`, etc.

3. **Normalize filenames**
   - For each Drive file, derive a **normalized name**:
     - Strip extension, punctuation.
     - Lowercase.
     - Replace spaces/underscores with `-`.
   - Keep both the original filename and the normalized variant.

4. **Match file to an existing course**
   - Matching strategy (in order):
     1. Exact match between normalized filename and `course.slug`.
     2. Case-insensitive equality between a prettified filename (spaces restored) and `course.title`.
     3. Substring/keyword match where filename contains course title or slug tokens.
   - If multiple candidates match, prefer:
     - The one whose `categoryUuid` best matches any category keywords in the filename.

5. **Fallback: match to a course category**
   - If no course matches:
     - Try matching against `courseCategories` by:
       - `name` (normalized).
       - `tagName`.
     - Choose the category whose `name` or `tagName` appears in the filename.

6. **Handle missing course creation**
   - If a category is found but no course exists:
     - Call **Create Course** from the Postman collection: `POST /api/ai/create-course` with body `categoryUuid`, `level`, `duration`, `imageUrl`, and `translations` (array of `languageCode`, `title`, `description`). Use the inferred course title/description for the default language.
     - Use the returned `data.course.uuid` as `courseUuid` when recording the pending upload.
     - If create-course fails (e.g. 404 for category), create the pending upload with `courseUuid = null` and `courseName` equal to the inferred title, and log for manual follow-up.

7. **Record the pending upload in QuizFactor**
   - For each new Drive file, call **Create Pending Quiz Upload** (see Postman collection):
     ```bash
     curl -X POST "$QF_BASE_URL/api/ai/pending-quiz-uploads" \
       -H "Content-Type: application/json" \
       -d '{
         "courseUuid": "COURSE_UUID_OR_NULL",
         "courseName": "Resolved or inferred course name",
         "filename": "original-file-name.ext",
         "driveFileId": "GOOGLE_DRIVE_FILE_ID",
         "status": "pending"
       }'
     ```
   - Response includes `data.uuid`, `data.status`, `data.createdAt`, etc. Use for idempotency or logging.

## Agent Checklist

- [ ] Read QuizFactor and Google Drive config from `~/.config/quizfactor/*`.
- [ ] Parse `drive_folder_ids` into an array.
- [ ] For each folder id, list all non-trashed files in that Drive folder.
- [ ] Optionally deduplicate against existing pending uploads (when a listing endpoint exists).
- [ ] Fetch `courses` and `courseCategories` from `GET /api/ai/courses`.
- [ ] For each new file:
  - [ ] Normalize filename and attempt course match.
  - [ ] If no course, attempt category match.
  - [ ] If category only, decide how to handle missing course (create or log).
  - [ ] Call the pending uploads endpoint with `status = "pending"`.
- [ ] Log any failures and ambiguous matches so a human can correct them later.

