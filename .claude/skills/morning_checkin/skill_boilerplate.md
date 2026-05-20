---
name: morning_checkin
description: Daily morning check-in. Opens the day — journal, optional daily prompt, then rundown of email/calendar/weather/tasks. Trigger with "morning check-in", "good morning", or any similar greeting.
---

# Morning Check-In

## Goal
Open today. Done in under 5 minutes.

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
Before asking if the owner is ready, internally gather all of the following:

- **Scratchpad** — Read `cortex/scratchpad.md`. Flag anything time-sensitive or directly relevant to today.
- **Email** — Check Gmail via MCP if configured. Flag anything urgent — one line per item.
- **Calendar** — Check Google Calendar via MCP if configured. List today's events briefly.
- **Weather** — Fetch current weather for your location if desired.
  - Example: `https://wttr.in/[YOUR CITY]?format="%t+%C+%w"` — format as a one-liner.
- **Todos** — Pull 3–5 tasks from `cortex/priorities.md` and `memory/goals/weekly.md`.
  - Max 5 meaningful tasks (projects, goals, research, errands with weight)
  - Small errands can be added beyond the 5
  - Match tasks to current phase and energy level
  - Do NOT include habit/routine tasks that are tracked separately

---

## Step 5 — Ask If Ready
Once everything is gathered, ask:

> "Ready for the rundown?"

Wait for confirmation before outputting Step 6.

---

## Step 6 — Rundown
Output in this order:

1. **Day M/DD/YYYY** | [weather one-liner if configured]
2. **Email** — flagged items or "Nothing urgent"
3. **Calendar** — today's events or "Nothing on the calendar"
4. **Scratchpad** — flagged items or item count if nothing urgent
5. **Today's Todos** — numbered list

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
- **Step 6** — Add or remove rundown sections based on what matters in your morning
