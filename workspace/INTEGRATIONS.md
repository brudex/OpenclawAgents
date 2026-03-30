# Gateway integrations (qf-course-researcher pattern)

Skills only **describe** calls; the **OpenClaw host** must supply secrets. Mirror `qf-course-researcher`: small files under `~/.config/...` and/or **`~/.openclaw/.env`**, **never** commit real tokens.

Suggested layout (create on server):

```text
~/.config/quizfactor/base_url          # QuizFactor API base URL (existing qf-* skills)
~/.config/notion/api_key               # Notion (existing)
~/.config/linkedin/access_token        # Optional: LinkedIn UGC / Marketing API
~/.config/reddit/client_id            # Reddit script app
~/.config/reddit/client_secret
~/.config/reddit/refresh_token        # After OAuth
~/.config/meta_ads/access_token       # Meta Marketing API (long-lived)
~/.config/google_ads/refresh_token   # Google Ads OAuth (or use gcloud ADC)
~/.config/tiktok/                     # TikTok for Business tokens if available
~/.config/hype-engine/api_key         # HypeEngine / Mixpost — Bearer token
~/.config/hype-engine/project_uuid
~/.config/hype-engine/base_url
~/.config/gemini/api_key          # Google AI Studio / Gemini API key (image + Veo video)
~/.config/openclaw/google_drive_credentials   # Path to service account JSON (marketer-agent: project brief folder)
~/.config/openclaw/marketing_brief_drive_folder_id   # Single line: Google Drive folder ID for full project brief
```

Environment variables (alternative to files — set in `~/.openclaw/.env` or systemd):

| Variable | Used for |
|----------|-----------|
| `QF_BASE_URL` | Override QuizFactor base if not using file |
| `QF_API_TOKEN` / `QUIZFACTOR_API_KEY` | Bearer for QuizFactor AI routes (match your Postman collection) |
| `NOTION_KEY` | Notion API (if not using file path) |
| `LINKEDIN_ACCESS_TOKEN` | LinkedIn API posts (if not using OpenClaw channel) |
| `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_REFRESH_TOKEN` | Reddit API |
| `META_ACCESS_TOKEN` | Meta Marketing API |
| `GOOGLE_ADS_DEVELOPER_TOKEN`, `GOOGLE_ADS_*` | Google Ads |
| `TIKTOK_ACCESS_TOKEN` | TikTok Marketing / Content API when eligible |
| `GEMINI_API_KEY` | **Primary** for **`auto-image-generation`** and **`auto-video-generation`** (Gemini native image / Imagen + **Veo** video) |
| `OPENAI_API_KEY`, `FAL_KEY` | Optional fallbacks if you add other tools later |
| `MARKETING_BRIEF_DRIVE_FOLDER_ID` | Override marketing brief folder (else read `~/.config/openclaw/marketing_brief_drive_folder_id`) |

## Google Drive — marketing project brief (`marketer-agent`)

The **full project brief** for marketing work lives in a shared Drive folder. **`marketer-agent`** should list and read files there (same Drive API usage as **`qf-record-pending-uploads`**, but **separate** config paths so quiz-import folders are not mixed with the brief folder).

**Canonical folder for this workspace:** `14DI9fDOoU52vvyKu4HRm-Ot57_p8uiRs` — [open in Drive](https://drive.google.com/drive/folders/14DI9fDOoU52vvyKu4HRm-Ot57_p8uiRs).

On the OpenClaw host:

1. Enable **Google Drive API** on a Google Cloud project; create a **service account** and download JSON.
2. **Share** the brief folder with the service account’s client email (e.g. `something@project.iam.gserviceaccount.com`) with at least **Viewer**.
3. Write config (adjust JSON path):

```bash
mkdir -p ~/.config/openclaw
echo "/absolute/path/to/google-service-account.json" > ~/.config/openclaw/google_drive_credentials
printf '%s\n' '14DI9fDOoU52vvyKu4HRm-Ot57_p8uiRs' > ~/.config/openclaw/marketing_brief_drive_folder_id
```

4. Resolve config at runtime the same way as **`qf-record-pending-uploads`** `## Configuration` (read paths from files, not hard-coded):

```bash
MARKETING_BRIEF_FOLDER_ID=$(cat ~/.config/openclaw/marketing_brief_drive_folder_id)
MARKETING_GOOGLE_CREDS_PATH=$(cat ~/.config/openclaw/google_drive_credentials)
```

If **`MARKETING_BRIEF_DRIVE_FOLDER_ID`** is set in the environment, use it **instead of** the file for the folder ID.

Use `files.list` with `q` including `'${MARKETING_BRIEF_FOLDER_ID}' in parents` and `trashed = false`, then export Docs / download binaries per [Drive API](https://developers.google.com/drive/api/guides/about-sdk) patterns. **`qf-record-pending-uploads`** documents the same credential style under `~/.config/quizfactor/` for **quiz** ingestion only — do **not** add this brief folder ID to `~/.config/quizfactor/drive_folder_ids`.

## HypeEngine (Twitter/X + LinkedIn posts)

This workspace routes **approved** **Twitter/X** and **LinkedIn feed** publishing through the **`hype-engine`** skill when configured. Files: `~/.config/hype-engine/api_key`, `project_uuid`, `base_url`. See **`skills/hype-engine/SKILL.md`** for Accounts, Media, Tags, and Posts `curl` examples.

## OpenClaw channels (preferred when available)

If **`~/.openclaw/openclaw.json`** defines **Telegram, Discord**, etc., use **channel tools** where the team uses them. For **X + LinkedIn feed**, default to **`hype-engine`** unless **`USER.md` / `TOOLS.md`** says otherwise. For direct LinkedIn API without HypeEngine, use **`~/.config/linkedin/`** or env vars in this doc.

## Gemini — image (generateContent)

Use an **image-capable** model id from the current [image generation](https://ai.google.dev/gemini-api/docs/image-generation) documentation. Auth header is **`x-goog-api-key`**, not `Authorization: Bearer`.

```bash
GEMINI_API_KEY=$(cat ~/.config/gemini/api_key)
# Replace MODEL_ID with a supported image model from the docs (examples: gemini-2.5-flash-image, gemini-3.1-flash-image-preview, …)
MODEL_ID="gemini-2.5-flash-image"

curl -sS -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/${MODEL_ID}:generateContent" \
  -H "x-goog-api-key: ${GEMINI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{"text": "YOUR_PROMPT_FROM_prompt-master.txt"}]
    }],
    "generationConfig": {
      "imageConfig": { "aspectRatio": "1:1" }
    }
  }'
```

Decode **`inlineData`** / base64 image parts from the JSON response into a file under `workspace/drafts/images/<run>/`.

### Imagen (optional `predict`)

```bash
curl -sS -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict" \
  -H "x-goog-api-key: ${GEMINI_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"instances":[{"prompt":"…"}],"parameters":{"sampleCount":1}}'
```

## Gemini — video (Veo, async)

Video generation is **long-running**. Start the operation, **poll** until `done`, then **download** the file. Endpoint and JSON shape are updated periodically — verify against [video / Veo](https://ai.google.dev/gemini-api/docs/video).

Illustrative flow (requires `jq`; adjust paths to match current API responses):

```bash
GEMINI_API_KEY=$(cat ~/.config/gemini/api_key)
BASE_URL="https://generativelanguage.googleapis.com/v1beta"

operation_name=$(curl -s "${BASE_URL}/models/veo-3.1-generate-preview:predictLongRunning" \
  -H "x-goog-api-key: ${GEMINI_API_KEY}" \
  -H "Content-Type: application/json" \
  -X POST \
  -d '{
    "instances": [{ "prompt": "YOUR_CINEMATIC_PROMPT_FROM_beat-sheet.md" }],
    "parameters": { "aspectRatio": "9:16" }
  }' | jq -r .name)

while true; do
  status=$(curl -s -H "x-goog-api-key: ${GEMINI_API_KEY}" "${BASE_URL}/${operation_name}")
  if [ "$(echo "$status" | jq .done)" = "true" ]; then
    video_uri=$(echo "$status" | jq -r '.response.generateVideoResponse.generatedSamples[0].video.uri // empty')
    [ -n "$video_uri" ] && curl -sL -o veo-output.mp4 -H "x-goog-api-key: ${GEMINI_API_KEY}" "$video_uri"
    break
  fi
  sleep 10
done
```

Save outputs under **`workspace/drafts/video/<run>/`** and record model + operation id in **`veo-render.md`**.

## Example: QuizFactor (with Bearer)

If your API requires auth (adjust header name to match Postman):

```bash
QF_BASE_URL=$(cat ~/.config/quizfactor/base_url)
QF_TOKEN=$(cat ~/.config/quizfactor/api_token)   # create this file on server if needed

curl -sS "$QF_BASE_URL/api/ai/courses" \
  -H "Authorization: Bearer $QF_TOKEN" \
  -H "Accept: application/json"
```

## Example: Notion

Use the **`notion`** skill patterns; minimal check:

```bash
NOTION_KEY=$(cat ~/.config/notion/api_key)
curl -sS -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"query":"QuizFactorA+","page_size":5}'
```

## Example: Reddit (app-only script flow is limited)

User OAuth is usually required for posting. Store refresh token securely; use **OpenClaw Reddit channel** if configured instead.

```bash
# Illustrative — real flow uses OAuth; see Reddit app settings
export REDDIT_CLIENT_ID=$(cat ~/.config/reddit/client_id)
export REDDIT_CLIENT_SECRET=$(cat ~/.config/reddit/client_secret)
# Then use Reddit OAuth token endpoint per current Reddit docs
```

## Example: Meta Marketing API

```bash
META_TOKEN=$(cat ~/.config/meta_ads/access_token)
curl -sS "https://graph.facebook.com/v21.0/me/adaccounts?access_token=$META_TOKEN"
```

## Draft-only mode

Every growth skill can run **without** any of the above: outputs go to **`workspace/drafts/...`**. Live API sections in each `SKILL.md` apply only when you enable automation.
