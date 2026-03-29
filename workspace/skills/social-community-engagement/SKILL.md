---
name: social-community-engagement
description: Drafts comment and DM responses with classification (question, complaint, praise, troll), escalation rules, and tone variants—writes under workspace/drafts/social/replies/; human sends all outbound messages unless automation is explicitly approved in USER.md or TOOLS.md.
metadata: {"clawdbot":{"emoji":"💬"},"openclaw":{"emoji":"💬"}}
---

# social-community-engagement

**Community** responses with **risk routing**—like `qf-course-researcher` classifies courses as Existing / Inactive / Missing, this skill **classifies** threads and **routes** escalation.

## Prerequisites

- Parent comment/post **quoted** or screenshot path noted.
- `USER.md`: refund policy summary, support email/handle, **topics only human handles** (legal, threats).
- Output:
  ```text
  workspace/drafts/social/replies/<YYYY-MM-DD>-<thread-id>.md
  ```

## Credentials & API (qf-style)

- **Draft replies:** No API keys. Human sends messages unless **`USER.md` / `TOOLS.md`** explicitly allow automation.
- **Live send (optional):** Use **OpenClaw**-connected channels for the platform in question; token paths for direct APIs live in **`workspace/INTEGRATIONS.md`** when you add them.

## High-level Workflow

1. **Classify (`classification`)**
   - One of: `question`, `complaint`, `praise`, `troll`, `partnership`, `security`.
   - **Severity:** low / med / high (high = legal, threats, PII).

2. **Policy check**
   - If **high** or `security` → **no draft**; output template: “ESCALATE_TO_HUMAN” + reason.

3. **Draft variants (med/low only)**
   - **2 replies:** **Short** (≤280 chars) and **Warm** (slightly longer).
   - **De-escalation** language for complaints; **no** argument.

4. **Facts**
   - Only use **facts** from provided brief; if unknown: “I’ll check with the team” pattern—no invented policy.

5. **DM vs public**
   - Note if reply should move to **DM** (PII, order numbers).

6. **Log (`reply-log.csv` append row)**
   - Date, thread id, classification, escalated Y/N, file path (optional if CSV used).

7. **Handoff**
   - Explicit: “Human must send; automation disabled by default.”

## Outputs (required)

- `workspace/drafts/social/replies/<YYYY-MM-DD>-<thread-id>.md` with classification + drafts or ESCALATE block.

## Agent Checklist

- [ ] Classification and severity set before drafting.
- [ ] High severity → no casual reply; escalation block only.
- [ ] Two tone variants for safe cases.
- [ ] No promises (refunds, features, deadlines) unless brief allows.
- [ ] PII handling: no full emails/phones in public reply text.
- [ ] User reminded: human sends unless documented auto-reply allowlist exists.
