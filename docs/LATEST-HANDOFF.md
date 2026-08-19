# LATEST-HANDOFF.md

This file always holds the NEWEST run's HANDOFF block and is overwritten at every landing, in the same
commit as the change — it is the Fable gate's inbox, not an archive. History lives in
`docs/run-journals/run-journal.jsonl` and `docs/PATCH-NOTES-CURRENT.md`.

It is NOT a second format. `docs/HANDOFF-FORMAT.md` remains the canonical FORMAT of the baton — the
eight fields, their order, and the rules per field. This file is only the machine-findable CURRENT COPY
of that same baton, so the gate can read one path instead of scrolling a run report. Gate input = this
copy + the journal tail; the format authority is HANDOFF-FORMAT.md.

---

**GATE STATUS: RATIFIED — 2026-08-19.** The Fable gate has ruled on the LIVING SYSTEM MAP run: verdict
**PASS**, **0 overturns**, `fable_phases` **2** so 2 − 2 = **zero fix loops**, on commit
`f13b1e5f26fa58e825795ac0bb2743962469cd6d`. The ratification artifact is `gate_ratification` **record
79** in `docs/run-journals/run-journal.jsonl`, which carries the dispositions reviewed, the three
ANCHOR SPOT-CHECKS the map's own rules make a gate duty, the Drive read the gate performed EARLY at
its own discretion, and the exceptions. The crew's in-run critique dispositions are therefore no
longer PROVISIONAL: all 24 bullets of records 75/76/77 were read in full and both rejections were
AUDITED and UPHELD. **PATCH-NOTES open item 18 is CLOSED by this record** — installation and first
exercise, not ongoing compliance, with residuals (i)–(viii) carried on the closed item as standing
limits — and the board's count moves to **18 listed, 12 open**. This is also the FIRST landing written
under the LEAN SCRIBE law as the scribe's standing shape.

The eight-field HANDOFF block below is the crew's baton. The gate has filled in the SHA the crew could
not know at write time (a file cannot contain its own landing SHA), split the Drive line into what the
gate itself verified and what stays deferred, recorded its own commit at the end of `Changed:`, and
rewritten `Open items:` to the ratified state. The **Ask Grok** question is PRESERVED VERBATIM —
ratification records a verdict on a run, it does not rewrite the run's question.

```
HANDOFF
SHA: f13b1e5f26fa58e825795ac0bb2743962469cd6d — LANDED on main, Tier 2 (local-shell land.ps1 into the
  standing clone C:\Users\chris\autonomy-system-live), and READ BACK by the gate from that clone
  rather than accepted from the crew's report. Base/parent e009fd3, the ratified record-74 gate
  commit. No tag: this run carried no version bump. GATE FILL-IN: the crew's baton said "STAGED
  (unpushed)" at write time, which was correct then and is exactly what tools/gen_map.py prints until
  a gate supplies the number. This ratification commit is the one carrying the file now — verify with
  git log -1; a file cannot contain its own landing SHA.
Drive: TWO HALVES, stated separately rather than as one green line.
  DISCHARGED BY THE GATE at 15:40Z, ahead of the deferral the gate was entitled to keep: the mirrored
  docs/SYSTEM-MAP.html is PRESENT in folder 1E-0tL4DGXk-HVYNlWUc6ccF6SzZh60OE — a file that had never
  existed on that mirror before, so presence alone is a real signal — with mimeType text/html, title
  "Living system map — autonomy-system v4.1.16", size ~34k, read by CONTENT and not by modifiedTime.
  That read also PROVES the tools/drive_sync.py ".html": "text/html" row this run added, which landed
  UNPROVEN: without it the page would have mirrored as application/octet-stream, which Drive neither
  indexes nor renders. Record 79 records the map-side check as done on that evidence — what it quotes
  is presence, MIME type, title and size, not the H1 string named before landing — and names the two
  strings below as the only ones still deferred.
  STILL DEFERRED to the next run under LEAN SCRIBE, carried forward unchanged rather than quietly
  dropped: (a) the exact string "docs/SYSTEM-MAP.html" in the mirrored docs/EFFICIENCY-MODE.md, inside
  the sentence "writes the fourth, `docs/SYSTEM-MAP.html`" — the word "fourth" is the one-word check;
  (b) the exact string "system-map-stale" in that same mirrored file. THIS LANDING ADDS ITS OWN, per
  the rule that each deferral is named separately: (c) the exact string "record 79" in the mirrored
  docs/LATEST-HANDOFF.md. Three strings, two files, one next run — and one read does not discharge a
  deferral it was never told about.
  ALREADY DISCHARGED, by the crew rather than by the gate: the previous deferral for e009fd3 — the
  mirrored docs/LATEST-HANDOFF.md (Drive id 1kTmQYp3_D2ICLnocaY_SD0esgAOXXzym, modifiedTime
  2026-08-19T12:18:05Z) was read and CONTAINS "record 74", closed by CONTENT, not by timestamp
  (record 78).
  NOT CHECKABLE ON DRIVE by construction: tools/gen_map.py, tools/validate_journal.py,
  tools/drive_sync.py and AGENTS.md never reach the mirror (docs/** only) — verify those in the
  standing clone at the landed SHA.
Changed: tools/gen_map.py (NEW — stdlib, deterministic, zero wall-clock; imports tools/gen_brief.py
  for SOURCES and helpers rather than copying them; generates docs/SYSTEM-MAP.html; --check exits 1
  when the page would change; exit 2 with a loud message on a missing/empty source, on an unreadable
  ladder/tier/lane structure, and on a BROKEN ANCHOR) · docs/SYSTEM-MAP.html (NEW, GENERATED — one
  self-contained page, ~34KB, inline CSS/JS, no external fetch, no localStorage, five panels in lay
  language for a non-coder Owner, light/dark, published anchor table, trailing manifest comment with
  SELF-DIGEST + MANIFEST-DIGEST + 15 source hashes) · tools/validate_journal.py (C6 GENERALISED, not
  forked: new check_generated_doc parameterised by a _GeneratedDoc descriptor, with check_brief_pack
  and the new check_system_map as thin wrappers over it; --system-map-path flag; the MANIFEST FLOOR
  and every finding shape now serve both outputs; new self-verifying SELF_TEST_CASE_COUNT constant
  that the self-test asserts against its own case count; --self-test 18 → 26 cases, all pass) ·
  docs/EFFICIENCY-MODE.md (SPEED PACK: four generated outputs and two generators; REGENERATION RULE
  requires both and names system-map-stale; the journal-count lag named with map-last ordering;
  loophole (i) extended to gen_map --check; loophole (ii) extended with the import coupling and its
  cost; the fan-out carve-out renamed GENERATED TRIO → GENERATED SET with an explicit
  never-hand-merge-a-generated-file rule) · docs/RUN-TEMPLATE.md (block 1 regeneration + both
  --check runs + map-last ordering + the fact that CI runs neither --check; block 3 four outputs;
  block 2 gate duty to spot-check three anchor rows against their paragraphs) · tools/drive_sync.py
  (one MIME row: .html → text/html) · docs/PATCH-NOTES-CURRENT.md (item 18 EXTENDED with the fourth
  output, the crew-side exit evidence, and four NEW named residuals; one UPDATED line; NOT closed;
  counts UNCHANGED at 18 listed, 13 open) · docs/BRIEF-PACK.md, docs/GROK-CONTEXT.txt, AGENTS.md
  (regenerated, same commit) · docs/LATEST-HANDOFF.md (this baton) ·
  docs/run-journals/run-journal.jsonl (records 75-77 grok_critique passes 1-3, record 78 patch).
  NO package files, no version bump, no tag, no .github/**, no routing or authority text.
  GATE COMMIT (the one carrying this file, docs/** only, the FIRST commit written under the lean
  scribe): record 79 gate_ratification appended to the journal · docs/PATCH-NOTES-CURRENT.md (item 18
  CLOSED in the board's closed style with its evidence stack, the residuals kept on the item as
  standing limits, a superseding 18-listed/12-open count line, and a second GATE NOTE that supersedes
  the record-74 "stays OPEN" sentence; nothing renumbered, reordered or added) · this baton's gate
  wording · docs/BRIEF-PACK.md, docs/GROK-CONTEXT.txt, AGENTS.md, docs/SYSTEM-MAP.html (all four
  regenerated in this same commit, both generators, map LAST after the journal append).
Significant: yes
Grok passes requested: 3 — full ladder run BEFORE landing via the Grok CLI on the Owner machine,
  each prompt file headed by the freshly generated docs/GROK-CONTEXT.txt per the GROK CONTEXT RULE.
  Pass 1 defects 8 bullets (exit 0, 218s, PROMPT_CHARS 14957), Pass 2 false-green 8 (exit 0, 40s,
  PROMPT_CHARS 16875), Pass 3 adversarial 8 (exit 0, 97s, PROMPT_CHARS 18694). All three exceed the
  1900-character guideline; the echoed PROMPT_CHARS is the compensating control, as at v4.1.14-16.
  24 bullets, 22 APPLIED (several partially, each partial stated in its own reason), 2 REJECTED with
  reasons. The ladder changed the artifact materially rather than decorating it: it produced the
  four-lane correction (the page had sold one-paste autopilot as the whole Owner model), the fix to
  "Fable appears nowhere in between" (false under the fix loop the same page describes), the
  lean-scribe deferral disclosure on the post-land checkpoint, the bounded LGTM rule, the receipt
  honesty line, the honest STAGED tile, the published anchor table, the "snapshot not live state"
  warning on Panel 5, the precise CI claim, the GENERATED SET rename with the no-hand-merge rule,
  the gate anchor spot-check duty, and three extra self-test cases (amputated map manifest,
  hand-edited MANIFEST-DIGEST, and a decoy manifest in the rendered body).
Open items: 18 listed, 12 open. RATIFIED AT THE GATE — item 18 (Speed pack + lane auto-briefings,
  extended by the LIVING SYSTEM MAP) CLOSED on evidence, not on assertion, by gate_ratification
  record 79: verdict PASS, overturns 0, fable_phases 2 so ZERO fix loops; evidence commits f13b1e5
  (this run) plus a1097a8 and f17aa1a (ratified earlier at record 74); ladder records 75-77 with all
  24 bullets read in full and BOTH rejections audited and UPHELD (75 b6 CI wiring — out of that
  run's ordered scope and already pre-authorized at record 74; 77 b1 stale-paste artifact — verified
  against the live file rather than argued); run record 78 verified against the landed content; and
  the gate's own early Drive read. Its exit was checked field by field: all four generated outputs
  present and FRESH, a SUBSEQUENT run self-briefed from the pack and journaled an honest sufficiency
  verdict rather than a green tick, the lean-scribe compensating control for e009fd3 discharged by
  CONTENT, and this run's Owner receipt carries the ROUTING LINE (Owner elected the Opus fast lane;
  reason recorded as OWNER ORDER and SPEED; the Cursor-first default unchanged). The crew
  deliberately did not self-close; the gate scribe closed it. ADDED: none; nothing renumbered or
  reordered. Item 13 (Review-gate SPOF) stays open and unwaived. STILL NOT CLAIMED, closure or no
  closure: this closes INSTALLATION and FIRST EXERCISE, not ongoing compliance and not pack QUALITY,
  and residuals (i)-(viii) stay ON the closed item as standing limits — an anchor proves presence,
  never preserved meaning; the map's journal count is a build-time floor that lags without going
  stale; CI runs neither --check, so a DELETED generated file keeps --all at exit 0 (the .github/**
  wiring stays pre-authorized for the next run that touches that path); and one crew wrote the
  generator, the checker and the page, so the pass condition is partly circular. Exceptions carried
  on record 79: the verify-docs CI conclusion is still NOT observed (compensating controls named
  there — self-test 26/26, --all exit 0, both --check exit 0, and the gate's Drive read);
  validate_journal.py --all --strict still exits 1 at base and after on legacy item 10 (pre-existing,
  unchanged; --all, which CI runs, exits 0 both times); and there is no Python on the Owner machine,
  so clone-side validator re-runs remain impossible and CI is the server check.
Ask Grok: the map now publishes its own anchor table so a human can check whether each quoted phrase
  still sits in a paragraph that MEANS the claim — but that check is unpaid human attention on the
  one artifact nobody re-reads, and pass 3 named it as the residual the whole design rests on. What
  is the cheapest MECHANICAL signal a generator could emit that would distinguish a phrase whose
  surrounding paragraph still asserts the claim from one whose paragraph now negates it, WITHOUT a
  language model in the loop and without the generator becoming a second rulebook? Second: the
  system now has four generated outputs riding every docs/tools commit and one shared checker
  guarding them. At what number of outputs does that stop being a briefing system and start being a
  merge hazard, and what observable in this repo would tell the gate it has crossed that line?
```
