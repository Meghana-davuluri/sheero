# Sheero Architecture

A walkthrough of how the pieces fit together. Audience: developers, recruiters, future-you.

---

## The thesis in one diagram

```
┌─────────────────────────────────────────────────────────┐
│  USER (you, on phone or laptop)                          │
└──────────────────────┬──────────────────────────────────┘
                       │  Telegram message
                       ▼
┌─────────────────────────────────────────────────────────┐
│  INTERFACE — @YourBot on Telegram                    │
│  • Phone / laptop / anywhere Telegram works              │
│  • Photos and documents land in cortex/inbox/            │
└──────────────────────┬──────────────────────────────────┘
                       │  long-polling
                       ▼
┌─────────────────────────────────────────────────────────┐
│  BOT — Python daemon (~262 LOC) on the Mac via launchd   │
│  • Owner-ID whitelist (single-user)                      │
│  • 10 msg/min rate limit                                 │
│  • $5/day cost cap                                       │
│  • Routes messages to `claude -p` with brain as CWD      │
│  • Session continuity via Claude Code `--resume`         │
│  • Auto-commits + pushes brain changes                   │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│  RUNTIME — Claude Code                                   │
│  • CLAUDE.md is the system prompt                        │
│  • Skills define repeatable workflows                    │
│  • Sub-agents handle specialized research                │
│  • MCP servers integrate external services               │
└──────────────────────┬──────────────────────────────────┘
                       │ reads / writes
                       ▼
┌─────────────────────────────────────────────────────────┐
│  BRAIN — git repo of markdown files                      │
│  ┌─────────────────────────────────────────────────┐    │
│  │  cortex/        identity, projects, people     │    │
│  │  memory/        daily logs + weekly + monthly  │    │
│  │  memory/feeds/  auto-fetched external data     │    │
│  │  journal/       decisions log + sessions       │    │
│  │  reference/     operational guides             │    │
│  │  templates/     reusable .md.template          │    │
│  │  pillars/       9 life domains                 │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

---

## The data flow that makes it work

```
┌─────────────────────────────────────────────────────────┐
│  External services (GitHub, Gmail, Calendar, meetings)   │
└──────────────────────┬──────────────────────────────────┘
                       │ sync skills (sync_github, etc.)
                       ▼
┌─────────────────────────────────────────────────────────┐
│  memory/feeds/                                           │
│  • github/YYYY-MM-DD.md                                  │
│  • gmail/<account>/YYYY-MM-DD.md (planned)               │
│  • calendar/<account>/YYYY-MM-DD.md (planned)            │
│  • meetings/YYYY-MM-DD_with-X.md                         │
└──────────────────────┬──────────────────────────────────┘
                       │ morning_checkin reads
                       │ weekly_rollup reads
                       │ refresh_topics reads
                       ▼
┌─────────────────────────────────────────────────────────┐
│  Higher-level summaries                                  │
│                                                          │
│  • memory/daily_log.md           ← evening_checkin       │
│  • memory/weekly/YYYY-Wnn.md     ← weekly_rollup         │
│  • memory/monthly/YYYY-MM.md     ← monthly_rollup        │
│  • cortex/projects/*.md          ← refresh_topics        │
│  • cortex/people/*.md            ← refresh_topics        │
└──────────────────────┬──────────────────────────────────┘
                       │ Sheero answers questions by
                       │ reading the right level
                       ▼
              "What happened today?"        → daily_log
              "What did I do this week?"    → weekly/W21
              "What's the latest on X?"     → projects/x.md
              "Who is Anna?"                → people/anna.md
```

---

## The four layers, summarized

| Layer | Tech | Why it's there |
|---|---|---|
| **Interface** | Telegram bot | Available on phone, laptop, anywhere. Free. Voice notes work natively. |
| **Bot daemon** | Python + python-telegram-bot v22 + launchd | Local. Single-user. Cost-capped. Zero cloud dependency. |
| **Runtime** | Claude Code | Provides the LLM loop, tool use, context management, skills system. Already great — Sheero doesn't reinvent it. |
| **Brain** | Markdown + git | Readable. Editable. Searchable. Diffable. Version-controlled. No vendor lock-in. |

---

## Why each design choice

### Markdown instead of SQLite or vector DB
- You can `cat` any memory file
- `git diff` shows what changed yesterday
- Obsidian, VS Code, any text editor opens it
- No migration risk if the underlying DB changes
- LLMs (including Claude) read markdown natively — no embedding step needed for retrieval

### Local-only Telegram bot (no cloud)
- $0/month hosting
- Personal email and inbox content never leave the laptop
- launchd starts it at login, no ops burden
- One sleeping laptop = silent bot. Trade-off accepted.

### Claude Code as the runtime, not a custom harness
- The hard parts (LLM calls, tool use, context window management, prompt caching) are already solved
- Skills system is the right abstraction — markdown files with steps
- Sub-agents for specialized work without bloating main context
- Updates and improvements come for free

### Three integrations (not 118)
- Gmail, Calendar, GitHub cover ~95% of useful daily context
- Each integration has real depth (multi-account Gmail, repos with PR/issue tracking)
- Easy to add a fourth (Linear, Notion) if a real need shows up — same skill pattern

### Hierarchical memory tree
- Daily logs answer "what today"
- Weekly rollups answer "what this week"
- Monthly rollups answer "what this month"
- Topic trees per project / person answer "what's the latest with X"
- Each level pre-compresses for the level above — fast to query, cheap on tokens

---

## The skill pattern

Every sync, rollup, and capture is a markdown file in `.claude/skills/<name>/skill.md`:

```yaml
---
name: <skill_name>
description: <what triggers it and what it does>
---

# <Skill Name>

## Goal
<one sentence>

## Step 1 — <what>
<commands or instructions>

## Step 2 — <what>
...

## Tone
<voice instructions>
```

Claude Code reads the file and executes the steps. No code compiles. No deployment. Edit a skill in your editor → it runs the new version next time.

---

## What's NOT in Sheero (deliberate)

- ❌ A desktop mascot or animated character
- ❌ A custom LLM harness (Claude Code already does this)
- ❌ A cloud backend or hosted services
- ❌ A vector database or embedding store
- ❌ More than ~5 integrations
- ❌ Real-time meeting bots (we use local Whisper, not a Meet participant)

Each `NOT` is a deliberate boundary — Sheero is opinionated about what it shouldn't try to do.
