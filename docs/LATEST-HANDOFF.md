# LATEST-HANDOFF.md

This file always holds the NEWEST run's HANDOFF block and is overwritten at every landing, in the same
commit as the change — it is the Fable gate's inbox, not an archive. History lives in
`docs/run-journals/run-journal.jsonl` and `docs/PATCH-NOTES-CURRENT.md`.

It is NOT a second format. `docs/HANDOFF-FORMAT.md` remains the canonical FORMAT of the baton — the
eight fields, their order, and the rules per field. This file is only the machine-findable CURRENT COPY
of that same baton, so the gate can read one path instead of scrolling a run report. Gate input = this
copy + the journal tail; the format authority is HANDOFF-FORMAT.md.

---

```
HANDOFF
SHA: the commit carrying this file — verify with git log -1. A file cannot contain its own landing
  SHA, and a predicted SHA is exactly the claim HANDOFF-FORMAT.md forbids.
Drive: pending this landing's sync — content strings to check are listed in the run report. Not
  verified at write time; an advanced modifiedTime alone would not verify it either.
Changed: docs/SYSTEM-CURRENT.md + docs/SYSTEM-SPEC-CURRENT.md (v4.1.13 titles, SPEC intro, history
  rows, byte-identical 8-line "### Efficiency mode (Fable bookends)" block) · docs/EFFICIENCY-MODE.md,
  docs/RUN-TEMPLATE.md, docs/CURSOR-LANE.md, docs/LATEST-HANDOFF.md (all new) ·
  docs/LANDING-PROTOCOL.md (+2 invariants: Tiers 1/2 are Claude-authored only; every landing refreshes
  this file) · CLAUDE.md (+3 pointer blocks) · docs/GROK.md (transport sentence names the run's
  orchestrating session) · docs/run-journals/INTERCONNECT.md (Cursor no longer deferred) ·
  docs/PATCH-NOTES-CURRENT.md (v4.1.13 addendum, open item 15, superseded note on the v4.1.11
  free-tools entry) · tools/validate_journal.py (cursor_dispatch + gate_ratification key checks, 2 new
  self-test fixtures) · .github/workflows/verify.yml (pull_request trigger unfiltered; push keeps its
  path filter) · docs/run-journals/run-journal.jsonl (patch_v4.1.13 + ladder records 52/53/54)
Significant: yes
Grok passes requested: 3 — ladder COMPLETE via CLI: Pass 1 defects 8/7 (288s), Pass 2 false-green 8/7
  (163s), Pass 3 adversarial 8/5 (381s); 24 bullets, 19 applied, 5 rejected, no empty pass
Open items: 15 listed, 13 open. None closed this run. NEW item 15 — Cursor lane activation: accounts
  paired and GitHub connected per Owner report 2026-08-18, but the lane is UNACTIVATED (no dispatch,
  no PR). Owner: scope the GitHub grant (URGENT — the grant is live now) and decide branch protection
  (ruleset vs manual-gate merging), both PENDING; Exit: the first Cursor PR passes the full review
  lane and merges with a journaled cursor_dispatch record. Item 13 (Review-gate SPOF) stays open and
  unwaived; the Owner's existing xAI key is recorded as AVAILABLE-not-wired against it.
Ask Grok: efficiency mode is written but unproven — no run has executed under it, the ≤5% Fable-token
  target has no meter, and gate_ratification is required by prose that nothing mechanically enforces.
  On the first real bookend run, what single observation would prove the gate actually ratified rather
  than rubber-stamped, and what would that observation look like if it were faked?
```
