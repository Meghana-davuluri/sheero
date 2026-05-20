---
name: email_triage
description: Triage your Gmail inbox. Surfaces the urgent few, flags bills/finance, counts the noise, and points her at what needs her attention. Trigger with "triage email", "email triage", "check inbox", or "inbox triage".
---

# Email Triage

## Goal

Turn a pile of unread emails into a short, actionable report in under 2 minutes.

Read-only — Sheero can see email but can't archive, reply, or mark read. The output tells your what deserves her attention; she acts in Gmail herself.

---

## Step 1 — Scope the pull

Default scope: **unread emails from the last 14 days** (query: `is:unread newer_than:14d`).

If your specifies a different scope ("triage last 3 days", "triage everything unread"), honor it.

Cap the pull at 50 messages per run. If the full unread set exceeds 50, note it: "N more unread beyond this batch — run again after clearing these."

---

## Step 2 — Fetch

Use `mcp__workspace-mcp__search_gmail_messages` with:
- `user_google_email`: `sheero.hari@gmail.com`
- `query`: `is:unread newer_than:14d` (or the scoped query)
- `page_size`: 50

Get sender, subject, snippet, and received date for each message.

---

## Step 3 — Classify

For each message, assign exactly one bucket based on sender + subject + snippet:

**🔴 URGENT** — needs a look today
- A real person (not automated) asking for something, waiting on her, or naming a short deadline
- A bill due within 7 days, or an overdue notice
- Meeting confirmation for a meeting happening in the next 48 hours
- Security alert (login from new device, password reset she didn't request, fraud notice)
- Anything from Sunil, Chaitanya, Ashwin, or known clients/recruiters

**🟡 IMPORTANT** — worth reading this week, not today
- Responses to threads she's in
- Job/recruiter emails that aren't time-sensitive
- E-commerce / marketplace platform notifications
- Personal communication from friends/family that doesn't need immediate reply
- Government / tax / immigration / visa-related mail (unless deadline → URGENT)

**💰 FINANCE** — bills, receipts, statements
- Utility bills, subscription charges, credit card statements
- Payment confirmations, refunds, payouts
- Bank/PayPal/Stripe/Venmo notices

**📧 NOISE** — safe to archive in bulk
- Newsletters (Substack, Medium, marketing lists)
- Social media notifications (LinkedIn digest, Twitter/X notifications)
- Generic promotional mail (shopping, travel deals)
- "Your order has shipped" type auto-mail for old orders
- GitHub/Vercel/other dev-tool notifications that aren't actionable

When in doubt between URGENT and IMPORTANT → IMPORTANT.
When in doubt between NOISE and IMPORTANT → IMPORTANT (better to surface than hide).

---

## Step 4 — Report

Output this format, nothing more:

```
Email triage — [N] unread in last 14 days

🔴 URGENT ([count])
- [Sender] — [Subject]
  → [1-line why it's urgent or what they want]
  [Gmail link]
- ...

🟡 IMPORTANT ([count])
- [Sender] — [Subject] ([1-line hook])
- ...

💰 FINANCE ([count])
- [Sender] — [Subject] ([amount/due if visible])
- ...

📧 NOISE — [count] (safe to archive in Gmail: click oldest, shift-click newest, archive)

[if any remain past the 50 cap:]
[K] more unread beyond this batch.
```

Gmail direct link format: `https://mail.google.com/mail/u/0/#inbox/[messageId]`

---

## Step 5 — Action prompt

End the report with one line:

> "Want me to draft a reply to any of these, add something to scratchpad, or just leave you to work it?"

Wait for her response before doing anything else.

---

## Tone

Direct. No preamble. No "let me check your inbox." Skip straight to the report.

If the inbox is empty or has < 5 unread → "Inbox is clean — nothing worth flagging." Done.

---

## Known limits

- Can't mark read, archive, label, star, or send from here — Sheero is read-only on Gmail by design.
- Can't see attachments' contents (only that an attachment exists).
- If she wants write access later, re-auth workspace-mcp with `gmail.modify` scope (30-sec task, requires her approval).
