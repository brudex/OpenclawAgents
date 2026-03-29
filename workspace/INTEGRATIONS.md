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
| `OPENAI_API_KEY`, `FAL_KEY`, `GEMINI_API_KEY` | Image/video generation tools |

## OpenClaw channels (preferred when available)

If **`~/.openclaw/openclaw.json`** already defines **Telegram, Discord, LinkedIn, etc.**, prefer **channel tools** for publish/read instead of raw curl. Skills should say: “use configured channel” first, curl second.

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
