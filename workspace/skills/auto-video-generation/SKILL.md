---
name: auto-video-generation
description: Video planning (beat sheet, VO, captions) plus actual MP4 when Gemini Veo is available on the key; with OpenClaw+Gemini configured, default to attempting Veo render after planning—else document handoff to Remotion/ffmpeg.
metadata: {"clawdbot":{"emoji":"🎬"},"openclaw":{"emoji":"🎬"}}
---

# auto-video-generation

Produce **production-ready planning artifacts** for video: not just a script, but **timed beats**, **shot direction**, **audio plan**, and **caption timing** so an editor or codegen tool (e.g. Remotion) can execute without guessing. Each run should leave a **dated, named folder or file set** under the workspace `drafts/` tree—same discipline as `qf-course-researcher` creates a dated Notion page.

## When Gemini is available (this workspace — default)

If **OpenClaw already has Gemini** (`~/.openclaw/.env`, `~/.config/gemini/api_key`, or host tools wrapping the same API), **after** writing the planning files, **attempt** a **Gemini Veo** render (async start → poll → download **`.mp4`**) per [Gemini video / Veo docs](https://ai.google.dev/gemini-api/docs/video) and **`workspace/INTEGRATIONS.md`**. Save e.g. **`veo-output.mp4`** under the same `workspace/drafts/video/<run>/` folder and log model, operation id, and path in **`veo-render.md`**.

- **If Veo succeeds:** the run delivers **both** the beat sheet **and** a real clip.
- **If the key has no Veo access, quota fails, or the API errors:** do **not** pretend a file exists—note the error in **`veo-render.md`** and fall back to **Remotion/ffmpeg** handoff in **`README-handoff.md`**.
- **Brief-only** only when the human explicitly asked no render.

## Prerequisites

- **Workspace context**
  - Read `USER.md` (brand, audience, taboo topics) and `SOUL.md` (voice) before writing.
  - Default output root:
    ```text
    workspace/drafts/video/<YYYY-MM-DD>-<slug>/
    ```
  - Create directories if missing (`drafts/video/…`).

- **Brief from human or upstream skill**
  - Required: **goal** (awareness, signup, explain), **primary platform**, **max duration** (seconds), **aspect ratio** (9:16 vertical vs 16:9).
  - Optional: link to `auto-research-agent` or `social-trend-monitor` brief for factual claims (cite in script notes).

- **Related skills in this repo (optional chaining)**
  - `video-generator/` (repo root) — Remotion-oriented references under `video-generator/references/` if the agent should align with existing composition patterns.
  - `eleven-labs-music/` — voice/music generation scripts when the human wants TTS or bed music; **do not** assume licensed trending TikTok audio unless rights confirmed.
  - `tiktok-video-ads-creator` — for **platform-native hook variants** after this skill produces the master brief; hand off `beat-sheet.md` + `shot-list.md`.

- **Tools**
  - Web search when the video references **news, stats, or product facts**—same rule as research skills: no invented statistics.
  - File write access to workspace `drafts/video/`.

## Credentials & API (qf-style)

- **Planning-only (exception):** When the human asked no render, or Gemini/Veo is unavailable after a real attempt — still ship beats + scripts under `workspace/drafts/video/...`.
- **Rendered video (default when Gemini + Veo available):** **`GEMINI_API_KEY`** / **`~/.config/gemini/api_key`** — **async** Veo flow: start → **poll** → **download** `veo-output.mp4` (or similar) into the draft folder. Merge **beat sheet + VO** into one cinematic **prompt**; set **`aspectRatio`** (`"9:16"` / `"16:9"`) per brief. Endpoints evolve — follow [Gemini video / Veo docs](https://ai.google.dev/gemini-api/docs/video) and **`workspace/INTEGRATIONS.md`**.
- **Fallback:** **Remotion + ffmpeg** or **`eleven-labs-music`** when Veo is not enabled on the project or the render fails; do not assume licensed trending TikTok audio unless rights confirmed.

## High-level Workflow

1. **Intake and platform lock**
   - Confirm **one primary platform** first edit (TikTok, Instagram Reels, YouTube Shorts, YouTube long, LinkedIn video).
   - Map to constraints:
     - **Vertical short (9:16):** safe zones for UI (caption, like button); **hook in 0–3s**; typical **15–60s** unless brief says otherwise.
     - **Long-form (16:9):** cold open **≤15s** or chapter hooks; act structure (setup → tension → payoff).

2. **Concept lock**
   - One **logline** (≤25 words) + **viewer takeaway** (one sentence).
   - List **non-goals** (what this video will not promise—legal/safety).

3. **Beat sheet with timestamps**
   - Produce `beat-sheet.md` with a table:

     | T_start | T_end | Audio (VO / line) | On-screen text | Visual (shot) |
     |---------|-------|-------------------|----------------|----------------|
     | 0:00 | 0:03 | Hook line | 3–5 words max | ECU / text pop |
     | … | … | … | … | … |

   - **Rule:** first row must cover **0:00–0:03** (or 0:00–0:05 for long-form cold open) with a **pattern interrupt** + clear topic promise.

4. **Shot list**
   - Produce `shot-list.md`:
     - For each beat: **shot type** (wide/medium/close-up), **movement** (static/pan/handheld), **B-roll** vs A-roll, **props**, **lighting note** (high-key, natural, etc.).
     - Flag **stock vs record** if applicable.

5. **Full VO script**
   - Plain script in `vo-script.md` (continuous prose or line-per-beat matching beat-sheet rows).
   - **WPM sanity:** for 30s VO, ~75–90 words typical; adjust if talent speaks fast/slow.

6. **Captions / subtitles outline**
   - `captions.srt` **outline** in markdown (timecodes + line) for short-form **burn-in** style, or note “SRT export left to editor.”
   - Keep **on-screen text ≤5 words** per card for vertical unless brief demands denser (educational).

7. **Audio plan**
   - Section in `audio-plan.md`:
     - **VO:** tone (warm, urgent, deadpan).
     - **Music:** genre + BPM range + “royalty-free only” unless human provides license.
     - **Trending sound:** if requested, **warn** in file: TikTok commercial use may require cleared sound; default to original or licensed bed.

8. **Handoff package**
   - Write `README-handoff.md` in the same folder summarizing:
     - Files included.
     - Next skill: e.g. “Pass `beat-sheet.md` to `tiktok-video-ads-creator` for hook A/B/C variants.”
     - **Approval gate:** “Human approves before upload.”

9. **Optional JSON for tooling**
   - If downstream automation expects JSON, add `brief.json` with keys: `platform`, `duration_target_sec`, `aspect_ratio`, `beats[]` `{start,end,audio,visual,on_screen_text}`.

10. **Scheduling**
    - For **campaign** use: one folder per video concept; date prefix avoids overwrites.
    - For **series:** use slug `series-name-ep-01` etc.

## Outputs (required files)

Minimum per run:

- `workspace/drafts/video/<YYYY-MM-DD>-<slug>/beat-sheet.md`
- `workspace/drafts/video/<YYYY-MM-DD>-<slug>/shot-list.md`
- `workspace/drafts/video/<YYYY-MM-DD>-<slug>/vo-script.md`
- `workspace/drafts/video/<YYYY-MM-DD>-<slug>/README-handoff.md`

Recommended:

- `audio-plan.md`, `captions-outline.md`, optional `brief.json`

## Agent Checklist

- [ ] Read `USER.md` / `SOUL.md` (or explicit brief overrides).
- [ ] Platform and duration locked before writing beats.
- [ ] **0–3s hook** row present for vertical short-form.
- [ ] No false “official” or certification claims unless sourced.
- [ ] All factual claims in VO either generic or tied to provided research with citation note in `README-handoff.md`.
- [ ] Audio/legal section addresses trending-sound risk.
- [ ] Folder created under `drafts/video/<date>-<slug>/` with all required files.
- [ ] User told exactly which path to open; if Gemini was configured, **`veo-render.md`** records whether an **MP4** was saved or why Veo was skipped/failed; never claim a clip without a file or explicit API failure note.
- [ ] If `video-generator/` patterns apply, reference `video-generator/references/composition-patterns.md` where useful (do not duplicate entire doc).
