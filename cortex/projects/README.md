# Projects — Topic Trees

One file per project or initiative. Each file is a living summary of the project's current state, decisions made, open threads, and recent activity.

## Why this exists

Without project topic trees, context about a project is scattered across:
- `cortex/work.md` (high-level project list)
- `journal/decisions_log.md` (decisions)
- Daily journal entries
- `memory/feeds/github/` (commit activity)
- Email threads about the project

Asking "what's the latest with PhotoFinder?" should be answerable from **one file**. That's what these topic trees do.

## File format

Each `<project_slug>.md` follows this loose template:

```markdown
---
name: <Project Name>
slug: <lowercase, hyphenated>
repo: <github URL if applicable>
status: active | parked | shipped | abandoned
last_activity: <YYYY-MM-DD>
last_refreshed: <YYYY-MM-DD>
related_people: [<names>]
---

# <Project Name>

## Summary
<2-3 sentences: what it is, why it exists, current phase>

## Current goal
<What's the next concrete milestone? Deadline if any.>

## Recent activity
<Last 1-2 weeks of meaningful changes — commits, decisions, blockers>

## Decisions made
<Bulleted log of decisions and why>

## Open threads
<What's in flight, what's blocked, what needs a decision>

## Backlog / next moves
<What's on deck if/when we get back to this>

## History
<Timeline of significant milestones — appended over time>
```

## How files are populated

- **Manually** at first — scaffold with what you know
- **Automatically** by `refresh_topics` skill (Phase 7) — pulls from GitHub feeds, daily logs, decisions log, scratchpad, and updates "Recent activity" + "History"

## What goes in here vs. somewhere else

- ✅ Project status, goals, decisions, blockers
- ✅ Project-specific context (architecture choices, customer feedback, deadlines)
- ❌ Granular task lists — those belong in `cortex/priorities.md` or a project's own issue tracker
- ❌ Code — that belongs in the project's repo
- ❌ One-off notes — those go to `cortex/scratchpad.md` and get processed at evening check-in

## Hotness

`refresh_topics` prioritizes projects with the most recent commits, mentions, or decisions. Active projects get richer refreshes than parked ones.

## Naming convention

- File name = slug (lowercase, hyphenated): `photofinder.md`, `acme-client.md`, `carsearch.md`
- Use one file per project even if it spans multiple repos (e.g., acme-client has 4 repos, one project file)
