# CURSOR-PILOT.md — first Cursor lane agent

I am this repo's first Cursor Ultra background agent. This file is the
bounded docs-only pilot that PATCH-NOTES open item 15 named as activation
evidence. It is not a claim the lane already works; that waits on CI, a
Grok critique of the diff, and a Claude gate merge.

Rules I must follow, in my own words (from CURSOR-LANE.md and CLAUDE.md):

1. Pull requests only. I branch from `main`, open a PR, and never push
   `main`. A `cursor/*` branch is Event-Bus staging; the merge is the
   canonical write and only a Claude gate performs it.
2. Scope is `docs/**` and `tools/**`. A PR that touches anything else is
   out of scope and should be closed, not repaired by the reviewer.
3. My output is UNVERIFIED under Hard Rule 3 until a Claude gate reviews
   and merges it after `verify-docs` CI plus a Grok critique. I build;
   I do not gate, and I do not approve my own work.
4. Hard stops bind this lane too: money, legal, third-party contact, and
   credentials escalate to the Owner.

Docs I actually read to write this: `CLAUDE.md`; `docs/CURSOR-LANE.md`;
`docs/PATCH-NOTES-CURRENT.md` (item 15); `docs/lessons/lessons.jsonl`
(L-20260817-01…06); `docs/run-journals/run-journal.jsonl` (tail through
the v4.1.13 ladder); `docs/RUN-TEMPLATE.md`; `docs/HANDOFF-FORMAT.md`.
retrieval_ref `LM-RET-2026-08-18T23:20Z-A` (same targets as above).
