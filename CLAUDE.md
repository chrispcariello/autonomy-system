# AUTONOMY-SYSTEM — session operating contract

You are working inside Chris Cariello's Autonomous Multi-Agent System. This file is the
standing contract for ANY Claude session attached to this repo. The full rules live in
`docs/SYSTEM-CURRENT.md` (FOR-CLAUDE package) and `docs/SYSTEM-SPEC-CURRENT.md` — read the
current version header + Hard rules + Version History before substantive work.

## Links
- Canonical (private; Claude writes here): https://github.com/chrispcariello/autonomy-system
- Public Drive mirror (read-only; Actions syncs it on every push to `main`) — this is what Grok reads: https://drive.google.com/drive/folders/1E-0tL4DGXk-HVYNlWUc6ccF6SzZh60OE

## Model split (Owner rule — do not violate)
- **Fable 5 Max/Ultracode**: highest-level orchestration and final quality gate ONLY.
- **Opus 5 Max/Ultracode**: ALL other Claude work (execution units, edits, builds, sweeps).
- Grok Heavy = critique; Grok Build = volume; both return UNVERIFIED — never authority.
- Cowork = hands + activator (browser, desktop, evidence): NOT a git source of truth, no live-write authority, never approves its own output.

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

## Critique policy (rule: docs/SYSTEM-CURRENT.md · prompts: docs/GROK.md)
Routine = 1 focused Grok Heavy pass. Significant (system rules, routing, safety/hard stops, multi-file
package changes, anything an Owner order names significant) = the 3-pass ladder: Pass 1 Defects →
Pass 2 False-green → Pass 3 Final adversarial. APPLY or explicitly REJECT each major finding with a
one-line journaled reason; an "LGTM" or empty critique is a FAIL on significant work, not a pass.
Efficiency may cut critique FREQUENCY, never DEPTH. Never hand Grok a GitHub link (private — it cannot
open it); hand it the Drive links.
- **Review-gate availability:** no PASS/CLOSED on significant work without its `grok_critique` records
  (1 routine / 3 ladder). No CLI *and* no browser session (Owner PC off = both) ⇒ status
  `BLOCKED_ON_CRITIQUE`: stage the work, journal a `critique_blocked` record, never false-green. Queue +
  record shapes: `docs/GROK.md` → "Review-gate availability".
- Run `python3 tools/validate_journal.py --all` before landing (CI runs it too, `verify-docs`).

## Landing rules
- Land via the best available tier in `docs/LANDING-PROTOCOL.md` (Tier 1 native push from a session created WITH the repo attached · Tier 2 local-shell · Tier 3 one-click); say which tier you used.
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

## Nightly hygiene
`docs/NIGHTLY-HYGIENE.md` runs unattended at 01:30 UTC daily — steps a–g, docs only, 20-minute cap, machine
mirror `docs/nightly-checklist.json`; it reports BLOCKED rather than claiming an unobserved push or sync.

## Reporting
Blunt, nothing falsely green (and nothing falsely red). Summary Reports carry: PASS/FAIL,
commit SHA + tag, Actions run conclusion, Drive verification, retrieval_ref, remaining open
items. One surplus improvement per cycle (loop step 7) — small, flagged, docs-first.
END EVERY RUN with the HANDOFF block, all eight fields, per `docs/HANDOFF-FORMAT.md`:
`HANDOFF / SHA: / Drive: / Changed: / Significant: yes|no / Grok passes requested: 1|3 / Open items: / Ask Grok:`
SHA is a pushed commit or exactly `STAGED (unpushed)`, never a prediction.

## Current map
`docs/SYSTEM-MAP-AND-AUTOMATION-ROADMAP.md` holds the as-built map, Grok bridge options, and
the phased automation roadmap. Grok Bots + Event Bus collapse rule are DEFERRED (Phase 2) —
do not invent or activate them. `docs/run-journals/INTERCONNECT.md` maps the repo → Actions → Drive → Grok → gate loop; `docs/OWNER-QUICK-REFERENCE.md` is the Owner's one-pager.
