# Decisions Log

Append-only. Format: `## YYYY-MM-DD — Title`, then Why/What/Status.

---

## 2026-04-28 — Newsletter cadence: bi-weekly starting May 6
**Why:** Q1 retro revealed a marketing cadence gap. Acme Corp ships fast but tells no one. Bi-weekly is sustainable (weekly is overcommitting given dev pace).
**What:** Every other Wednesday, Substack newsletter, ~600 words per issue.
**Status:** Active. First issue due 2026-05-06.

---

## 2026-04-22 — Stripe Checkout over custom payment form
**Why:** Custom Stripe form added 2 weeks of work and ongoing security maintenance. Checkout is fully managed by Stripe. Trade-off: less branding control, but small cost for indie scale.
**What:** Migrated new sign-ups to Stripe Checkout; existing payment methods unchanged.
**Status:** Done.

---

## 2026-04-12 — Pricing tier bump $15 → $25/mo
**Why:** Customer interviews showed willingness to pay $25-30 for the AI features. $15 was undervaluing the product.
**What:** New sign-ups pay $25/mo. Existing customers grandfathered at $15.
**Status:** Done. Conversion rate held at 6% (target was 4% minimum at the higher price).
