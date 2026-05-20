---
name: agents
description: Sub-agent definitions for specialized research and autonomous tasks.
type: reference
---

# agents — Sub-Agent Definitions

This folder holds agent definition files. Each agent is a specialized sub-process that Sheero can launch for focused, multi-step tasks — keeping the main conversation clean and the context window lean.

---

## Available Agents

| Agent | Trigger | What It Does |
|-------|---------|-------------|
| `job_search` | "find jobs", "job search", "check job boards" | Scans job boards, matches skills, drafts resumes/cover letters, tracks applications |

Add your own agents here — examples to consider: `market_research`, `recipe_curator`, `financial_review`, `content_planner`. Each agent is just a markdown file in this folder with YAML frontmatter.

---

## How Agents Work

Agents are launched via the Agent tool inside Claude Code. Each agent definition is a markdown file with YAML frontmatter that tells Claude what the agent does, what tools it has access to, and how to behave.

---

## When to Use an Agent vs. Inline

| Use an agent when...                               | Handle inline when...             |
|----------------------------------------------------|-----------------------------------|
| The task requires many web searches                | It's a quick lookup               |
| You want results without cluttering the main chat  | It's a single-step task           |
| The task could run in the background               | You need the result immediately   |
| It's a recurring research task                     | It's a one-off question           |
