# HANDOFF-FORMAT.md — the end-of-run block

Every Claude run ends by emitting this block. It is the baton: the next session, the Owner, and Grok
all pick up from it. No block = the run is not finished, however good the work was.

## The block

```
HANDOFF
SHA:
Drive:
Changed:
Significant: yes|no
Grok passes requested: 1|3
Open items:
Ask Grok:
```

Eight lines, these fields, this order. Do not rename, reorder, or drop a field — write "none" or
"n/a — <reason>" instead of deleting a line.

## Filled example

```
HANDOFF
SHA: 7f3ab19 (pushed to main, Tier 1 native push)
Drive: mirror folder 1E-0tL4DGXk-HVYNlWUc6ccF6SzZh60OE — SYSTEM-CURRENT.md modifiedTime advanced to
  2026-08-18T02:41:07Z, Actions run 32104881933 green
Changed: docs/SYSTEM-CURRENT.md (+27 title/history/Critique policy), docs/SYSTEM-SPEC-CURRENT.md
  (+30 same section mirrored), docs/GROK.md (new), docs/HANDOFF-FORMAT.md (new), CLAUDE.md (+12)
Significant: yes
Grok passes requested: 3
Open items: 12 carried forward from PATCH-NOTES-CURRENT.md (none closed this run); NEW — nightly task
  observability: first firing unobserved until 2026-08-19 01:30 UTC, exit = first green nightly
  journal record
Ask Grok: The Critique policy says an empty critique is a FAIL on significant work, but nothing
  enforces the 3-pass count at the gate. Where can a significant change still land on one pass, and
  what evidence would prove the ladder actually ran?
```

## Rules per field

- **SHA** — the pushed commit SHA, or exactly `STAGED (unpushed)` when nothing landed. Never a
  prediction, never a SHA you built but did not push. If a push failed, write
  `STAGED (unpushed) — <landing tier attempted> failed: <reason>`. A SHA is a claim; back it with a push.
- **Drive** — the mirror evidence: folder or file link plus the observed `modifiedTime` (and the Actions
  run conclusion if you saw it). If you did not observe the sync, write `not verified this run` — do
  not infer it from a green push.
- **Changed** — every file touched, with a one-phrase what. Staged-but-unlanded files are listed too,
  marked staged.
- **Significant** — `yes` for any change to system rules, routing, safety rules or hard stops, any
  multi-file package change, or anything an Owner order named significant. When unsure → `yes`. This
  field decides the critique depth, so it is the one field never to soften.
- **Grok passes requested** — `1` for routine, `3` for significant (Pass 1 Defects / Pass 2 False-green /
  Pass 3 Final adversarial). Must agree with the Significant field. If the ladder was cut short — credits,
  Grok down — say so here: `3 (only 1 run — Grok unreachable; change staged, not landed)`.
- **Open items** — the count carried from `docs/PATCH-NOTES-CURRENT.md` plus anything opened or closed
  this run, each with owner and exit criterion. "No open items" may only be written if it is true.
- **Ask Grok** — one concrete question for the next critique pass, not a topic. Bad: "review the critique
  policy". Good: "where can a significant change still land on one pass?" If there is genuinely nothing
  to ask, write `none — <why>`; that is rare and reviewable.

## Where it goes

Paste the block at the end of the run report, and append the same facts as a run-journal record in the
same commit as the change (`docs/run-journals/run-journal.jsonl`). The critique policy that sets the
pass count lives in `docs/SYSTEM-CURRENT.md`; the prompt blocks are in `docs/GROK.md`.
