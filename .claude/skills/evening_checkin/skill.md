---
name: evening_checkin
description: Daily evening check-in. Collect today's data, nudge incomplete habits, enforce journal, log and commit. Trigger with "evening check-in", "closing out", "night check-in", or similar.
---

# Evening Check-In

## Goal
Close the day right. Log it. Make sure you showed up. Done in under 10 minutes.

---

## Step 1 — Collect Today's Data
Output a template for the owner to fill in and paste back.

Pull the current habit list from `pillars/physical/habits.md` and build the template from that. Fallback default:

```
Drop today's data and I'll close it out.

[TODAY'S DATE — Day M/DD/YYYY]
sleep:
exercise:
journal:
deep_work:
no_doomscroll:
```

Wait for the owner to submit the filled-in template before doing anything else.

---

## Step 2 — Nudge Incomplete Habits
Before logging, check for any missed or blank habit fields.

For each incomplete habit, flag it with a direct nudge — one sentence, no hype:
- Frame it honestly: the discomfort of doing it now is nothing. Showing up anyway is the identity you're building.

Ask: *"Want to knock any of these out before we close the day?"*

Wait for their response. If they complete something, update the data before logging.

---

## Step 3 — Enforce Journal Entry
If the journal field is blank, empty, or skipped — do not log. Prompt:
> "Journal entry is required. Even one sentence. What happened today?"

Wait for a real entry before proceeding. Non-negotiable.

---

## Step 4 — Log Today
Log to `memory/daily_log.md` using the standard Day M/DD/YYYY format.
Journal entry goes BELOW the habit data.
Fix obvious typos. Leave slang alone.

If you have a scoring rubric for habits (`reference/guides/scoring_rubric.md`), calculate and include the score.

---

## Step 5 — Scratchpad Review
Read `cortex/scratchpad.md`. For each item in the inbox:
- If actionable → add to todo list or priorities, then remove it
- If an idea worth keeping → move to the appropriate project file, then remove it
- If a question → answer it now, then remove it
- If already handled → remove it
- If genuinely unresolvable tonight → leave it, flag it, and get confirmation to carry over

Default is clear. Carry-overs require a stated reason.

---

## Step 6 — (Optional) Weekly Finances Review
If today is Friday (or your preferred weekly review day), prompt:

> "It's the end of the week — time for a quick finances review. Paste this week's transactions and I'll categorize and flag."

Wait for transactions. Categorize, total, flag anomalies, and log to `pillars/financial/weekly_review.md` (create this file if it doesn't exist).

---

## Step 7 — Todo Review
Check what was on today's todo list. Show completed vs. not completed — just the ledger, no judgment. Flag anything unfinished that should carry to tomorrow.

---

## Step 8 — Commit & Push
Run git add, commit, and push to GitHub after logging.
Commit message format: `Daily log — [date]`

---

## Step 9 — Verify
After committing, confirm:
- [ ] Log entry exists with correct date
- [ ] Git push succeeded
- [ ] Scratchpad cleared of processed items

If anything failed, fix it before closing.

---

## Tone
Direct. No fluff. No cheerleading. Short sentences. Honest.

---

## Customization Notes

- **Step 1** — Replace habit fields with your actual daily habits. Common ones: sleep, exercise, meditation, reading, journaling, diet adherence.
- **Step 4** — If you want habit scoring, create a `scoring_rubric.md` that defines point values per habit.
- **Step 6** — Remove or move the finances review if you do it differently.
