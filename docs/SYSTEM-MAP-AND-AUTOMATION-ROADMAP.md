# SYSTEM MAP + AUTOMATION ROADMAP — 2026-08-18

retrieval_ref `LM-RET-2026-08-18T00:27Z-P` (orchestration-memory@150de8033090, repo@6320e80, lessons L-20260817-01…06, PATCH-NOTES open items 1–11)
Package version at time of writing: **v4.1.9** (main `6320e80`, tags v4.1.7/v4.1.8/v4.1.9).
Routing note: analysis and synthesis authored at the orchestrator level (Fable) — this is architecture/gating work, not team execution; mechanical state inventory pulled live from the canonical repo before writing.

Owner question this answers: *how does the system work today, and what else is needed for (a) complete automation, (b) Grok integration with easy two-way communication, (c) all files accessible and updateable, (d) the full loop + self-improvement running end-to-end.*

---

## 1. AS-BUILT MAP (what exists and what is proven)

### 1.1 Layers and surfaces

```
OWNER (Chris) — duration, hard stops, irreversible decisions
  │
  ├── CLAUDE COWORK (cloud session + desktop bridge)          [activator/observer]
  │     • drives Owner's Chrome (claude-in-chrome): GCP, GitHub web, Google consent, grok.com
  │     • desktop bridge: Downloads folder, Desktop Commander (host PowerShell/python, his git+GCM)
  │     • Google Drive MCP (read/search/create/trash in Owner's Drive)
  │     • may NOT hold live-write authority (HR2); relays through Owner-side tools
  │
  ├── CLAUDE CODE SESSIONS (cloud, repo attachable at creation)  [live-write authority per HR1]
  │     • Fable = orchestration + gate; Opus subagents = execution units
  │     • repo READ from sandbox proven (ls-remote/fetch in both smoke runs)
  │     • repo PUSH: blocked unless the GitHub source is bound AT SESSION CREATION (see 3.1)
  │
  ├── GROK (Owner's SuperGrok subscription, grok.com)          [critique; UNVERIFIED only]
  │     • Grok Heavy "Team of Experts · Grok 4.5" — exercised twice 2026-08-17/18
  │       ("Smoke Path Risks and Fragile Claims" 9 bullets/3 applied;
  │        "Second Smoke Critique Reveals Failures" 10 bullets/3 applied)
  │     • no API wiring; no file access; browser/paste bridge only
  │
  └── AUTOMATION FABRIC
        • GitHub repo chrispcariello/autonomy-system (PRIVATE) — canonical store
        • GitHub Actions sync-docs-to-drive.yml — push(docs/**) → Drive mirror
        • Google Drive AUTONOMY-SYSTEM folder — shared mirror (currently private to Owner)
        • GitHub secrets: GOOGLE_OAUTH_CLIENT_ID / _SECRET / _REFRESH_TOKEN (owner-auth,
          app published → no 7-day expiry); GOOGLE_SERVICE_ACCOUNT_JSON fallback (update-only)
```

### 1.2 Data flows (arrows = proven direction)

```
Claude session ──edit docs──► repo main ──push──► Actions ──OAuth──► Drive mirror
     ▲                            ▲                                     │
     │ fetch/read (proven)        │ Owner one-click / browser commit    │ read via Drive MCP (proven)
     └────────────────────────────┴──── Owner PC (clone + GCM) ◄────────┘
Grok ◄──paste/browser (manual or Cowork-driven)── Claude/Owner
Grok ──bullets──► Owner/Claude ──apply + commit──► repo   (UNVERIFIED→VERIFIED by gate)
```

### 1.3 Proven-working evidence (all same-day, verifiable)

| Capability | Evidence |
|---|---|
| push → Actions → Drive (create+update) | runs 32077957124 (37s), 32078520555, 32080113097 all green; SYNC-SMOKE.txt created in Drive by OAuth (id 1JO-_5dfA6WLKHx8dhvSbAf60crGFZXqg) |
| Version-bump patch cycle (Opus executes, Fable gates, specguard) | v4.1.9: commits 213916f + 5338d51, tag v4.1.9; SPEC 0 FAIL, enum 7/7, one bounce honestly logged |
| Fresh-session loop run (retrieval → Opus unit → Grok critique → gate → landing) | smoke commits 515990b, 6320e80 (author "Opus Unit"), retrieval_refs C/D recorded |
| Grok Heavy critique with applied output | 9+10 bullets, 3+3 applied, chats in Owner's Grok history |
| Owner-browser automation (GCP, GitHub web, Google OAuth consent) | OAuth client provisioned + app published + consent completed with zero Owner clicks |
| Owner-PC execution (host PowerShell/python, git+GCM, secrets via API sealed-box) | 3 GitHub secrets set HTTP 201; drive_oauth_runner end-to-end |
| Learning Memory + Event Bus discipline | lessons.jsonl L-01…06; run-journal.jsonl 30 records in repo (33 in session master — see gap G3) |
| Spec linting | specguard.py: version-numbering, mode-enum, reset-timezone, model-budget, --check-note, --self-test 14/14 |

### 1.4 The loop (SYSTEM-CURRENT steps 1–8): spec vs. mechanical reality

| Step | Spec | Reality today |
|---|---|---|
| 1 Start | Owner sets duration; Cowork activates | MANUAL — Owner pastes a directive. No scheduled start. |
| 2 Assign/Route | parallel fan-out; retrieval first | WORKING in-session (Agent tool, model:opus; HR7 refs recorded) |
| 3 Teams work | five standing teams | PARTIAL — ad-hoc Opus units, not standing App/Web/Research/Safety/Discovery teams |
| 4 Self-test | fail → auto-return; 3 fails stop thread | WORKING as practice (gate bounces logged); pass criteria still undefined in docs (open item 6) |
| 5 Grok Heavy critique | selective | WORKING via browser/paste; not automated; volume path (Grok Build) unwired |
| 6 Learn | lesson to Learning Memory | WORKING (lessons.jsonl, six lessons) |
| 7 Next + surplus | ≥1 unrequested improvement | PRACTICED (e.g., CLAUDE.md shipped with this analysis) |
| 8 Report / Meta-Improvement | end-of-run pass | PRACTICED manually; not scheduled; no standing cadence |

---

## 2. GAP ANALYSIS — keyed to the Owner's four asks

### G1. "Completely automated"

What's missing, in dependency order:

1. **Native session→repo push** (the root blocker for hands-off loops). Both smoke runs read the repo from the sandbox but hit the push 403; landings needed Owner one-click. Root cause is now understood: **source binding happens at session creation** — the desktop app's add-repo-to-EXISTING-session flow is defective (ofid_c89a3ea091e63676 / ofid_6905a097c17ba275, open item 11), but the web picker attach-at-creation path is verified to attach (autonomy-system@main chip resolves). **Next exit criterion: one session created on web WITH the repo attached that performs a git push from inside the sandbox.** Until that passes, "landing = Owner one-click" is the honest state.
2. **Scheduled runs (loop step 1).** Claude scheduled tasks can fire a standing directive on a cron (e.g., nightly 30-minute cycle) into a fresh session. Requirements: the standing prompt must be fully self-contained, and the firing environment must carry the repo source (test as part of the same exit criterion). Completion notifications (push/email) close the reporting loop without the Owner watching.
3. **CI-enforced self-tests.** specguard runs only when a session remembers to run it. Add a spec-lint workflow job on push(docs/**): report-only at first, fail-closed once stable. Three concrete misses from 2026-08-17 become its test cases: cross-file version sync, cross-file section presence, title-vs-history match.
4. **Session self-configuration.** A repo-root **CLAUDE.md** (shipped alongside this analysis as the cycle's surplus) makes any repo-attached session auto-load the system contract: model split, HR1–7, retrieval discipline, file locations, landing rules, never-commit-secrets. Removes per-run prompt overhead — the standing scheduled directive can shrink to "run one loop cycle per CLAUDE.md."

### G2. "Integrated with Grok / easy communication"

Three bridges, cheapest first (Owner rule: free/already-available tooling preferred):

| Bridge | Cost | Direction | Automation ceiling | Status |
|---|---|---|---|---|
| B1 Browser (grok.com in Owner's Chrome, Cowork-driven or Owner paste) | $0 (SuperGrok already paid) | two-way, manual-ish | needs Owner's Chrome online; brittle UI | **WORKING** — used twice tonight |
| B2 Drive shared links (Grok reads current docs itself) | $0 | one-way (Grok reads) | read-only; needs link-sharing enabled on AUTONOMY-SYSTEM (currently private) | one permission change away |
| B3 xAI API (tools/grok_bridge.py + GROK_API_KEY secret; Actions job posts diffs for critique, lands replies as PRs) | ~$ (xAI API billing is separate from SuperGrok) | two-way, fully headless | full — this is the only bridge that works inside scheduled/CI runs with no human and no desktop | NOT BUILT — needs Owner decision on API spend |

The "easy communication" pattern that fits the spec: **Grok output enters the system only as UNVERIFIED artifacts** — with B3, a `grok-critique` workflow writes Grok's bullets to a branch/PR (`grok-inbox/`), and a Claude session verifies → merges. **PR = UNVERIFIED, merge = VERIFIED** maps the Event Bus state machine onto GitHub natively, keeps HR1 intact (Claude performs the promoting write), and gives Grok a durable, linkable voice in the repo without ever holding write authority.

### G3. "All files accessible and updateable"

Current truth table:

| Actor | Read | Write | Path |
|---|---|---|---|
| Claude Code session (repo attached at creation) | ✅ | ⏳ push pending exit-criterion test | native git |
| Claude Code session (no source) | ✅ (fetch worked) | ❌ 403 by design | Owner one-click relay |
| Cowork session (this one) | ✅ | via relays only (HR2-consistent) | device bridge / browser / Drive MCP |
| Owner PC | ✅ | ✅ | clone + GCM (proven repeatedly) |
| GitHub Actions | ✅ | Drive only (not repo) | OAuth owner-auth |
| Grok | ❌ (private repo + private Drive) | ❌ (by design — permanent) | B1 paste only, today |
| Drive mirror | n/a | auto from repo (one-way, correct) | sync-docs-to-drive |

Fixes: the exit-criterion push test (G1.1) closes the biggest gap; **enabling link-view sharing on the AUTONOMY-SYSTEM folder** closes Grok's read gap for $0 (one Owner nod — it makes the mirror readable to anyone with the link); B3 gives Grok a *voice* (never a pen). Also: the session-master journal currently leads the repo copy (33 vs 30 records) — the catch-up commit accompanying this analysis re-synchronizes them, and the standing rule should be *journal updates ride every landing commit* so the repo copy never lags again.

### G4. "Loop + self-improvement fully working"

Missing pieces beyond G1–G3: (a) define self-test pass criteria + the 3-fail counter scope in the docs (open item 6 — small doc patch, v4.1.10 candidate); (b) give the Meta-Improvement Pass a standing slot (last 5 minutes of every scheduled run: write lesson, update open items, flag one surplus for next run); (c) build the specguard cross-file check (open item 2) so the linter catches the drift class that actually bit twice; (d) the five standing teams stay OUT until run volume justifies them — ad-hoc Opus units are currently the right size (bluntly: standing teams today would be structure theater); (e) Grok Bots + Event Bus collapse rule stay deferred by directive (Phase 2) — activating bots before B3 exists would just amplify the paste bridge's manual load.

---

## 3. ROADMAP — phased, minimal-cost-first

**Phase A — free, this week (mostly one session):**
A1. Exit-criterion test: web-created session WITH repo attached → native push (closes G1.1; also the fix-verification for open item 11's workaround).
A2. CLAUDE.md in repo root (**shipped with this commit** — surplus of this cycle).
A3. spec-lint CI job (report-only) running specguard on both package files.
A4. Journal catch-up + "journal rides every landing" rule (**shipped with this commit**).
A5. Owner nod: link-view sharing on AUTONOMY-SYSTEM folder → Grok can read current docs (B2).
A6. Doc patch v4.1.10: self-test pass criteria + 3-fail scope; SPEC team-table phrasing (open items 3, 6).

**Phase B — free, needs Owner's Chrome online:**
B1. Codify the browser Grok bridge as a procedure doc (prompt template, where bullets land: `docs/grok-inbox/` committed as UNVERIFIED, applied-count recorded) — turns tonight's ad-hoc success into a repeatable step 5.
B2. Scheduled run pilot: one nightly 30-min cycle with a fixed standing directive + completion notification; measure what breaks.

**Phase C — small spend, Owner decision required:**
C1. xAI API key as repo secret + `tools/grok_bridge.py` + `grok-critique.yml` (PR-based UNVERIFIED flow per G2). This is the single change that makes step 5 work headlessly inside scheduled runs.
C2. specguard cross-file checks (version sync, section presence, title-vs-history) + flip spec-lint to fail-closed.

**Phase D — Phase-2 per spec, only after C proves out:**
D1. Grok Bots standing roles (Watcher/Evidence/Cleanup) on the API bridge.
D2. Event Bus duplicate-collapse rule (required before bots emit continuously — currently correctly absent).
D3. Pooled Fable/Opus budget split reporting (open item 1 — needs the Owner's reporting decision first).

## 4. HONEST CONSTRAINTS AND RISKS

1. **Cloud sessions cannot reach the Owner's browser or PC when the desktop app is closed** — any run that needs grok.com-via-Chrome or host git is day-time-only until B3/C1 exists. This is the hard wall between "mostly automated" and "completely automated," and no amount of Claude-side work removes it — only the API bridge does.
2. **Two credentials now underpin the fabric**: the Google OAuth refresh token (GitHub secrets; revocable at myaccount.google.com) and his GCM GitHub token (his PC). Rotation paths exist and are documented; neither ever entered chat.
3. **The desktop add-repo picker defect (open item 11)** is Anthropic-side app behavior; the workaround (attach at creation) is fully in Owner control, but the defect should still be reported with both ofid refs.
4. **Sandbox ↔ repo drift** is the system's recurring failure mode (journal 30 vs 33, lessons 04→06, title-bump miss). Every mitigation in this roadmap (CLAUDE.md, CI lint, journal-rides-every-commit, cross-file checks) is aimed at that one disease.
5. **Grok remains advisory forever** — the design goal is Grok with a durable voice (PRs) and zero authority; nothing in this roadmap gives Grok a write path, deliberately.

## 5. OPEN ITEMS RECONCILIATION (11 → phases)

1 pooled budget → D3 · 2 cross-file specguard → C2 · 3 SPEC team table → A6 · 4 v4.1.5 drops → A6/backlog · 5 write-ledger → C2-adjacent backlog · 6 self-test criteria → A6 · 7 Grok "low" unquantified → C1 (API gives real quota signals) · 8 heuristic advisories → noise, keep listed · 9 collapse rule + Grok Bots deferred → D1/D2 · 10 ~~Actions sync~~ CLOSED 2026-08-17 · 11 desktop picker defect → A1 workaround + Owner support report.

— End. Canonical home: `docs/SYSTEM-MAP-AND-AUTOMATION-ROADMAP.md`; Drive mirror updates automatically on landing.
