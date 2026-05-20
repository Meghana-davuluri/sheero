# Sheero Roadmap

Tracking the evolution of Sheero from a context-aware assistant to a fully auto-fetched, Telegram-accessible personal AI.

---

## Status legend

- ✅ Done
- 🚧 In progress
- ⏳ Planned
- 💭 Idea — not committed

---

## Phase 1 — Foundation ✅

The core file-based brain, three rituals, manual context.

- ✅ Repo structure (`cortex`, `memory`, `journal`, `reference`, `templates`, `pillars`)
- ✅ `CLAUDE.md` as system prompt
- ✅ `morning_checkin` skill
- ✅ `evening_checkin` skill (with weekly review on Sundays)
- ✅ `save` skill
- ✅ Sub-agents: `job_search` (one example; add more as needed)
- ✅ Templates: daily log, decision, weekly review

---

## Phase 2 — Content layer ✅

Real content for the brain to write into and read from.

- ✅ Decisions log + session log
- ✅ Daily log with structured habit + journal format
- ✅ Daily prompts (theme-matched reflections for morning check-in)
- ✅ Habits / journal / sleep / workouts files in pillars
- ✅ Operational references
- ✅ Financial tracking scaffold
- ✅ Workspace + values + learning + relationships pillar files

---

## Phase 3 — Telegram bot ✅

`@YourBot` is live, running as a launchd daemon on the Mac.

- ✅ `bot.py` — Python daemon (python-telegram-bot v22) routing messages to `claude -p`
- ✅ Owner-ID whitelist (single-user lockdown)
- ✅ Rate limit (10 msgs/min)
- ✅ Daily cost cap ($5/day, configurable)
- ✅ Session continuity via Claude Code `--resume`
- ✅ Photo/document uploads → `cortex/inbox/`
- ✅ `/status` and `/reset` commands
- ✅ `launchd` autostart (`com.example.telegram.plist`)
- ✅ `notify.py` — scheduled morning/midday push notifications
- ✅ Opportunity scan launchd job
- ✅ Auto-capture behavior in CLAUDE.md (note:/save:/idea: prefixes auto-route to scratchpad)
- ✅ Bot README with setup, start/stop, troubleshooting

---

## Phase 4 — Job search tooling ✅

Active outbound job/gig pipeline.

- ✅ `pillars/occupational/applications.md` — application tracker
- ✅ `pillars/occupational/ai_gig_leads.md` — gig opportunities
- ✅ `pillars/occupational/daily_opportunities.md` — daily scan output
- ✅ `pillars/occupational/opportunity_tracker.py` — scanning script
- ✅ Resume drafts (Anthropic FDE, Mindera fullstack)
- ✅ `email_triage` skill

---

## Phase 5 — Folder refactor (brain anatomy) ✅

Renamed folders from numbered `00_*` / `01_*` convention to a metaphor-based structure so Sheero's structure is original and distinctive.

- ✅ `00_context/` → `cortex/`
- ✅ `00_system/tracking/` → `memory/`
- ✅ `00_logs/` → `journal/`
- ✅ `00_references/` → `reference/`
- ✅ `00_templates/` → `templates/`
- ✅ `01_physical/` ... `09_community/` → `pillars/physical/` ... `pillars/community/`
- ✅ Updated `CLAUDE.md` folder map
- ✅ Updated path references in every skill
- ✅ Updated `BRAIN_DIR` / `INBOX_DIR` paths in `bot.py` and `notify.py`
- ✅ Updated README + ROADMAP

**Definition of done:** Folders match the new structure, every script/skill works against the new paths, Telegram bot continues to run without interruption.

---

## Phase 6 — Auto-fetch ⏳ (Gmail OAuth paused 2026-05-19)

Pull external data into markdown feeds automatically, so Sheero stops relying on real-time fetches during check-ins.

### Status as of 2026-05-19

- ✅ Google Cloud project: reusing `photofinder` (project number `YOUR_GCP_PROJECT_NUMBER`)
- ✅ Gmail API enabled
- ✅ OAuth Consent Screen configured (External, Testing mode, personal Gmail added as test user)
- ✅ OAuth Client created — `sheero Gmail MCP` (Desktop type, Client ID prefix `YOUR_GCP_PROJECT_NUMBER-aso8...`)
- ✅ Credentials directory created at `~/.config/sheero/`
- 🚧 **Paused on:** downloading `credentials.json` — Google's new Auth Platform UI is hiding both the Download JSON button and the Client Secret value
- ⏳ **Next move when resuming:** either (a) try the Credentials list page in a different browser, (b) use "Reset secret" flow to surface a one-time copyable secret, or (c) fall back to `gcloud` API
- ⏳ Once credentials.json is saved, run the Terminal `read -s` command saved in chat to seed the file with proper permissions
- ⏳ Then proceed to Gmail MCP install + OAuth handshake

### Multi-account email + calendar setup

Sheero supports **multiple Gmail and Calendar accounts** via separate MCP server instances. Each account gets its own OAuth flow and its own feed folder, so work and personal contexts stay cleanly separated.

**Initial accounts to wire up:**
| Account | Role | MCP name |
|---|---|---|
| `you@yourwork.com` | yourwork LLC work | `gmail-yourwork`, `calendar-yourwork` |
| Personal Gmail | Family, friends, accounts, general | `gmail-personal`, `calendar-personal` |

Additional accounts (extra inboxes, side projects, etc.) can be added later as new MCP instances with no code changes.

### Skills to build

- ⏳ Set up Google Cloud OAuth credentials for each Gmail/Calendar account
- ⏳ Install Gmail MCP (`@gongrzhe/server-gmail-autoauth-mcp` or equivalent) once per account
- ⏳ Install Calendar MCP once per account
- ⏳ `sync_gmail` skill — accepts an account param (`yourwork` | `personal` | `all`, default `all`). Writes to `memory/feeds/gmail/<account>/YYYY-MM-DD.md`
- ⏳ `sync_calendar` skill — accepts an account param. Pulls today + tomorrow. Writes to `memory/feeds/calendar/<account>/YYYY-MM-DD.md`
- ✅ `sync_github` skill — uses `gh` CLI for active repos, open PRs, assigned issues. Writes to `memory/feeds/github/YYYY-MM-DD.md`. **Shipped 2026-05-19.**
- ✅ `sync_all` orchestrator — runs every available sync skill in sequence, skips silently if a skill isn't built yet. **Shipped 2026-05-19.**
- ✅ Update `morning_checkin` to read from feeds (feed-first pattern: read today's `memory/feeds/<source>/YYYY-MM-DD.md`, fall back to running the sync skill, skip silently if not configured). GitHub section added to the rundown. **Shipped 2026-05-19.**
- ⏳ Lightweight HTML / quoted-reply cleanup inside sync skills

### Folder layout for feeds

```
memory/feeds/
├── gmail/
│   ├── yourwork/
│   │   └── 2026-05-19.md
│   └── personal/
│       └── 2026-05-19.md
├── calendar/
│   ├── yourwork/
│   │   └── 2026-05-19.md
│   └── personal/
│       └── 2026-05-19.md
└── github/
    └── 2026-05-19.md
```

**Definition of done:** Running `sync all` produces a complete snapshot of both Gmail inboxes, both Calendars, and GitHub state. Morning check-in reads from cached feeds, separates work vs. personal context, and runs in under 10 seconds.

---

## Phase 7 — Memory tree (hierarchical rollups) ⏳

Day → week → month compression so "what happened this month?" works.

- ✅ `weekly_rollup` skill — reads daily logs + feeds + decisions + session log + git history, writes `memory/weekly/YYYY-Wnn.md`. Handles partial weeks gracefully. **Shipped 2026-05-19.**
- ✅ `monthly_rollup` skill — reads the month's weekly rollups, falls back to daily logs + feeds for weeks without rollups, writes `memory/monthly/YYYY-MM.md`. Handles partial months. **Shipped 2026-05-19** (first rollup at `memory/monthly/2026-05.md`, partial).
- ✅ `refresh_topics` skill — scans 14-day window of feeds + daily logs + decisions + git history, hotness-scored, updates `cortex/people/*.md` and `cortex/projects/*.md`. Preserves hand-written sections, rewrites Recent activity, appends to History, bumps frontmatter. Flags stale projects (30+ days no activity) for review. **Shipped 2026-05-19.**
- ✅ Seed `cortex/projects/` with one file per active project. **Shipped 2026-05-19.**
- ✅ Seed `cortex/people/` with starter file for alex-cofounder. **Shipped 2026-05-19.**
- ✅ Topic-tree READMEs in both folders documenting the file format and how `refresh_topics` will populate them. **Shipped 2026-05-19.**

**Definition of done:** Browse `memory/weekly/*.md` and see real, useful summaries. Ask "what's the latest with PhotoFinder?" via Telegram and get an answer grounded in `cortex/projects/photofinder.md`.

---

## Phase 8 — Meeting capture 🟡 (skill shipped, awaiting one-time BlackHole setup)

Local Whisper-based meeting note-taker. Captures system audio via BlackHole, transcribes with `whisper.cpp`, summarizes, updates topic trees.

- ✅ `meeting_capture` skill — start/stop recording, ffmpeg → whisper.cpp → markdown transcript → Claude summary → topic-tree updates. **Shipped 2026-05-19.**
- ✅ Transcripts → `memory/feeds/meetings/<session>_<topic>.md`
- ✅ Post-meeting summary → `journal/meetings/<session>_<topic>.md`
- ✅ Mentioned people auto-flagged for `refresh_topics`
- ⏳ **One-time setup (you do this when first using):** `brew install blackhole-2ch whisper-cpp ffmpeg`, create macOS Multi-Output Device named "Meeting Capture", download `ggml-base.en.bin` whisper model to `~/.config/sheero/whisper-models/`. See `.claude/skills/meeting_capture/skill.md` for full instructions.

**Definition of done:** Start a Google Meet, switch macOS audio to "Meeting Capture", say "start meeting [with X about Y]" to Sheero, do the meeting, say "stop meeting", find a clean summary in `journal/meetings/` and topic-tree updates for everyone mentioned.

---

## Phase 9 — Public portfolio 🟡 (materials drafted, public repo pending)

Once the private Sheero has been running smoothly for ~2 weeks, create the sanitized public version + blog post.

- ✅ **Architecture diagram + system walkthrough** at `docs/architecture.md` — ready to export as PNG for blog/repo
- ✅ **Public repo plan** at `docs/public_repo_plan.md` — exact playbook (file scrub list, sample-data persona, sanitization script outline, `gh repo create` command, pin instructions)
- ✅ **Blog post first-pass draft** at `reference/blog_draft_devto.md` — ~1,500 words, 4 working titles, after-draft checklist, ready to edit + publish on dev.to
- ⏳ **Create the public repo** (`gh repo create YOUR-GITHUB-USERNAME/sheero --public ...`) — do this in Month 2 once private Sheero has run for 2 weeks
- ⏳ **Generate fake "Jane Doe" sample data** in the public repo (daily logs, weekly + monthly rollups, project file)
- ⏳ **5-minute Loom video** demoing Sheero in action with the test brain
- ⏳ **Publish blog post on dev.to** + cross-post teaser to LinkedIn
- ⏳ **Pin public repo + standalone bot repo** on GitHub profile

**Definition of done:** Pin public `sheero` repo on GitHub profile. Blog post live on dev.to. Anyone visiting `github.com/YOUR-GITHUB-USERNAME` can grasp the project in under 60 seconds.

---

## Future ideas (not committed)

- 💭 Voice replies via macOS `say` or ElevenLabs (only if a real use case emerges)
- 💭 "Subconscious loop" — background processing when idle (compress feeds, refresh topics on a timer)
- 💭 Search across the wiki (BM25 over markdown files, or small embedding store)
- 💭 Multi-device sync (currently bot only works when Mac is awake — could add a tiny always-on Raspberry Pi or similar)
- 💭 Linear or Notion sync (only if either becomes part of daily workflow)
- 💭 Sub-agents for new domains (financial review, content planning)

---

## Out of scope (explicitly NOT planned)

- ❌ Desktop mascot / animated character — no portfolio value, doesn't fit Claude Code
- ❌ 118 integrations — focused depth beats broad coverage
- ❌ Cloud hosting for the bot — local-only is a feature, not a limitation
- ❌ Vector database / embedding store as the primary memory — markdown is the substrate
- ❌ Building our own LLM harness — Claude Code is the runtime, by design

---

## Maintenance principles

- Every new feature is a markdown skill or a small focused module — no big abstractions
- Every change Sheero makes is committed to git — full history is the audit trail
- Three integrations max in active use — if a fourth is added, justify which one gets dropped
- No feature ships without a one-paragraph entry in this roadmap and a definition of done
