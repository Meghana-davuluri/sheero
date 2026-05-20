---
name: weekly_rollup
description: Compress one ISO week of daily logs, feeds, decisions, and session notes into a single summary file at memory/weekly/YYYY-Wnn.md. Trigger with "weekly rollup", "weekly review", or "summarize this week".
---

# weekly_rollup

## Goal

Take all the granular data Sheero accumulated in one ISO week — daily logs, GitHub feeds, decisions, session notes, scratchpad processing — and produce ONE clean summary file at `memory/weekly/YYYY-Wnn.md`.

This is the foundation of the memory tree. Daily logs answer "what happened today?" The weekly rollup answers "what happened this week?" without making you read seven separate files.

---

## When to run

- **Sunday evening** as part of the evening check-in (eventually wired in automatically)
- **Manually** when you ask Sheero "summarize this week" or "weekly rollup"
- **From the Telegram bot** for the same trigger phrases

---

## Step 1 — Determine the target week

Default to the **current ISO week** (this is the week we're closing out).

To get the ISO week and Monday/Sunday bounds:

```bash
WEEK=$(date +"%G-W%V")            # e.g., 2026-W21
MONDAY=$(date -v -mon +"%Y-%m-%d" 2>/dev/null || date -d "monday" +"%Y-%m-%d")
SUNDAY=$(date -v +sun +"%Y-%m-%d" 2>/dev/null || date -d "sunday" +"%Y-%m-%d")
```

If the user asks for "last week" or specifies a week (e.g., "weekly rollup for W19"), use that target instead.

If a rollup file already exists for the target week, **read it first** and treat this run as an update (preserve any hand-written notes the owner added, merge in the new auto-generated parts).

---

## Step 2 — Gather the week's data (silent, parallel where safe)

### A. Daily log entries for this week

Read `memory/daily_log.md`. Pull every `## Day M/DD/YYYY` block whose date falls between Monday and Sunday (inclusive).

For each day, extract:
- Habit data (sleep, exercise, etc.)
- Journal entry
- Dominant theme (last line of journal usually states it)

### B. GitHub feeds for this week

Read every `memory/feeds/github/YYYY-MM-DD.md` whose date is in the week range.

For each day, capture:
- Active repos + commit counts
- Open PRs, issues, review requests
- Any flags

### C. Gmail feeds for this week (if they exist)

Read every `memory/feeds/gmail/<account>/YYYY-MM-DD.md` in range. Skip silently if `memory/feeds/gmail/` doesn't exist yet (Phase 6 still partial).

### D. Calendar feeds for this week (if they exist)

Same pattern. Skip silently if missing.

### E. Meeting transcripts for this week (if they exist)

Read `memory/feeds/meetings/*.md` files in range. Skip silently if missing.

### F. Decisions logged this week

Read `journal/decisions_log.md`. Pull `## YYYY-MM-DD — Title` blocks whose date is in the week range.

### G. Session log entries this week

Read `journal/session_log.md`. Pull entries with dates in the week range.

### H. Scratchpad items processed this week

Read `cortex/scratchpad.md`. If the scratchpad is empty or near-empty, that means items were processed during evening check-ins this week — count is harder to derive, just note "scratchpad currently clean" or list any carryovers.

---

## Step 3 — Synthesize across all sources

Build a coherent narrative, not a dump. Key sections:

### Highlights
Three to five sentences identifying the **important** outcomes of the week. Not a list of everything — the things that mattered.

### People mentioned
Anyone surfaced in daily journals, decisions, or feeds. Count mentions if helpful. Link to `cortex/people/<name>.md` if those files exist (they may not yet — Phase 7 also adds topic trees).

### Projects worked on
Group by project (e.g., main product, client work, side projects, Sheero itself, job search if applicable, etc.). For each: rough commit count from GitHub feed, status notes from daily logs or decisions.

### Themes from journals
Identify the recurring dominant themes (clarity, frustration, momentum, etc.) across daily journal entries. Patterns matter — three "frustration" days in a row is signal.

### Decisions made
Bulleted list of decisions logged this week, with one-line context each.

### Open threads at week's end
What's mid-flight: open PRs, half-done projects, unanswered emails, things to carry to next week.

### Habits / metrics
Roll up habit data if it's in daily logs. Average sleep, exercise days, etc. Skip if there's no habit data.

### What didn't happen
Notable absences. Was there a goal on Monday that's still untouched on Sunday? Flag it without being preachy.

---

## Step 4 — Write the rollup file

Save to `memory/weekly/YYYY-Wnn.md` (e.g., `memory/weekly/2026-W21.md`).

Template:

```markdown
---
week: <YYYY-Wnn>
range: <Monday-date> to <Sunday-date>
generated: <ISO-8601 UTC>
sources: daily_log, feeds_github, [feeds_gmail], [feeds_calendar], [feeds_meetings], decisions_log, session_log, scratchpad
days_with_journal: <count>
github_commits: <total across the week>
---

# Week of <Month DD>–<DD>, <Year> (<YYYY-Wnn>)

## Highlights

<3-5 sentence narrative of what mattered this week>

## People mentioned

- <Name> (<n mentions>) — <one-line context>

If none, omit this section.

## Projects worked on

| Project | Commits | Status / notes |
|---|---|---|
| <project> | <n> | <notes> |

## Themes from journals

<2-3 sentence read on the emotional/energetic shape of the week>

## Decisions made

- **<YYYY-MM-DD — Title>** — <one-line summary>

If none, write *"No decisions logged this week."*

## Open threads at week's end

- <thread> — <one-line context>

## Habits / metrics

Only include if daily logs had habit data. Otherwise omit.

## What didn't happen

- <untouched goal> — <flag, no judgment>

If everything planned actually got done, write *"Nothing flagged — week tracked to plan."*
```

---

## Step 5 — Report to the owner

Brief 3-line message:

> "Weekly rollup for <YYYY-Wnn> done. Wrote `memory/weekly/<YYYY-Wnn>.md`.
> [One-line headline pulled from the Highlights section]
> [Flag if any "open thread" or "what didn't happen" item is urgent, else 'Nothing flagged.']"

---

## Step 6 — Do NOT commit

The rollup file is just data. It gets committed when `evening_checkin` or `save` runs next. Don't make a separate commit.

---

## Edge cases

- **Empty week** (no daily logs, no GitHub activity) — still write the file with empty sections and a one-line note: *"Quiet week — minimal data captured."* Consistency matters; future skills need to be able to find the rollup file.
- **Partial week** (running on Tuesday for the current week) — produce a partial rollup with a note: *"⚠️ Partial week — generated <date> mid-week. Re-run on Sunday for full week."*
- **Re-run on same week** — overwrite the file but preserve any sections the owner manually edited (look for a `<!-- manual -->` marker at the top of any section).
- **Stale feed data** — if a feed file exists but is older than 7 days, note "feed file present but may be stale: <date>".

---

## Tone

Honest. Patterns matter more than positivity. If the week was hard, say so without dressing it up. If it was productive, say so without inflating it. The rollup is for *future you* to read, and future you wants accurate data, not cheerleading.
