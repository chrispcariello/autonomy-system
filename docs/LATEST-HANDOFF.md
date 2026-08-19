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
  and a predicted SHA is exactly the claim HANDOFF-FORMAT.md forbids. Base/parent: 3af3ca9 (the
  ratified v4.1.14 gate commit). Tag v4.1.15 rides THIS commit. Landing tier: 2 (local-shell
  land.ps1 into the standing clone).
Drive: pending this landing's sync at write time — not verified when this line was written, and an
  advanced modifiedTime alone would not verify it. CONTENT strings the gate should check, named
  before landing per LANDING-PROTOCOL: "Owner routing directive" in the mirrored SYSTEM-CURRENT.md
  AND SYSTEM-SPEC-CURRENT.md; "USAGE RECEIPT" in the mirrored RUN-TEMPLATE.md; "Receipts — what you
  get after every run" in the mirrored OWNER-FLOW.md; "v4.1.15" in both mirrored package titles.
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
  grok_critique passes 1–3, record 66 patch_v4.1.15)
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
Open items: 17 listed, 13 open. ADDED item 17 (Owner routing directive + mandatory usage receipts) at
  the end of the authoritative v4.1.11 list; nothing renumbered, reordered or closed this cycle. Item
  17's exit is the directive present and IDENTICAL in both package files on main AND a gate-composed
  usage receipt delivered on a ratified run — the crew does NOT close it; the gate scribe does, and
  the receipt this gate composes is the first opportunity to satisfy the second half. A ceremonial
  zero-spawn run does not close it. Item 13 (Review-gate SPOF) stays open and unwaived. NOT CLAIMED:
  no usage receipt has ever been delivered, and nothing mechanically enforces receipt presence,
  receipt truthfulness, the routing split, or the rejection of a boilerplate non-dispatch reason —
  gate discipline pending open items 2 and 5. Pre-existing exception, not introduced here:
  validate_journal.py --all --strict exits 1 at base on legacy item 10; --all (what CI runs) exits 0
  before and after, --self-test 11/11.
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
