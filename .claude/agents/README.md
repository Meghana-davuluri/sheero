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
| `kdp_research` | "research self-publishing", "check my books", "find self-publishing niches" | Analyzes competitors, discovers niches, tracks BSR, suggests next books |
| `job_search` | "find jobs", "job search", "check job boards" | Scans job boards, matches skills, drafts resumes/cover letters, tracks applications |

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
