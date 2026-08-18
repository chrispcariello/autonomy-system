# AUTONOMY-SYSTEM — session operating contract

You are working inside Chris Cariello's Autonomous Multi-Agent System. This file is the
standing contract for ANY Claude session attached to this repo. The full rules live in
`docs/SYSTEM-CURRENT.md` (FOR-CLAUDE package) and `docs/SYSTEM-SPEC-CURRENT.md` — read the
current version header + Hard rules + Version History before substantive work.

## Model split (Owner rule — do not violate)
- **Fable 5 Max/Ultracode**: highest-level orchestration and final quality gate ONLY.
- **Opus 5 Max/Ultracode**: ALL other Claude work (execution units, edits, builds, sweeps).
- Grok Heavy = critique; Grok Build = volume; both return UNVERIFIED — never authority.

## Hard rules (condensed — full text in docs/SYSTEM-CURRENT.md)
1. Only the Claude Code surface performs live system writes; Snapshot → Verify → Rollback first.
2. Cowork holds NO live-write authority of any duration.
3. Non-Claude output enters as UNVERIFIED (Event Bus / PR) until a Claude gate verifies.
6. Money, legal, third-party contact, credentials always escalate to the Owner.
7. Significant tasks REQUIRE a Learning Memory retrieval reference recorded on the task
   (`LM-RET-<UTC>-<letter>` + targets). A missing retrieval_ref is a self-test failure.

## Before any significant task
1. Read `docs/lessons/lessons.jsonl` (all of it — currently L-20260817-01…06) and the tail of
   `docs/run-journals/run-journal.jsonl`; record your retrieval_ref.
2. Check `docs/PATCH-NOTES-CURRENT.md` → REMAINING OPEN ITEMS. Do not silently re-close or
   re-open items; report bluntly. "No open items" may only be claimed if true for the version+date.
3. Run `python3 tools/specguard.py --spec <file>` before AND after touching either package doc.

## Landing rules
- Version-number bump ⇒ history rows in BOTH package files in the same patch (L-20260817-04),
  exactly one "(this document)" per file on the newest row, AFTER the em dash; bump the title
  headers too (a miss on 2026-08-17 cost a follow-up commit). Tag on version change.
- Journal rides every landing: append run-journal records in the SAME commit as the change.
  Never write outcome claims (green runs, Drive syncs) before the outcome is observed.
- Weekly reset string is exactly `Sunday 9:00 PM America/New_York` at every site.
- NEVER commit secrets, OAuth client secrets, tokens, service-account keys, or .env files.
  Never print secret values in chat or logs; lengths and pass/fail shapes only.
- Push lands on `main`. Drive mirrors automatically via `.github/workflows/sync-docs-to-drive.yml`
  (OAuth owner-auth; SA fallback is update-only). Do not claim LIVE unless the file is visible
  in Drive (folder 1E-0tL4DGXk-HVYNlWUc6ccF6SzZh60OE).

## Reporting
Blunt, nothing falsely green (and nothing falsely red). Summary Reports carry: PASS/FAIL,
commit SHA + tag, Actions run conclusion, Drive verification, retrieval_ref, remaining open
items. One surplus improvement per cycle (loop step 7) — small, flagged, docs-first.

## Current map
`docs/SYSTEM-MAP-AND-AUTOMATION-ROADMAP.md` holds the as-built map, Grok bridge options, and
the phased automation roadmap. Grok Bots + Event Bus collapse rule are DEFERRED (Phase 2) —
do not invent or activate them.
