# Blog Draft — "Why my personal AI lives in 200 Markdown files instead of a vector database"

> **Status:** First-pass draft. Edit before publishing on dev.to.
> **Target platform:** dev.to (primary), cross-post teaser to LinkedIn
> **Estimated length when polished:** 1,500-2,000 words
> **Pitch:** I built a personal AI assistant on Claude Code. It's markdown-first, Telegram-accessible, local-only. Here's the architecture and the design choices.

---

## Suggested titles (pick one)

1. **Why my personal AI lives in 200 Markdown files instead of a vector database**
2. **I stopped trying to replace Claude Code and built a memory layer instead**
3. **Building a personal AI executive assistant on top of Claude Code**
4. **The case for markdown-first AI memory: how I built Sheero**

I'd lean toward **#1** — it's the most provocative and most clearly differentiated. The phrase "200 Markdown files" is a strong concrete hook.

---

## Draft

### Opening hook (the problem)

Most personal AI assistants want to be your harness. They want their own desktop app, their own LLM loop, their own everything. OpenHuman has a mascot. Hermes has a self-learning loop. OpenClaw wants you in a terminal-first workflow.

I tried building one of these and stopped. The problem isn't the LLM — Claude Code already does the LLM loop better than I could. The problem is **persistent memory**. Claude Code is brilliant in a single session and amnesiac across sessions. It doesn't know who I am next Tuesday unless I tell it.

So I built **Sheero** — a personal AI assistant that doesn't replace Claude Code. It's the *memory layer* Claude Code is missing, exposed over Telegram so I can talk to it from anywhere.

This post walks through the architecture and the design choices that made it work.

---

### What Sheero is, in one paragraph

Sheero is a git repo of markdown files (my "brain"), plus a small Python Telegram bot that runs as a launchd daemon on my Mac, plus a set of Claude Code skills (markdown files with steps) that read and write the brain. Everything's local. Nothing is in the cloud except the LLM calls themselves. The whole thing costs ~$10/month to run.

---

### The architecture diagram

> [Insert diagram from docs/architecture.md — the four-layer diagram]

Four layers:

1. **Interface** — Telegram bot (`@YourBot`)
2. **Bot daemon** — Python (~262 LOC) on my Mac via launchd
3. **Runtime** — Claude Code
4. **Brain** — markdown + git

---

### Design choice 1: Markdown instead of a vector database

The default architecture for AI memory in 2026 is some flavor of vector store. Embed everything, search by similarity, retrieve top-K for context.

I considered this. I built a small prototype. Then I deleted it. Here's why.

**Markdown gives me five things a vector store doesn't:**

1. I can `cat` any memory file and read it myself
2. `git diff` shows me what changed yesterday
3. I can edit memory by hand — open the file, change a sentence, save
4. Obsidian, VS Code, any text editor opens it
5. Claude (the LLM) reads markdown natively — no embedding step needed for retrieval

The vector-store version had **none** of those. It was a black box. If the embeddings drifted or the DB got corrupted, I'd lose memory I couldn't even read.

The trade-off is real: vector stores are faster for semantic search at scale. But my brain isn't at scale. It's hundreds of files, not millions. `grep` is fast enough. `Claude reading the right file` is precise enough.

> **Quote-worthy:** "You can't trust a memory you can't read."

---

### Design choice 2: Claude Code as the runtime, not a custom harness

OpenHuman's whole codebase is essentially a Rust + Tauri harness reimplementing what Claude Code already does — LLM calls, tool use, context window management, prompt caching. Months of work to build something equivalent.

I just... used Claude Code.

Sheero's "code" is mostly markdown skill files:

```yaml
---
name: sync_github
description: Pull GitHub activity into memory/feeds/github/YYYY-MM-DD.md
---

# sync_github

## Step 1 — Check gh CLI is ready
Run `gh auth status`.

## Step 2 — Gather data
Run `gh api graphql ...`
Run `gh search prs --author=@me ...`

## Step 3 — Format the feed file
Write to memory/feeds/github/YYYY-MM-DD.md using this template:
[...]
```

Claude Code reads the skill file and executes the steps. No compilation. No deployment. Edit a skill in my editor and it runs the new version on next invocation.

The whole engineering project — eight months of OpenHuman's Rust harness — collapses into about 10 markdown files for me. Because the hard parts are already solved.

---

### Design choice 3: Telegram, not a desktop app

OpenHuman has a desktop mascot. A cute animated character that lives on your screen, lip-syncs to its voice, has mood states. It's beautifully done. I don't want it.

What I want is to talk to my assistant **from my phone**. From a cafe. From a walk. From a meeting where I can't open my laptop. The desktop mascot can't help me there.

Telegram is the answer. It's available on every device. Free. Voice notes work natively. The bot UX is mature. The bot API is excellent.

So my "interface" is a 262-line Python script:

```python
async def on_text(update, ctx):
    if not is_owner(update): return
    if not rate_limit_ok(...): return
    if get_today_spend() >= DAILY_CAP: return

    reply, session, cost = await call_claude(msg, session)
    add_spend(cost)
    await send_long(update.message, reply)
```

`call_claude` invokes `claude -p` (Claude Code's headless mode) with the brain directory as the working directory. Claude reads the relevant markdown files, decides what to say, returns text. The bot sends the reply.

Owner-ID whitelist. Rate limit. $5/day cost cap. Session continuity via Claude Code's `--resume` flag. That's it.

It runs on my Mac via launchd. No cloud. Total monthly hosting: $0.

---

### Design choice 4: Hierarchical memory tree

Daily journal entries answer "what happened today." But I also want to answer:

- "What happened this week?"
- "What happened this month?"
- "What's the latest with PhotoFinder?"
- "When did Anna and I last talk?"

If I had to grep through 365 daily files to answer these, the system would be useless.

So I built a **three-level memory tree**, inspired by OpenHuman's same-named concept:

```
Day → Week → Month
            ↑
       (and per-entity topic trees: projects, people)
```

A `weekly_rollup` skill reads the week's daily logs + GitHub feeds + decisions + git history, and writes a single `memory/weekly/2026-W21.md` summarizing the week.

A `monthly_rollup` skill reads the month's weeklies + any gaps from daily logs, and writes `memory/monthly/2026-05.md`.

A `refresh_topics` skill walks the same data sources and updates per-project / per-person files in `cortex/projects/` and `cortex/people/`.

Now when I ask Sheero "what's the latest with PhotoFinder?", Sheero reads one file: `cortex/projects/photofinder.md`. Not 14 daily logs. One file.

---

### What Sheero is NOT

The negative space is as important as the architecture:

- **Not a desktop mascot.** No animated character, no on-screen face.
- **Not 118 integrations.** Three deep (Gmail, Calendar, GitHub) beats 50 shallow.
- **Not cloud-hosted.** The bot runs on my laptop. Closed lid = silent bot. Acceptable trade-off.
- **Not a custom LLM harness.** Claude Code is the runtime, by design.
- **Not a vector database.** Markdown is the substrate.

Each "not" is a deliberate boundary.

---

### The numbers

- **~1,200 lines of code** total (bot.py + supporting scripts + opportunity_tracker)
- **~20 markdown skill files** that drive every workflow
- **~$10/month** in Claude API calls
- **0** servers
- **0** cloud services
- **1** laptop

For comparison, OpenHuman's Rust core is ~50,000+ lines of code. Different goals, different constraints — but worth noting how much you can do with how little, when you build *on top of* great tools instead of recreating them.

---

### What's next

Phase 6 is partial — Gmail and Calendar sync are paused on Google Workspace OAuth approval. Phase 8 (meeting capture via local Whisper) is shipped as a skill but I haven't used it on a real meeting yet. Phase 9 (this public version) is in progress.

The full codebase is at [github.com/YOUR-GITHUB-USERNAME/sheero](https://github.com/YOUR-GITHUB-USERNAME/sheero) — the *template* you can fork and personalize for yourself.

The private version, which is **my** brain, stays private. You shouldn't have to expose your journal to demo your engineering.

---

### One thing I'd tell my past self

Stop trying to build the harness. Build on top of the one that already exists.

---

## After-draft checklist (do before publishing)

- [ ] Rewrite opening to be specifically about *your* journey — show your voice
- [ ] Add a screenshot of the architecture diagram (export from docs/architecture.md)
- [ ] Add a 30-second GIF of Sheero responding to a Telegram message (Loom → Giphy)
- [ ] Verify all code snippets render correctly in dev.to's markdown
- [ ] Add tags on dev.to: `ai`, `claudecode`, `productivity`, `personalknowledge`, `opensource`
- [ ] Link out to OpenHuman, Karpathy's tweet, Claude Code docs
- [ ] Add a "if you want to fork this" section at the end with one-line install
- [ ] Cross-post a 100-word teaser to LinkedIn with the dev.to link
- [ ] Pin the public repo on your GitHub profile before publishing

## Where to publish

- **Primary:** [dev.to](https://dev.to) — free, devs read it, GitHub-friendly
- **Cross-post:** LinkedIn (teaser only, link to dev.to)
- **Optional secondary:** Medium, Hashnode (only if you want extra reach)
