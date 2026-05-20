---
name: monthly_rollup
description: Compress one calendar month of weekly rollups (and any standalone daily logs / feeds) into a single summary at memory/monthly/YYYY-MM.md. Trigger with "monthly rollup", "monthly review", or "summarize this month".
---

# monthly_rollup

## Goal

One calendar month of activity, compressed into a single file at `memory/monthly/YYYY-MM.md`. Reads the weekly rollups first (they're already pre-compressed), then fills gaps from daily logs and feeds for any week without a rollup.

This is the third level of the memory tree. Daily → weekly → monthly. Each level abstracts further.

---

## When to run

- **Last day of the month** (or first day of the next) as part of the evening check-in
- **Manually** when asked for "monthly rollup" or "summarize this month"
- **From the Telegram bot** with the same triggers

---

## Step 1 — Determine the target month

Default: **the month that just ended**. If you're running this on June 1, target May.

If today is mid-month and the user asks for "this month so far," produce a partial monthly with a banner warning, similar to weekly_rollup's partial-week handling.

```bash
# Last completed month (default)
LAST_MONTH=$(date -v -1m +"%Y-%m" 2>/dev/null || date -d "last month" +"%Y-%m")
# Or current month if asked
THIS_MONTH=$(date +"%Y-%m")
```

The user can also say "monthly rollup for 2026-04" — use that target.

---

## Step 2 — Identify weeks in the target month

A calendar month contains 4-5 ISO weeks (some weeks straddle months). Get the list:

```bash
# All ISO weeks whose Monday or Sunday falls within the target month
```

For each week, check whether `memory/weekly/YYYY-Wnn.md` exists.

---

## Step 3 — Gather

For each week in the month:

- **If `memory/weekly/YYYY-Wnn.md` exists:** read it. This is the pre-compressed source — use its sections (Highlights, People, Projects, Themes, Decisions, Open threads, What didn't happen).
- **If it doesn't exist:** fall back to reading daily logs + feeds for that week directly. Note the gap in the monthly's frontmatter.

Also gather, across the whole month:

- **Decisions log entries** (`journal/decisions_log.md`) dated in the target month
- **Session log entries** (`journal/session_log.md`) dated in the target month
- **Git history** for sheero-brain in the month
- **Project status snapshots** — read each `cortex/projects/*.md` for `last_activity` dates and `status` fields

---

## Step 4 — Synthesize

Build a month-level narrative. Sections:

### Headline
Two to three sentences: the month's defining story. Not exhaustive — distilled.

### Highlights
Bullet list of the 5-10 most consequential events/decisions/outcomes across the month. Each one references which week it happened in.

### People in the month
Names that appeared meaningfully. Frequency counts. Note who entered vs. who exited the picture vs. who was consistently present.

### Projects in the month
Per-project status (active / shipped / parked / abandoned) with commit counts and a one-line trajectory. Show which projects gained momentum, which slowed, which started, which ended.

### Themes
What emotional/energetic patterns ran through the month. Is there a dominant arc (e.g., "frustration → clarity → execution")?

### Decisions of consequence
Decisions logged this month that have downstream effects. Skip routine ones.

### Open at month's end
What's mid-flight going into the next month. The "to be continued" items.

### What didn't happen
Goals from the start of the month (if known) that didn't move. Flag without preaching.

### Habit / metric trends
If daily logs captured habit data, roll up the month's averages — sleep, exercise, etc.

---

## Step 5 — Write the file

Save to `memory/monthly/YYYY-MM.md`. Template:

```markdown
---
month: <YYYY-MM>
range: <first-of-month> to <last-of-month>
generated: <ISO-8601 UTC>
weeks_covered: <comma-separated ISO weeks>
weekly_rollups_found: <count out of total weeks>
days_with_journal: <count>
github_commits: <total across the month>
partial: <true|false — only true if month not yet complete>
---

# <Month YYYY> Monthly Rollup

[Optional banner if partial month]

## Headline

<2-3 sentence story of the month>

## Highlights

- <Week label>: <event>
- ...

## People in the month

- <Name> (<n mentions, across N weeks>) — <trajectory>

## Projects in the month

| Project | Status | Commits | Trajectory |
|---|---|---|---|
| <project> | <active/shipped/parked/abandoned> | <n> | <one-line> |

## Themes

<2-3 sentences>

## Decisions of consequence

- **<YYYY-MM-DD — Title>** — <why it matters>

## Open at month's end

- <thread>

## What didn't happen

- <untouched goal/intent>

## Habit / metric trends

Only if daily logs had habit data.
```

---

## Step 6 — Report to the owner

> "Monthly rollup for <YYYY-MM> done. Wrote `memory/monthly/<YYYY-MM>.md`.
> Coverage: <N>/<total> weeks had weekly rollups; the rest were reconstructed from daily logs and feeds.
> [One-line headline]
> [Flag line if anything urgent for next month, else 'Nothing flagged.']"

Keep it to 4 lines max.

---

## Step 7 — Do NOT commit

Same as weekly_rollup. The file is data; it gets committed when `evening_checkin` or `save` runs next.

---

## Edge cases

- **No weekly rollups at all this month** — write the monthly directly from daily logs + feeds. Note in the frontmatter that `weekly_rollups_found: 0`. Quality will be lower; suggest the owner run `weekly_rollup` retroactively for each week.
- **Empty month** — still write the file with a "Quiet month — minimal data captured." note.
- **Re-run on the same month** — overwrite the file but preserve any sections the owner manually edited (look for `<!-- manual -->` marker).
- **Cross-year months** (e.g., December for a January run) — fine, target by `YYYY-MM` either way.

---

## Tone

Same as weekly_rollup: honest, narrative, no cheerleading. The monthly is what future-you will read to remember what mattered. Be accurate over flattering.
