---
name: adverts-creator
description: Platform-specific ad packs with character-limit matrices, 2–8 labeled variants, UTM matrix, audience angle notes, and compliance block—writes to workspace/drafts/ads/; pairs with auto-image-generation for creative tests.
metadata: {"clawdbot":{"emoji":"💰"},"openclaw":{"emoji":"💰"}}
---

# adverts-creator

**Paid social** copy packs with **variant discipline**—like `qf-course-researcher` enumerates certifications in a database, this skill enumerates **variants** in a table with **test hypotheses**.

## Prerequisites

- Offer, **landing URL**, **prohibited claims**, **geo**, **language** from human.
- UTM convention: `utm_source`, `utm_medium`, `utm_campaign`, `utm_content=<variant_label>`.
- Output:
  ```text
  workspace/drafts/ads/<YYYY-MM-DD>-<campaign-slug>/
  ```

## Credentials & API (qf-style)

- **Draft-only:** No keys; variants and UTM matrix under `workspace/drafts/ads/...`.
- **Live campaigns:** **Meta Marketing API** — e.g. `~/.config/meta_ads/access_token` or `META_ACCESS_TOKEN`; example `curl` in **`workspace/INTEGRATIONS.md`**. **Google Ads** — developer token + OAuth (`GOOGLE_ADS_*`); see Google’s current Ads API auth docs. Never commit tokens.

## High-level Workflow

1. **Platform matrix (`platform-limits.md`)**

   | Platform | Headline max | Primary text | Description | CTA chars |
   |----------|--------------|--------------|-------------|-----------|
   | Meta | ~40 ideal | ~125 first screen | optional | short |
   | Google RSA | 30×N headlines | 90 desc | — | — |
   | TikTok | punchy short | 1–2 sentences | — | CTA button text |
   | LinkedIn | ~70 headline | ~150 visible | optional | — |

2. **Angle list (`angles.md`)**
   - 4–6 **angles**: pain, aspiration, proof, speed, social proof, risk reversal.

3. **Variant table (`variants.csv` + `variants.md`)**
   - Columns: `variant_label`, `headline`, `primary_text`, `description`, `cta`, `hypothesis`, `utm_content`.

4. **Minimum count**
   - **≥2 variants**; recommend **3–5** for Meta; **≥10 headlines** for Google RSA if requested (rotate combinations note).

5. **Targeting notes (`targeting.md`)**
   - **Suggested** interests, behaviors, exclusions—labeled **non-binding** for media buyer.

6. **Compliance (`compliance.md`)**
   - Sensitive categories checklist; **no** before/after health claims unless allowed; **no** fake countdown.

7. **Creative handoff (`creative-briefs.md`)**
   - Link to `auto-image-generation` folder paths per variant if parallel run.

8. **Scheduling**
   - One folder per **flight**; suffix `-v2` if copy refresh mid-campaign.

## Outputs (required)

- `variants.md` (human-readable), `platform-limits.md`, `compliance.md`, `README-handoff.md`

## Agent Checklist

- [ ] Every variant has unique `variant_label` and `utm_content`.
- [ ] Character limits respected per platform section used.
- [ ] ≥2 variants minimum.
- [ ] No unverifiable stats or fake urgency.
- [ ] Landing URL consistent; UTM appendix complete.
- [ ] User given folder path; media buyer owns live upload.
