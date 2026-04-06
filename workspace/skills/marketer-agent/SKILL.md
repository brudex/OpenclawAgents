---
name: marketer-agent
description: Marketing strategy and GTM—ICP, positioning, channel plan, briefs; handoffs to social-media-manager, social-content-writer, x-post-writer, linkedin-article-writer (articles), adverts-creator; dated packs under workspace/drafts/marketing/.
metadata: {"clawdbot":{"emoji":"📈"},"openclaw":{"emoji":"📈"}}
---

# marketer-agent

Turn **business goals** into **market-facing clarity**: who we sell to, what we say, where we show up, and how success is measured—then **hand off** executable briefs to content and ads skills.

## Prerequisites

- **Google Drive — product information (discovery source)**
  - **Product / brief folder ID** lives in **`~/.config/quizfactor/product-info-drive`**: a **single line** containing the Google Drive **folder ID** for authoritative **product information** (Docs, PDFs, exports). Trim whitespace after reading.
  - Before drafting `00-brief.md`, **read everything authoritative in that folder** (Docs, PDFs, markdown exports): **source-of-truth product brief**. Ingest the same way as **`qf-record-pending-uploads`** lists files: Drive API **`files.list`** with `q` = parent = that folder ID and `trashed = false`, then export/download text per file; **or** the host’s built-in Google/Drive integration if already connected.
  - **Cross-reference — `qf-record-pending-uploads`:** That skill uses **`~/.config/quizfactor/google_drive_credentials`** (service account path) and **`~/.config/quizfactor/drive_folder_ids`** (one quiz folder ID per line). **Marketer-agent** uses the **same** credentials file when using a service account, but **must** read the **product** folder from **`product-info-drive`**, **not** from `drive_folder_ids` (those are quiz-import folders only).
  - **Host policy (operator expectation):** On many OpenClaw hosts, **Google is already logged in or integrated** at the platform level. In that case **do not** tell the user to add a service-account JSON or **`~/.config/quizfactor/google_drive_credentials`** for marketer-agent — **connect / use Google through the host** (OpenClaw Google integration, Drive-capable tools, MCP, `gcloud`/user ADC, or whatever the runtime exposes). That file is only for **headless service-account** flows (e.g. alongside **`qf-record-pending-uploads`**).
  - **Auth — prefer the host’s Google integration:** If **OpenClaw** (or the runtime) already has **Google / Drive signed in** or exposes Drive via **tools / MCP / `TOOLS.md`**, use that to read the product folder. **Do not** refuse to use Drive solely because **`~/.config/quizfactor/google_drive_credentials`** is missing — that file is for **service-account** flows (shared with **`qf-record-pending-uploads`** on headless hosts), not the only option for marketer-agent.
  - **Service-account fallback (optional):** When no host Google integration is available, use **`~/.config/quizfactor/google_drive_credentials`** → path to JSON key, same as **`qf-record-pending-uploads`** **Configuration** (`QF_GOOGLE_CREDS_PATH`). Share the **product-info** folder with that service account’s **`client_email`** (Viewer).
  - **Fallback folder IDs** (if **`product-info-drive`** is missing): **`~/.config/marketer/drive_folder_id`** (single line), then legacy **`~/.config/openclaw/marketing_brief_drive_folder_id`**. **Do not** put marketer brief IDs in **`~/.config/quizfactor/drive_folder_ids`** (that file is only for **`qf-record-pending-uploads`** quiz watch folders).
  - Recommended paths when using **service account** (skip `google_drive_credentials` if the host Google integration already covers Drive):
    ```bash
    mkdir -p ~/.config/quizfactor ~/.config/marketer
    echo "/absolute/path/to/google-service-account.json" > ~/.config/quizfactor/google_drive_credentials
    echo 'YOUR_GOOGLE_DRIVE_FOLDER_ID_FOR_PRODUCT_INFO' > ~/.config/quizfactor/product-info-drive
    ```

- Inputs from human: **product** or initiative name, **goal** (awareness, leads, activation, retention), **geo**, **budget band** (optional), **constraints** (compliance, taboo claims) — **after** reconciling with the Drive brief (resolve conflicts by asking the human).
- Read **`USER.md`**, **`SOUL.md`** for brand voice and claims policy.
- Optional: `auto-research-agent` **`report.md`** path for category/competitor context.
- Output root:
  ```text
  workspace/drafts/marketing/<YYYY-MM-DD>-<campaign-or-initiative-slug>/
  ```

## Configuration

**Primary product / brief folder ID:** **`~/.config/quizfactor/product-info-drive`** (single line = Google Drive folder ID). Fallbacks exist for older setups; see resolution order below.

Always derive config from files rather than hard-coding.

**Product / brief folder ID — resolution order (first match wins):**

1. Environment variable **`MARKETING_BRIEF_DRIVE_FOLDER_ID`** if set.
2. **`~/.config/quizfactor/product-info-drive`** (trim whitespace / newlines) — **preferred** for product information.
3. **`~/.config/marketer/drive_folder_id`** (trim whitespace / newlines).
4. Legacy: **`~/.config/openclaw/marketing_brief_drive_folder_id`** if the above are absent.

**Drive authentication — use the first option that works:**

1. **Host Google / Drive already connected** (OpenClaw integration, Drive-capable tool, user OAuth on the host): read the brief folder **without** requiring `~/.config/quizfactor/google_drive_credentials`. **Do not** lead with “credentials file missing at `quizfactor/google_drive_credentials`” — try the integrated Google path first; only mention the JSON pointer if that path fails or does not exist.
2. **Service account file:** if `~/.config/quizfactor/google_drive_credentials` exists and points to a readable JSON key:
   ```bash
   QF_GOOGLE_CREDS_PATH=$(cat ~/.config/quizfactor/google_drive_credentials)
   ```
   Same resolution as **`qf-record-pending-uploads`** `## Configuration`.

**Product / brief folder ID** (resolve for Drive ingest — apply env override first in code):

```bash
# After checking MARKETING_BRIEF_DRIVE_FOLDER_ID:
MARKETING_BRIEF_FOLDER_ID=$(cat ~/.config/quizfactor/product-info-drive)
# If missing, fall back to ~/.config/marketer/drive_folder_id, then legacy openclaw path.
```

Same **`QF_GOOGLE_CREDS_PATH`** pattern as **`qf-record-pending-uploads`** when using a service account (see that skill’s **Configuration**).

Env / folder-ID precedence: see **`INTEGRATIONS.md`**. Use Google client libraries or raw HTTP with OAuth2 **when** using a service account; otherwise use whatever credential path the host integration supplies.

**Folder access:** With user Google, the signed-in account must open the brief folder; with a service account, share the folder with its **`client_email`** (Viewer is enough).

## Brief gate (mandatory — do not “fly blind”)

Before **any** GTM outputs (`00-brief.md`, channel plan, campaign concepts, ad briefs), you must have a **real product or initiative brief** from at least one of:

1. **Google Drive** — Host Google/Drive integration **or** service account via **`~/.config/quizfactor/google_drive_credentials`**, plus a resolvable product/brief folder ID (**`MARKETING_BRIEF_DRIVE_FOLDER_ID`** env, **`~/.config/quizfactor/product-info-drive`**, then **`~/.config/marketer/drive_folder_id`**, or legacy **`~/.config/openclaw/marketing_brief_drive_folder_id`**); folder ingested per workflow step 1 below (same listing pattern as **`qf-record-pending-uploads`**, different config file).
2. **Human in chat** — they paste or clearly state: what is being sold, for whom, goal, and constraints (enough to write `00-brief.md` without guessing).
3. **Workspace file** — e.g. `product-brief.md`, `docs/brief.md`, or a path the human points to; read it fully before drafting.

**If none of the above is available:**

- **Stop.** Do **not** write the required output pack, do **not** invent a placeholder product, and do **not** produce campaigns about **this skill**, OpenClaw, “the marketer agent,” or generic “how to use agents” unless the user **explicitly** asked for that.
- Reply briefly with **one** concrete next step: use the host’s Google/Drive connection if available **or** paste the brief here **or** add a file under the workspace **or** add service-account paths from **Prerequisites** when no host Google integration exists.
- Do not offer a long menu of equivalent options unless the user asked how to connect Drive; default suggestion: **paste the brief** (fastest).

**If Drive cannot be read** (no host Google integration **and** missing/unreadable service-account pointer or JSON): treat Drive as **unavailable** and use chat or workspace brief only — still obey the gate above.

## Credentials & API (qf-style)

- **Draft-only:** No keys; all artifacts under `workspace/drafts/marketing/...`.
- **QuizFactor / Drive alignment:** Product content is read from the folder ID in **`~/.config/quizfactor/product-info-drive`**. **`qf-record-pending-uploads`** uses **`drive_folder_ids`** and **`google_drive_credentials`** — same credential file, **different** folder config; do not confuse the two.
- **Optional:** Sync summaries to **Notion** via **`notion`** skill; paid ad **live** execution via **`adverts-creator`** + **`INTEGRATIONS.md`**; social calendar via **`social-media-manager`**. **Google Drive:** product brief ingest per **Prerequisites**; optional **`social/drive_folder_id`** (see **`INTEGRATIONS.md`**) is for **LinkedIn article** handoff to interns (`04-articles/`), **not** for exporting routine Twitter/LinkedIn feed posts (those use **`hype-engine`**).

## High-level Workflow

1. **Ingest brief (Drive and/or fallback)**
   - Satisfy **Brief gate** first. If Drive is reachable: resolve **`MARKETING_BRIEF_FOLDER_ID`** from **Configuration** (env → **`product-info-drive`** → marketer → legacy), then list/read the folder using **host Google/Drive** **or** **`QF_GOOGLE_CREDS_PATH`** (service account), mirroring **`qf-record-pending-uploads`** Drive listing (`files.list`, parent = folder ID).
   - If Drive is unavailable, use the human’s pasted brief and/or the agreed workspace file only — then proceed; if still no brief, **stop** per **Brief gate** (do not fabricate GTM).

2. **Brief lock (`00-brief.md`)**
   - Goal, primary **CTA**, timeline, **success metrics** (e.g. signups, trials, MQLs), non-goals — aligned to the Drive brief + human inputs.

3. **ICP (`01-icp.md`)**
   - Segments, **jobs-to-be-done**, pains, objections, buying triggers; **anti-ICP** (who not to target).

4. **Positioning (`02-positioning.md`)**
   - Category, **differentiation** (vs status quo + 1–2 named competitor archetypes if research provided), **one-line positioning**, proof types needed (data, logos, demos).

5. **Messaging pillars (`03-messaging-pillars.md`)**
   - 3–4 pillars: **headline**, proof point, example use in copy; **words to use / avoid** per `USER.md`.

6. **Offer & funnel (`04-offer-funnel.md`)**
   - Offer stack (lead magnet, trial, demo), **funnel stages**, suggested next asset per stage; alignment with product **if** `product-manager` outputs exist.

7. **Campaign concept (`05-campaign-concept.md`)**
   - Named campaign angle, **hero hook**, 2–3 supporting angles, **creative guardrails** (legal, brand).

8. **Channel plan (`06-channel-plan.md`)**
   - Table: Channel | Role (reach / nurture / convert) | Format | Cadence suggestion | **Handoff skill** (e.g. `linkedin-article-writer`, `social-media-manager`, `adverts-creator`, `tiktok-video-ads-creator`).

9. **Creative & copy briefs (`briefs/`)**
   - One file per major deliverable type: `linkedin-thought-leadership-brief.md`, `social-week-brief.md`, `paid-ads-brief.md` — each with objective, audience, **must-say**, **never-say**, CTA, **approval gate** note.

10. **Measurement (`07-metrics.md`)**
   - North star + **leading indicators**; UTM / campaign naming convention; what to report weekly.

11. **Handoff index (`README-handoff.md`)**
    - Ordered list: which skill to run next, **input paths** from this folder, expected **output paths** under `workspace/drafts/...`.
    - **Recommended social execution chain** (document explicitly when social is in scope):  
      `social-media-manager` (intake + **`social-content-planning`** → **`calendar.md`**) → **per-slot writers** (**`linkedin-article-writer`** for **articles only**; **`x-post-writer`** for X; **`social-content-writer`** for short LinkedIn feed + Reddit + other platforms; optional **`agency-marketing`**) → publish-ready **`post-body.md`** / **`teaser.md`** → **optional** **`social-caption-writer`** → bundles + **`APPROVAL.md`** → **`hype-engine`**. Track **`pipeline-state.md`** in the campaign folder.

## Coordination (explicit)

| Downstream skill | Typical input from this folder |
|------------------|--------------------------------|
| `social-media-manager` | `06-channel-plan.md`, `briefs/social-week-brief.md` |
| `social-content-planning` | Pillars + calendar hints from channel plan |
| `adverts-creator` | `briefs/paid-ads-brief.md`, offer + UTM from `04` / `07` |
| `linkedin-article-writer` | `briefs/linkedin-thought-leadership-brief.md` (long **articles** only) |
| `social-content-writer` | Short feed / multi-platform slots from `briefs/social-week-brief.md` + `calendar.md` |
| `x-post-writer` | X-only slots from `calendar.md` |
| `agency-marketing` | Deep persona execution (e.g. SEO, TikTok specialist) using `references/` after strategy is set |
| `auto-research-agent` | Optional upstream; marketer consumes `report.md` |

## Outputs (required)

- `00-brief.md`, `02-positioning.md`, `03-messaging-pillars.md`, `06-channel-plan.md`, `README-handoff.md`
- At least **one** file under `briefs/`

## Agent Checklist

- [ ] **Brief gate passed:** real product/initiative identified from Drive **or** chat **or** workspace file — not an invented or meta campaign about the skill unless explicitly requested.
- [ ] **Drive:** used host Google integration **or** `QF_GOOGLE_CREDS_PATH` when present; product folder ID from **`~/.config/quizfactor/product-info-drive`** (or fallback per **Configuration**); **not** from **`drive_folder_ids`**; **Drive product folder** ingested when auth + folder ID work, otherwise skipped with a documented fallback source.
- [ ] ICP and positioning are **specific** (not “everyone” / “best platform”).
- [ ] Claims match evidence or are framed as opinion; no fabricated stats.
- [ ] Channel plan names **handoff skills** and file paths.
- [ ] Compliance / disclosure called out where promos or paid social apply.
- [ ] User given folder path and suggested order: brief → positioning → briefs → handoffs.
