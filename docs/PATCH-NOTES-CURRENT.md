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
