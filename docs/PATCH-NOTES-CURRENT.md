# SYSTEM v4.1.6 — Patch Notes (hygiene-only)

**Cycle:** 2026-08-17. retrieval_ref `LM-RET-2026-08-17T01:50Z-B` (orchestration-memory@b62df0a539c8, preferences@fea4f809c4c2, lessons L-20260817-01/02/03) — recorded on the task and echoed by the patch unit.
**Routing:** Fable 5 orchestrated and gated; one Opus 5 unit executed both files (1 auto-return bounce). Grok not called.
**Snapshot → Verify → Rollback:** sources untouched (sha256 verified before and after, twice); patch landed as new files; rollback = delete `patch-v4.1.6/`. Staged docs only — no live path was authorized and none was used.

## CHANGELOG (line-level)

**SYSTEM-v4.1.6-FOR-CLAUDE.md** (from v4.1.5; 10 lines replaced + 2 inserted, all other lines byte-identical, confirmed by diff):
- L1 title → v4.1.6
- L70 Hard Rule 7 → enforcement clause restored: "A missing retrieval reference is a self-test failure" (SPEC-intent wording) [fix 2]
- L104 / L118 / L140 / L151 → weekly reset now "Sunday 9:00 PM America/New_York" at all four sites, one identical rendering, zero stale "9pm" [fix 5]
- L120 enum → `[NORMAL | CONSERVE_CLAUDE | CLAUDE_CRITICAL | CONSERVE_GROK | GROK_DOWN | CONSERVE_BOTH | UNKNOWN]`; STOP_LONG_RUNS removed (an action, redundant with CONSERVE_BOTH — logged in the v4.1.6 history row) [fix 3]
- L130 Unknown row → Mode cell is the real token UNKNOWN; condition moved to Action ("Treat as CONSERVE_CLAUDE if Owner reported high usage; browser-check before any long Claude run") [fix 3]
- L151 standing order → steps (4)/(5) mapped to enum "(mode: CLAUDE_CRITICAL)" / "(mode: CONSERVE_BOTH)"; L154 → "record UNKNOWN (mode: UNKNOWN)" [fix 3]
- History → v4.1.3 row marked "cost caveat superseded at v4.1.5 by the role-based cost note" [fix 6]; **v4.1.4 row inserted** attributing Credit-Aware Routing (browser checks, thresholds, Grok Build delegation strategies, Sunday reset, standing order) [fix 1]; v4.1.5 row unchanged; v4.1.6 row added, carries "(this document)" after the dash so the linter parses it

**SYSTEM-v4.1.6-SPEC.md** (from v4.1.3 SPEC; 11 lines replaced + 3 inserted):
- L1–3 header → v4.1.6, 2026-08-17, hygiene-only intro
- L8 Design Goal → "coordinated by Claude Code (Claude Fable 5 Max/Ultracode orchestrates; Claude Opus 5 Max/Ultracode executes all other Claude work)" [fix 4]
- L36–37 Main Coordinator → split heading + Owner model-split line (role-based, not cost-based; Fable priced higher), replacing the obsolete "Fable = non-critical fallback" line
- L103 Hard Rule 1 → matches FOR-CLAUDE: Claude Code surface holds live-write authority (orchestrator Fable, other work Opus)
- L127–129 Model Routing → Cowork row caveat updated to role-based framing; Fable = orchestration/verification/live-write authority surface; Opus = all other Claude work; Discovery row untouched
- History → "(this document)" removed from v4.1.3 row + superseded note added [fixes 6, 7]; v4.1.4, v4.1.5, v4.1.6 rows added; exactly one "(this document)", on v4.1.6, linter-parseable [fix 7]

## specguard evidence (before → after)

- FOR-CLAUDE: **13 findings [10 FAIL, 3 ADVISORY] → 3 [2 FAIL, 1 ADVISORY]**. Cleared: v4.1.4 numbering gap, both enum mismatches, all 4 timezone-less reset sites, reset-format inconsistency, Credit-Aware-Routing and Hard-rules attribution advisories. Version run now parses v1→v4.1.6 contiguously, zero unparsed history rows.
- SPEC: **3 findings [0 FAIL] → 2 [0 FAIL]**; Design Goal advisory cleared; version run parses v1→v4.1.6, no gaps.
- Full outputs: `specguard-before.txt` / `specguard-after.txt`; source hashes: `snapshot-hashes.txt`.

## DONE MEANS — verified item by item at the gate

v4.1.4 present in FOR-CLAUDE history ✓ · HR7 fail-on-missing-retrieval_ref present ✓ · enum covers every threshold mode (7/7, both directions) ✓ · Design Goal matches Fable/Opus split ✓ · reset carries America/New_York (4/4 sites) ✓ · remaining gaps listed below ✓

## OPEN ITEMS after this patch (not falsely green — these remain)

1. **Pooled Fable/Opus budget** (FOR-CLAUDE L118 template line + L124 shared threshold table): two separately-budgeted models still report as one figure — "Fable exhausted, Opus fine" is inexpressible, and a note written from the template cannot pass `specguard --check-note` (no dedicated per-model lines). Not ordered in this patch; needs an Owner decision on split reporting.
2. **Credit-Aware Routing lives only in the FOR-CLAUDE package** — the SPEC now logs it (v4.1.4 row) but does not mirror the section body; the SPEC stays silent on thresholds, the standing order, and the reset.
3. **SPEC team table (L48–52)** still uses pre-split phrasing ("Claude Code (Opus/Fable)", "Claude Code + Opus 5") — not ordered; now stylistically inconsistent with the rebound Hard Rule 1 and routing table.
4. **v4.1.5 condensation drops** flagged last cycle remain unrestored in FOR-CLAUDE (UNVERIFIED→verified promotion path owner, "raise an Issue" on 3 fails, "never an authority", non-significant carve-out, worktrees/Grok-Build bridge as shared infra) — not ordered.
5. **Write-safety auditability**: Hard Rules 1/2/4 remain honor-system (no write-ledger, no actor/model attribution on writes).
6. **Self-test pass criteria and the 3-fail counter scope** remain undefined in both docs.
7. **Grok "low" is unquantified**, so the CONSERVE_BOTH trigger stays a judgement call; the reset moment is transcribed from the Owner directive, not verified against the provider UI.
8. **Heuristic advisories**: Hierarchy (FOR-CLAUDE) and Layers (SPEC) unattributed in history — keyword-heuristic noise, listed for completeness.
9. **Deferred by directive, unchanged**: Event Bus duplicate-collapse rule (Phase 2); Grok Bot Layer (deferred, not cancelled).

## Lesson written (process defect this patch exposed)

**L-20260817-04** — Multi-file source-of-truth drift: the FOR-CLAUDE package advanced two versions (v4.1.4, v4.1.5) while the SPEC sat at v4.1.3, and nothing flagged the divergence until a manual review. Every version row must land in every file of the package in the same patch; a cross-file version-sync check belongs in specguard (proposed, not built — out of scope this cycle). Corollary fixed this cycle: the "(this document)" marker placed before the em dash made the newest history row invisible to the numbering check — the newest row is exactly the one that must be machine-checked.

## v4.1.7 addendum (2026-08-17, storage promotion)

- ADDED: "## Durable storage rule" section in SYSTEM-CURRENT.md and SYSTEM-SPEC-CURRENT.md (AUTONOMY-SYSTEM shared durable home; product-local staging temporary; runs incomplete until artifacts promoted; superseded files to delete-me/). Logged as v4.1.7 history rows in both files — no unattributed sections (L-20260817-01), no package drift (L-20260817-04).
- Open items: all 9 v4.1.6 items above stand unchanged; plus specguard still lacks a cross-file version-sync check.

## v4.1.8 addendum (2026-08-17, git + Actions wiring)

- ADDED: "## Shared visibility + version control" section in both SYSTEM docs (GitHub repo `autonomy-system` canonical; Drive folder 1E-0tL4DGXk-HVYNlWUc6ccF6SzZh60OE shared mirror; run incomplete until commit+tag, Drive sync, and SHA+link in Summary Report; no secrets in repo). Logged as v4.1.8 rows in both files.
- ADDED: .github/workflows/sync-docs-to-drive.yml + tools/drive_sync.py (upsert docs/ to the Drive folder; fails with BLOCKED_ON_OWNER_SECRETS message until GOOGLE_SERVICE_ACCOUNT_JSON secret exists). Repo README carries the service-account setup steps.
- Open items: all prior items stand; Actions sync BLOCKED_ON_OWNER_SECRETS until the Owner creates the Google service account + GitHub secret.

## v4.1.9 addendum (2026-08-17, SPEC credit-body mirror)

**What changed**

- ADDED: full `## Credit-Aware Routing (browser checks)` section in SYSTEM-SPEC-CURRENT.md (58 lines, inserted between `## Model Routing` and `## Deferred` — the position analogous to where the FOR-CLAUDE package carries it, and never after Version History). Substance mirrored from SYSTEM-CURRENT.md: CREDIT-CHECK note posted by Cowork to the Event Bus as UNVERIFIED, both threshold tables, the full seven-value Recommendation enum `[NORMAL | CONSERVE_CLAUDE | CLAUDE_CRITICAL | CONSERVE_GROK | GROK_DOWN | CONSERVE_BOTH | UNKNOWN]`, the six Grok Build delegation strategies (volume/critique/planning offload to the Grok stack, batch don't stream, verify-before-apply, fail soft), the standing order for Cowork, and the weekly reset "Sunday 9:00 PM America/New_York" at all four in-section sites, byte-identical to the FOR-CLAUDE rendering.
- ADDED: v4.1.9 history rows in BOTH package files in the same patch (L-20260817-04). "(this document)" moved from the v4.1.8 row to the v4.1.9 row in each file — after the em dash, so the newest row still parses (one marker per file, verified).
- UNCHANGED: SYSTEM-CURRENT.md keeps its Credit-Aware Routing section and every other body section byte-identical; its only edit is the two history lines. No architecture change, no Grok Bot activation, no Event Bus collapse rule invented.
- FOLLOW-UP (same cycle, second commit): title headers bumped to v4.1.9 in both files (SPEC title + intro line, FOR-CLAUDE title). The patch unit bumped history rows but not titles; the Fable gate greps also missed it — caught at Drive-mirror verification. specguard has no title-vs-history check; candidate for the cross-file sync check (open item 2).
- Voice-only adaptations (SPEC style, no substance change): prose intro instead of a `### Purpose` heading; "Snapshot → Verify → Rollback" written in full in delegation strategy 1 where the FOR-CLAUDE copy abbreviates it to "Snapshot → Rollback" (same gate, and the SPEC's established phrasing); "below 5% remaining" for "< 5% remaining" in the standing order.

**Why**

Open item 2 from the v4.1.6 patch — Credit-Aware Routing lived only in the FOR-CLAUDE package while the SPEC logged it in history (v4.1.4 row) and stayed silent on thresholds, the standing order, and the reset. Root cause is L-20260817-04 (multi-file source-of-truth drift): every version row must land in every package file in the same patch. This cycle also shows the sharper form of that defect — a *body section* can be missing from a sibling file while both files lint clean, which is why L-20260817-06 was written.

**specguard evidence (before → after)**

- SYSTEM-SPEC-CURRENT.md: **2 findings [0 FAIL, 2 ADVISORY] → 1 [0 FAIL, 1 ADVISORY]**. `credit-section-missing` cleared; mode/enum checks now actually run on the SPEC and pass (enum 7/7 against declared threshold modes, identical set and spelling to SYSTEM-CURRENT). Remaining: the pre-existing `section-not-in-history` advisory on 'Layers' (keyword heuristic, unchanged). Version run parses v1 → v4.1.9 contiguously.
- SYSTEM-CURRENT.md: **3 findings [2 FAIL, 1 ADVISORY] → 3 [2 FAIL, 1 ADVISORY]** — identical baseline and after (the two `model-budget-collapsed` FAILs on the pooled template line and the pooled threshold heading, plus the 'Hierarchy' advisory). No new failures. Version run parses v1 → v4.1.9 contiguously.
- Net: zero new FAILs in either file; one advisory cleared.

**NOTE — pooled Fable/Opus budget (open item 1, deliberately NOT fixed here)**

The mirror faithfully reproduces the pooled wording, so `Claude Fable/Opus weekly: ~XX% used (~YY% remaining)` and `### Claude thresholds (Fable / Opus weekly)` now exist at a **second site** (SPEC) as well as in FOR-CLAUDE. specguard does **not** raise `model-budget-collapsed` on the SPEC copy: `check_model_budget` only runs when the document has an H2 section whose title contains "model split", and the SPEC keeps the Owner model split as an H3 bullet under Layers → Main Coordinator. So the SPEC's pooled line is unlinted, not clean. Accepted residual for this hygiene patch, recorded rather than papered over; fixing it means splitting per-model reporting, which still needs an Owner decision.

## REMAINING OPEN ITEMS after v4.1.9 (not falsely green — these remain)

CLOSED this cycle: v4.1.6 open item 2 (Credit-Aware Routing body missing from the SPEC).

1. **Pooled Fable/Opus budget** — two separately-budgeted models still report as one figure in the CREDIT-CHECK template and the shared threshold table; "Fable exhausted, Opus fine" is inexpressible and a note written from the template cannot pass `specguard --check-note`. Now duplicated at a second site (SPEC) by the v4.1.9 mirror, and unlinted there (see NOTE above). Needs an Owner decision on split reporting; not ordered.
2. **specguard cross-file version-sync check** — still **proposed, not built**. This cycle proves it must also compare *section presence and content* across package files, not just version rows: both files linted clean while the SPEC was missing a 58-line body section (L-20260817-06).
3. **SPEC team table (L48–52)** still uses pre-split phrasing ("Claude Code (Opus/Fable)", "Claude Code + Opus 5") — stylistically inconsistent with the rebound Hard Rule 1 and routing table; not ordered.
4. **v4.1.5 condensation drops** remain unrestored in FOR-CLAUDE (UNVERIFIED→verified promotion path owner, "raise an Issue" on 3 fails, "never an authority", non-significant carve-out, worktrees/Grok-Build bridge as shared infra) — not ordered.
5. **Write-safety auditability**: Hard Rules 1/2/4 remain honor-system (no write-ledger, no actor/model attribution on writes).
6. **Self-test pass criteria and the 3-fail counter scope** remain undefined in both docs.
7. **Grok "low" is unquantified**, so the CONSERVE_BOTH trigger stays a judgement call; the reset moment is transcribed from the Owner directive, not verified against the provider UI. The mirror copies this imprecision into the SPEC unchanged.
8. **Heuristic advisories**: Hierarchy (FOR-CLAUDE) and Layers (SPEC) unattributed in history — keyword-heuristic noise, listed for completeness.
9. **Deferred by directive, unchanged**: Event Bus duplicate-collapse rule (Phase 2, no rule invented here); Grok Bot Layer (deferred, not cancelled, not activated here).
10. ~~Actions sync BLOCKED_ON_OWNER_SECRETS~~ — CLOSED earlier on 2026-08-17, before this patch: the sync-docs-to-drive workflow is LIVE on Owner OAuth (GOOGLE_OAUTH_CLIENT_ID/CLIENT_SECRET/REFRESH_TOKEN repo secrets; Drive-visible create proof SYNC-SMOKE.txt), with the service-account path retained as update-only fallback. Listed because the v4.1.6-era open-items list above still names it; kept here so the closure is on the record, not silently dropped.

## Lesson written this cycle

**L-20260817-06** — A section that exists as a body in one package file but only as a history mention in its sibling is drift the current linter cannot see: specguard lints one file at a time, so the SPEC's missing Credit-Aware Routing body registered only as an ADVISORY while the FOR-CLAUDE copy looked fine. Mirroring must copy substance verbatim (enum tokens, threshold rows, timezone string), not paraphrase, and the proposed cross-file check must compare section presence, not just version rows.

## System health smoke — 2026-08-17

retrieval_ref `LM-RET-2026-08-17T23:12Z-C` (orchestration-memory@81a2c4cbccb1, repo@48559ee, SYSTEM-CURRENT L10/L96–100, PATCH-NOTES tail) — Fable gate, echoed by Opus unit.

- [x] GitHub canonical readable — ls-remote HEAD 48559ee from cloud sandbox 23:12Z; push was proxy-blocked at run start (session source grant pending); actual push result = this commit's own presence on main
- [x] Drive mirror reachable — folder 1E-0tL4DGXk-HVYNlWUc6ccF6SzZh60OE, PATCH-NOTES-CURRENT.md (10roA9WnUm17NL22cmONJKsnFT4L9EZS2) modified 2026-08-17T23:00:06Z
- [x] Actions sync path present — sync-docs-to-drive.yml (push:main, paths docs/**), last green run 32077957124; THIS run's outcome goes in the Summary Report, not pre-claimed here
- [x] Fable/Opus routing stated — SYSTEM-CURRENT hierarchy L10 + routing table L96–100 (role-based split)
- [x] Grok Heavy critique path exercised — grok.com "Heavy — Team of Experts · Grok 4.5", chat "Smoke Path Risks and Fragile Claims" in Owner's Grok history, 9 bullets received, 3 applied
- [x] Open items still listed bluntly — v4.1.9's REMAINING OPEN ITEMS list (10 items) above stands unchanged; none closed, none added, by this smoke

Routing this smoke: Fable gated/routed only; one Opus unit executed (one infra bounce); one Grok Heavy critique call.
