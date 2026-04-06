---
name: hype-engine
description: HypeEngine API v1 for managing social media accounts, media, tags, and posts—canonical live path for Twitter/X and LinkedIn feed posts after approval when this stack is configured.
homepage: https://example.com/hypeengine
metadata: {"clawdbot":{"emoji":"📣"},"openclaw":{"emoji":"📣"}}
---

# hype-engine

Use the HypeEngine API v1 to manage social media **accounts**, upload **media**, organize **tags**, and create/schedule **posts** across channels.

## Twitter/X and LinkedIn: use this skill to post

For this workspace, **live** posts to **Twitter/X** and **LinkedIn** (feed / teaser-style updates) go through **HypeEngine** when `~/.config/hype-engine/` is configured—not direct Twitter or LinkedIn Marketing API calls from other skills. **Accounts are already connected**; the operator’s job on publish is to **push** approved content through the Posts API, not to re-do OAuth each run.

- **Upstream (typical order):** `linkedin-article-writer` (**articles** + `teaser.md`) **or** `x-post-writer` / `social-content-writer` (`post-body.md`) → **`social-media-manager`** **`post-bundle.md`** + **`APPROVAL.md`** — optional **`social-caption-writer`** polish — then this skill ships to X/LinkedIn (or human approval in chat).
- **This skill:** Resolve **account UUIDs** via the Accounts API (X and LinkedIn rows), **upload** images from **`post-image.png`** / **`article-hero.png`** via the **Media API** when the bundle lists a file path, map caption/teaser HTML into the Posts API `content[].body`, attach **`content[].media`** UUIDs, then **create the post once** via **POST `/posts`** with **`date` + `time`** from **`APPROVAL.md`** / **`calendar.md`** (see **Scheduling — no separate “publish now”** below). **Do not** call a separate “publish now” API by default—HypeEngine should **queue and publish** (or publish at the scheduled time) from that single create.
- **Threads (X):** If the draft is a multi-tweet thread, either post as HypeEngine supports multi-part content for that account, or post tweet 1 and reply-chain per product behavior—document which you used in the run summary.
- If HypeEngine is **down or unconfigured**, stop and say so; do not silently fall back to another API unless **`USER.md` / `TOOLS.md`** explicitly allows OpenClaw channels or raw LinkedIn for that agent.

## Idempotency — do not publish the same calendar row twice

Duplicate feed posts usually happen when **cron + manual run** both call **Create Post**, or when **AM and PM jobs** both match the same row.

**Before** calling **POST** `/posts` for a campaign row:

1. Open **`workspace/drafts/social/<campaign>/APPROVAL.md`** for that **Post ID**.  
2. If **`HypeEngine post UUID`** (or **`Status`** = `published`) is **already filled** for that row → **do nothing** for that row; log *“skipped — already published”*.  
3. After a **successful** POST `/posts` response (scheduled post created), **immediately** write the returned **post UUID** (and **`media UUID`** if new upload) into **`APPROVAL.md`** for that row. Optionally append a line to **`publish-log.md`**. HypeEngine publishes at **`date`/`time`**—no follow-up “publish” call unless explicitly required by your deployment.

**Cron jobs:** Each job must filter rows by **calendar `Local time`** (e.g. AM job → only `09:00` slots; PM job → only `18:00` slots) **and** **Approved = yes** **and** **empty `HypeEngine post UUID`**. Do not use a vague “all rows for today” message without the time filter.

**Manual test:** Publish **one** row, verify UUID written, then re-run the agent — it should **skip** that row.

## LinkedIn: feed post vs long-form **article**

- **In scope here (Posts API):** short **LinkedIn feed updates**—including **`teaser.md`**-style copy that **links to** or promotes an article, carousels, and normal feed posts. This matches how Mixpost-style schedulers usually work.
- **Out of scope here:** publishing a full LinkedIn **Article** (the native long-form editor). That flow is often **separate** from a single scheduled “post”; this skill does **not** promise LinkedIn Article API support unless your HypeEngine build documents it explicitly.
- **Practical handoff:** **`linkedin-article-writer`** keeps **`article.md`**. Use **HypeEngine** for the **feed teaser**; publish the **article** via **LinkedIn’s article UI**, or hand off a **Google Doc/Drive** export for a human—document in the campaign **`README-handoff.md`**.

## Setup

1. Ensure you have a running HypeEngine / Mixpost instance and know its base URL (for example `http://localhost:3000` or `https://your-domain.com`).
2. Obtain an API access token for the project (the value used as `{{access_token}}` / `Bearer` token in the Postman collection).
3. Store configuration so OpenClaw can read it automatically:

```bash
mkdir -p ~/.config/hype-engine
echo "hypengn_your_api_key_here" > ~/.config/hype-engine/api_key
echo "your-project-uuid-here"   > ~/.config/hype-engine/project_uuid
echo "https://your-hypeengine-base-url" > ~/.config/hype-engine/base_url
```

> **Important:** This skill expects:
> - API key at `~/.config/hype-engine/api_key`
> - Project UUID at `~/.config/hype-engine/project_uuid`
> - Base URL at `~/.config/hype-engine/base_url`
>
> OpenClaw should read these paths when constructing `curl` requests for this skill.

## API Basics

All requests should derive configuration from the config files:

```bash
HYPE_API_KEY=$(cat ~/.config/hype-engine/api_key)
HYPE_PROJECT_UUID=$(cat ~/.config/hype-engine/project_uuid)
HYPE_BASE_URL=$(cat ~/.config/hype-engine/base_url)
```

Use Bearer authentication and JSON responses:

```bash
curl -X GET "$HYPE_BASE_URL/api/v1/$HYPE_PROJECT_UUID/health" \
  -H "Authorization: Bearer $HYPE_API_KEY" \
  -H "Accept: application/json"
```

> **Note:** The Postman collection `HypeEngine-API-v1.postman_collection.json` defines variables `{{base_url}}`, `{{project_uuid}}`, and `{{access_token}}`. This skill maps them to:
> - `{{base_url}}` → value from `~/.config/hype-engine/base_url`
> - `{{project_uuid}}` → value from `~/.config/hype-engine/project_uuid`
> - `{{access_token}}` → value from `~/.config/hype-engine/api_key`

## Accounts API (which profiles can post)

**List accounts for the current project:**

```bash
HYPE_API_KEY=$(cat ~/.config/hype-engine/api_key)
HYPE_PROJECT_UUID=$(cat ~/.config/hype-engine/project_uuid)
HYPE_BASE_URL=$(cat ~/.config/hype-engine/base_url)

curl -X GET "$HYPE_BASE_URL/api/v1/$HYPE_PROJECT_UUID/accounts" \
  -H "Authorization: Bearer $HYPE_API_KEY" \
  -H "Accept: application/json"
```

Use this to discover the `uuid` of each connected account (Twitter/X, Instagram, Facebook, LinkedIn, etc.) so you can target them when creating posts.

## Media API (assets for posts)

**List media:**

```bash
curl -X GET "$HYPE_BASE_URL/api/v1/media?page=1&limit=20" \
  -H "Authorization: Bearer $HYPE_API_KEY" \
  -H "Accept: application/json"
```

**Upload media (image or video):**

```bash
curl -X POST "$HYPE_BASE_URL/api/v1/$HYPE_PROJECT_UUID/media" \
  -H "Authorization: Bearer $HYPE_API_KEY" \
  -F "file=@/path/to/file.png" \
  -F "name=Optional descriptive name"
```

The response includes a `uuid` for the uploaded media, which you can reference when creating posts.

## Tags API (organizing content)

**List tags for the current project:**

```bash
curl -X GET "$HYPE_BASE_URL/api/v1/$HYPE_PROJECT_UUID/tags" \
  -H "Authorization: Bearer $HYPE_API_KEY" \
  -H "Accept: application/json"
```

Use this to discover tag UUIDs to attach to posts (for workflows like "favorites", campaigns, or thematic groupings).

## Posts API (creating and scheduling posts)

### Scheduling — no separate “publish now” (default for this workspace)

**Preferred flow:** one **POST `/posts`** per approved row, with:

- **`date`** and **`time`** set from **`APPROVAL.md` Go-live datetime** (same as **`calendar.md` Local time** for that slot).

HypeEngine then **schedules** the post and **publishes when the time arrives** (or per your instance’s rules if the datetime is “now” / past—verify in the HypeEngine UI). The agent **does not** need a second call to “publish now” unless **`USER.md` / `TOOLS.md`** or the human explicitly requires it **and** your API documents a separate publish endpoint.

**Avoid:** creating a **draft** (omit `date`/`time`) and expecting auto-publish—drafts stay until something publishes them. **Avoid:** duplicate **POST `/posts`** for the same slot (idempotency).

### List posts

```bash
curl -X GET "$HYPE_BASE_URL/api/v1/$HYPE_PROJECT_UUID/posts?status=&page=1&limit=20" \
  -H "Authorization: Bearer $HYPE_API_KEY" \
  -H "Accept: application/json"
```

`status` filter (optional):
- `0` – draft
- `1` – scheduled
- `2` – published
- `3` – failed

### Create a post for multiple accounts

This mirrors the **Create Post** request from the Postman collection while keeping the payload easy to edit.

```bash
curl -X POST "$HYPE_BASE_URL/api/v1/$HYPE_PROJECT_UUID/posts" \
  -H "Authorization: Bearer $HYPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "versions": [
      {
        "accountUuid": "",
        "original": true,
        "content": [
          {
            "body": "<p>Base content for all accounts</p>",
            "media": ["MEDIA_UUID_1"]
          }
        ]
      },
      {
        "accountUuid": "ACCOUNT_UUID_TWITTER",
        "original": false,
        "content": [
          {
            "body": "<p>Custom content for Twitter account</p>",
            "media": ["MEDIA_UUID_1", "MEDIA_UUID_2"]
          }
        ]
      }
    ],
    "accountUuids": [
      "ACCOUNT_UUID_TWITTER",
      "ACCOUNT_UUID_INSTAGRAM"
    ],
    "tags": [
      "TAG_UUID_1",
      "TAG_UUID_2"
    ],
    "date": "2024-12-25",
    "time": "14:30"
  }'
```

- `versions` describes the base/original content and any per-account overrides.
- `accountUuids` is the list of accounts this post should publish to.
- `tags` is an array of tag UUIDs (from the Tags API).
- `date` and `time` control scheduling—**set both** from **`APPROVAL.md`** so HypeEngine handles the queue; omit only if you intentionally want a **draft** (not the default here).

### Update an existing post

```bash
POST_UUID="existing-post-uuid"

curl -X PUT "$HYPE_BASE_URL/api/v1/$HYPE_PROJECT_UUID/posts/$POST_UUID" \
  -H "Authorization: Bearer $HYPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "versions": [
      {
        "accountUuid": "",
        "original": true,
        "content": [
          {
            "body": "<p>Updated base content</p>",
            "media": ["MEDIA_UUID_1"]
          }
        ]
      }
    ],
    "accountUuids": ["ACCOUNT_UUID_TWITTER"],
    "tags": ["TAG_UUID_1"],
    "date": null,
    "time": null
  }'
```

## Typical social posting workflow

- **Check APPROVAL first:** For each **Post ID**, if **`HypeEngine post UUID`** is set → **skip** (see *Idempotency* above).
- **Assume connected accounts**: In this workspace, LinkedIn + Twitter are **already linked** in HypeEngine—list UUIDs when needed, then **push** approved posts; no per-run OAuth narrative.
- **Discover accounts**: Call the Accounts API to list available social accounts and grab their UUIDs. **Filter** to the **Twitter/X** and **LinkedIn** accounts you need before building `accountUuids`.
- **Find or upload media**: Use the Media API to either list existing media or upload new images/videos and capture their UUIDs.
- **Pick / create tags**: Use the Tags API to find tag UUIDs to attach to the post.
- **Create posts (default):** POST `/posts` with **`date` + `time`** + media UUIDs—let HypeEngine schedule/publish. **Update** only for edits, not as a second “go live” step.
- **Pair with workspace drafts**: Read approved copy from `workspace/drafts/social/.../post-bundle.md` or captions files, and `workspace/drafts/linkedin/.../teaser.md` for LinkedIn teasers; convert line breaks to `<p>` / `<br>` as required by your HypeEngine payload format. **Do not** pull routine feed posts from Google Drive—Drive is for **LinkedIn article** handoff only (`INTEGRATIONS.md`).

