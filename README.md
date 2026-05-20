# Sheero — Personal AI Executive Assistant

> **Public template repository.** This is the open-source, sanitized version of Sheero. Everything here is the engineering — skills, agents, bot code, architecture, design docs. The sample data (`cortex/me.md`, `cortex/projects/acme-corp.md`, daily logs, rollups) is a fictional "Jane Doe" persona running an imaginary indie SaaS called "Acme Corp" — there to demonstrate what real Sheero output looks like. Fork this, replace the persona with your own context, and run your own Sheero.

> A persistent, file-based AI executive assistant designed to work *with* Claude Code, not replace it. Sheero is the memory layer Claude Code is missing — a structured markdown knowledge base of your life, accessible from anywhere via Telegram, running entirely on your own machine.

---

## Thesis

Most AI agent projects build their own harness — their own UI, their own LLM loop, their own tools. They compete with Claude Code, Cursor, and Codex.

Sheero does the opposite. **Claude Code already does the hard parts.** What's missing is a persistent, structured, file-based memory of your life, plus a way to talk to your assistant from anywhere.

That's what Sheero is.

- **Persistent markdown brain** — identity, work, priorities, daily logs, decisions, references, nine life pillars. Everything Sheero knows is plain markdown in a git repo. You read it, edit it, `git diff` it. No opaque database, no proprietary format.
- **Telegram as the primary interface** — `@YourBot` runs as a launchd daemon on your Mac. Message it from your phone, it routes to Claude Code with your brain as the working directory, and replies with full context.
- **Local-only by design** — no cloud, no vendor lock-in, no monthly hosting bill. Your inbox and journal never leave your laptop.
- **Auto-capture, daily rituals, scheduled nudges** — note/idea/todo messages auto-save to the scratchpad. Morning and evening check-ins open and close the day. Scheduled push notifications from the bot keep momentum without you remembering to ask.

Inspired by [Andrej Karpathy's obsidian-wiki workflow](https://x.com/karpathy/status/2039805659525644595) and [OpenHuman's memory tree](https://github.com/tinyhumansai/openhuman), redesigned as a **Claude Code-native, Telegram-first, local-only** system.

---

## Architecture

```
┌──────────────────────────────────────────────────────┐
│  Interface — Telegram (@YourBot)                 │
│  Phone, laptop, anywhere you already have Telegram   │
└──────────────────────┬───────────────────────────────┘
                       │  long-polling
                       ▼
┌──────────────────────────────────────────────────────┐
│  Sheero Bot — Python daemon on your Mac              │
│  • started by launchd at login                       │
│  • owner-ID whitelist, rate limit, $5/day cost cap   │
│  • routes messages to `claude -p` with brain as CWD  │
│  • session continuity via `--resume`                 │
│  • photo/document uploads land in cortex/inbox/      │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│  Sheero brain — git repo of markdown files           │
│  • cortex/    — identity, work, priorities,          │
│                 scratchpad, inbox, daily prompts     │
│  • memory/    — daily logs, weekly review            │
│  • journal/   — decisions log, session log           │
│  • reference/ — operational guides                   │
│  • templates/ — reusable templates                   │
│  • pillars/   — nine life domains                    │
└──────────────────────┬───────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────┐
│  Runtime — Claude Code                               │
│  • CLAUDE.md is the system prompt                    │
│  • .claude/skills/ define repeatable workflows       │
│  • .claude/agents/ define specialized researchers    │
│  • .claude/bots/telegram/ runs the bot daemon        │
└──────────────────────────────────────────────────────┘
```

---

## Folder Structure

```
sheero-brain/
│
├── CLAUDE.md                          ← system prompt
├── README.md                          ← you are here
├── ROADMAP.md                         ← current status + planned features
│
├── cortex/                            ← identity, focus, capture inbox
│   ├── me.md
│   ├── work.md
│   ├── priorities.md
│   ├── 2_Year_Goals.md
│   ├── scratchpad.md
│   ├── daily_prompts.md               ← theme-matched reflections for morning check-in
│   └── inbox/                         ← Telegram-uploaded photos/docs (gitignored content)
│
├── memory/                            ← daily logs (weekly/monthly rollups planned)
│   └── daily_log.md
│
├── journal/                           ← decisions log + session log
├── reference/                         ← operational guides
├── templates/                         ← daily_log_entry, decision, weekly_review templates
│
├── pillars/                           ← nine life domains
│   ├── physical/
│   ├── emotional/
│   ├── social/
│   ├── spiritual/
│   ├── intellectual/
│   ├── environmental/
│   ├── occupational/
│   ├── financial/
│   └── community/
│
└── .claude/
    ├── CLAUDE.md
    ├── settings.json                  ← Claude Code permissions
    ├── skills/
    │   ├── morning_checkin/
    │   ├── evening_checkin/
    │   ├── save/
    │   └── email_triage/
    ├── agents/
    │   ├── job_search.md
    │   └── kdp_research.md
    └── bots/
        └── telegram/                  ← @YourBot daemon
            ├── bot.py
            ├── notify.py              ← scheduled push notifications
            ├── com.example.telegram.plist
            ├── com.example.notify-morning.plist
            ├── com.example.notify-midday.plist
            ├── com.example.opportunities.plist
            ├── pyproject.toml
            └── README.md
```

---

## Core Skills

| Skill              | Trigger                                    | What it does                                                                   |
|--------------------|--------------------------------------------|--------------------------------------------------------------------------------|
| `morning_checkin`  | "good morning", "morning check-in"         | Journal prompt → daily reflection → email/calendar/weather/tasks rundown → commit |
| `evening_checkin`  | "evening check-in", "closing out"          | Collect daily data → nudge incomplete tasks → log → scratchpad + inbox review → commit |
| `email_triage`     | "triage email", "check inbox"              | Read recent email, classify, surface action items                              |
| `save`             | `/save`                                    | Stage, commit, push → surface open todos and scratchpad items                  |

Plus auto-capture (configured in `CLAUDE.md`): messages starting with `note:` / `save:` / `idea:` / `todo:` / `reminder:` are appended to scratchpad automatically with a timestamp — no command needed.

---

## Sub-agents

Specialized research workers in `.claude/agents/`:

| Agent           | Focus                                                                  |
|-----------------|------------------------------------------------------------------------|
| `job_search`    | Job listings, application tracking, opportunity research               |
| `kdp_research`  | Amazon self-publishing self-publishing — keyword research, listings, optimization  |

---

## Telegram Interface

Sheero is accessible via **[@YourBot](https://t.me/YourBot)** on Telegram. The bot is a Python daemon running locally on your Mac via `launchd` — no cloud, no hosting bill, your data never leaves your laptop.

**What it does:**
- Text messages → routed to `claude -p` with the brain as CWD, replies back with full context
- Photos/documents → saved to `cortex/inbox/` with timestamps, processed at evening check-in
- `/status` → uptime, today's spend, active session ID
- `/reset` → clear the Claude session, next message starts fresh

**Safeguards:**
- Owner-ID whitelist — bot only responds to your Telegram user ID
- Rate limit — 10 messages per minute
- Daily cost cap — $5/day default, configurable
- Session continuity via Claude Code's `--resume`

**Scheduled push notifications:**
- Morning nudge — "Ready to start the day?"
- Midday nudge — "How's the day going?"
- Opportunity scan — periodic job/gig lead surfacing

**Note:** the bot is only up when your Mac is awake. Telegram queues messages during short sleeps, so it's fine for normal use. Long trips = silent bot until you're back at your laptop.

Full bot docs at [`.claude/bots/telegram/README.md`](.claude/bots/telegram/README.md).

---

## What Sheero is NOT

- **Not another agent harness** — Claude Code is the runtime. Sheero is the memory + workflow layer on top.
- **Not a desktop mascot** — no animated character, no on-screen face. Sheero lives in your terminal and your Telegram.
- **Not 118 integrations** — focused integrations beat exhaustive ones. Add when needed, justify each one.
- **Not cloud-hosted** — bot runs locally. No Railway, no Fly, no AWS bill.
- **Not a vector database** — everything is plain markdown. You read it, search it, edit it, diff it.

---

## Cost

| Item | Cost |
|---|---|
| Telegram bot | Free |
| Bot hosting (your Mac via launchd) | Free |
| Claude API for bot responses | Capped at $5/day (~$30–$60/mo at active use) |
| Gmail / Calendar access via Claude Code | Free |
| GitHub access (`gh` CLI) | Free |
| **Typical monthly cost** | **$20–$50/mo realistic** |

---

## Setup

### 1. Clone

```bash
git clone https://github.com/YOUR-GITHUB-USERNAME/sheero-brain.git sheero
cd sheero
```

### 2. Fill in context

Copy the boilerplate templates in `cortex/` and fill them in:

```bash
cp cortex/me_boilerplate.md.template cortex/me.md
cp cortex/work_boilerplate.md.template cortex/work.md
cp cortex/priorities_boilerplate.md.template cortex/priorities.md
```

### 3. Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

[Full setup guide →](https://docs.anthropic.com/en/docs/claude-code)

### 4. Start your first session

```bash
cd ~/sheero
claude
```

Say "good morning" to trigger your first check-in.

### 5. (Optional) Set up the Telegram bot

See [`.claude/bots/telegram/README.md`](.claude/bots/telegram/README.md) for the full setup — BotFather token, owner ID, env file, launchd installation.

---

## Roadmap

See [`ROADMAP.md`](ROADMAP.md) for current status and planned features.

---

## Credits

- Folder structure pattern adapted from the [RIGGS Boilerplate](https://github.com/Bagu-Hanto/riggs_boilerplate) (MIT)
- Memory tree pattern inspiration from [OpenHuman](https://github.com/tinyhumansai/openhuman)
- Obsidian-wiki philosophy from [Andrej Karpathy](https://x.com/karpathy/status/2039805659525644595)

---

## License

MIT — fork it, modify it, make it yours.
