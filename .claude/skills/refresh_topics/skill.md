---
name: refresh_topics
description: Update cortex/projects/*.md and cortex/people/*.md topic-tree files with fresh activity pulled from recent feeds, daily logs, decisions, and git history. Hotness-gated — prioritizes entities mentioned most recently. Trigger with "refresh topics", "update projects", or "refresh entities".
---

# refresh_topics

## Goal

Keep the project + people topic trees current. Each `cortex/projects/<slug>.md` and `cortex/people/<name>.md` is a living summary that should reflect what's happened recently for that entity. This skill walks recent data sources, attributes activity to entities, and updates ONLY the auto-managed sections in each file.

This is what makes Sheero's memory feel alive — without it, the topic trees are static snapshots that grow stale.

---

## Core principle: preserve hand-written content

Each topic-tree file has TWO kinds of sections:

| Section | Who manages it | Auto-update? |
|---|---|---|
| `## Summary` | Owner writes manually | ❌ Never touch |
| `## Current goal` | Owner writes manually | ❌ Never touch |
| `## Current context` (people) | Owner writes manually | ❌ Never touch |
| `## Decisions made` / `## Decisions / commitments` | Mixed | 🟡 Append new entries only — never delete |
| `## Recent activity` | Auto-managed | ✅ Rewrite each run |
| `## Open threads` | Mixed | 🟡 Add inferred ones; don't delete owner's entries |
| `## Backlog / next moves` | Owner writes manually | ❌ Never touch |
| `## History` | Auto-managed (append-only) | ✅ Append new entries, never delete or rewrite past entries |
| `## Notes` | Owner writes manually | ❌ Never touch |

**Rule:** when in doubt, leave it alone. A wrong rewrite is worse than a stale section.

---

## Step 1 — Determine the lookback window

Default: **last 14 days**. This is the window the skill scans for activity.

If the user asks "refresh topics for the last month" or specifies a different window, use that.

```bash
LOOKBACK_DAYS=14
SINCE_DATE=$(date -u -v -${LOOKBACK_DAYS}d +"%Y-%m-%d" 2>/dev/null || date -u -d "${LOOKBACK_DAYS} days ago" +"%Y-%m-%d")
TODAY=$(date -u +"%Y-%m-%d")
```

---

## Step 2 — Inventory entities

List all topic-tree files:

```bash
ls cortex/projects/*.md | grep -v README
ls cortex/people/*.md | grep -v README
```

For each file, read its frontmatter to get:
- `slug` or filename → the canonical name
- `aliases` → alternative names to match in text
- `repo` (for projects) → for matching git activity
- `last_refreshed` → if very recent (< 1 day) skip unless force-refresh

---

## Step 3 — Gather recent activity (in parallel where safe)

For the lookback window, collect:

### A. Daily log entries
```bash
# Pull every "## Day M/DD/YYYY" block whose date is in the window
```
Read `memory/daily_log.md`. Extract journal text for each day in window.

### B. GitHub feeds
```bash
ls memory/feeds/github/*.md | filter to dates in window
```
For each daily feed, extract the "Active repos" table and Flags section.

### C. Gmail feeds (if exist)
```bash
ls memory/feeds/gmail/*/*.md | filter to window
```
Skip silently if folder doesn't exist (Phase 6 partial).

### D. Calendar feeds (if exist)
Same — skip silently if missing.

### E. Meeting transcripts (if exist)
```bash
ls memory/feeds/meetings/*.md | filter to window
```
Skip silently if missing.

### F. Decisions logged in window
```bash
grep "^## 20" journal/decisions_log.md  # then filter to window
```

### G. Session log entries in window
Same pattern with `journal/session_log.md`.

### H. Git commits in sheero-brain (window)
```bash
git log --since="$SINCE_DATE" --pretty=format:"%h %ad %s" --date=short
```

### I. Scratchpad current state
Read `cortex/scratchpad.md` — anything currently in flight worth attributing to a project.

---

## Step 4 — Compute hotness per entity

For each entity (project / person), count mentions across all sources gathered in Step 3:

- Exact name match (case-insensitive)
- Aliases from frontmatter
- For projects: repo URL or repo name in GitHub feeds
- Strong signals (commits to a project's repo, decisions tagged with project) count 3x; weak signals (single mention in a daily journal) count 1x

Produce a hotness score per entity. Sort descending.

**Strategy:**
- Top 5 hottest → full refresh (rewrite Recent activity, append to History if new)
- Next 5 → light refresh (Recent activity only)
- Rest → skip this run (their files are still valid, just not freshly touched)

This matches the OpenHuman memory-tree pattern: heavily-referenced entities get more aggressive refreshing.

---

## Step 5 — For each hot entity, update the file

### 5a. Rewrite `## Recent activity` section

Replace the current "Recent activity" block with a fresh one derived from Step 3 data attributed to this entity. Format:

```markdown
## Recent activity

- YYYY-MM-DD: <one-line summary of what happened> (source: <github|daily_log|decision|meeting>)
- YYYY-MM-DD: <another item>
- ...
```

Keep it tight — 5-10 entries max. Older items get migrated to History.

### 5b. Append to `## History` (never overwrite)

For any entity event in Step 3 that's not already in the History section (check by date + first 30 chars of description), append a new bullet to History.

History is append-only — never delete or rewrite past entries.

### 5c. Update frontmatter

Update `last_refreshed: <today>`. If activity was found, also update `last_activity: <most recent date>`.

### 5d. Status inference (optional, conservative)

If a project hasn't had any activity for 30+ days in the lookback windows, suggest in `## Open threads` something like: *"⚠️ No activity since YYYY-MM-DD — review whether this project should be marked `parked`."*

Don't change the status frontmatter automatically — just flag it for the owner to review.

---

## Step 6 — Report to the owner

After processing, output a brief summary:

> "Refreshed N project + N person topic trees. Window: last 14 days.
>
> Most active this window: [project1] (N events), [project2] (N events), ...
>
> Files updated: [list]
> Skipped (low activity): [list]
> Flagged: [any 'no activity in 30+ days' alerts]"

Keep it under 8 lines.

---

## Step 7 — Do NOT commit automatically

Topic-tree updates get committed alongside the next `evening_checkin` or `save` run. Don't create a `refresh_topics` commit on its own — keeps the git log readable.

---

## Edge cases

- **New entity surfaces in data but no file exists** — Don't create the file automatically. Instead, flag it in the report: *"Potential new entity detected: 'X' mentioned N times. Create `cortex/projects/x.md` or `cortex/people/x.md` if relevant."*
- **Two entities with similar names** (e.g., "Sheero" the project vs. "Alex Co-founder" the person) — match by longest-string-first to avoid false attribution; prefer exact aliases from frontmatter.
- **Mention in a quoted email or third-party message** — attribute it, but mark the source so the owner knows it's secondhand.
- **Conflicting status signals** (e.g., "shipped" in one decision but recent commits keep happening) — leave status alone, flag the contradiction in Open threads for owner review.
- **Empty window (no activity at all)** — still bump `last_refreshed` so we know it ran, but report "no activity in window."

---

## Tone

Direct, factual. The topic trees should read like a project status doc, not a journal. Use past tense for History, present tense for Recent activity and Open threads. Avoid adjectives like "great" or "impressive" — let the data speak.
