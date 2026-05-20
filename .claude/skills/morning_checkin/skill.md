---
name: morning_checkin
description: Daily morning check-in. Opens the day — journal, optional daily prompt, then rundown of email/calendar/weather/tasks. Trigger ONLY with "morning check-in", "good morning", or explicit morning-routine requests. Do NOT trigger on generic greetings like "hi" or "hello" — your often messages Sheero throughout the day and most greetings are casual, not routine starts.
---

# Morning Check-In

## Goal
Open today. Done in under 5 minutes.

---

## Step 0 — Time-of-Day Check
Before doing anything, check the current local time (shell: `date +%H`).
- If the hour is ≥ 12 (afternoon or later), pause and ask:
  > "It's {{HH:MM}} — did you mean the *evening* check-in? Say 'yes' for evening, or 'morning anyway' to continue with morning routine."
- If the user confirms evening, stop and run evening_checkin instead.
- Otherwise proceed.

---

## Step 1 — Open Prompt
Ask the owner two things in one message:

> "Good morning. What's on your mind?
> Also — how many hours did you sleep?"

Wait for their response before proceeding.

---

## Step 2 — Log Journal Entry
Log their response to `memory/daily_log.md` under today's date with the heading **Morning Journal**.

Identify the dominant theme of the journal entry (self-criticism, inaction, acceptance, gratitude, frustration, clarity, etc.).

---

## Step 3 — (Optional) Daily Prompt
If you have a `cortex/daily_prompts.md` or equivalent, select a prompt or reflection that matches the dominant theme from Step 2. Output it and wait for any response before continuing.

If no prompt file exists, skip this step.

---

## Step 4 — Gather Everything (Silent)
Before asking if the owner is ready, internally gather all of the following.

**Pattern: prefer reading today's feed file. If it doesn't exist, run the corresponding sync skill first, then read.**

- **Scratchpad** — Read `cortex/scratchpad.md`. Flag anything time-sensitive or directly relevant to today.
- **GitHub** — Check `memory/feeds/github/YYYY-MM-DD.md` for today's date.
  - If it exists, read it and surface: active repos this week (top 3), open PRs awaiting review, anything in the "Flags" section.
  - If it doesn't exist, run the `sync_github` skill first, then read the freshly written file.
- **Email** — Check `memory/feeds/gmail/<account>/YYYY-MM-DD.md` for each configured account (yourwork, personal).
  - If feed exists, surface flagged urgent items.
  - If feed doesn't exist AND Gmail MCP is configured, run `sync_gmail` first.
  - If Gmail MCP isn't configured yet (Phase 6 still partial), skip this section silently.
- **Calendar** — Same pattern: `memory/feeds/calendar/<account>/YYYY-MM-DD.md`, fall back to `sync_calendar` if missing, skip if MCP not configured.
- **Weather** — Fetch current weather (one-liner, real-time, no feed needed).
  - Example: `https://wttr.in/Anytown?format="%t+%C+%w"`
- **Todos** — Pull 3–5 tasks from `cortex/priorities.md`.
  - Max 5 meaningful tasks (projects, goals, research, errands with weight)
  - Small errands can be added beyond the 5
  - Match tasks to current phase and energy level
  - Do NOT include habit/routine tasks that are tracked separately

### Why prefer feeds over live fetches?

Feeds are faster, work offline, and produce a permanent record. Live fetches make the check-in slow and dependent on API availability. The feed files double as the morning rundown's source AND the data weekly_rollup compresses into summaries.

---

## Step 5 — Ask If Ready
Once everything is gathered, ask:

> "Ready for the rundown?"

Wait for confirmation before outputting Step 6.

---

## Step 6 — Rundown
Output in this order:

1. **Day M/DD/YYYY** | [weather one-liner if configured]
2. **Email** — split by account if multiple feeds, or "Nothing urgent" / "Email sync not configured"
3. **Calendar** — today's events or "Nothing on the calendar" / "Calendar sync not configured"
4. **GitHub** — top 3 active repos this week, open PRs awaiting review, any flags from the feed. Or "Nothing new" if everything's quiet.
5. **Scratchpad** — flagged items or item count if nothing urgent
6. **Today's Todos** — numbered list

### Output format guidance

- Each section is one line if there's nothing to flag — don't pad with "Nothing to report on this front."
- If a feed is missing because the sync skill isn't built yet (e.g., Gmail mid-Phase-6), say so once at the bottom: "*Email/Calendar feeds not yet configured.*"
- Total rundown should fit on one screen — terse, scannable.

---

## Step 7 — Commit & Push
Run git add, commit, and push to GitHub.
Commit message format: `Morning note — [date]`

Confirm:
- [ ] Morning journal entry logged
- [ ] Git push succeeded

If anything failed, fix it before closing.

---

## Tone
Direct. No fluff. No cheerleading. Short sentences. Honest.

---

## Customization Notes

- **Step 3** — Replace with your own daily reflection system (stoic precepts, affirmations, tarot, etc.)
- **Step 4 Weather** — Update the city in the wttr.in URL
- **Step 4 Todos** — Adjust file paths if your priorities/goals files are named differently
- **Step 4 Feed-first pattern** — If you add new sync skills (e.g., `sync_linear`, `sync_notion`), follow the same shape: read today's feed file, fall back to running the sync skill, skip silently if not configured.
- **Step 6** — Add or remove rundown sections based on what matters in your morning
