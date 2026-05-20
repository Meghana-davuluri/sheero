# Sheero — Design Document

> **Historical reference.** Captures the planning that led to the May 2026 README rewrite and the brain-anatomy folder refactor. The folder paths shown below (`00_context/`, `00_system/`, `01_*` through `09_*`) reflect pre-refactor structure — current structure is `cortex/`, `memory/`, `journal/`, `reference/`, `templates/`, `pillars/`.
> Date: 2026-05-19

---

## Decisions locked in

| Decision | Choice |
|---|---|
| Naming | Stay with **Sheero**. The Telegram side is the *interface*, not a new product. |
| Versioning | **No v1/v2 split.** Sheero evolves in place. Existing features stay; new features are added alongside. |
| Hosting | **Local on your Mac only.** No Railway, no Fly, no cloud. Bot runs via `launchd`. |
| Repo visibility | **`sheero-brain` stays private permanently.** Real personal data never goes public. |
| Public portfolio | A separate sanitized public repo + blog post, **as a Month 2 follow-up**, not now. |

---

## What Sheero is today

Sheero is a **persistent, file-based AI executive assistant built on Claude Code**. The current state:

- A git repo of markdown files that act as Sheero's brain
- `CLAUDE.md` is the system prompt that orients Claude Code every session
- `cortex/` holds identity, work, priorities, scratchpad — loaded on demand
- `journal/` holds decision log + session log
- `memory/` holds the daily log
- `01–09_pillars/` cover nine life domains (physical, emotional, social, etc.)
- `.claude/skills/` defines three skills: `morning_checkin`, `evening_checkin`, `save`
- `.claude/agents/` defines two sub-agents: `job_search`, `kdp_research`
- The README mentions Gmail MCP, Google Calendar MCP, and Telegram MCP as integrations — these are **referenced as intent**, not yet wired up in skills

**What works well today:**
- Markdown + git gives full ownership and version history
- Morning + evening rituals capture the day
- Scratchpad → review → process loop keeps the inbox clean
- Skills are reusable and editable markdown files

**What's missing today:**
- Sheero only knows what you tell it in real time. No proactive data pulling.
- No persistent memory of external events (emails received, meetings held, PRs opened)
- No way to ask "what happened last week / this month?"
- No interface beyond the Claude Code terminal — can't talk to Sheero from your phone naturally (Telegram is listed but not built)
- People and projects aren't tracked as first-class entities

---

## What we're borrowing from OpenHuman

After a full read of OpenHuman's docs, these are the ideas worth taking:

| OpenHuman idea | What it gives | Adopt? |
|---|---|---|
| **Auto-fetch loop** | Background sync from integrations every ~20 min, no manual prompting | ✅ Yes |
| **Memory Tree (hierarchical rollups)** | Day → week → month compression so "what happened this month?" works | ✅ Yes |
| **Topic trees per entity** | Per-person and per-project summary files, refreshed by frequency of mention | ✅ Yes |
| **Obsidian wiki layout** | The markdown is browseable and editable, not opaque | ✅ Already Sheero's design |
| **3–5 integrations instead of 118** | Stay focused on what you actually use | ✅ Yes (Gmail, Calendar, GitHub) |
| **Voice (TTS/STT)** | Voice-first conversation | 🟡 Later. v1 voice = macOS `say` for free. ElevenLabs only if needed. |
| **Meeting note-taker** | Capture and summarize meetings | 🟡 Yes, but as **local Whisper**, not as a bot participant in the call |
| **Lightweight token cleanup** | Strip HTML/quotes from feeds before they hit Claude | 🟡 Tiny version — clean step inside sync skills |
| **Desktop mascot with face** | Visible character on screen | ❌ Skip — no portfolio value, lots of work, doesn't fit Claude Code |
| **118 OAuth integrations** | Connect everything | ❌ Skip — 3 deep beats 50 shallow |
| **Their custom Tauri/Rust harness** | Their own desktop app | ❌ Skip — Claude Code already does this |
| **Their hosted cloud backend** | Their voice + LLM routing service | ❌ Skip — local-only by design |
| **Subconscious loop ("dreaming")** | Background processing when idle | 🟡 Optional much later — interesting but not essential |

---

## Sheero's thesis

> **Sheero is a personal AI executive assistant designed to work *with* Claude Code, not replace it.**
>
> Where most AI agent projects build their own harness — their own UI, their own LLM loop, their own tools — Sheero takes the opposite approach. Claude Code already does the hard parts. What's missing is a **persistent, structured, file-based memory of your life**, plus a way to **talk to Sheero from anywhere**.
>
> Two big additions on top of what Sheero already has:
>
> 1. **Auto-fetched memory.** Gmail, Calendar, and GitHub sync into markdown feeds automatically. Daily logs roll up into weekly and monthly summaries. People and projects become first-class entities with their own files.
> 2. **Telegram as the primary interface.** The README has mentioned Telegram from day one; now it actually works. Talk to Sheero from your phone like texting a friend. Markdown files become invisible plumbing.
>
> Inspired by Andrej Karpathy's obsidian-wiki workflow and OpenHuman's memory tree, redesigned as a **Claude Code-native, Telegram-first, local-only** system.

---

## Updated folder structure

```
sheero-brain/                            ← private, your real life
│
├── CLAUDE.md                            ← system prompt (existing, lightly updated)
├── README.md                            ← thesis + setup (rewritten)
│
├── cortex/                          ← identity (existing)
│   ├── me.md
│   ├── work.md
│   ├── priorities.md
│   ├── 2_Year_Goals.md
│   ├── scratchpad.md
│   │
│   ├── people/                          ← NEW: topic trees per person
│   │   ├── alex-cofounder.md               ← auto-updated from feeds
│   │   ├── anna.md
│   │   └── ...
│   │
│   └── projects/                        ← NEW: topic trees per project
│       ├── askexample.md
│       ├── photofinder.md
│       ├── carsearch.md
│       ├── acme-client.md
│       └── kdp.md
│
├── 00_system/
│   ├── tracking/
│   │   ├── daily_log.md                 ← existing
│   │   ├── weekly/                      ← NEW: weekly rollups
│   │   └── monthly/                     ← NEW: monthly rollups
│   │
│   └── feeds/                           ← NEW: auto-fetched data
│       ├── gmail/YYYY-MM-DD.md
│       ├── calendar/YYYY-MM-DD.md
│       ├── github/YYYY-MM-DD.md
│       └── meetings/YYYY-MM-DD_with-X.md
│
├── journal/                             ← existing
├── reference/                       ← existing (this draft lives here)
├── templates/                        ← existing
│
├── pillars/physical/ ... pillars/community/       ← existing pillar folders
│
├── bot/                                 ← NEW: Telegram bot service
│   ├── sheero_bot.py                    ← main bot script
│   ├── requirements.txt
│   ├── config.example.toml              ← committed, no secrets
│   ├── config.toml                      ← gitignored, has bot token + Claude key
│   ├── com.example.sheero.bot.plist     ← launchd config
│   └── README.md                        ← setup instructions
│
└── .claude/
    ├── CLAUDE.md                        ← existing
    ├── skills/
    │   ├── morning_checkin/             ← existing (will read from feeds/ instead of fetching live)
    │   ├── evening_checkin/             ← existing
    │   ├── save/                        ← existing
    │   ├── sync_gmail/                  ← NEW
    │   ├── sync_calendar/               ← NEW
    │   ├── sync_github/                 ← NEW
    │   ├── sync_all/                    ← NEW
    │   ├── weekly_rollup/               ← NEW
    │   ├── monthly_rollup/              ← NEW
    │   ├── refresh_topics/              ← NEW (updates people/projects topic trees)
    │   └── meeting_capture/             ← NEW (local Whisper)
    │
    └── agents/                          ← existing
```

---

## How the Telegram interface works (local-only)

```
┌──────────────────────────────────────┐
│  YOU on your phone or laptop         │
└──────────────┬───────────────────────┘
               │  Telegram message
               ▼
┌──────────────────────────────────────┐
│  Telegram servers (free, hosted)     │
└──────────────┬───────────────────────┘
               │  long-polling
               ▼
┌──────────────────────────────────────┐
│  @sheeroooBot — Python service       │
│  RUNNING ON YOUR MAC                 │
│  • started by launchd at login       │
│  • reads ~/sheero/*.md               │
│  • calls Claude API                  │
│  • writes new entries when asked     │
│  • runs `git commit && push`         │
└──────────────────────────────────────┘
```

### What "local-only" means in practice

- **Bot is up only when your Mac is awake.** Closed laptop = silent bot. Telegram queues messages briefly, so a short sleep is fine; a long trip is not.
- **$0 hosting cost.** No cloud bill ever.
- **Data stays local.** The only things that leave your Mac are (a) the text you send Telegram and (b) the prompts you send to Claude API. Markdown files never leave.
- **Simpler setup.** No deployment pipeline, no cloud env vars. Just a `.plist` file in `~/Library/LaunchAgents/`.

### Example interactions

- "Summarize today" → reads `daily_log.md` + today's feeds, sends back a clean summary
- "What did Anna email me this week?" → reads `feeds/gmail/*`, summarizes
- "Add to scratchpad: idea for PhotoFinder onboarding flow" → appends to `cortex/scratchpad.md`, commits, pushes
- "What's on my calendar tomorrow?" → reads `feeds/calendar/2026-05-20.md`
- "How's self-publishing doing this month?" → reads `cortex/projects/kdp.md` + recent logs
- Voice note from Telegram → Whisper → text → same flow

The bot is **read + write + commit**. Every change goes through git, so the safety net stays intact.

---

## Cost breakdown

| Item | Cost |
|---|---|
| Telegram bot | Free |
| Bot hosting (your Mac via launchd) | Free |
| Claude API for bot responses | ~$3–10/mo |
| Whisper API for voice notes (optional) | ~$1–3/mo realistic |
| Gmail / Calendar MCP | Free |
| GitHub access (`gh` CLI) | Free |
| TTS for replies (optional, much later) | Free with macOS `say` |
| **Total realistic monthly cost** | **$4–13/mo** |

---

## Build order

### Phase 1 — Foundation (this week)
1. Rewrite `README.md` with the thesis above
2. Add `ROADMAP.md` listing the milestones below
3. Commit the daily log change + new docs together

### Phase 2 — Auto-fetch (weekend 1)
4. Build `sync_gmail/skill.md` — pulls today's unread/recent via Gmail MCP, writes `feeds/gmail/YYYY-MM-DD.md`
5. Build `sync_calendar/skill.md` — pulls today + tomorrow via Calendar MCP
6. Build `sync_github/skill.md` — uses `gh` CLI to list open PRs/issues across your repos
7. Build `sync_all/skill.md` — orchestrator that runs all three
8. Update `morning_checkin` to **read from feeds** instead of fetching live

### Phase 3 — Memory Tree (weekend 2)
9. Build `weekly_rollup/skill.md` — reads the week's daily logs + feeds, writes `weekly/YYYY-Wnn.md`
10. Build `monthly_rollup/skill.md` — reads the month's weekly rollups, writes `monthly/YYYY-MM.md`
11. Build `refresh_topics/skill.md` — scans recent feeds, updates `people/*.md` and `projects/*.md`

### Phase 4 — Telegram (weekend 3)
12. Create `@sheeroooBot` via BotFather
13. Write `bot/sheero_bot.py` (~150 LOC) — receives messages, reads relevant `.md` files, calls Claude API, writes back, commits
14. Add `bot/com.example.sheero.bot.plist` for launchd auto-start
15. Add `bot/README.md` explaining the setup

### Phase 5 — Meeting capture (weekend 4)
16. Build `meeting_capture/skill.md` using local Whisper + BlackHole audio routing
17. Auto-write transcripts into `feeds/meetings/`
18. Summary post-meeting flows into `journal/meetings/`

### Phase 6 — Public portfolio piece (month 2, after the above works)
19. Create separate public repo `sheero` (template-only, no personal data)
20. Add sanitized samples (fake persona "Jane Doe", 3 weeks of generated rollups)
21. Architecture diagram + screenshots + short Loom video
22. Write blog post: "How I built a personal AI assistant on top of Claude Code"

---

## What goes in the rewritten README

1. **Headline** — "Sheero: a personal AI executive assistant, Claude Code-native, Telegram-first, local-only"
2. **Thesis paragraph** — the one above
3. **Architecture diagram** — three layers (Telegram interface, Sheero memory, Claude Code runtime)
4. **What's in the box** — auto-fetch, hierarchical rollups, topic trees, Telegram bot, meeting capture
5. **What this is NOT** — not another agent harness, not a mascot, not 118 integrations, not cloud-hosted
6. **Folder structure** — the updated tree above
7. **Setup guide** — clone, fill context, install Claude Code, set up Telegram bot, run launchd
8. **Credits** — Karpathy's obsidian-wiki, OpenHuman's memory tree, RIGGS boilerplate
9. **License** — MIT (kept from existing)

---

## Public portfolio strategy (deferred to Month 2)

When the private Sheero is working and proven, build the public side:

| Asset | Purpose |
|---|---|
| **Public template repo** (`sheero` or similar) | Sanitized clone — skills, agents, CLAUDE.md template, sample data with fake persona, README with thesis. Recruiters can clone and try it. |
| **Standalone bot repo** (`claude-telegram-bridge`) | Just the bot code as a reusable artifact. Anyone with a markdown brain can use it. Easy stars target. |
| **Blog post** | "How I built a personal AI assistant on Claude Code" — Medium / dev.to / LinkedIn. Drives traffic to the GitHub repos. |
| **Loom video** | 5-minute screen recording of Sheero in action with a fake test brain. Embed in README. |
| **Architecture diagrams** | PNG / mermaid in the public README. |

**Why this combo works:** the blog post is the discovery channel, the public repos are the proof, the video makes it real in 90 seconds. Zero personal exposure.

---

## Open questions

1. **Bot name on Telegram** — ✅ Decided: `@sheeroooBot`
2. **Single-user assumption** — only you talk to the bot, right? (Simpler auth: bot only responds to your Telegram user ID.)
3. **Voice replies** — text-only for v1, add voice (macOS `say` or ElevenLabs) later?
4. **Bot autostart** — launchd at login, or manual `python sheero_bot.py` from terminal for now?
5. **Eventual blog platform** — Medium, dev.to, LinkedIn, or your own site?

---

## What's NOT being touched without approval

- `CLAUDE.md`, `cortex/me.md`, daily log, decisions log, existing skill files (protected per CLAUDE.md)
- The existing `README.md` (waiting for this draft to be approved before rewriting)
- Any commits beyond the pending daily log change

---

## Next step

Review this draft. Once approved:
1. Rewrite `README.md` using the structure above
2. Add `ROADMAP.md` with the build order
3. Commit everything together with the pending daily log change
4. Start Phase 2: build `sync_gmail` as the first new skill
