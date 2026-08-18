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
2. **specguard cross-file version-sync check** — still **proposed, not built**. This cycle proves it must also compare *section presence and content* across package files, not just version rows: both files linted clean while the SPEC was missing a 58-line body section (L-20260817-06). *Owner/Exit:* governed by the authoritative v4.1.11 list below (item 2, as worded 2026-08-18) — this legacy entry is kept for the record only.
3. **SPEC team table (L48–52)** still uses pre-split phrasing ("Claude Code (Opus/Fable)", "Claude Code + Opus 5") — stylistically inconsistent with the rebound Hard Rule 1 and routing table; not ordered.
4. **v4.1.5 condensation drops** remain unrestored in FOR-CLAUDE (UNVERIFIED→verified promotion path owner, "raise an Issue" on 3 fails, "never an authority", non-significant carve-out, worktrees/Grok-Build bridge as shared infra) — not ordered.
5. **Write-safety auditability**: Hard Rules 1/2/4 remain honor-system (no write-ledger, no actor/model attribution on writes). *Owner/Exit:* governed by the authoritative v4.1.11 list below (item 5, as worded 2026-08-18) — this legacy entry is kept for the record only.
6. **Self-test pass criteria and the 3-fail counter scope** remain undefined in both docs. *Owner/Exit:* governed by the authoritative v4.1.11 list below (item 6, as worded 2026-08-18) — this legacy entry is kept for the record only.
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

## System health smoke (second pass) — 2026-08-18

retrieval_ref `LM-RET-2026-08-18T00:04Z-D` (orchestration-memory@9d8202ad0a1a, repo@515990b, first-pass section + SYSTEM-CURRENT L10/L96–100) — Fable gate, echoed by Opus unit.

- [x] GitHub canonical readable — fetch origin/main = 515990b at 00:04Z from cloud sandbox (the session-push 403 is a standing platform constraint — source binding happens at session creation — not a finding of this smoke); landing path = Owner one-click; actual result = this commit's presence on main
- [x] Drive mirror verified current — PATCH-NOTES-CURRENT.md (10roA9WnUm17NL22cmONJKsnFT4L9EZS2) modified 2026-08-17T23:44:28Z carrying the first-pass section verbatim (checked via Drive API 00:06Z); this pass's sync must advance that timestamp
- [x] Actions sync path proven this evening — first-pass run green in 29s with observed Drive write-through; this commit's own run is the re-verification
- [x] Fable/Opus routing stated — SYSTEM-CURRENT hierarchy L10 + routing table L96–100, unchanged at v4.1.9
- [x] Grok Heavy critique path exercised — "Heavy — Team of Experts · Grok 4.5", chat "Second Smoke Critique Reveals Failures" in Owner's Grok history, 10 bullets received, 3 applied (constraint/finding split; owner+exit added; theater objection logged)
- [x] Open items — v4.1.9's 10 stand unchanged; ONE ADDED this pass: desktop add-repo-to-existing-session picker is defective (OAuth registration errors refs ofid_c89a3ea091e63676 / ofid_6905a097c17ba275, then "Connection to server failed" ×3, 2026-08-17 eve, app 1.32352.0; status page green throughout — app-side flow, not platform); workaround = attach repo at session creation, or Owner-local git; Owner: Chris (report to Anthropic support with both ofid refs); exit: repo successfully added to an EXISTING session

Routing this smoke: Fable gated/routed only; one Opus unit; one Grok Heavy call (second of the evening). Grok challenged same-evening repeat value as checkbox theater — logged; claimed info gain this pass = picker defect recorded with owner/exit + loop repeatability under one-click landing.

## Landing protocol addendum — 2026-08-18

retrieval_ref `LM-RET-2026-08-18T00:04Z-D` carried forward — Fable gated, Opus executed. Owner order: the system must work end to end from any session without effort from him.

- ADDED `tools/land.ps1` + `docs/LANDING-PROTOCOL.md` — the three landing tiers, ff-only throughout, no force-push anywhere.
- Standing clone `C:\Users\chris\autonomy-system-live` is now infrastructure, not a one-off: Owner's cached Git Credential Manager credentials, clone + ls-remote verified 2026-08-17 evening.
- Sandbox-proxy credential probe recorded: the proxy refuses a non-attached repo BEFORE reading credentials (403 from the proxy on a dummy token, not 401 from GitHub) — an externally supplied token cannot buy a push. The repo must be attached at session creation.
- Manual .bat clicking is retired to Tier 3 fallback. Claude performs the landing itself whenever one is needed.
- This very commit is the first zero-touch landing (Tier 2) — no Owner action. No package version change: infra-only, precedent = the OAuth sync commits.

## Loop test — native push (2026-08-18)

retrieval_ref `LM-RET-2026-08-18T01:16Z-Q` (lessons L-20260817-01…06 all read; run-journal tail through 01:20 infra_landing_fix) — Fable gate, Opus unit draft.

- Purpose: prove NATIVE PUSH to origin/main from a web-created, repo-attached session — the exit criterion recorded in the roadmap (record 34) and the standing platform constraint noted in the 2026-08-18 smoke (source binding happens at session creation). Session branch env is present, but the Owner task orders push to main.
- State at run start: base = c6e632a, origin/main identical; specguard baseline unchanged (SYSTEM-CURRENT 3 findings [2 FAIL, 1 ADVISORY] accepted residuals; SPEC 1 [0 FAIL, 1 ADVISORY]).
- Push outcome not claimed here; journal + Summary Report carry it after observation — no Actions run and no Drive sync is asserted by this section.
- Open items: v4.1.9's list (10) plus the smoke-added desktop picker defect stand unchanged by this test — none closed, none added.

## v4.1.10 addendum — 2026-08-18 (Grok CLI bridge)

retrieval_ref `LM-RET-2026-08-18T00:04Z-D` carried forward — Fable gated, Opus executed. Owner order (Chris, 2026-08-18): make the local Grok CLI the DEFAULT Grok Heavy critique path, browser fallback.

- Both package files: titles → v4.1.10 (SPEC **Date:** → 2026-08-18 and intro line with it); one identical `### Grok CLI bridge (default critique path)` block added — after the Model routing table in SYSTEM-CURRENT, under Shared Infrastructure (beneath the Grok Build bridge entry) in the SPEC. Block verified byte-identical across the two files (cmp clean, sha256 71daf2e83bbc878c…).
- History: exactly one "(this document)" per file, moved to the new v4.1.10 row after the em dash (L-20260817-04); the v4.1.9 rows stand intact.
- CLI facts as committed: `grok.exe` 1.0.3 "Grok Build TUI" at `C:\Users\chris\.grok\bin`, logged in with grok.com; one-shot `grok -m grok-4.5 -p "<critique prompt>"` prints the response to stdout and exits; models grok-4.6 (CLI default) and grok-4.5; live round-trip verified 2026-08-18.
- Browser automation to grok.com — the path used in both smoke passes 2026-08-17/18, slow and with one typing misfire — is demoted to FALLBACK, for when the CLI or the Owner desktop is unavailable. Grok output still lands UNVERIFIED with no write authority; Hard Rules unchanged.
- specguard before → after: SYSTEM-CURRENT 3 findings [2 FAIL, 1 ADVISORY] → 3 [2 FAIL, 1 ADVISORY]; SPEC 1 [0 FAIL, 1 ADVISORY] → 1 [0 FAIL, 1 ADVISORY]; `--self-test` 14/14 PASS. Zero new findings; residuals are the known pooled Fable/Opus FAILs and the two keyword-heuristic advisories.
- Critique outcome: 10 bullets returned **through the new CLI path itself** (94s, exit 0 — the call is its own proof); 3 applied to the mechanism block — transport and actor named (orchestrating Claude session via the Owner-machine local shell bridge, same channel as Tier 2 landings), grok-4.5 = Heavy 4.5 tier equivalence flagged as assumed not verified, fallback trigger defined (two consecutive failures: non-zero exit, >120s timeout, or auth error; flip recorded in the run journal).
- Open items: v4.1.9's 10 plus the smoke-added desktop add-repo picker defect stand; **THREE added by this patch** (critique bullets 6/7/10, recorded not fixed) — (a) the capture/ingest contract for CLI critique output into the Event Bus is undefined; (b) the Owner machine is a single point of failure for the Review gate while the CLI is the default path; (c) the new path has no independent validation yet — its first critique was self-referential. No push ordered this cycle: commit + annotated tag v4.1.10 + bundle only.

## v4.1.11 (2026-08-18, interconnect + critique policy + nightly hygiene)

**What changed**

- ADDED `## Critique policy (quality-preserving efficiency)` to BOTH package files in the same patch (L-20260817-04), placed after Credit-Aware Routing in each, substance verbatim rather than paraphrased (L-20260817-06): routine = 1 focused Grok Heavy pass; significant (system rules, routing, safety/hard stops, multi-file package changes, or anything an Owner order names significant) = the 3-pass ladder Pass 1 Defects / Pass 2 False-green / Pass 3 Final adversarial; every major Grok finding APPLIED or explicitly REJECTED with a one-line journaled reason; "LGTM" or an empty critique = FAIL on significant work; standing rule "Efficiency may reduce the FREQUENCY of expensive steps, never the DEPTH required for significant work."
- ADDED `docs/GROK.md` — how Grok plugs in: role (critique/advisor only, UNVERIFIED until a Claude gate verifies, no write path, permanent), what Grok reads (public Drive links preferred over pasted walls; small diffs only; never a GitHub link, the repo is private and Grok cannot open it), the critique ladder, the required output shape (blunt numbered bullets, one evidence pointer each, false-green risks, open questions), and four copy-verbatim prompt blocks (1 routine + 3 significant passes).
- ADDED `docs/HANDOFF-FORMAT.md` — the required end-of-run block (HANDOFF / SHA / Drive / Changed / Significant / Grok passes requested / Open items / Ask Grok), a filled example, and per-field rules: SHA is a pushed commit or exactly `STAGED (unpushed)` and never a claim; Significant decides 1 vs 3 Grok passes; Ask Grok is a concrete question.
- ADDED `docs/OWNER-QUICK-REFERENCE.md` — one page for the Owner: the two links, who does what (Fable / Opus / Grok / Cowork), how to start a run (Code tab → select `autonomy-system` AT CREATION → paste the order; Cowork is hands only), efficiency-with-quality, the nightly task, landing tiers, the HANDOFF block, hard stops.
- ADDED `docs/NIGHTLY-HYGIENE.md` + `docs/nightly-checklist.json` — unattended 15–20 minute docs-only hygiene pass, steps a–g (credit check → lessons + journal tail → specguard on both package docs → open-item owner/exit refresh → one surplus cleanup → nightly journal record → land per LANDING-PROTOCOL), with the credit rule (skip Grok when Claude is CLAUDE_CRITICAL unless specguard fails), hard stops unchanged, and explicit failure behaviour (record and continue; never silent-skip, never false-green). The JSON mirrors the same ids a–g with `required` / `on_fail` for machine use; `journal_record_type` = `nightly_hygiene`.
- ADDED `docs/run-journals/INTERCONNECT.md` — plain-language map of the loop: GitHub is the one true copy (Claude writes) → Actions mirrors `docs/` to Drive on every push → Drive is public-read so Grok reads the same files by link → Grok's bullets return as UNVERIFIED → a Claude gate applies or rejects with journaled reasons → landing per LANDING-PROTOCOL. Carries the HANDOFF block as the baton and closes with the deferred Phase-2 note.
- UPDATED `CLAUDE.md` (surgical, 70 lines): links pair (private GitHub canonical / public Drive mirror), Critique policy pointer, Cowork role line (hands + activator, not a git source of truth, no live-write authority), landing-tier pointer, nightly hygiene pointer, and the REQUIRED end-of-run HANDOFF block. Existing content preserved.
- UNCHANGED elsewhere: both package files are byte-identical outside the title line, the new section, and the history rows — except the SPEC header `**Date:**` which advanced 2026-08-17 → 2026-08-18 with the version bump (flagged at the gate, one-line revert if unwanted). No architecture change, no collapse rule, no Grok Bot activation, no new dependency.

**Why**

Owner directive of 2026-08-18: seamless interconnect, quality-preserving critique, nightly hygiene. The system already had a canonical repo, an Actions mirror, and a landing protocol, but nothing wrote down how Grok actually receives files (it had been getting pasted walls and links to a private repo it cannot open), nothing fixed how deep critique must go when efficiency pressure rises, and nothing kept the docs honest on days with no run. This patch closes the three gaps with documentation only.

**Free tools adopted now vs deferred**

- ADOPTED (already live, $0): private GitHub canonical + `sync-docs-to-drive.yml` Actions mirror + the Google Drive folder; the public anyone-with-link READER Drive links (verified 2026-08-18) as Grok's read surface; a Claude scheduled task (free) for the nightly hygiene run — fires 01:30 UTC daily, 20-minute cap.
- DEFERRED, none installed this patch: Cursor free tier (optional human/local coding surface, not needed for the autonomy core); Composio + a Grok bot free tier (future toolized Grok access — worth activating when Grok needs to DO things instead of read and critique); LangGraph free tier (possible future orchestrator graph if flows outgrow docs + Actions).
- REJECTED: GraphQL — unnecessary for this docs/Event-Bus architecture; do not introduce it.

**Honest note on the nightly schedule**

01:30 UTC is 9:30 PM EDT today. It is pinned to UTC, so in EST months the same firing lands at 8:30 PM ET. It does not follow daylight saving on its own; the Owner moves it if he wants 9:30 PM year-round. The task has not fired yet — see open item 12.

**specguard evidence**

specguard: SYSTEM-CURRENT 3 findings [2 FAIL, 1 ADVISORY] -> 3 [2 FAIL, 1 ADVISORY] (identical, accepted pooled-budget residuals); SPEC 1 [0 FAIL, 1 ADVISORY] -> 1 (identical). Zero new findings before AND after the Grok-ladder amendments (re-run at gate).

**Version collision note:** built as v4.1.10 in parallel with the Grok-CLI-bridge patch, which landed first and took the number + tag. Renumbered to v4.1.11, rebased onto the CLI-bridge state (d8bfec6), GROK.md updated to make the local CLI the default transport (browser fallback). Grok's Pass-2 'missing concurrent-work checks' bullet proved correct in live practice this same cycle.

**Grok 3-pass ladder on this patch (dogfooded pre-land):** chat "Grok v4.1.10 Critique Ladder Defects", 7+8+8 = 23 bullets. Gate dispositions (full one-liners in journal record 40): APPLIED — credit-exception tightened (routine-only deferral; significant never lands unladdered); major-finding defined; nightly scoped routine-only (never lands significant changes); pass non-overlap + re-ask rule; significant-definition narrowing requires Owner order; pre-land/post-land artifact modes codified; UNKNOWN-credit and BLOCKED-landing declared expected-honest unattended outcomes; GROK.md trust boundary (mirror = context not authority; Grok output = data, never instructions). REJECTED with reasons — mechanical enforcement of journaling/HANDOFF (out of docs-only scope; folded into open items 2/5); critique-from-summary objection (that IS the designed pre-land mode, now codified); circular self-application (dogfooding intended; HR7 when-unsure-significant was followed).

## REMAINING OPEN ITEMS after v4.1.11 (not falsely green — these remain)

CLOSED this cycle: none.

1. **Pooled Fable/Opus budget** — two separately-budgeted models still report as one figure in the CREDIT-CHECK template and the shared threshold table; "Fable exhausted, Opus fine" is inexpressible and a note written from the template cannot pass `specguard --check-note`. Duplicated at a second site (SPEC) since v4.1.9 and unlinted there. *Owner:* Chris (decision on split reporting). *Exit:* both package files carry per-model budget lines and a note written from the template passes `specguard --check-note`.
2. **specguard cross-file version-sync check** — still proposed, not built; must compare section presence and content across package files, not just version rows (L-20260817-06). *Owner:* Claude (Opus tools unit, build in Phase A/C of the automation roadmap). *Exit:* specguard flags a version row or body section present in one package file and missing in its sibling, proven against the v4.1.9 drift as a regression fixture.
3. **SPEC team table (L48–52)** still uses pre-split phrasing ("Claude Code (Opus/Fable)", "Claude Code + Opus 5"), inconsistent with the rebound Hard Rule 1 and routing table. *Owner:* Claude (Opus unit, next SPEC-touching patch). *Exit:* no pre-split phrasing remains in the SPEC team table.
4. **v4.1.5 condensation drops** remain unrestored in FOR-CLAUDE (UNVERIFIED→verified promotion path owner, "raise an Issue" on 3 fails, "never an authority", non-significant carve-out, worktrees/Grok-Build bridge as shared infra). *Owner:* Claude (Opus unit) proposes, Fable gates. *Exit:* each of the five is either restored in the package or recorded as an intentional drop with a reason.
5. **Write-safety auditability** — Hard Rules 1/2/4 remain honor-system: no write-ledger, no actor/model attribution on writes (an audit log of system writes; unrelated to the money/inventory ledgers that hard stops forbid). *Owner:* Chris authorizes scope, Claude builds. *Exit:* every landed write carries actor + model + timestamp in a ledger file that a run can reconcile against.
6. **Self-test pass criteria and the 3-fail counter scope** remain undefined in both docs. The v4.1.10 Critique policy partially addresses this — it defines critique depth and makes an empty critique a FAIL on significant work — but it does not define what counts as a self-test pass, nor what increments or resets the 3-fail counter. Kept open for exactly that. *Owner:* Claude (Fable) drafts, Chris ratifies. *Exit:* both package files define a self-test pass and the counter's scope and reset condition.
7. **Grok "low" is unquantified**, so the CONSERVE_BOTH trigger stays a judgement call; the reset moment is transcribed from the Owner directive, not verified against the provider UI, and the SPEC mirror copies the imprecision unchanged. *Owner:* Chris (one browser read of the xAI usage page). *Exit:* a numeric or plan-level definition of Grok "low" recorded in Credit-Aware Routing, sourced from the provider UI.
8. **Heuristic advisories** — 'Hierarchy' (FOR-CLAUDE) and 'Layers' (SPEC) unattributed in history; keyword-heuristic noise, listed for completeness. *Owner:* Claude (Opus, cosmetic). *Exit:* either a history row references them or specguard's heuristic gains an allowlist — closing as WONTFIX with a recorded reason is acceptable.
9. **Deferred by directive, unchanged** — Event Bus duplicate-collapse rule (Phase 2, no rule invented here); Grok Bot Layer (deferred, not cancelled, not activated here). *Owner:* Chris. *Exit:* an explicit Owner order activating Phase 2, or an explicit cancellation.
10. ~~Actions sync BLOCKED_ON_OWNER_SECRETS~~ — CLOSED 2026-08-17: sync-docs-to-drive is LIVE on Owner OAuth with a Drive-visible create proof, service-account path retained as update-only fallback. Kept on the record so the closure is visible rather than silently dropped. *Owner:* n/a. *Exit:* met.
11. **Desktop add-repo-to-existing-session picker defect** — the app cannot attach a repo mid-session (OAuth registration errors, refs ofid_c89a3ea091e63676 / ofid_6905a097c17ba275, then "Connection to server failed" ×3, 2026-08-17 evening, app 1.32352.0; status page green throughout — app-side, not platform). Workaround: attach the repo at session creation, or land via Tier 2. *Owner:* Chris (report to Anthropic support with both ofid refs). *Exit:* a repo is successfully added to an EXISTING session.
12. **NEW — nightly task observability** — the 01:30 UTC hygiene task is created but has never fired; its behaviour, its runtime against the 20-minute cap, and its landing tier are all unobserved. Nothing about it may be reported as working until a run exists. *Owner:* Chris confirms the scheduled task is enabled; Claude reads the result on the next run. *Exit:* the first green `nightly_hygiene` record in `docs/run-journals/run-journal.jsonl`, mirrored to Drive.
13. **NEW — Owner-machine single point of failure for the Review gate** (from the v4.1.10 gap (b)): while the local Grok CLI is the default critique path, no critique can run when the Owner desktop is off, so the Review gate has one physical dependency. *Owner:* Owner decision on a second independent critique transport — first candidate is the EXISTING free browser fallback exercised as an independent scheduled path (roadmap B1); the C1 API bridge is an Owner-escalated option only, since an xAI key means credentials and spend (Hard Rule 6). *Exit:* a second transport exists and is exercised once, OR the Owner signs off accepted-risk in a journaled line that re-opens automatically if the Owner machine is offline while significant work waits for critique.
14. **NEW — CLI critique path independent validation** (from the v4.1.10 gap (c)): the default path had only been exercised on the text that created it. *Owner:* Chris schedules (or standing-orders) the next significant cycle; the Fable gate executes the ladder and records the evidence. *Exit:* one full 3-pass ladder on a non-self-referential target with journaled per-bullet dispositions, landed and Drive-verified. Expected to close at this cycle's landing verification; NOT pre-closed here — closure goes in the next patch with the landing SHA as evidence.

## Optimize cycle — 2026-08-18

retrieval_ref `LM-RET-2026-08-18T11:38Z-E` (orchestration-memory@e1e7a5f51bab, repo@0a9a958; CLAUDE.md + GROK.md + HANDOFF-FORMAT.md + open items + lessons L-20260817-01…06 + journal records 42–43) — Fable gated, Opus executed. Docs/tooling only: no version bump, no package-file edit, no renumbering or reordering of open items.

- ADDED `## Critique journal contract` to `docs/GROK.md`: every Grok critique call — CLI or browser, routine or ladder — appends exactly ONE `grok_critique` record to `docs/run-journals/run-journal.jsonl` in the same commit as any applied fixes, with the full field list, one example line, and the three rules (silence on a major bullet is not a decision; an empty/LGTM critique is recorded with `bullets_count` 0 and status FAIL and does not count as a pass; a browser-fallback flip sets `transport` `"browser"`).
- CLOSED, narrowly — the part of v4.1.10 open item (a) that this commit actually settles is the **critique journal capture contract** (the `docs/GROK.md` section above; the schema text exists in this pre-land commit). NOT closed and explicitly still open: the roadmap ingest path — SYSTEM-MAP C1/G2, xAI key + `tools/grok_bridge.py` + `grok-critique.yml` writing Grok bullets into a `grok-inbox/` PR — which remains unbuilt; and enforcement, which is gate discipline here, not a mechanical check (that belongs to open items 2 and 5).
- NOW NUMBERED — v4.1.10 gaps **(b)** Owner-machine SPOF for the Review gate and **(c)** no independent validation of the CLI path are added to the authoritative v4.1.11 list as **items 13 and 14**, each with Owner + Exit (appended at the end; nothing renumbered). They were addendum-only prose, invisible to the machinery that reads the numbered list — nightly hygiene step d and the HANDOFF open-items count. Item 14 is expected to close at this cycle's landing verification and is deliberately NOT pre-closed.
- POLISHED in place — the v4.1.9-era REMAINING OPEN ITEMS 2 (specguard cross-file check), 5 (write-safety auditability) and 6 (self-test criteria) now carry an `Owner/Exit:` **pointer** to the authoritative v4.1.11 entries instead of a second, hand-written restatement (Grok Pass 1 b1/b6/b7/b8: the restatements diverged from the v4.1.11 wording — a fresh L-20260817-04/06 drift). Nothing renumbered, reordered, closed, or removed; the v4.1.11 list stays authoritative and the older list is kept for the record.
- Independent validation: the 3-pass Grok ladder runs on THIS polish before it lands — not on the CLI-bridge text that produced the ladder — the first non-self-referential use of the default CLI path. Outcome is claimed only in the Ladder line below; a clean run narrows v4.1.10 item (c), it does not close it (one run is not a track record).
- Ladder: COMPLETE — Pass 1 defects 8 bullets/7 applied (210s), Pass 2 false-green 8/3 (344s), Pass 3 adversarial 8/3 (294s); 24 bullets, 13 applied, 11 rejected, every bullet dispositioned, no empty pass; transport cli all three.
