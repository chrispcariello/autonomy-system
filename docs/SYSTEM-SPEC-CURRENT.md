# AUTONOMOUS MULTI-AGENT SYSTEM — SPECIFICATION v4.1.7
**Date:** 2026-08-17  
v4.1.7 adds the Durable storage rule (shared durable home AUTONOMY-SYSTEM); v4.1.6 was the hygiene patch (history completed, Fable/Opus alignment, reset timezone).

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
- **v4.1.7** — (this document) ADDED: Durable storage rule (AUTONOMY-SYSTEM shared durable home; product-local staging is temporary; runs incomplete until artifacts promoted; superseded files to delete-me/)
