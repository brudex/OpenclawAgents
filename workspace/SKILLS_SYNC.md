# Sync workspace skills to the OpenClaw host

Nana’s setup: skills live under the **OpenClaw workspace** so the gateway can **auto-refresh** them (watcher). On the server, that is typically:

```text
~/.openclaw/workspace/
```

This repo keeps the same tree under **`OpenclawAgents/workspace/`**. Deploy by copying/syncing that folder to the server workspace root.

## From your Mac (example)

Replace `contaboadmin` and remote path if your home directory differs.

```bash
rsync -avz --delete \
  /Users/michaelyeboah/Desktop/Projects/OpenclawAgents/workspace/ \
  contaboadmin:~/.openclaw/workspace/
```

- **`--delete`** removes remote files you deleted locally (use carefully).
- Omit `--delete` if you keep extra private files only on the server.

## What gets synced

- `INTEGRATIONS.md` — consolidated **config paths**, **env vars**, and **curl** patterns (same idea as `qf-course-researcher` Prerequisites)
- `skills/**/SKILL.md` — AgentSkills (including new skills from `SkillsToAdd.md`)
- `AGENTS.md`, `USER.md`, `SOUL.md`, etc. — session context
- Existing `qf-*`, `notion`, `youtube-watcher`, … unchanged unless you edit them here first

## After sync

- Restart the gateway **or** start a **new session** if skills don’t appear.
- With **skill watcher** enabled, edits under `skills/` may apply on the next agent turn.

## Source of truth

Requirements are documented in **`SkillsToAdd.md`** (repo root). Implementations live in **`workspace/skills/<skill-name>/SKILL.md`**.
