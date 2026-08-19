# LATEST-HANDOFF.md

This file always holds the NEWEST run's HANDOFF block and is overwritten at every landing, in the same
commit as the change — it is the Fable gate's inbox, not an archive. History lives in
`docs/run-journals/run-journal.jsonl` and `docs/PATCH-NOTES-CURRENT.md`.

It is NOT a second format. `docs/HANDOFF-FORMAT.md` remains the canonical FORMAT of the baton — the
eight fields, their order, and the rules per field. This file is only the machine-findable CURRENT COPY
of that same baton, so the gate can read one path instead of scrolling a run report. Gate input = this
copy + the journal tail; the format authority is HANDOFF-FORMAT.md.

---

**GATE STATUS: PENDING.** This run is an Opus crew run landed under efficiency mode; its critique
dispositions are PROVISIONAL until a Fable `gate_ratification` record says otherwise. It also carries
the crew-side evidence for PATCH-NOTES open item 18 and does NOT close it — the gate closes it.

```
HANDOFF
SHA: STAGED (unpushed)
Drive: NOT VERIFIED AT WRITE TIME, and deliberately so — this run lands under the LEAN SCRIBE rule
  now in force (ratified at record 74), so the Drive CONTENT re-read of THIS landing is DEFERRED to
  the next run as a journaled compensating control. CONTENT STRINGS NAMED BEFORE LANDING, for the
  gate or the next run to find in the mirror folder 1E-0tL4DGXk-HVYNlWUc6ccF6SzZh60OE:
  (1) the mirrored docs/SYSTEM-MAP.html is PRESENT at all (a file that has never existed on the
  mirror before, so presence alone is a real signal here);
  (2) the exact string "How this system works" in that mirrored page (its H1);
  (3) the exact string "docs/SYSTEM-MAP.html" in the mirrored docs/EFFICIENCY-MODE.md, inside the
  sentence "writes the fourth, `docs/SYSTEM-MAP.html`" — the word "fourth" is the one-word check;
  (4) the exact string "system-map-stale" in that same mirrored docs/EFFICIENCY-MODE.md.
  THIS RUN DID DISCHARGE THE PREVIOUS DEFERRAL: the mirrored docs/LATEST-HANDOFF.md (Drive id
  1kTmQYp3_D2ICLnocaY_SD0esgAOXXzym, modifiedTime 2026-08-19T12:18:05Z) was read and CONTAINS
  "record 74", so the deferred CONTENT check for e009fd3 is closed by CONTENT, not by timestamp.
  NOT CHECKABLE ON DRIVE by construction: tools/gen_map.py, tools/validate_journal.py,
  tools/drive_sync.py and AGENTS.md never reach the mirror (docs/** only) — verify those in the
  standing clone at the landed SHA. One transport note: tools/drive_sync.py previously had no MIME
  row for .html, so the first mirrored copy of the map would have uploaded as
  application/octet-stream, which Drive neither indexes nor renders; this run adds ".html":
  "text/html" so the next run's CONTENT read is actually possible. That row is UNPROVEN until a
  sync runs.
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
Open items: 18 listed, 13 open — UNCHANGED. No item added, closed, renumbered or reordered. Item 18
  EXTENDED with the fourth generated output and with this run's crew-side exit evidence: the
  pack-first self-brief and the lean-scribe compensating control are both journaled on record 78.
  Item 18 is deliberately NOT self-closed. Four NEW residuals recorded ON item 18 rather than
  carried silently: an anchor proves presence, never preserved meaning; the map's journal count is a
  build-time floor that lags without going stale; CI runs neither --check so a DELETED map keeps
  --all at exit 0 (the .github/** wiring was pre-authorized at record 74 and stayed out of this
  run's ordered scope); and one crew wrote the generator, the checker and the page, so the pass
  condition is partly circular. Exceptions: validate_journal.py --all --strict still exits 1 at base
  and after, on legacy item 10 (pre-existing, unchanged; --all, which CI runs, exits 0 both times),
  and the verify-docs CI conclusion is not observed by this crew.
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
