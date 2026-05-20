# People — Topic Trees

One file per person who matters in your life or work. Each file is a living summary that Sheero updates over time by reading recent feeds, daily logs, and meeting transcripts.

## Why this exists

Without topic trees, context about a person is scattered across:
- Daily journal mentions
- Email threads
- Meeting transcripts
- Decision notes

Asking "what's the latest with Anna?" would mean grepping eight files. With a topic tree, the answer lives in one place.

## File format

Each `<name>.md` follows this loose template:

```markdown
---
name: <Full Name>
aliases: <nicknames, handles>
role: <one-line role description>
relationship: <work / family / friend / etc.>
last_interaction: <YYYY-MM-DD>
last_refreshed: <YYYY-MM-DD>
---

# <Full Name>

## Summary
<2-3 sentences: who they are, why they matter to you>

## Current context
<What's active with this person right now — open threads, recent conversations>

## Decisions / commitments
<Things one or both of you agreed to>

## History
<Bullet timeline of significant interactions — appended over time>
```

## How files are populated

- **Manually** at first — start with what you know, write it down
- **Automatically** by `refresh_topics` skill (Phase 7) — scans recent daily logs, gmail feeds, meeting transcripts, and updates the "Current context" and "History" sections

## What goes in here vs. somewhere else

- ✅ Personal facts about the person (their kid's name, their preferences, what they're working on)
- ✅ Ongoing threads (what we discussed last, what's pending)
- ❌ One-off facts that don't recur — those live in the daily log
- ❌ Private medical / financial info about *them* — respect their privacy even in your own brain

## Hotness

`refresh_topics` will prioritize files for people who appear most often in recent feeds (the OpenHuman pattern). A person mentioned 12 times this week gets a richer auto-refresh than one mentioned once.
