# AUTONOMOUS MULTI-AGENT SYSTEM — SPECIFICATION v4.1.10
**Date:** 2026-08-18  
v4.1.10 makes the local Grok CLI the default Grok Heavy critique path (browser grok.com is the fallback); v4.1.9 mirrored the Credit-Aware Routing body into this SPEC; v4.1.8 added Shared visibility + version control (GitHub canonical, Drive mirror); v4.1.7 added the Durable storage rule.

---

## Design Goal
High-autonomy multi-agent system started by Claude Cowork, coordinated by Claude Code (Claude Fable 5 Max/Ultracode orchestrates; Claude Opus 5 Max/Ultracode executes all other Claude work), running a continuous timed loop with critique, learning, and mandatory surplus improvement.

---

## Layers

### Owner
- **Sets run duration**
- Defines hard stops
- Final irreversible decisions only

### Claude Cowork — Autonomous Activator / Bootstrapper
Cowork starts the run and does live computer-use that no other surface can do. It is a worker and activator, **never an authority**.

**MAY:**
- Start a run and launch the Main Coordinator (Claude Code)
- Launch the Grok Build bridge as a process
- Operate live browser, desktop, Discord for observation and evidence
- Write to the Event Bus inbox as UNVERIFIED

**MAY NOT:**
- Write, edit, or delete any live system file, ledger, inventory, or order record
- Run terminal commands that mutate live state (including via processes it launched)
- Move money, contact third parties, or handle credentials
- Approve, verify, or promote its own output

Processes Cowork launches inherit this restriction. Launching a writer does not confer the right to write. Any relied-on Cowork action must produce a capturable artifact (URL, screenshot, export).

### Main Coordinator — Claude Code (Fable 5 orchestrates · Opus 5 executes)
- Model split (Owner rule, v4.1.5): Fable 5 Max/Ultracode = highest-level orchestration and final quality gate; Opus 5 Max/Ultracode = all other Claude work. Role-based, not cost-based (Fable is priced higher than Opus on token rates).
- **Sole authority for live system writes**
- Decomposes, routes in parallel, verifies
- Enforces Snapshot → Verify → Rollback before any live write
- Calls Grok Heavy and Grok Build through the bridge
- Promotes verified Event Bus results into Learning Memory or live state

### Five Specialist Teams

| Team | Sub-agents | Models / Tools |
|------|-----------|----------------|
| App | Frontend · Backend · UI/UX · QA · Integration | Claude Code (Opus/Fable) + Grok Build 4.6 · Critique: Grok Heavy 4.5 |
| Web | Design · Content · SEO · Performance | Claude Code (Opus/Fable) + Grok Build 4.6 · Critique: Grok Heavy 4.5 |
| Research | Watcher · Analyst · Source Verification · Market Signal | Claude Cowork (live) + Grok Heavy 4.5 |
| Safety | Snapshot · Rollback · Policy Guard · Test Runner | Claude Code + Opus 5 + Grok Build 4.6 |
| Discovery | Ranker · Opportunity Scout · Surplus/Cleanup · Vision Proposer | Grok Heavy 4.5 + Claude Opus 5 |

Each team runs 3–5 single-responsibility sub-agents. Infrastructure (Event Bus, Learning Memory, Snapshot/Rollback) is **shared** — not owned by Discovery or any single team.

**Per-team inner loop:**  
**Retrieve lessons** → Execute → Self-Test → Grok Heavy 4.5 Critique → Collaborate → Improve → Lesson to Learning Memory

### Shared Infrastructure
- **Event Bus** — results land as UNVERIFIED first. Retention: keep all records for the current project indefinitely unless the Owner authorizes pruning; never auto-delete UNVERIFIED or rejected notes within an active run. **Collapse rule (duplicates):** not defined yet. Keep-everything is correct while the Grok Bot layer is deferred. Decide a collapse/dedupe rule before Phase 2 activation — continuous bots can emit the same finding hourly. Do not invent a collapse rule mid-run.
- **Learning Memory** — written after every pass AND retrieved before every significant task
- Snapshot → Verify → Rollback
- Claude Code worktrees
- Grok Build bridge
- Claude Cowork live surface

### Grok CLI bridge (default critique path)

- **Default:** critique calls run one-shot on the Owner-machine local shell — `grok -m grok-4.5 -p "<critique prompt>"` (CLI model id per `grok models`; grok-4.5 = Heavy 4.5 tier equivalence assumed from the models list, not independently verified) — which prints the response to stdout and exits (Grok Build TUI 1.0.3, `C:\Users\chris\.grok\bin`, logged in with grok.com; live round-trip verified 2026-08-18).
- **Transport & actor:** the orchestrating Claude session (Fable gate surface) invokes the CLI through the Owner-machine local shell bridge — the same proven channel as Tier 2 landings (see docs/LANDING-PROTOCOL.md); prompt text passes as one quoted argument.
- **Volume work** may use `-m grok-4.6` (CLI default model); critique stays on grok-4.5.
- **Fallback:** browser automation to grok.com, triggered when a CLI call fails twice consecutively (non-zero exit, >120s timeout, or auth error); the orchestrator flips the path and records the flip in the run journal.
- Unchanged: Grok output still lands UNVERIFIED and carries no write authority (Hard Rules unchanged).

---

## Definition: "Significant" task (Hard Rule 7)

A task is **significant** if any of the following is true:
1. It can lead to a live write
2. It touches money, legal, ledger, inventory, or order state
3. It spans more than one sub-agent
4. It is the team's first task of the cycle
5. It produces an artifact that other teams will rely on

If none apply, the task is non-significant and retrieval is optional.  
When unsure, treat it as significant.

---

## Continuous Autonomous Loop

1. **Start** — **Owner sets duration**; Cowork activates and launches Claude Code
2. **Assign / Route** — Parallel fan-out. Before significant tasks, retrieve Learning Memory lessons and record the retrieval reference on the task.
3. **Teams Work** — All five teams (parallel where possible); each significant unit begins with retrieval inside the inner loop
4. **Self-Test** — Fail → auto-return to Work. Three consecutive failures stop that thread only and raise an Issue; they do not stop the run.
5. **Review** — Grok Heavy critique (selective on low-risk work)
6. **Learn** — Structured lesson → Learning Memory
7. **Next + Surplus** — ≥1 unrequested improvement required. Discovery owns cleanup via Surplus/Cleanup sub-agent.
8. **Report** — Features · Quality · Issues · Next Steps  
   → time remains: back to step 2  
   → time up: **META-IMPROVEMENT PASS** → END

**Meta-Improvement Pass:**  
The Coordinator critiques the run's *process*, not only its output: routing quality, wasted parallelism, retrieval compliance, surplus quality, recurring self-test failures.  
**Write boundary:** the pass may write to Learning Memory and to documentation only. Any change it proposes to live system behaviour is a normal live write and **must** go through Snapshot → Verify → Rollback. The pass does not bypass Hard Rule 1.

---

## Hard Rules
1. Only Claude Code may perform live system writes (orchestrator model: Fable 5 Max/Ultracode; other Claude work: Opus 5 Max/Ultracode)
2. Cowork holds NO live-write authority of any duration
3. Everything else returns UNVERIFIED results to the Event Bus
4. No live write without Snapshot → Verify → Rollback
5. Owner interrupted only for true hard stops or final irreversible decisions
6. Money, legal, third-party contact, credentials always escalate
7. No significant task starts without a Learning Memory retrieval recorded on the task. A missing retrieval reference is a self-test failure.

---

## Efficiency Rules
1. Parallel fan-out by default
2. Credit + task-type routing
3. Nested sub-agent trees (3–5 per team)
4. Selective critique
5. Learning Memory first
6. Surplus mandatory every cycle
7. Free / already-available orchestration only

---

## Durable storage rule

/root/staging (or any product-local sandbox) is temporary only.
A run is incomplete until final system docs, patch notes, lessons, and run journals are written to AUTONOMY-SYSTEM (shared durable home).
Summary Reports must include the shared path or link to final artifacts.
Superseded files go to AUTONOMY-SYSTEM/delete-me/.

---

## Shared visibility + version control

- Canonical store: private GitHub repo `autonomy-system`
- Shared mirror: Google Drive AUTONOMY-SYSTEM folder for external review
- A run is incomplete until: (1) docs committed + tagged on version change, (2) Drive mirror updated via Actions or explicit sync, (3) Summary Report includes commit SHA and Drive folder link
- /root/staging remains temporary only
- Never commit secrets, OAuth client secrets, service-account keys, or .env files

---

## Model Routing
| Task | Surface | Model |
|------|---------|-------|
| Activation / live observation | Claude Cowork | (Claude model active in the Cowork session; routing is role-based per the v4.1.5 split — cost not guaranteed) |
| Orchestration, verification, live-write authority surface | Claude Code | Claude Fable 5 Max/Ultracode |
| All other Claude work (implementation, revisions, most team tasks) | Claude Code | Claude Opus 5 Max/Ultracode |
| Volume work | Grok Build | Grok Build 4.6 |
| Critique | Grok Heavy | Grok Heavy 4.5 |
| Discovery ranking | Grok Heavy + Claude Code | Grok Heavy 4.5 + Opus 5 |

---

## Credit-Aware Routing (browser checks)

Before multi-step work, Claude Cowork checks **Claude** and **Grok/xAI** usage in the browser so that work can be delegated before a provider is exhausted mid-run. The check is an input to routing, not an authority: Cowork observes and reports, the Coordinator routes.

**Claude weekly reset: Sunday 9:00 PM America/New_York.**

### Who checks
- **Claude Cowork** — primary credit checker (browser computer-use); posts the result to the Event Bus inbox as UNVERIFIED, like any other Cowork observation
- **Claude Code** — requests a Cowork usage check before a long run; never assumes unlimited Claude budget
- **Grok / Grok Build** — receives delegated work when Claude is low; Grok limits still apply where they are known

### How to check (browser)
**Claude:** open the Claude/Anthropic usage or limits page; read weekly Fable 5 and Opus 5 used/remaining.
**Grok/xAI:** open the Grok or xAI account/usage page; read remaining quota for Grok, Grok Heavy, and Grok Build if shown. If only plan-level limits are visible, record that.

**CREDIT-CHECK note format (Event Bus UNVERIFIED):**
```
CREDIT-CHECK [timestamp]
Claude Fable/Opus weekly: ~XX% used (~YY% remaining) · reset Sunday 9:00 PM America/New_York
Grok/xAI: [exact % if found | plan-level only | page not found]
Recommendation: [NORMAL | CONSERVE_CLAUDE | CLAUDE_CRITICAL | CONSERVE_GROK | GROK_DOWN | CONSERVE_BOTH | UNKNOWN]
```
Numbers are never invented. If a figure is unreadable, it is recorded as UNKNOWN.

### Claude thresholds (Fable / Opus weekly)
| Remaining | Mode | Action |
|-----------|------|--------|
| > 20% | NORMAL | Standard routing |
| 5–20% | CONSERVE_CLAUDE | Keep orchestration brief; shift volume → Grok Build; critique → Grok Heavy; avoid long multi-team Claude loops |
| < 5% | CLAUDE_CRITICAL | No new Claude autonomous multi-step runs. Short checks only. Delegate planning, volume, critique, long loops to Grok stack |
| Unknown | UNKNOWN | Treat as CONSERVE_CLAUDE if Owner reported high usage; browser-check before any long Claude run |

### Grok thresholds
| State | Mode | Action |
|-------|------|--------|
| Comfortable headroom | NORMAL | Accept delegated volume + critique |
| Low / near cap | CONSERVE_GROK | Fewer Heavy critiques; smaller Build jobs; return work to Claude only if Claude has headroom |
| Exhausted / unavailable | GROK_DOWN | Claude-only for critical path if Claude has credits; else stop long runs |
| Page unreadable | UNKNOWN | Do not assume unlimited Grok; prefer smaller batches |

**Both low → CONSERVE_BOTH:** stop long autonomous loops; Owner-critical short tasks only; queue the rest until the Claude reset (Sunday 9:00 PM America/New_York) and/or Grok recovery.

### Grok Build delegation strategies (when Claude is low)
1. **Volume offload** — sweeps, bulk edits, drafts → Grok Build; Claude only verifies and applies, under Snapshot → Verify → Rollback
2. **Critique offload** — design and adversarial review → Grok Heavy; routine critique skipped on low-risk docs
3. **Planning offload** — decomposition, options, test design → Grok or Grok Heavy; Claude keeps final verification and the live write
4. **Batch, don’t stream** — one clear package with acceptance criteria per Build job
5. **Verify-before-apply** — Build output is always UNVERIFIED; stage it for after credit recovery if Claude is critical
6. **Fail soft** — if Grok is also low, stop expansion, write a queue list, do not burn the last Claude credits

### Standing order for Cowork
Before any multi-step autonomous run: (1) browser-check Claude weekly Fable/Opus usage, (2) browser-check Grok/xAI usage if reachable, (3) post the CREDIT-CHECK note to the Event Bus as UNVERIFIED, (4) if Claude is below 5% remaining do not start a long Claude loop — prepare Grok handoff packages instead (mode: CLAUDE_CRITICAL), (5) if both providers are low, stop long runs and report (mode: CONSERVE_BOTH), (6) the Claude weekly reset is Sunday 9:00 PM America/New_York.

### What this does not claim
There is no silent mid-call API for exact Claude or Grok percentages. The browser read is the method. If the UI is blocked or has changed, record UNKNOWN (mode: UNKNOWN) and conserve.

---

## Deferred
**Grok Bot Layer (Phase 1 package)** — specified, deferred from core at v4, not cancelled. Activate in Phase 2. Do not delete or treat as superseded.

---

## Version History
- **v1** — ADDED: initial tiered architecture and continuous loop
- **v2** — ADDED: efficiency upgrades, sub-agents, parallel fan-out
- **v3** — ADDED: active Learning Memory, Meta-Improvement, Surplus rule, Grok Bot layer
- **v4** — ADDED: Claude Cowork as Activator. RETAINED: Claude Code sole live-write authority. DEFERRED: Grok Bot layer. REMOVED (regression, later fixed): Meta-Improvement Pass wording, retrieve-before-work, auto-return self-test path, named sub-agent clarity, efficiency section
- **v4.1** — FIXED: Cowork MAY/MAY NOT boundary. RESTORED: Meta-Improvement, retrieval, self-test return, named sub-agents, efficiency rules
- **v4.1.1** — FIXED: defined "significant"; Retrieve in inner loop; bus retention; shared-infrastructure correction. REMOVED (regression): Meta-Improvement write boundary; Owner sets duration from step 1; full version history block
- **v4.1.2** — RESTORED: Meta-Improvement write boundary; Owner sets duration; full version history
- **v4.1.3** — ADDED: Fable cost caveat on the Fable routing row (not only Cowork); Event Bus duplicate-collapse rule explicitly deferred until Phase 2 (keep-everything remains correct until then) (cost caveat superseded at v4.1.5 by the role-based cost note)
- **v4.1.4** — ADDED (FOR-CLAUDE package): Credit-Aware Routing — browser usage checks, Claude/Grok thresholds, Grok Build delegation strategies, Sunday weekly reset, standing order for Cowork. Section lives in the FOR-CLAUDE package; not yet mirrored into this SPEC body
- **v4.1.5** — CHANGED model split: Fable 5 Max/Ultracode = highest-level orchestration; Opus 5 Max/Ultracode = all other Claude work (Owner rule; not cost-based); Hard Rule 1 rebound from 'Claude Code + Opus 5' to the Claude Code surface
- **v4.1.6** — FIXED (hygiene): history completed; Design Goal, Main Coordinator, Hard Rule 1 and Model Routing aligned to the v4.1.5 split; reset timezone America/New_York (in FOR-CLAUDE package)
- **v4.1.7** — ADDED: Durable storage rule (AUTONOMY-SYSTEM shared durable home; product-local staging is temporary; runs incomplete until artifacts promoted; superseded files to delete-me/)
- **v4.1.8** — ADDED: Shared visibility + version control (private GitHub repo autonomy-system is canonical; Drive AUTONOMY-SYSTEM folder is the shared mirror; commit + tag on version change; Drive mirror updated via Actions or explicit sync; Summary Reports carry commit SHA + Drive link; never commit secrets)
- **v4.1.9** — ADDED: Credit-Aware Routing body mirrored from the FOR-CLAUDE package (was history-only in this SPEC since the v4.1.4 row): CREDIT-CHECK note posted by Cowork to the Event Bus as UNVERIFIED, Claude and Grok threshold modes with the full Recommendation enum, Grok Build delegation strategies, standing order for Cowork, weekly reset Sunday 9:00 PM America/New_York. No substantive rule changes
- **v4.1.10** — (this document) CHANGED: the Grok Heavy critique path now defaults to the local one-shot Grok CLI on the Owner machine (`grok -m grok-4.5 -p "<critique prompt>"`, Grok Build TUI 1.0.3, grok.com login, verified 2026-08-18); volume work may use `-m grok-4.6`; browser grok.com demoted to FALLBACK. Mechanism block mirrored verbatim from the FOR-CLAUDE package into Shared Infrastructure. Grok output still lands UNVERIFIED with no write authority; Hard Rules unchanged
