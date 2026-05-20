---
name: sync_github
description: Pull GitHub activity (recent commits, open PRs, open issues assigned to me) across all of your repos and write to memory/feeds/github/YYYY-MM-DD.md. Trigger with "sync github" or "github sync".
---

# sync_github

## Goal

Take a snapshot of what's happening across your GitHub repositories today, save it as markdown in `memory/feeds/github/YYYY-MM-DD.md`, and surface anything that needs attention.

This skill is part of the auto-fetch system. Run it on demand or as part of `sync_all`. Morning check-in reads the latest feed file instead of fetching live.

---

## Step 1 — Check gh CLI is ready

Run `gh auth status` to confirm authentication.

If not authenticated, stop and tell the owner: *"GitHub CLI not authenticated. Run `gh auth login` then retry."*

---

## Step 2 — Gather data (in parallel where possible)

Run these commands and capture output:

### A. Recent commits across all repos (last 7 days)

```bash
gh api graphql -f query='
{
  viewer {
    contributionsCollection(from: "<SEVEN_DAYS_AGO_ISO>") {
      commitContributionsByRepository(maxRepositories: 30) {
        repository { nameWithOwner url }
        contributions(first: 1) { totalCount }
      }
    }
  }
}' --jq '.data.viewer.contributionsCollection.commitContributionsByRepository[] | "\(.repository.nameWithOwner)|\(.contributions.totalCount)|\(.repository.url)"'
```

Where `<SEVEN_DAYS_AGO_ISO>` = today minus 7 days in ISO 8601 (e.g., `2026-05-12T00:00:00Z`).

### B. Open PRs authored by You

```bash
gh search prs --author=@me --state=open --limit 30 \
  --json title,repository,url,createdAt,isDraft,updatedAt
```

### C. Open issues assigned to You

```bash
gh search issues --assignee=@me --state=open --limit 30 \
  --json title,repository,url,createdAt,updatedAt
```

### D. (Optional) Open PRs that need your review

```bash
gh search prs --review-requested=@me --state=open --limit 20 \
  --json title,repository,url,createdAt
```

---

## Step 3 — Detect uncommitted work in the local sheero-brain repo

Since Sheero edits this repo itself, check for uncommitted changes:

```bash
cd ~/sheero && git status --short
```

If there are uncommitted files, flag them in the feed — they represent in-flight work that won't show up in commit counts yet.

---

## Step 4 — Format the feed file

Write to `memory/feeds/github/YYYY-MM-DD.md` using today's date in UTC. Use this template:

```markdown
---
date: <YYYY-MM-DD>
source: github
fetched_at: <ISO-8601 UTC timestamp>
active_repos: <count from Section A>
open_prs_authored: <count from Section B>
open_issues_assigned: <count from Section C>
---

# GitHub — <Day, Month DD, YYYY>

## Active repos (last 7 days)

Repos with at least one commit in the past week, sorted by commit count.

| Repo | Commits | Link |
|---|---|---|
| <repo> | <n> | <url> |
| ... | ... | ... |

If no active repos this week, write: *"No commits in the past 7 days."*

## In-flight work

### Open PRs (authored by me)

For each: title, repo, draft status, created date, URL.
- If a PR is **draft** and older than 14 days, flag it as **stale draft**
- If a PR is **non-draft** and older than 14 days, flag it as **needs follow-up**

If none, write: *"No open PRs."*

### Issues assigned to me

For each: title, repo, created date, URL.

If none, write: *"No open issues assigned."*

### PRs awaiting my review

For each: title, repo, created date, URL.

If none, omit this section.

## Uncommitted work in sheero-brain

If `git status` shows changes, list them here with one line per file. Note: this is *only* the sheero-brain repo, not other repos. If clean, write: *"Clean working tree."*

## Flags

Bullet list of anything urgent:
- Stale drafts (older than 14 days)
- PRs that need follow-up (older than 14 days, non-draft)
- Issues older than 30 days
- More than 5 uncommitted files in sheero-brain (suggests work that should be committed)

If nothing flagged, write: *"Nothing urgent."*
```

---

## Step 5 — Tell the owner

Report briefly to the owner:

> "GitHub sync complete. Wrote `memory/feeds/github/<date>.md`. [Active: N repos. Open PRs: N. Issues: N.] [Flag line if any urgent items, else 'Nothing urgent.']"

Keep it to 2-3 lines max.

---

## Step 6 — Do NOT commit automatically

The feed file is just data. Don't commit it as a separate change — feeds get committed when `morning_checkin` or `save` runs next.

This keeps the git log readable (one commit per session, not one per sync).

---

## Notes for edge cases

- **gh rate limit hit**: report the rate limit reset time, write a partial feed with what was gathered, flag the gap
- **No GitHub activity at all**: still write the feed file with empty sections — consistency matters for `morning_checkin` to read reliably
- **Forks / contributions to others' repos**: the `viewer` GraphQL query already includes these, no special handling needed
- **Private vs public**: include both, the markdown is local-only
- **Timezone**: the fetched_at timestamp is UTC, but the human-readable header date should also be UTC for consistency with other feeds

---

## Tone

Direct, no fluff. Just data and flags. No "Great job committing today!" — this is a status report, not a cheerleader.
