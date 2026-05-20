# Public Repo Plan

This file is the playbook for creating a sanitized public version of Sheero — for the portfolio piece (ROADMAP Phase 9). Do this when the private Sheero has been running smoothly for at least two weeks.

---

## The goal

Land a public GitHub repo + blog post that:
- Shows engineering depth (auto-fetch, memory tree, Telegram bot, hierarchical summaries)
- Exposes the architecture so other engineers can fork it
- Contains **zero** personal info (no real journal, no real emails, no real names except yours)
- Demonstrates the value with realistic-looking sample data

---

## Repo structure

Create a new public repo named **`sheero`** (or `sheero-template`) under `YOUR-GITHUB-USERNAME`.

Mirror the private repo's structure with these changes:

| Private | Public |
|---|---|
| `cortex/me.md` (your real info) | `cortex/me.md.template` (boilerplate only) |
| `cortex/work.md` (your real projects) | `cortex/work.md.template` |
| `cortex/priorities.md` (your real priorities) | `cortex/priorities.md.template` |
| `cortex/scratchpad.md` (your real ideas) | Empty `cortex/scratchpad.md` placeholder |
| `cortex/projects/*.md` (real project files) | `cortex/projects/.gitkeep` + one fictional sample (`acme-corp.md`) |
| `cortex/people/*.md` (real people files) | `cortex/people/.gitkeep` + one fictional sample (`jane-doe.md`) |
| `memory/daily_log.md` (real journal) | `memory/daily_log.md` with 7 fake "Jane Doe" entries |
| `memory/weekly/*.md` | 2-3 fake weekly rollups (so visitors see real-looking output) |
| `memory/monthly/*.md` | 1 fake monthly rollup |
| `memory/feeds/github/*.md` | 1-2 fake feed files |
| `journal/decisions_log.md` (your real decisions) | Empty header + one fake "started Sheero" decision |
| `journal/session_log.md` | Same pattern |
| `pillars/*/` content | Empty boilerplate files in each |
| `.claude/skills/*/skill.md` | ✅ Same — these are the engineering artifact, no personal data |
| `.claude/agents/*.md` | ✅ Same |
| `.claude/bots/telegram/*` | ✅ Same (no secrets — those are in `~/.config/sheero/`) |
| `README.md`, `ROADMAP.md`, `docs/` | ✅ Same |

---

## Files that copy AS-IS (no scrubbing needed)

These contain no personal info:

```
README.md
ROADMAP.md
docs/architecture.md
docs/public_repo_plan.md  (this file — well, mostly)
.gitignore
LICENSE (create new MIT with your name)
.claude/CLAUDE.md
.claude/skills/morning_checkin/skill.md
.claude/skills/morning_checkin/skill_boilerplate.md
.claude/skills/evening_checkin/skill.md
.claude/skills/evening_checkin/skill_boilerplate.md
.claude/skills/save/skill.md
.claude/skills/save/skill_boilerplate.md
.claude/skills/email_triage/skill.md
.claude/skills/sync_github/skill.md
.claude/skills/sync_all/skill.md
.claude/skills/weekly_rollup/skill.md
.claude/skills/monthly_rollup/skill.md
.claude/skills/refresh_topics/skill.md
.claude/skills/meeting_capture/skill.md
.claude/agents/job_search.md     (review first — may need sanitizing)
.claude/bots/telegram/bot.py
.claude/bots/telegram/notify.py
.claude/bots/telegram/README.md
.claude/bots/telegram/com.example.*.plist  (update paths if needed)
.claude/bots/telegram/pyproject.toml
cortex/people/README.md
cortex/projects/README.md
memory/feeds/README.md
reference/sheero_v2_draft.md (review — may have personal notes)
templates/ (all .md.template files)
```

---

## Sample data to generate

Pick one fictional persona for the demo. Suggested: **Jane Doe**, full-stack developer building a side project called "Acme Corp."

### `cortex/me.md` (fictional)
```markdown
# Jane Doe — Personal Profile

Last updated: 2026-05-01

## Identity
**Name:** Jane Doe
**Location:** Austin, TX
**Age:** 32

Full-stack developer building Acme Corp on the side. Daily journaler.

## Values
- Ship something every week
- Health over hustle
- Honest with myself in the journal

## Current Situation
Building Acme Corp evenings + weekends while working a day job.
```

### `cortex/projects/acme-corp.md` (fictional)
A fictional project with realistic-looking activity (5 commits/week, decisions logged, an open thread about pricing).

### `memory/daily_log.md` (fictional)
7 daily entries for "Jane Doe" with realistic habit data, journal entries, and dominant themes.

### `memory/weekly/2026-W18.md` and `2026-W19.md`
Two fictional weekly rollups generated from the daily logs, showing what the memory tree produces.

### `memory/monthly/2026-04.md`
One fictional monthly rollup.

### `memory/feeds/github/2026-05-01.md` and `2026-05-02.md`
Two fictional GitHub feed snapshots showing acme-corp activity.

---

## Steps to actually create the public repo

When you're ready (Month 2 of the ROADMAP):

### Step 1: Create the repo
```bash
gh repo create YOUR-GITHUB-USERNAME/sheero --public --description "Personal AI executive assistant designed to work *with* Claude Code. Markdown-first memory tree, Telegram interface, local-only. Inspired by Karpathy's obsidian-wiki and OpenHuman's memory tree." --license MIT
```

### Step 2: Clone the private repo to a new local folder
```bash
cd ~/Desktop
git clone https://github.com/YOUR-GITHUB-USERNAME/sheero-brain.git sheero-public
cd sheero-public
git remote set-url origin https://github.com/YOUR-GITHUB-USERNAME/sheero.git
```

### Step 3: Run the sanitization script

Write a `scripts/sanitize.sh` that:
1. Removes / replaces every file in the scrub list above
2. Generates fake sample data files
3. Replaces `You` with `Jane Doe` in any docs (review hits before committing)
4. Wipes `cortex/inbox/`

### Step 4: Commit and push
```bash
git add -A
git commit -m "Initial public release of Sheero template"
git push -u origin main
```

### Step 5: Pin the repo on your profile
- GitHub → your profile → "Customize your pins" → check `sheero`

### Step 6: Add a screenshot + Loom video to README
- Record a 5-min demo of Sheero in action with the fake brain
- Add an architecture diagram (export from docs/architecture.md as PNG)

---

## Blog post (write second, after public repo lives)

See `reference/blog_draft_devto.md` for the first-pass draft.

Platform: **dev.to** (primary), cross-post teaser to LinkedIn.

When the blog goes live, link to:
- The public `sheero` repo
- The Loom video
- This personal repo (private — only as a "if you're curious about the live system")

---

## Anti-goals for the public version

- ❌ Real names of people your actually works with (alex-cofounder, anyone else)
- ❌ Real project names beyond your own public repos (askexample can be mentioned if it's public, but not internal details)
- ❌ Real financial info, journal entries, sleep data
- ❌ Email addresses, phone numbers, calendar events
- ❌ Anything that would be embarrassing in 5 years

---

## When to revisit this plan

- Before creating the public repo — make sure the scrub list still matches the private structure
- After 6 months of running Sheero — the public version may benefit from your real lessons learned
- Before any major refactor — the public version should reflect current best practice
