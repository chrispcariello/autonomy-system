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
  SHA, and a predicted SHA is exactly the claim HANDOFF-FORMAT.md forbids. Base/parent: 3ce0fc3 —
  the ratified v4.1.14 commit this gate record gates, whose own parent was 59aaa51. Tag v4.1.14
  rides 3ce0fc3, not this one.
Drive: pending this landing's sync — CONTENT strings to check are named here so the gate can verify
  rather than infer: "Autopilot lane" in the mirrored EFFICIENCY-MODE.md, SYSTEM-CURRENT.md and
  SYSTEM-SPEC-CURRENT.md; "AUTOPILOT prompt" in the mirrored RUN-TEMPLATE.md; "fix-loop" in the
  mirrored SYSTEM-CURRENT.md; and OWNER-FLOW.md present at all (a new file must be CREATED in the
  mirror, not merely updated). Not verified at write time; an advanced modifiedTime alone would not
  verify it either. GATE UPDATE: those v4.1.14 strings were CONTENT-verified in the mirror by the
  gate — OWNER-FLOW.md read back in full, created 2026-08-19T09:39:03Z. This ratification commit's
  own sync is again pending at write time; its CONTENT string is "record 62" in the mirrored
  PATCH-NOTES-CURRENT.md.
Changed: docs/OWNER-FLOW.md (NEW — Owner-facing lay-language map of the four lanes, the one-card
  principle, who bills what with the no-meter caveat, desktop-hands + parking rule, honest
  no-franchise-kit-yet note, where things live) · docs/RUN-TEMPLATE.md (+ blocks 4 PLAN and
  5 AUTOPILOT; intro now says five blocks) · docs/EFFICIENCY-MODE.md (+ ### Autopilot lane: three
  verdicts, bounded 3-loop fix loop, verdict mapping, fix-loop critique rule, one-gate coverage,
  first-gate standard, post-land honesty, no-supervisor honesty, phase arithmetic) ·
  docs/SYSTEM-CURRENT.md + docs/SYSTEM-SPEC-CURRENT.md (v4.1.13 → v4.1.14 titles, SPEC Date + intro,
  history rows in both, exactly one "(this document)" per file; ONE identical line appended to the
  byte-identical ### Efficiency mode block — sha256 matches across both files) ·
  docs/PATCH-NOTES-CURRENT.md (open item 16 ADDED at the end, nothing renumbered; count superseded to
  16 listed / 13 open; v4.1.14 addendum) · docs/LATEST-HANDOFF.md (this baton) ·
  docs/run-journals/run-journal.jsonl (records 58/59/60 grok_critique passes 1–3, record 61
  patch_v4.1.14) · GATE COMMIT (the one carrying this file, docs/** only): record 62
  gate_ratification appended to the journal, item 16 closed on the open-items board with a
  superseding 16-listed/12-open count line, this baton's gate wording, and lesson L-20260819-01
Significant: yes
Grok passes requested: 3 — full ladder run BEFORE landing via the Grok CLI on the Owner machine:
  Pass 1 defects 8 bullets / 8 applied (exit 0, 53s), Pass 2 false-green 8 / 6 applied 2 rejected
  (exit 0, 38s), Pass 3 adversarial 8 / 7 applied 1 rejected (exit 0, 44s). 24 bullets, 21 applied,
  3 rejected, every bullet dispositioned, no empty pass, transport cli all three.
Open items: 16 listed, 12 open. RATIFIED at the gate — item 16 (Autopilot lane) CLOSED on evidence,
  not on assertion, by gate_ratification record 62: verdict PASS, overturns 0, fable_phases 2 so
  ZERO fix loops, target carrying the literal prefix "autopilot: ", evidence commit 3ce0fc3
  (tag v4.1.14) plus grok_critique records 58-60. All 24 ladder bullets were read in full by the
  gate and none of the 3 rejections was overturned. The v4.1.14 crew deliberately did NOT close this
  item; the gate scribe did, checking every field of the exit test against the record. ADDED: none;
  nothing renumbered or reordered. Honest limit, recorded not waived: this ratifies ONE clean pass —
  FIX, the 3-loop ceiling and BLOCK remain unexercised, and fable_phases is still an unmetered proxy
  (open items 2 and 5). Item 13 (Review-gate SPOF) stays open and unwaived.
Ask Grok: this lane's gate is POST-LAND by design — the crew commits, then Fable reads it — so the
  only pre-land protection is the crew's own ladder plus the validators, and the only check that the
  ladder was REAL rather than well-formed is one unmechanised human-shaped judgement at the gate.
  What is the cheapest artifact a crew could produce that would make a FAKED ladder detectable by a
  script rather than by that judgement, and what would that artifact have to contain to be forgery-
  resistant given that the same crew writes both the diff and the journal records about it?
  Related: records 58-61 carry estimated ts values, two postdating the runs end - what minimal
  machine-stamped evidence bundle would make journal times reconcilable against commit and mirror
  anchors by script alone?
```
