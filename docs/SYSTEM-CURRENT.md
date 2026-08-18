# SYSTEM v4.1.10 — PACKAGE FOR CLAUDE

Source of truth for the Autonomous Multi-Agent System.

## Hierarchy

```
OWNER (sets duration · hard stops · final irreversible decisions)
  └── CLAUDE COWORK (Activator — NO live writes of any duration)
        └── MAIN COORDINATOR = Claude Code + Claude Fable 5 Max/Ultracode for highest-level orchestration; Claude Opus 5 Max/Ultracode for remaining Claude work (SOLE live-write authority remains Claude Code)
              ├── App Team (Frontend · Backend · UI/UX · QA · Integration)
              ├── Web Team (Design · Content · SEO · Performance)
              ├── Research Team (Watcher · Analyst · Source Verify · Market)
              ├── Safety Team (Snapshot · Rollback · Policy Guard · Test Runner)
              └── Discovery Team (Ranker · Scout · Surplus/Cleanup · Vision)
                    │
                    └── SHARED (not owned by any one team):
                          Event Bus · Learning Memory · Snapshot/Rollback
                          → Loop → Meta-Improvement Pass → Summary Report
```

## Cowork boundary

**MAY:** start run, launch Claude Code, launch Grok Build process, live observation, write Event Bus as UNVERIFIED

**MAY NOT:** any live system/ledger/inventory write, mutating terminal commands, money, third-party contact, credentials, approve/promote own output

Processes Cowork launches inherit the no-write restriction. Relied-on actions need a capturable artifact.

## "Significant" task (Hard Rule 7)

Significant if any of:
1. Can lead to a live write
2. Touches money / legal / ledger / inventory / orders
3. Spans more than one sub-agent
4. Is the team's first task of the cycle
5. Produces an artifact other teams will rely on

When unsure → significant.

## Continuous loop

1. **Start** — **Owner sets duration**; Cowork activates; launches Claude Code
2. Assign / Route — parallel; Learning Memory retrieval first on significant tasks
3. Teams Work — significant units start with **Retrieve** inside the inner loop
4. Self-Test — fail → auto-return; 3 fails → stop thread only
5. Review — Grok Heavy critique (selective on low-risk)
6. Learn — lesson → Learning Memory
7. Next + Surplus — ≥1 unrequested improvement; Discovery owns cleanup
8. Report → time left: back to 2; time up: **Meta-Improvement Pass** → END

## Meta-Improvement Pass — write boundary

Critiques process only (routing, parallelism, retrieval compliance, surplus quality, self-test failures).  
**May write to Learning Memory and documentation only.**  
Any proposed change to live system behaviour is a normal live write and **must** go through Snapshot → Verify → Rollback. Does not bypass Hard Rule 1.

## Per-team inner loop

**Retrieve lessons** → Execute → Self-Test → Grok Heavy Critique → Collaborate → Improve → Lesson to Learning Memory

## Hard rules

1. Only Claude Code may perform live system writes (orchestrator model: Fable 5 Max/Ultracode; other Claude work: Opus 5 Max/Ultracode)
2. Cowork holds NO live-write authority of any duration
3. Everything else → Event Bus as UNVERIFIED
4. No live write without Snapshot → Verify → Rollback
5. Owner only for true hard stops / irreversible decisions
6. Money, legal, third-party, credentials always escalate
7. Significant tasks require Learning Memory retrieval recorded on the task. A missing retrieval reference is a self-test failure

## Event Bus retention

Keep all records for the current project indefinitely unless the Owner authorizes pruning. Never auto-delete UNVERIFIED or rejected notes within an active run. Duplicate-collapse rule is deferred until Phase 2 (bots); keep-everything until then.

## Durable storage rule

/root/staging (or any product-local sandbox) is temporary only.
A run is incomplete until final system docs, patch notes, lessons, and run journals are written to AUTONOMY-SYSTEM (shared durable home).
Summary Reports must include the shared path or link to final artifacts.
Superseded files go to AUTONOMY-SYSTEM/delete-me/.

## Shared visibility + version control

- Canonical store: private GitHub repo `autonomy-system`
- Shared mirror: Google Drive AUTONOMY-SYSTEM folder for external review
- A run is incomplete until: (1) docs committed + tagged on version change, (2) Drive mirror updated via Actions or explicit sync, (3) Summary Report includes commit SHA and Drive folder link
- /root/staging remains temporary only
- Never commit secrets, OAuth client secrets, service-account keys, or .env files

## Model routing

| Task | Surface | Model |
|------|---------|-------|
| Activation / observation | Claude Cowork | Claude in Cowork session |
| Highest-level orchestration + live-write authority surface | Claude Code | **Claude Fable 5 Max/Ultracode** |
| All other Claude work (implementation, revisions, most team tasks) | Claude Code | **Claude Opus 5 Max/Ultracode** |
| Volume work | Grok Build | Grok Build 4.6 |
| Critique | Grok Heavy | Grok Heavy 4.5 |
| Discovery | Grok Heavy + Code | Heavy 4.5 + Opus 5 |

### Grok CLI bridge (default critique path)

- **Default:** critique calls run one-shot on the Owner-machine local shell — `grok -m grok-4.5 -p "<critique prompt>"` (CLI model id per `grok models`; grok-4.5 = Heavy 4.5 tier equivalence assumed from the models list, not independently verified) — which prints the response to stdout and exits (Grok Build TUI 1.0.3, `C:\Users\chris\.grok\bin`, logged in with grok.com; live round-trip verified 2026-08-18).
- **Transport & actor:** the orchestrating Claude session (Fable gate surface) invokes the CLI through the Owner-machine local shell bridge — the same proven channel as Tier 2 landings (see docs/LANDING-PROTOCOL.md); prompt text passes as one quoted argument.
- **Volume work** may use `-m grok-4.6` (CLI default model); critique stays on grok-4.5.
- **Fallback:** browser automation to grok.com, triggered when a CLI call fails twice consecutively (non-zero exit, >120s timeout, or auth error); the orchestrator flips the path and records the flip in the run journal.
- Unchanged: Grok output still lands UNVERIFIED and carries no write authority (Hard Rules unchanged).

## Efficiency rules

1. Parallel fan-out by default
2. Credit + task-type routing
3. Nested sub-agent trees (3–5 per team)
4. Selective critique
5. Learning Memory first
6. Surplus mandatory every cycle
7. Free / already-available orchestration only

---

## Credit-Aware Routing (browser checks)

### Purpose
Before multi-step work, check **Claude** and **Grok/xAI** usage in the browser so tasks can be delegated before a provider is exhausted mid-run.

**Claude weekly reset: Sunday 9:00 PM America/New_York.**

### Who checks
- **Claude Cowork** — primary credit checker (browser computer-use)
- **Claude Code** — request a Cowork usage check before a long run; never assume unlimited Claude budget
- **Grok / Grok Build** — receive delegated work when Claude is low; still respect Grok limits when known

### How to check (browser)
**Claude:** open Claude/Anthropic usage or limits page; read weekly Fable 5 and Opus 5 used/remaining.  
**Grok/xAI:** open Grok or xAI account/usage page; read remaining quota for Grok, Grok Heavy, Grok Build if shown. If only plan-level limits are visible, record that.

**CREDIT-CHECK note format (Event Bus UNVERIFIED):**
```
CREDIT-CHECK [timestamp]
Claude Fable/Opus weekly: ~XX% used (~YY% remaining) · reset Sunday 9:00 PM America/New_York
Grok/xAI: [exact % if found | plan-level only | page not found]
Recommendation: [NORMAL | CONSERVE_CLAUDE | CLAUDE_CRITICAL | CONSERVE_GROK | GROK_DOWN | CONSERVE_BOTH | UNKNOWN]
```
Do not invent numbers. If unreadable, say UNKNOWN.

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

**Both low → CONSERVE_BOTH:** stop long autonomous loops; Owner-critical short tasks only; queue the rest until Claude reset (Sunday 9:00 PM America/New_York) and/or Grok recovery.

### Grok Build delegation strategies (when Claude is low)
1. **Volume offload** — sweeps, bulk edits, drafts → Grok Build; Claude only verifies/applies after Snapshot → Rollback  
2. **Critique offload** — design/adversarial review → Grok Heavy; skip routine critique on low-risk docs  
3. **Planning offload** — decomposition, options, test design → Grok or Grok Heavy; Claude keeps final verify + live write  
4. **Batch, don’t stream** — one clear package with acceptance criteria per Build job  
5. **Verify-before-apply** — Build output is always UNVERIFIED; stage for after credit recovery if Claude is critical  
6. **Fail soft** — if Grok is also low, stop expansion, write a queue list, do not burn last Claude credits  

### Standing order for Cowork
Before any multi-step autonomous run: (1) browser-check Claude weekly Fable/Opus usage, (2) browser-check Grok/xAI usage if reachable, (3) post CREDIT-CHECK note, (4) if Claude < 5% remaining do not start a long Claude loop — prepare Grok handoff packages instead (mode: CLAUDE_CRITICAL), (5) if both low stop long runs and report (mode: CONSERVE_BOTH), (6) Claude weekly reset is Sunday 9:00 PM America/New_York.

### What this does not claim
No silent mid-call API for exact Claude or Grok %. Browser read is the method. If the UI is blocked or changed, record UNKNOWN (mode: UNKNOWN) and conserve.


## Claude model split (Owner rule)

- **Claude Fable 5 Max / Ultracode** — highest-level orchestration only (decompose, route, verify, final quality gate, Meta-Improvement process critique).
- **Claude Opus 5 Max / Ultracode** — all other Claude work (implementation, drafts, revisions, most team execution).
- **Live writes** still only through Claude Code, under system hard stops + Snapshot → Verify → Rollback.
- **Note:** Fable is priced higher than Opus on token rates; this split is capability/role based by Owner choice, not cost savings.

## Deferred

Grok Bot Layer (Phase 1) — specified, deferred, not cancelled. Phase 2.

## Version History
- v1 — ADDED: tiered architecture + loop
- v2 — ADDED: efficiency, sub-agents, parallel fan-out
- v3 — ADDED: active Learning Memory, Meta-Improvement, Surplus, Grok Bot layer
- v4 — ADDED: Cowork as Activator. DEFERRED: Grok Bots. REMOVED (later fixed): Meta-Improvement wording, retrieve-before-work, self-test return, efficiency section
- v4.1 — FIXED: Cowork MAY/MAY NOT. RESTORED: Meta-Improvement, retrieval, self-test return, sub-agents, efficiency
- v4.1.1 — FIXED: "significant", Retrieve in inner loop, bus retention. REMOVED (regression): Meta-Improvement write boundary; Owner sets duration; full version history
- **v4.1.2** — RESTORED: Meta-Improvement write boundary; Owner sets duration; full version history
- **v4.1.3** — ADDED: Fable cost caveat on Fable row; Event Bus collapse rule explicitly deferred to Phase 2 (cost caveat superseded at v4.1.5 by the role-based cost note)
- **v4.1.4** — ADDED: Credit-Aware Routing (browser checks, Claude/Grok usage thresholds, Grok Build delegation strategies, Sunday weekly reset, standing order for Cowork)
- **v4.1.5** — CHANGED model split: Fable 5 Max/Ultracode = highest-level orchestration; Opus 5 Max/Ultracode = all other Claude work (Owner rule; not cost-based)
- **v4.1.6** — FIXED (hygiene): v4.1.4 history row restored; Hard Rule 7 enforcement clause restored; CREDIT-CHECK enum now covers every threshold mode (STOP_LONG_RUNS removed as redundant with CONSERVE_BOTH); weekly reset timezone stated (America/New_York); v4.1.3 cost-caveat entry marked superseded; SPEC aligned to Fable/Opus split
- **v4.1.7** — ADDED: Durable storage rule (AUTONOMY-SYSTEM shared durable home; product-local staging is temporary; runs incomplete until artifacts promoted; superseded files to delete-me/)
- **v4.1.8** — ADDED: Shared visibility + version control (private GitHub repo autonomy-system is canonical; Drive AUTONOMY-SYSTEM folder is the shared mirror; commit + tag on version change; Drive mirror updated via Actions or explicit sync; Summary Reports carry commit SHA + Drive link; never commit secrets)
- **v4.1.9** — ADDED (SPEC-side): SYSTEM-SPEC-CURRENT.md now carries the Credit-Aware Routing body (CREDIT-CHECK note, Claude/Grok threshold modes and Recommendation enum, Grok Build delegation strategies, standing order, weekly reset) mirrored from this package; this document's Credit-Aware Routing section is unchanged. Hygiene only, no substantive rule changes
- **v4.1.10** — (this document) CHANGED: the Grok Heavy critique path now defaults to the local one-shot Grok CLI on the Owner machine (`grok -m grok-4.5 -p "<critique prompt>"`, Grok Build TUI 1.0.3, grok.com login, verified 2026-08-18); volume work may use `-m grok-4.6`; browser grok.com demoted to FALLBACK. Grok output still lands UNVERIFIED with no write authority; Hard Rules unchanged
