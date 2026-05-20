---
name: Acme Corp
slug: acme-corp
repo: https://github.com/JaneDoe/acme-corp
status: active
last_activity: 2026-05-01
last_refreshed: 2026-05-01
related_people: [Sarah (cofounder), Mike (beta customer #1)]
---

# Acme Corp

## Summary

Indie SaaS for small businesses — a CRM with a built-in AI assistant that drafts follow-ups, summarizes calls, and flags stale leads. In public beta with ~120 paying customers at $15/month tier.

## Current goal

Ship onboarding flow v2 by Friday 2026-05-04. The current flow has a 38% completion rate; targeting 60%+ with the redesign.

## Recent activity

- 2026-05-01: Stripe webhook for new pricing tier wired up (source: github_feed)
- 2026-04-30: Customer feedback session with Mike — wants AI scheduling (source: meeting)
- 2026-04-29: Onboarding mockups approved by Sarah (source: daily_log)
- 2026-04-28: Q1 retro — biggest win was launching the AI assistant; biggest miss was no marketing cadence (source: decision)

## Decisions made

- 2026-04-15: Bump pricing tier from $15 → $25 for new sign-ups (grandfather existing)
- 2026-04-22: Use Stripe Checkout instead of custom payment form
- 2026-04-28: Newsletter cadence — every other Wednesday

## Open threads

- Onboarding v2 — in progress, ships Friday
- Stripe webhook idempotency — Sarah flagged a potential edge case
- Customer support — backlog growing, hire VA?

## Backlog / next moves

- AI scheduling (cron-style) — Mike's feature request
- Better analytics dashboard for customers
- Mobile app — still parked
