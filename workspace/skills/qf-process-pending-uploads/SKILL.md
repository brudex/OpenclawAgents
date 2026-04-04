---
name: qf-process-pending-uploads
description: Processes pending quiz uploads by downloading Google Drive files, extracting questions with the full-document prompt, and loading them into QuizFactor via POST /api/ai/load-quizzes. Use after pending uploads have been recorded.
metadata: {"clawdbot":{"emoji":"📥"}}
---

# qf-process-pending-uploads

Take rows from the **pending uploads** table, download the source file from Google Drive, extract questions using the full-document extraction prompt, and push them into QuizFactor in one call via **Load Quizzes** (`POST /api/ai/load-quizzes`).

This skill assumes `qf-record-pending-uploads` has already created pending rows for each Drive file. Request/response examples follow `QuizeFactor AI Routes.postman_collection.json`.

## Prerequisites

- **Shared config with `qf-record-pending-uploads`**
  - Reuse:
    ```bash
    QF_BASE_URL=$(cat ~/.config/quizfactor/base_url)
    QF_DRIVE_FOLDER_ID=$(cat ~/.config/quizfactor/drive_folder_id)
    QF_GOOGLE_CREDS_PATH=$(cat ~/.config/quizfactor/google_drive_credentials)
    ```

- **QuizFactor AI routes (from Postman collection)**
  - `GET /api/ai/courses` – verify `courseUuid` and course metadata.
  - `GET /api/ai/pending-quiz-uploads` – list pending uploads (optional `?status=pending`).
  - `POST /api/ai/load-quizzes` – load quizzes and questions in one request (replaces create-quiz + add-quiz-questions).
  - `PATCH /api/ai/pending-quiz-uploads/:uuid` – update status after processing.

## Data Flow

1. **Fetch pending uploads**
   - Call:
     ```bash
     curl -X GET "$QF_BASE_URL/api/ai/pending-quiz-uploads?limit=20"
     ```
   - Filter by `status = "pending"` if the API does not support a query param, or use `?status=pending` if it does.
   - Each row has: `uuid`, `courseUuid`, `courseName`, `filename`, `driveFileId`, `status`, `errorMessage`, `createdAt`, `updatedAt`.

2. **Download the Google Drive file**
   - For each row, use `driveFileId` with the Drive API (`files.get` / `files.export` for Docs) to download content.
   - Support at least: plain text, Markdown, PDF, and simple Word/Google Docs (exported to text).

3. **Extract questions via full-document prompt**
   - Use the prompt in `extraction-prompt-fulldocument.md`.
   - Feed the entire cleaned document text; expect a JSON **array** of topic blocks:
     - Each block: `topic`, `quizTitle` (optional; fallback to `topic`), `questions` array.
     - Each question: `questionType`, `difficulty`, `points`, `translations` with `languageCode`, `questionText`, `options` (object), `correctAnswer` (array of option keys), `explanation`.
   - Keep the extraction output as-is for `load-quizzes`: **no mapping** to a different schema. The extraction format matches the `jsonData` format required by the API (including `correctAnswer` as an array for both single-choice and multi-choice).
   - Validate: at least one translation, non-empty options, and non-empty `correctAnswer` array; drop invalid questions. Default `difficulty` to `"medium"` and `points` to `1` when missing.

4. **Load quizzes into QuizFactor (single API call)**
   - If `courseUuid` on the pending row is null:
     - Treat as blocked: update the pending upload to a status like `"blocked_missing_course"` with an `errorMessage`, and skip.
     - Optionally try a last-chance match using `courseName` and `GET /api/ai/courses`; if found, use that `courseUuid`.
   - When `courseUuid` is set, call **Load Quizzes** once with the full extraction array:
     ```bash
     curl -X POST "$QF_BASE_URL/api/ai/load-quizzes" \
       -H "Content-Type: application/json" \
       -d '{
         "courseUuid": "COURSE_UUID_FROM_PENDING_ROW",
         "jsonData": [
           {
             "topic": "Topic or Chapter Title",
             "quizTitle": "Title of quiz",
             "questions": [
               {
                 "questionType": "single-choice",
                 "difficulty": "medium",
                 "points": 1,
                 "translations": [
                   {
                     "languageCode": "en",
                     "questionText": "Full question text",
                     "options": {
                       "option_1": "First option",
                       "option_2": "Second option"
                     },
                     "correctAnswer": ["option_2"],
                     "explanation": "Short explanation or empty string"
                   }
                 ]
               }
             ]
           }
         ]
       }'
     ```
   - **Request body**: `courseUuid` (required) + `jsonData` (array of topic blocks in extraction format). No separate create-quiz or add-quiz-questions calls.
   - **Response (200)**:
     ```json
     {
       "status": "00",
       "message": "Quizzes loaded successfully",
       "data": {
         "topicsCreated": 1,
         "quizzesCreated": 2,
         "questionsImported": 4,
         "errors": []
       }
     }
     ```
   - If the API returns errors in `data.errors`, log them and consider the upload partially failed; set status to `"failed"` and put a summary in `errorMessage`.

5. **Update pending upload status**
   - On success:
     ```bash
     curl -X PATCH "$QF_BASE_URL/api/ai/pending-quiz-uploads/PENDING_UUID" \
       -H "Content-Type: application/json" \
       -d '{"status": "completed"}'
     ```
     (Postman also shows `"status": "processed"` as a valid value; use whichever the backend expects.)
   - On failure:
     ```bash
     curl -X PATCH "$QF_BASE_URL/api/ai/pending-quiz-uploads/PENDING_UUID" \
       -H "Content-Type: application/json" \
       -d '{"status": "failed", "errorMessage": "Brief reason"}'
     ```

## Agent Checklist

- [ ] Load QuizFactor base URL and Google Drive credentials from `~/.config/quizfactor`.
- [ ] Fetch pending uploads (filter by `status = "pending"`).
- [ ] For each pending row:
  - [ ] Download the file from Drive using `driveFileId`.
  - [ ] Run the full-document extraction prompt to get the `jsonData` array.
  - [ ] If `courseUuid` is null, mark as blocked or try to resolve from `courseName`; otherwise skip load.
  - [ ] Call `POST /api/ai/load-quizzes` with `{ "courseUuid": "...", "jsonData": [ ... ] }`.
  - [ ] On success, PATCH the pending upload to `"completed"` (or `"processed"`); on failure, set `"failed"` and `errorMessage`.
