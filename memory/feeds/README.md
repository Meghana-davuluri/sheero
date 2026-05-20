# Feeds — Auto-fetched External Data

This folder holds snapshots of external data sources, pulled automatically by sync skills. Each subfolder is one data source; each file inside is one day's snapshot.

## Why feeds?

Skills like `morning_checkin` used to fetch Gmail/Calendar/GitHub *live* during a check-in. That made check-ins slow and dependent on API availability. The new pattern:

1. **Sync skills** pull data into `feeds/` on a schedule (or on demand)
2. **Consumer skills** (morning_checkin, evening_checkin, telegram bot replies) read from `feeds/`

Result: fast, offline-capable check-ins. Reliable. And the feed files themselves are a permanent record you can `grep` later.

## Folder layout

```
feeds/
├── github/YYYY-MM-DD.md            ← sync_github skill
├── gmail/<account>/YYYY-MM-DD.md   ← sync_gmail skill (planned)
└── calendar/<account>/YYYY-MM-DD.md ← sync_calendar skill (planned)
```

## Skills that write here

| Skill | Writes to | Status |
|---|---|---|
| `sync_github` | `github/YYYY-MM-DD.md` | ✅ Active |
| `sync_gmail` | `gmail/<account>/YYYY-MM-DD.md` | ⏳ Planned (Phase 6 — paused on Gmail OAuth) |
| `sync_calendar` | `calendar/<account>/YYYY-MM-DD.md` | ⏳ Planned |
| `meeting_capture` | `meetings/YYYY-MM-DD_with-X.md` | ⏳ Planned (Phase 8) |

## Retention

Old feed files are not auto-deleted. They are part of the brain — `weekly_rollup` and `monthly_rollup` (Phase 7) will compress them into hierarchical summaries, but the raw files stay forever in git history regardless.
