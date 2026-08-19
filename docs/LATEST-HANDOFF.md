# LATEST-HANDOFF.md

This file always holds the NEWEST run's HANDOFF block and is overwritten at every landing, in the same
commit as the change — it is the Fable gate's inbox, not an archive. History lives in
`docs/run-journals/run-journal.jsonl` and `docs/PATCH-NOTES-CURRENT.md`.

It is NOT a second format. `docs/HANDOFF-FORMAT.md` remains the canonical FORMAT of the baton — the
eight fields, their order, and the rules per field. This file is only the machine-findable CURRENT COPY
of that same baton, so the gate can read one path instead of scrolling a run report. Gate input = this
copy + the journal tail; the format authority is HANDOFF-FORMAT.md.

---

**GATE STATUS: RATIFIED — 2026-08-19.** The Fable gate has ruled on v4.1.16: verdict **PASS**, **0
overturns**, and **BOTH commits ratified** — `a1097a8a0063c66d5495b6be5cb1c69e438abc4a` (tag
v4.1.16) and the correction `f17aa1a57c2ae5b32ee730b7441fa98db290e640`. The ratification artifact is
`gate_ratification` **record 74** in `docs/run-journals/run-journal.jsonl`, which carries the
dispositions reviewed, the gate rulings, the evidence read and the exceptions. The crew's in-run
critique dispositions are therefore no longer PROVISIONAL. The eight-field HANDOFF block below is the
run baton exactly as the crew wrote it and is PRESERVED VERBATIM — including the Ask Grok question;
ratification records a verdict on it, it does not rewrite it. One field reference to read with its
write-time in mind: the SHA field's "correction commit … which is the commit carrying this file"
described f17aa1a at the moment that block was written; this ratification commit is the one carrying
the file now. Item 18 stays OPEN — its exit needs the NEXT run's self-brief and the lean-scribe
compensating control.

```
HANDOFF
SHA: a1097a8a0063c66d5495b6be5cb1c69e438abc4a — LANDED on main, Tier 2 (local-shell land.ps1 into the
  standing clone C:\Users\chris\autonomy-system-live), confirmed by land.ps1 printing "LANDED a1097a8
  on main" and by git ls-remote refs/heads/main. Base/parent 4949bbc8cf04d7bdba85612e4920522c9866c51b
  (the ratified v4.1.15 gate commit). Annotated tag v4.1.16 rides a1097a8 and is PUSHED
  (refs/tags/v4.1.16 = 316355ab629c04ea01f0ee540558b976bcfb8939).
  PLUS ONE CORRECTION COMMIT on top, which is the commit carrying this file (verify with git log -1;
  a file cannot contain its own landing SHA). It is PATCH-NOTES-only + the regenerated outputs, it
  records that the v4.1.16 package history rows understate the validator self-test (18, not 17) and
  the generator's source count (15, not twelve), and it deliberately LEAVES those two package rows
  frozen — a two-package-file edit is SIGNIFICANT by the written test and this run would not narrow
  that definition by session judgment. The tag is NOT retargeted. Full reasoning: PATCH-NOTES v4.1.16
  addendum, journal records 72-73.
Drive: VERIFIED for a1097a8 by CONTENT, not by timestamp — mirrored docs/BRIEF-PACK.md (Drive id
  13FsAcqayVdZ5YV2wBr0WeOSJ1XBZ8qtT, created 2026-08-19T12:02:31Z) is present in folder
  1E-0tL4DGXk-HVYNlWUc6ccF6SzZh60OE and CONTAINS "MANIFEST" and "v4.1.16". The correction commit's
  own sync is NOT verified at write time, and an
  advanced modifiedTime alone would not verify it either. CONTENT strings named BEFORE landing per
  LANDING-PROTOCOL, for the gate (or, if the gate defers under the lean-scribe rule it is ratifying,
  for the NEXT run): "MANIFEST" in the mirrored docs/BRIEF-PACK.md; "The SPEED PACK" in the mirrored
  docs/EFFICIENCY-MODE.md (exact heading: "## The SPEED PACK — self-brief from the generated brief,
  then verify it"); "lean scribe" appears as "**LEAN SCRIBE.**" in that same file and as "LEAN SCRIBE
  deferral" in the mirrored docs/LANDING-PROTOCOL.md; "v4.1.16" in both mirrored package titles.
  NOT CHECKABLE ON DRIVE, by construction: AGENTS.md, docs/GROK-CONTEXT.txt's tooling and tools/**
  never reach the mirror (the sync covers docs/** only), so AGENTS.md and tools/gen_brief.py are
  verified by reading the standing clone at the landed SHA instead — claiming Drive verification for a
  file Drive never receives would be a false green with a plausible shape.
Changed: tools/gen_brief.py (NEW — stdlib, deterministic, zero wall-clock output; reads 15 canonical
  sources and writes three generated files; loud failure + exit 2 on a missing/empty source, on
  cross-file drift in the shared efficiency block, and on a schema fork between the validator's
  required keys and the document that owns each schema) · docs/BRIEF-PACK.md, docs/GROK-CONTEXT.txt,
  AGENTS.md (NEW, all three GENERATED and committed in this same commit — the first exercise of the
  regeneration rule) · tools/validate_journal.py (+C6 BRIEF-PACK staleness check wired into --all:
  re-hashes every manifest source and both other generated outputs, FAILs naming stale files, enforces
  a MANIFEST FLOOR against manifest amputation, recomputes MANIFEST-DIGEST, and detects a hand-edited
  pack via SELF-DIGEST; --self-test 11 → 18 cases) · docs/EFFICIENCY-MODE.md (NEW "## The SPEED PACK"
  section: self-brief via pack, regeneration rule, Grok context rule, lean scribe, batch gating with a
  hard eligibility test, parallel-crew fan-out; step 8 amended for the lean-scribe deferral) ·
  docs/RUN-TEMPLATE.md (block 1 self-brief + regeneration + --check in the pre-land validators; block 2
  batch gating + lean scribe; block 3 "Read AGENTS.md and docs/BRIEF-PACK.md first" + regenerate +
  never-touch list; block 5 fan-out rules and the scribe's regeneration check) · docs/GROK.md (GROK
  CONTEXT RULE, the version-lag trap, the ASCII-transform hazard) · docs/CURSOR-LANE.md (standing
  briefing section with its three unobservable assumptions; dispatch step 1) · docs/LANDING-PROTOCOL.md
  (lean-scribe deferral invariant, non-mirrored-path invariant, gen_brief --check in the pre-land step,
  and the WRONG "no branch protection exists" sentence corrected against CURSOR-LANE) ·
  docs/SYSTEM-CURRENT.md + docs/SYSTEM-SPEC-CURRENT.md (v4.1.16 titles, SPEC Date/intro, history rows
  with exactly one "(this document)" per file; ONE new byte-identical SPEED PACK line in the shared
  "### Efficiency mode (Fable bookends)" block, plus the stale "CURSOR LANE — ACTIVATION PENDING"
  sentence corrected to ACTIVE in both — block sha256 EQUAL across the two files after both edits) ·
  docs/PATCH-NOTES-CURRENT.md (item 18 ADDED with its named residuals; count superseded to 18 listed /
  13 open; v4.1.16 addendum; nothing renumbered, reordered or closed) · docs/LATEST-HANDOFF.md (this
  baton) · docs/run-journals/run-journal.jsonl (records 68/69/70 grok_critique passes 1–3, record 71
  patch_v4.1.16); CORRECTION COMMIT (this one, docs-only): docs/PATCH-NOTES-CURRENT.md v4.1.16
  addendum correction paragraph, regenerated docs/BRIEF-PACK.md + AGENTS.md, this baton, and journal
  records 72 (routine grok_critique) and 73 (patch_v4.1.16_correction).
Significant: yes
Grok passes requested: 3 (+1 routine on the correction commit) — full ladder run BEFORE landing via the Grok CLI on the Owner machine, each
  prompt file beginning with the freshly generated docs/GROK-CONTEXT.txt (first exercise of the new
  GROK CONTEXT RULE): Pass 1 defects 8 bullets (exit 0, 200s), Pass 2 false-green 8 (exit 0, 190s),
  Pass 3 adversarial 8 (exit 0, 159s). 24 bullets, 22 applied (several partially, each partial stated
  inside its own reason), 2 rejected with reasons. PROMPT_CHARS echoed 6952 / 9012 / 9991 — all three
  exceed the 1900-char guideline and the echo is the compensating control, as at v4.1.14/v4.1.15. The
  ladder changed the build materially rather than decorating it: it produced the cross-file drift
  guard, the schema-fork guard, the MANIFEST FLOOR against amputation, the closer-only regeneration
  rule for fan-out waves, the batch-eligibility hard test, and the correction of two factual errors
  that were live in the package before this run (the stale Cursor ACTIVATION PENDING text and the
  "no branch protection exists" sentence in LANDING-PROTOCOL). The correction commit took its own
  ROUTINE pass (record 72, 6 bullets, 6 applied, exit 0, 160s, PROMPT_CHARS 4071) and that pass
  OVERTURNED the crew's first plan: it had proposed editing both package files, which is SIGNIFICANT
  by the written test, so the package edits were reverted and the correction became PATCH-NOTES-only.
Open items: 18 listed, 13 open. ADDED item 18 (Speed pack + lane auto-briefings) at the end of the
  authoritative list; nothing renumbered, reordered or closed this run, and item 18 is NOT self-closed
  — its exit needs the first SUBSEQUENT run to self-brief via the pack and journal the lean-scribe
  compensating control. Item 13 (Review-gate SPOF) stays open and unwaived. Residuals recorded ON item
  18 rather than carried silently: deleting the generated files still beats the staleness check (an
  absent pack skips cleanly by the ordered semantic; the detector is gen_brief --check, and wiring it
  into CI needs .github/** which was out of scope here); batch eligibility and the Significant field
  are unmechanised, so a split-run evasion rests on gate judgement; whether a Cursor agent reads or
  RE-READS AGENTS.md is unobservable from this repo; and BRIEF-PACK.md is ~544 lines against the
  ~350-line target — a deliberate cost of ladder Pass 2 b1, printed as a NOTE by the generator rather
  than hidden, and a trim call the gate may take. Exceptions: validate_journal.py --all --strict exits
  1 at base on legacy item 10 (pre-existing, carried unchanged; --all, which CI runs, exits 0 before
  and after), and the verify-docs CI conclusion is not observed by this crew.
Ask Grok: the staleness check proves the pack matches its manifest, and the new MANIFEST FLOOR stops
  the manifest from shrinking — but nothing yet proves the pack's PROSE still describes the sources it
  hashes, and the same run writes the generator, the floor and the pack. Given that, what is the
  cheapest artifact a run could emit that would let a script detect a pack whose extracted sections no
  longer correspond to the sections they claim to quote — and what would it have to be anchored to to
  stay forgery-resistant when one crew writes both the extractor and the thing it extracts? Second, on
  the lean scribe: the compensating control is a read the NEXT run performs, so a run that never
  happens silently converts a deferral into a deletion. What observable signal, available in this
  repo, would distinguish a deferral that was genuinely discharged from one that simply aged out?
```
