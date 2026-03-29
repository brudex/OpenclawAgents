---
name: hype-engine
description: HypeEngine API v1 for managing social media accounts, media, tags, and posts.
homepage: https://example.com/hypeengine
metadata: {"clawdbot":{"emoji":"📣"}}
---

# hype-engine

Use the HypeEngine API v1 to manage social media **accounts**, upload **media**, organize **tags**, and create/schedule **posts** across channels.

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
- `date` and `time` control scheduling; omit them to create a draft.

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

- **Discover accounts**: Call the Accounts API to list available social accounts and grab their UUIDs.
- **Find or upload media**: Use the Media API to either list existing media or upload new images/videos and capture their UUIDs.
- **Pick / create tags**: Use the Tags API to find tag UUIDs to attach to the post.
- **Create or update posts**: Use the Posts API examples above to draft, schedule, or update posts across multiple accounts, attaching media and tags as needed.

