---
name: sync_all
description: Orchestrator — runs every available sync skill (GitHub, Gmail, Calendar) in sequence. Trigger with "sync all", "sync everything", or "refresh feeds".
---

# sync_all

## Goal

Run every available sync skill in one shot so all `memory/feeds/` data is fresh. This is the skill `morning_checkin` can call before its rundown to ensure the feed files reflect the last few minutes, not yesterday.

---

## Available sync skills

Run each one that exists. Skip silently if the skill file is missing — that means it hasn't been built yet, not an error.

| Skill | Status | Reads from |
|---|---|---|
| `sync_github` | ✅ Active | `gh` CLI |
| `sync_gmail` | ⏳ Planned (Phase 6 — OAuth setup paused) | Gmail MCP per account |
| `sync_calendar` | ⏳ Planned (Phase 6) | Calendar MCP per account |

---

## Step 1 — Run each available sync

For each skill in the table above, check if `.claude/skills/<skill_name>/skill.md` exists.

- **If yes:** Read the skill file and execute its steps. Capture a one-line result (e.g., "GitHub: 9 active repos, 0 open PRs").
- **If no:** Skip silently. Don't report it as an error.

Run them **in sequence**, not parallel — keeps the output readable and avoids hitting rate limits across services.

---

## Step 2 — Tell the owner

After all skills run, report a single consolidated message:

> "Sync complete.
> - GitHub: <one-line summary>
> - Gmail (yourwork): <one-line summary or 'skipped — not configured'>
> - Gmail (personal): <one-line summary or 'skipped — not configured'>
> - Calendar (yourwork): <one-line summary or 'skipped — not configured'>
> - Calendar (personal): <one-line summary or 'skipped — not configured'>
>
> [Flag line if any urgent items, else 'Nothing urgent.']"

Keep it tight. The detail lives in the feed files, not in the report.

---

## Step 3 — Do NOT commit

Same as the individual sync skills — feed files get committed when `morning_checkin` or `save` runs next. Don't make a separate commit just for a sync.

---

## When to run this

- **Manually** when you want fresh feeds before asking Sheero a question
- **Automatically** as the first step of `morning_checkin` (once integrated)
- **From the Telegram bot** when the user says "sync" or "refresh"
- **From a scheduled launchd plist** if you want automatic refreshes (not set up yet)

---

## Tone

Direct. No fluff. Just status. If a service is down or rate-limited, say so factually with the reset time.
