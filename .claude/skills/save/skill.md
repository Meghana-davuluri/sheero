---
name: save
description: Commit and push all brain changes to git. Stages modified and untracked files, drafts a session commit message, commits, and pushes. Also checks scratchpad, surfaces open todos, and logs a session note.
---

# /save — Commit, Push & Quick Sync

## Goal
Stage, commit, and push all session changes to GitHub. Then do a quick sync:
check the scratchpad, surface open todos, and capture a session note.

## Steps

### 1 — Assess
Run `git status` and `git diff --stat` in parallel to see what changed.
Skip files that should never be committed:
- Any credentials, tokens, or `.env` files
- Image/video files (JPG, PNG, MOV) unless explicitly requested

### 2 — Stage
Add all modified and untracked files using specific file paths.
Never use `git add -A` or `git add .` — always name the files explicitly.

### 3 — Draft Commit Message
Write a concise commit message:
- First line: `Work session YYYY-MM-DD — [session note or 2-4 word summary]`
- Bullet list: one line per meaningful change (new files, major edits, decisions made)
- Keep bullets factual — what changed, not why

Format:
```
Work session YYYY-MM-DD — [theme]

- [change 1]
- [change 2]
- [change 3]

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

### 4 — Commit & Push
Commit using a HEREDOC, then push to origin master.

### 5 — Scratchpad Peek
Read `cortex/scratchpad.md`. If the inbox has items, flag them briefly:
> "Scratchpad has X item(s): [one-line summary of each]. Process at evening check-in."
If empty, say nothing.

### 6 — Open Todos
Read `cortex/priorities.md`. List any unchecked items for today:
> "Still open today: [item 1], [item 2]"
If everything is checked or there are no today items, say nothing.

### 7 — Confirm
Report: files committed, commit hash, push status. Keep it to 2-3 lines.
