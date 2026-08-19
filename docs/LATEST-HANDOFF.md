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
SHA: the commit carrying this file — verify with git log -1. A file cannot contain its own landing SHA
  and a predicted SHA is exactly the claim HANDOFF-FORMAT.md forbids. Base/parent: e096535 — the
  ratified v4.1.15 commit this gate record gates, whose own parent was 3af3ca9 (the ratified v4.1.14
  gate commit). Tag v4.1.15 rides e096535, NOT the commit carrying this file. Landing tier: 2
  (local-shell land.ps1 into the standing clone) for e096535 and for this gate commit alike.
Drive: pending this landing's sync at write time — not verified when this line was written, and an
  advanced modifiedTime alone would not verify it. CONTENT strings the gate should check, named
  before landing per LANDING-PROTOCOL: "Owner routing directive" in the mirrored SYSTEM-CURRENT.md
  AND SYSTEM-SPEC-CURRENT.md; "USAGE RECEIPT" in the mirrored RUN-TEMPLATE.md; "Receipts — what you
  get after every run" in the mirrored OWNER-FLOW.md; "v4.1.15" in both mirrored package titles.
  GATE UPDATE: this ratification commit's own sync is again pending at write time; its CONTENT string
  is "record 67" in the mirrored PATCH-NOTES-CURRENT.md, and the gate reports the poll result plainly
  rather than inferring it from a modifiedTime. The v4.1.15 strings named above were NOT re-read by
  this gate at write time; record 67 states exactly what the gate did and did not observe — including
  the unobserved verify-docs CI conclusion and the compensating controls accepted in its place.
Changed: docs/SYSTEM-CURRENT.md + docs/SYSTEM-SPEC-CURRENT.md (v4.1.14 → v4.1.15 titles, SPEC Date +
  intro, history rows in both with exactly one "(this document)" per file; the Owner routing
  directive appended inside ## Credit-Aware Routing, BYTE-IDENTICAL in both — directive sha256
  980cd8d984a0e6918c6efb1a620feee97110a6ee05670a766d722c1edc41904e, full added region incl. the
  ladder-added SCOPE paragraph 689c9fb762d287d59e1a33768be1db1ca68c4aa2cd79ac190d87f7efd56a0196; the
  byte-identical ### Efficiency mode block UNTOUCHED, sha256
  9a7fcfd019c5e691395e17b669b5d63bcc58a9b298a17d6b2a4f71f2fba0f956 before and after in both) ·
  docs/RUN-TEMPLATE.md (block 5 plan step must state the routing split and the one-line reason for any
  above-trivial coding NOT sent to Cursor; block 5 step 8 and block 2 GATE must END the Owner message
  with the USAGE RECEIPT, reconciled against journal records) · docs/EFFICIENCY-MODE.md (Autopilot
  lane: receipt rule + reconciliation + blind spots, Cursor-first default with exclusions, hot-path
  carve-out and fail-closed tie-break, Grok drafting/research lane bounded by the trust boundary) ·
  docs/OWNER-FLOW.md (NEW "Receipts" section in lay language; who-bills-what updated for the
  Cursor-first coding default and the Grok drafting lane) · docs/PATCH-NOTES-CURRENT.md (open item 17
  ADDED at the end, nothing renumbered; count superseded to 17 listed / 13 open; v4.1.15 addendum) ·
  docs/LATEST-HANDOFF.md (this baton) · docs/run-journals/run-journal.jsonl (records 63/64/65
  grok_critique passes 1–3, record 66 patch_v4.1.15) · GATE COMMIT (the one carrying this file,
  docs/** only): record 67 gate_ratification appended to the journal, item 17 CLOSED on the
  open-items board with a superseding 17-listed/12-open count line, this baton's gate wording, and
  the first USAGE RECEIPT appended below this block
Significant: yes
Grok passes requested: 3 — full ladder run BEFORE landing via the Grok CLI on the Owner machine:
  Pass 1 defects 8 bullets / 8 applied (exit 0, 84s), Pass 2 false-green 8 / 8 applied (exit 0, 99s),
  Pass 3 adversarial 8 / 8 applied (exit 0, 124s). 24 bullets, 24 applied, 0 rejected, every bullet
  dispositioned, no empty pass, transport cli all three. FLAGGED FOR THE GATE, not presented as a
  score: a ladder with ZERO rejections is either an unusually apt critique or an insufficiently
  sceptical crew — read records 63/64/65 and overturn anything accepted too easily. Two partials are
  recorded inside their APPLYs: Pass 2 b8's "credit saved" field was deliberately NOT built (the
  counterfactual is unmeasurable; a routing line + an explicit "activity, not savings" statement was
  built instead), and Pass 3 b4's no-rollback premise is inaccurate for the Cursor lane (a PR is not
  landed until a Claude gate merges it) — the useful half was applied and the correction written in.
  Prompt files r15p1/2/3.txt echoed PROMPT_CHARS 2861 / 3179 / 3120; all three exceed the 1900-char
  guideline and the echo is the compensating control, as at v4.1.14.
Open items: 17 listed, 12 open. RATIFIED at the gate — item 17 (Owner routing directive + mandatory
  usage receipts) CLOSED on evidence, not on assertion, by gate_ratification record 67: verdict PASS,
  overturns 0, fable_phases 2 so ZERO fix loops, evidence commit e096535 (tag v4.1.15, parent
  3af3ca9) plus grok_critique records 63-65 and run record 66, and the first gate-composed USAGE
  RECEIPT, appended below this block by this same commit. All 24 ladder bullets were read in full by
  the gate and nothing was overturned; the zero-rejection ladder was AUDITED rather than waved
  through, the two partial-applies being transparently recorded inside their own APPLY reasons. The
  ladder-added SCOPE paragraph was read in full and ADOPTED as ratified policy text: it bounds the
  directive to routing preference only, amends no authority rule, and its hot-path and surgery
  exclusions stand as written. The v4.1.15 crew deliberately did NOT close this item; the gate scribe
  did, checking every field of the exit test against the record, the non-ceremonial test included
  (crew agent a106e9cb spawned; the receipt carries the routing line). ADDED: none; nothing
  renumbered or reordered. Item 13 (Review-gate SPOF) stays open and unwaived. STILL NOT CLAIMED,
  closure or no closure: this closes INSTALLATION, not compliance — nothing mechanically enforces
  receipt presence, receipt truthfulness, the routing split, or the rejection of a boilerplate
  non-dispatch reason (gate discipline pending open items 2 and 5), and the receipt's token line
  still reconciles against nothing. Exceptions carried on record 67: the verify-docs CI conclusion
  was NOT observed this run (compensating controls named there); validate_journal.py --all --strict
  exits 1 at base on legacy item 10, pre-existing and carried unchanged, while --all (what CI runs)
  exits 0 before and after; and ts on records 63-65 are record-WRITE times per lesson
  L-20260819-01.
Ask Grok: the usage receipt reconciles three of its four lines against records this same orchestration
  wrote, and the fourth — tokens — reconciles against nothing at all, while the only surface that can
  see the token numbers is the same surface that composes the receipt and spends the Fable phases it
  reports. Given that, what is the cheapest artifact a RUN could emit that would let a script detect a
  receipt whose token line is fabricated or materially incomplete — and what would that artifact have
  to be anchored to (commit time, mirror creation time, CI run id, something else) to stay
  forgery-resistant when the same crew writes both the numbers and the record about them? Second, on
  the policy: what observable signal, available in the repo, would distinguish a Cursor-first default
  that is actually biting from one that is being honoured on paper while every run finds a legal
  reason to stay on Opus?
```

---

Appended by the ratification gate of 2026-08-19 (`gate_ratification` record 67), per the v4.1.15 rule
that every run ends with a gate-composed receipt. It is NOT a ninth HANDOFF field — the baton above
still carries exactly the eight fields of `docs/HANDOFF-FORMAT.md`.

```
USAGE RECEIPT (gate-composed; token lines self-reported by spawn results, marked per the v4.1.15 rule):
RUN v4.1.14 autopilot pilot - crew a871d795 248759 tok, scribe a6215d6c 118804 tok (Opus weight) | fable_phases 2 | grok 3 passes 53/38/44s (records 58-60) | cursor 0 dispatches, routing note journaled (record 61)
RUN v4.1.15 surgery - crew a106e9cb 240603 tok (Opus weight), gate-scribe tokens reported in the Owner verdict message (post-write by construction) | fable_phases 2 | grok 3 passes 84/99/124s (records 63-65) | cursor not dispatched, routing note journaled (record 66); routing split: Opus authoring+landing, Grok critique, Cursor excluded (surgery-class - first exercise of the new exclusion)
Blind spots per the directive: gate/plan turns, Owner-pasted sessions, cached re-reads, provider caps; reconciliation proves internal consistency, not billed truth.
```
