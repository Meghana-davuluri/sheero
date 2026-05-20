---
name: cortex
description: Live context about the owner. The most frequently read folder in the system.
type: reference
---

# cortex — Owner Context

This is the most important folder in RIGGS. It holds everything the assistant needs to understand who it's working for, what they're doing, and what matters right now.

RIGGS reads these files on demand — not all at once. CLAUDE.md tells it when to load each one.

---

## Files in This Folder

| File              | Purpose                                        | When RIGGS Reads It                             |
|-------------------|------------------------------------------------|-------------------------------------------------|
| `me.md`           | Owner's background, identity, values, skills   | First time owner context is needed in a session |
| `work.md`         | Active projects, businesses, income streams    | When asked about work or advising on priorities |
| `priorities.md`   | Current focus, this week's tasks, urgent items | Every check-in and task-related question        |
| `scratchpad.md`   | Capture inbox — raw ideas and notes            | Every morning and evening check-in              |
| `2_Year_Goals.md` | Short and long-term goals by life pillar       | When advising on decisions or framing work      |

---

## How to Use This Folder

- Fill in `me.md`, `work.md`, and `priorities.md` first — these are the minimum required for RIGGS to be useful
- Use `scratchpad.md` as a dump zone throughout the day — don't organize it, just capture
- Keep `priorities.md` updated weekly — stale priorities lead to stale suggestions
- `2_Year_Goals.md` is optional at first but becomes valuable once the system is running
