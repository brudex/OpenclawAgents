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
~/.config/gemini/api_key          # Google AI Studio / Gemini API key (image + Veo video when configured)
~/.config/quizfactor/google_drive_credentials   # Path to service account JSON (qf-* skills; marketer-agent optional if host Google/Drive already connected)
~/.config/marketer/drive_folder_id   # Single line: marketer-agent — Google Drive folder ID for full project brief (not quiz imports)
~/.config/openclaw/marketing_brief_drive_folder_id   # Legacy fallback if marketer/drive_folder_id is missing
~/.config/social/drive_folder_id   # Optional: shared Drive folder for LinkedIn *article* handoff to interns — not for routine feed posts (see below)
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
| `MARKETING_BRIEF_DRIVE_FOLDER_ID` | Override marketing brief folder (else `~/.config/marketer/drive_folder_id`, else legacy `~/.config/openclaw/marketing_brief_drive_folder_id`) |
| `SOCIAL_POSTING_DRIVE_FOLDER_ID` | Override LinkedIn **article** handoff folder (else `~/.config/social/drive_folder_id`) — **not** used for routine Twitter/LinkedIn feed posts |
| `BRAND_IMAGES_DIR` | Absolute path to **brand kit** (logos, `palette.md`, `logo-usage.md`). Default: **`workspace/brand-images/`** next to this repo’s workspace root. Example on server: `/home/admin/.openclaw/workspace/brand-images` |

## Brand images (`brand-images/`)

**QuizFactor / product-branded** social and article images use a **fixed folder** of assets + text so Gemini does not invent the wrong logo.

- **Layout:** See **`workspace/brand-images/README.md`** (`logo-primary.png`, `palette.md`, `logo-usage.md`, optional `product-context.md`).
- **Override path:** Set **`BRAND_IMAGES_DIR`** in `~/.openclaw/.env` if the kit lives outside the repo (e.g. `/home/admin/.openclaw/workspace/brand-images`).
- **Skill:** **`auto-image-generation`** must **list and read** this directory **before** every render (see that skill → *Brand kit*).

## Google Drive — LinkedIn articles only (intern handoff)

In this workspace, **save to Google Drive for long-form LinkedIn articles**, not for routine social feed posts.

- **LinkedIn + Twitter feed posts** (short updates, threads, **`teaser.md`**, etc.): stay in **`workspace/drafts/social/...`**, then **`social-media-manager`** **pushes** approved bundles through **`hype-engine`** (already connected). **Do not** treat Drive as the default export path for those posts.
- **LinkedIn articles (`article.md`)**: optional **Google Doc** export under **`04-articles/`** so **interns** can open the Doc and publish via LinkedIn’s **article** composer. Document links in **`publish-handoff.md`** / campaign **`README-handoff.md`**.

**Config (pick one):**

- **`~/.config/social/drive_folder_id`** — single line, folder ID for the shared **article** handoff tree (name is legacy; purpose here is articles).
- Env **`SOCIAL_POSTING_DRIVE_FOLDER_ID`** overrides the file.

**Share** the folder with:

- The **OpenClaw** Google account (or service account **`client_email`**) for upload/list.
- **Interns / editors** who publish articles (Editor or Commenter as you prefer).

**Suggested Drive layout (create manually or via agent + `gws-*` tools):**

| Area | Purpose |
|------|---------|
| `01-briefs/` | *(Optional)* Reference materials the team drops in; not required for HypeEngine posting |
| `02-calendar/` | *(Optional)* Team calendar / Sheet if you mirror schedule outside the repo |
| `04-articles/` | **`linkedin-article-writer`**: one Doc per article (full body); link from **`publish-handoff.md`** |

**Do not** maintain **`03-ready-to-post/`** for LinkedIn/X feed copy in this setup—that duplicates **`hype-engine`**, which is the canonical path for those posts.

**Auth:** Same patterns as **marketing brief** — prefer **host Google / OpenClaw-linked Google**; else service account JSON at **`~/.config/quizfactor/google_drive_credentials`** with this folder shared to that account.

**OpenClaw skills (optional upload):** If installed, **`gws-drive-upload`**, **`gws-docs-write`**, and related packages from **`openclaw-setup.md`** can create/update **article** Docs from `workspace/drafts/linkedin/...`. Skills only **describe** the workflow; the host must expose those tools.

**Skills that reference this flow:** **`linkedin-article-writer`** (primary), **`social-media-manager`** (optional read of team files at intake only — not export of every post), **`marketer-agent`** (upstream brief read uses a **different** Drive folder — see below).

## Google Drive — marketing project brief (`marketer-agent`)

The **full project brief** for marketing work lives in a shared Drive folder. **`marketer-agent`** should list and read files there (same Drive API patterns as **`qf-record-pending-uploads`** when using a service account, but **separate** folder-ID config so quiz-import folders are not mixed with the brief folder).

**Canonical folder for this workspace:** `14DI9fDOoU52vvyKu4HRm-Ot57_p8uiRs` — [open in Drive](https://drive.google.com/drive/folders/14DI9fDOoU52vvyKu4HRm-Ot57_p8uiRs).

### When OpenClaw already has Google / Drive connected

If the **host** (OpenClaw UI, linked Google account, or Drive-capable tools/MCP) already provides authenticated Drive access, **`marketer-agent`** should **use that** to read the brief folder. You still need a resolvable **folder ID** (`~/.config/marketer/drive_folder_id`, env **`MARKETING_BRIEF_DRIVE_FOLDER_ID`**, or legacy openclaw file). You do **not** need to create **`~/.config/quizfactor/google_drive_credentials`** for marketer-agent in that setup (that file remains important for **`qf-record-pending-uploads`** on headless/service-account setups).

**Operator note:** If your server team confirms **Google is already logged in / integrated**, treat Drive auth for marketer-agent as **handled by the host**. Agents should **not** insist on a separate service-account JSON for marketing brief ingest; add **`google_drive_credentials`** only when you rely on a key file for QuizFactor or other automation without user Google.

### Service-account setup (headless or no host Google integration)

1. Enable **Google Drive API** on a Google Cloud project; create a **service account** and download JSON.
2. **Share** the brief folder with the service account’s client email (e.g. `something@project.iam.gserviceaccount.com`) with at least **Viewer**.
3. Write config (adjust JSON path). **Reuse** `~/.config/quizfactor/google_drive_credentials` if you already set it for **`qf-record-pending-uploads`**; add the marketer brief folder ID under **`~/.config/marketer/`**:

```bash
mkdir -p ~/.config/quizfactor ~/.config/marketer
echo "/absolute/path/to/google-service-account.json" > ~/.config/quizfactor/google_drive_credentials
printf '%s\n' '14DI9fDOoU52vvyKu4HRm-Ot57_p8uiRs' > ~/.config/marketer/drive_folder_id
```

**Folder ID** resolution: env **`MARKETING_BRIEF_DRIVE_FOLDER_ID`** if set; else **`~/.config/marketer/drive_folder_id`**; else legacy **`~/.config/openclaw/marketing_brief_drive_folder_id`**.

When using a service account:

```bash
QF_GOOGLE_CREDS_PATH=$(cat ~/.config/quizfactor/google_drive_credentials)
MARKETING_BRIEF_FOLDER_ID=$(cat ~/.config/marketer/drive_folder_id)
```

Use `files.list` with `q` including `'${MARKETING_BRIEF_FOLDER_ID}' in parents` and `trashed = false`, then export Docs / download binaries per [Drive API](https://developers.google.com/drive/api/guides/about-sdk) patterns. **`qf-record-pending-uploads`** uses **`~/.config/quizfactor/drive_folder_ids`** for **quiz** ingestion only — do **not** add this brief folder ID there.

## HypeEngine (Twitter/X + LinkedIn posts)

This workspace routes **approved** **Twitter/X** and **LinkedIn feed** publishing through the **`hype-engine`** skill when configured. Files: `~/.config/hype-engine/api_key`, `project_uuid`, `base_url`. See **`skills/hype-engine/SKILL.md`** for Accounts, Media, Tags, and Posts `curl` examples.

## OpenClaw channels (preferred when available)

If **`~/.openclaw/openclaw.json`** defines **Telegram, Discord**, etc., use **channel tools** where the team uses them. For **X + LinkedIn feed**, default to **`hype-engine`** unless **`USER.md` / `TOOLS.md`** says otherwise. For direct LinkedIn API without HypeEngine, use **`~/.config/linkedin/`** or env vars in this doc.

## Gemini — image (generateContent)

**Workspace default:** Gemini is **already configured** on the OpenClaw host for this project. Skills should **use** it for real image/video generation when relevant—not skip renders assuming keys are absent unless a check fails.

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

Same **workspace default** as image: assume Gemini is available; **attempt Veo** for **`auto-video-generation`** when the project supports it (see skill for failure handoff).

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
