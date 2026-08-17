# Smoke-test journal — SYSTEM v4.1.6 — 2026-08-17

## retrieval_refs used today

- `LM-RET-2026-08-17T10:30Z-C` — smoke
- `LM-RET-2026-08-17T10:35Z-D` — rerun
- `LM-RET-2026-08-17T10:45Z-E` — this storage promotion

## Status

All smoke checks **PASS**:

- v4.1.6 confirmed
- HR7 enforcement quoted
- one-Opus-unit execution verified twice
- quotes gate-verified
- zero live/ledger writes

Patch v4.1.6 gate: **PASS** with 2 accepted residual FAILs (pooled Fable/Opus budget) + 9 open items listed in `PATCH-NOTES-CURRENT.md`.

## Interop note

"Grok (and any non-Claude reviewer) cannot read Claude-local /root/staging. Only artifacts promoted to AUTONOMY-SYSTEM (shared durable home) are reviewable outside this sandbox."

## Pointers

`SYSTEM-CURRENT.md` and `PATCH-NOTES-CURRENT.md` live in `AUTONOMY-SYSTEM/` (Drive links added by the orchestrator after promotion; local build path: `/root/staging/system-selftest-2026-08-14/AUTONOMY-SYSTEM/`).

Note: package version at promotion time is v4.1.7 (= v4.1.6 + Durable storage rule); this journal covers the v4.1.6 smoke tests.

Drive links (added at promotion): AUTONOMY-SYSTEM folder https://drive.google.com/drive/folders/1E-0tL4DGXk-HVYNlWUc6ccF6SzZh60OE · SYSTEM-CURRENT.md https://drive.google.com/file/d/1DqpkDvXF2mlCSlilpd1UnMDRglQQ77Nq/view · SYSTEM-SPEC-CURRENT.md https://drive.google.com/file/d/1TyuWBUFM3oxjRIkdHwRNso-msvxRxnZH/view
