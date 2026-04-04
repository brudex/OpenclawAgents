---
name: qf-record-pending-uploads
description: Watches a Google Drive folder for new quiz files, maps them to QuizFactor courses or categories using the AI routes collection, creates a course when none matches, then records pending quiz uploads. Use when importing new quiz source files from Drive into QuizFactor.
metadata: {"clawdbot":{"emoji":"🧾"}}
---

# qf-record-pending-uploads

Monitor a Google Drive folder for new quiz files, infer the target QuizFactor course or category from the filename, and record each file as a **pending upload** in QuizFactor.

When **no course** in `GET /api/ai/courses` matches the file, the agent **must create a course first** (`POST /api/ai/create-course`), then call **`POST /api/ai/pending-quiz-uploads`** with the new `courseUuid`. Do **not** insert a pending upload with `courseUuid = null` if create-course can succeed.

This skill focuses on **discovery and classification only** – it does **not** parse questions or create quizzes. That is handled by `qf-process-pending-uploads`.

## Prerequisites

- **Google Drive**
  - Google Cloud project with the Drive API enabled.
  - Service account or OAuth credentials with **read access** to each **quiz** folder you list in `drive_folder_ids`.
  - **Same Google key file as `marketer-agent`:** service account JSON path is **`~/.config/quizfactor/google_drive_credentials`** (see **Configuration** — `QF_GOOGLE_CREDS_PATH`). **`marketer-agent`** uses that file too; it keeps the **GTM brief** folder ID in **`~/.config/marketer/drive_folder_id`** (legacy: **`~/.config/openclaw/marketing_brief_drive_folder_id`** — see **`INTEGRATIONS.md`**). **Do not** put the marketing brief folder ID in `drive_folder_ids` — pending-upload logic would treat brief PDFs/Docs as quiz sources.
  - Recommended config paths:
    ```bash
    mkdir -p ~/.config/quizfactor ~/.config/marketer
    # Shared with marketer-agent / qf-process-pending-uploads:
    echo "/absolute/path/to/google-service-account.json" > ~/.config/quizfactor/google_drive_credentials
    # Quiz import folders only — one Google Drive folder ID per line (do not use JSON array syntax):
    printf '%s\n' 'GOOGLE_DRIVE_FOLDER_ID_1' 'GOOGLE_DRIVE_FOLDER_ID_2' > ~/.config/quizfactor/drive_folder_ids
    ```

- **QuizFactor API**
  - Base URL from the Postman collection:
    ```bash
    mkdir -p ~/.config/quizfactor
    echo "https://quizefactor.cachetechs.com" > ~/.config/quizfactor/base_url
    ```
  - AI routes (see **`QuizeFactor AI Routes.postman_collection.json`**):
    - `GET /api/ai/courses` – returns `courseCategories` and `courses`.
    - `POST /api/ai/create-course-category` – when no category matches; response `data.category.uuid` (201). See **Create Course Category** in the collection.
    - `POST /api/ai/create-course` – **required** when no existing course matches; response `data.course.uuid` (201). See **Create Course** below and in the collection.
    - `POST /api/ai/pending-quiz-uploads` – **after** you have a `courseUuid` from a matched or newly created course.
    - `GET /api/ai/pending-quiz-uploads` – list pending uploads (dedupe optional).

## Configuration

Always derive config from files rather than hard-coding:

```bash
QF_BASE_URL=$(cat ~/.config/quizfactor/base_url)
QF_DRIVE_FOLDER_IDS=$(cat ~/.config/quizfactor/drive_folder_ids)
QF_GOOGLE_CREDS_PATH=$(cat ~/.config/quizfactor/google_drive_credentials)
```

The agent may use either Google client libraries (Python/Node) or raw HTTP with OAuth2, but must honor these paths.

`QF_DRIVE_FOLDER_IDS` is read as text and should be treated as an **array** of folder IDs, with one ID per line.

## Create Course (from Postman) — use before `pending-quiz-uploads` when no course matches

**Request**

- **Method:** `POST`
- **URL:** `$QF_BASE_URL/api/ai/create-course`
- **Headers:** `Content-Type: application/json`
- **Body** (example matches **Create Course** in the collection):

```json
{
  "categoryUuid": "dc3850a3-0065-43ed-b399-9dea5e9afe7a",
  "level": "beginner",
  "duration": 40,
  "imageUrl": "https://example.com/images/algebra-course.jpg",
  "translations": [
    {
      "languageCode": "en",
      "title": "Introduction to Algebra",
      "description": "Learn variables, expressions, and basic equations."
    }
  ]
}
```

- `categoryUuid` — required; obtain from an existing `courseCategories[]` match or from **`POST /api/ai/create-course-category`** → `data.category.uuid`.
- `level`, `duration`, `imageUrl` — use sensible defaults when unknown (e.g. `intermediate`, `30`, `null` or omit `imageUrl` if the API allows).
- `translations` — at least `en` with `title` and `description` derived from the inferred course name and a short description.

**Success response (201 Created)**

```json
{
  "status": "00",
  "data": {
    "message": "Course created successfully",
    "course": {
      "id": 128,
      "uuid": "0a737479-375c-4edc-a376-ae226af45da4",
      "categoryUuid": "dc3850a3-0065-43ed-b399-9dea5e9afe7a",
      "level": "beginner",
      "duration": 40,
      "slug": null,
      "imageUrl": "https://example.com/images/algebra-course.jpg",
      "isActive": true,
      "totalQuizzes": 0,
      "createdAt": "2026-03-13T22:38:21.210Z",
      "updatedAt": "2026-03-13T22:38:21.210Z",
      "translations": []
    }
  }
}
```

- Use **`data.course.uuid`** as **`courseUuid`** for **`POST /api/ai/pending-quiz-uploads`**.

**Failure (e.g. 404 Not Found)** — invalid `categoryUuid` per collection example. If create-course cannot succeed, you may record the pending upload with `courseUuid: null` and a clear `courseName`, and log for follow-up.

## High-level Workflow

1. **Iterate drive folder IDs**
   - Split `QF_DRIVE_FOLDER_IDS` by newline into an array of folder IDs.
   - For each folder id `FOLDER_ID` in the array, list files in that folder.

2. **List files in the current Google Drive folder**
   - Use Drive API `files.list` with:
     - `q` filtering by parent folder `FOLDER_ID` and `trashed = false`.
     - Fields including `id`, `name`, `mimeType`, and timestamps.

3. **Fetch QuizFactor course and category metadata**
   - Call:
     ```bash
     curl -X GET "$QF_BASE_URL/api/ai/courses"
     ```
   - Use:
     - `data.courseCategories[]` – `uuid`, `name`, `tagName`, `description`, `type`.
     - `data.courses[]` – `uuid`, `title`, `slug`, `categoryUuid`, etc.

4. **Normalize filenames**
   - For each Drive file, derive a **normalized name**:
     - Strip extension, punctuation.
     - Lowercase.
     - Replace spaces/underscores with `-`.
   - Keep both the original filename and the normalized variant.

5. **Match file to an existing course**
   - Matching strategy (in order):
     1. Exact match between normalized filename and `course.slug`.
     2. Case-insensitive equality between a prettified filename (spaces restored) and `course.title`.
     3. Substring/keyword match where filename contains course title or slug tokens.
   - If multiple candidates match, prefer:
     - The one whose `categoryUuid` best matches any category keywords in the filename.
   - If a course matches: note its **`uuid`** and go to **step 8** (pending upload) with that `courseUuid` — **skip create-course**.

6. **No course match — resolve category**
   - If **no** course matches `data.courses[]`:
     - Try matching against `courseCategories` by `name` (normalized) and `tagName`.
     - If **no** category fits: create one with **`POST /api/ai/create-course-category`** (see collection), then use **`data.category.uuid`** as `categoryUuid` for create-course.

7. **No course match — create course (mandatory before pending upload)**
   - With a resolved **`categoryUuid`** (from step 6), call **`POST /api/ai/create-course`** as documented in **Create Course (from Postman)** above.
   - On **201** success, read **`data.course.uuid`** — this is the **`courseUuid`** for the pending upload.
   - Only if create-course **fails** after category resolution: optionally call **`POST /api/ai/pending-quiz-uploads`** with `courseUuid: null`, `courseName` set to the inferred title, and log the error.

8. **Record the pending upload in QuizFactor**
   - For each new Drive file, after you have a **`courseUuid`** (from step 5 match or step 7 create-course), call **Create Pending Quiz Upload** (see Postman collection):
     ```bash
     curl -X POST "$QF_BASE_URL/api/ai/pending-quiz-uploads" \
       -H "Content-Type: application/json" \
       -d '{
         "courseUuid": "COURSE_UUID_FROM_MATCH_OR_CREATE_COURSE",
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
  - [ ] Normalize filename and attempt **course** match against `data.courses[]`.
  - [ ] If a course matches: use its **`uuid`** and call **`pending-quiz-uploads`** (no create-course).
  - [ ] If **no** course matches: resolve or create **category**, then **`POST /api/ai/create-course`**, then use **`data.course.uuid`** for **`pending-quiz-uploads`** (see Postman for request/response shapes).
  - [ ] Only use `courseUuid: null` when create-course cannot succeed; log why.
- [ ] Log any failures and ambiguous matches so a human can correct them later.
