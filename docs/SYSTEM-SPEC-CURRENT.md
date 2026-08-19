# AUTONOMOUS MULTI-AGENT SYSTEM — SPECIFICATION v4.1.16
**Date:** 2026-08-19  
v4.1.16 adds the SPEED PACK and automatic lane briefings (a deterministic generator writes a crew brief, a Grok prompt header and a repo-root AGENTS.md from the canonical docs; a validator staleness check keeps them fresh on every update) plus the lean-scribe, batch-gating and parallel-crew rules; v4.1.15 added the Owner's standing routing directive (Claude conserved as the scarce meter; above-trivial repo coding routes to Cursor by default; Grok used liberally for critique, drafting and research; Fable only at bookends and gates) and the mandatory per-run USAGE RECEIPT composed by the gate; v4.1.14 added the Autopilot lane (one Owner paste; Fable plans, spawns the Opus crew, stays out of the room, and gates on return with a bounded fix loop); v4.1.13 added Efficiency mode (Fable bookends) and the Cursor lane (a second builder pool whose output enters only as pull requests); v4.1.12 added Review-gate availability (BLOCKED_ON_CRITIQUE when no critique transport is actually running); v4.1.11 added the Critique policy (routine 1-pass / significant 3-pass ladder); v4.1.10 made the local Grok CLI the default critique path.

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

### Owner routing directive (standing, 2026-08-19)

Claude usage is the scarce resource — conserve it first. Repo-based coding routes to Cursor background agents BY DEFAULT when the change is above trivial size and fits the PR lane; Cursor usage draws zero Claude credit (Owner holds Cursor Ultra, bundled with SuperGrok Heavy). Opus handles trivial edits, canonical writes and merges, Owner-machine hands, session-tool work, and anything Cursor cannot reach. Grok capacity is used liberally: critique always, plus drafting, research, and large-text summarization through the Grok CLI as UNVERIFIED input to a Claude gate — HR3 unchanged, Grok never writes to the repo. Fable appears only at bookends and gates.

Every run ends with a USAGE RECEIPT composed by the gate: tokens per spawned agent as reported by the spawn results (only the gating surface sees them), Fable phase count, Grok passes with durations, Cursor dispatches. The Anthropic plan meter is not machine-readable; token receipts are the honest proxy, and the Owner reads the true meter in the Claude app's usage settings.

Scope of this directive, so it cannot be over-read: it changes ROUTING PREFERENCE ONLY. The Hard Rules are unchanged, the Fable/Opus model split is unchanged, Claude Code remains the sole live-write authority, and Grok gains no write path — a routing preference cannot amend an authority rule, and a session that reads this section as a builder charter overriding the model split or Hard Rule 1 has misread it. Cursor-first IS the standard routing at every threshold mode above: the mode table governs HOW MUCH Claude work runs, never whether coding goes to Cursor. No credit state, `CLAUDE_CRITICAL` included, authorizes skipping or thinning a Claude gate, a critique pass, or the Cursor merge review — scarcity means fewer and shorter runs, never cheaper reviews. The Cursor default does not reach system surgery, package-file work, canonical merges, or a hot-path repair where `main` is red or the lane's own tooling is what broke; those stay with Opus, and when speed is the reason the reason recorded is speed.

---

## Critique policy (quality-preserving efficiency)

Critique frequency is an efficiency dial; critique depth is not. The rule is fixed: "Efficiency may reduce the FREQUENCY of expensive steps, never the DEPTH required for significant work."

### Routine vs significant
- **Routine** — low-risk work that triggers none of the significant conditions: typo and formatting fixes, single-file non-rule edits, journal appends, restatements of existing rules.
- **Significant** — any change to system rules; any change to routing; any change to safety rules or hard stops; any multi-file package change; anything an Owner order names significant. The Hard Rule 7 significance test above still applies in full. When unsure, treat the work as significant.

### Critique ladder
- **Routine → 1 focused Grok Heavy pass.**
- **Significant → 3-pass Grok Heavy ladder, in this order:**
  1. **Pass 1 — Defects:** defects, contradictions, missing evidence.
  2. **Pass 2 — False-green:** false-green risks, process holes, "looks done but isn't".
  3. **Pass 3 — Final adversarial:** what makes this unsafe, incomplete, or drifted from Owner vision.

### Handling findings
- Every major Grok finding is either APPLIED or explicitly REJECTED by Claude, each with a one-line reason recorded in the run journal.
- An "LGTM" or an empty critique is a **FAIL** for significant work: the request is re-scoped and re-asked, never accepted as a pass.
- Grok output remains UNVERIFIED until a Claude gate verifies it. Grok has no write path.
- Credit exception (frequency only, never depth): under CLAUDE_CRITICAL, ROUTINE critiques may be deferred or batched, and the nightly hygiene run may skip Grok unless specguard fails. Significant work NEVER lands without the full 3-pass ladder, in any credit mode — if the ladder cannot run, the work stages and waits.

- **Major finding** = any bullet naming a rule contradiction, a safety/hard-stop weakening, or a false-green path. Style and wording notes are minor and may be batched.
- Ladder passes must be non-overlapping: a pass that substantially repeats a prior pass is re-asked once with narrowed scope before it counts.
- The definition of "significant" may only be narrowed by an explicit Owner order recorded in PATCH-NOTES — never by session judgment under time or credit pressure.
- Pre-land critique of a significant patch reviews pasted excerpts + diff hunks (the mirror still shows the previous version); post-land, the public Drive links are the artifact. Both modes are valid; say which was used.
- Nightly hygiene is routine by construction (appends + one reversible cleanup). If a nightly run would touch the SYSTEM-CURRENT or SYSTEM-SPEC-CURRENT body or any system rule, it STOPS and defers to an attended run — nightly never lands significant changes.

### Review-gate availability
- Significant work MUST NOT be marked PASS or CLOSED without its required `grok_critique` records in `docs/run-journals/run-journal.jsonl` — 1 record for routine, 3 for the ladder. Missing records = the work is not reviewed, whatever the prose says.
- If the Grok CLI is unavailable AND no browser session is running, the status is **BLOCKED_ON_CRITIQUE**: the work stages, nothing false-greens, and the queue clears only when critique actually runs and its dispositions are journaled.
- HONESTY: the browser fallback still requires a running Owner session on a running Owner machine. Owner PC off = BOTH default paths are down = BLOCKED_ON_CRITIQUE is the only honest status; "fallback exists" is not availability.
- The Owner may journal an accepted-risk line for temporary CLI-only operation (PATCH-NOTES open item 13). That waiver AUTO-REOPENS the moment significant work waits for critique while the Owner machine is offline.
- A second independent critique transport stays Owner-escalated: any transport needing credentials or spend is Hard Rule 6 — proposed to the Owner, never self-activated. No paid xAI API is adopted here.

### Efficiency mode (Fable bookends)
- **Default run shape:** Fable appears at most TWICE per run — an optional short kickoff (only when the task shape is NOT covered by `docs/RUN-TEMPLATE.md`) and the mandatory end gate. Everything between them runs on execution sessions (Opus) or the Cursor lane. Target: ≤5% of a run's tokens spent on Fable — a run-shape TARGET, never a ceiling on gate depth: the end gate is EXEMPT from it whenever ratification demands more. Token share is not measurable with today's tooling, so the tracked proxy is the FABLE PHASE COUNT (0, 1 or 2) recorded per run; an unmeasured target is a goal, not a claim. The cap governs Fable SURFACE APPEARANCES only, never the gate's authority, and the six re-entry triggers below are EXEMPT from it: the cap always yields to a triggered re-entry.
- **In-run dispositions are journaled immediately; PROVISIONAL applies only to the RATIFICATION layer.** The execution unit still APPLIES or REJECTS every bullet with a one-line journaled reason under the unchanged critique journal contract — `PROVISIONAL` is not a new disposition value and no record schema changes. It means the Fable gate may OVERTURN any disposition when it ratifies from `docs/LATEST-HANDOFF.md` + the run journal; an overturn re-opens the item and is itself journaled. Ratification is itself a journaled record — `type` `"gate_ratification"` (target, dispositions reviewed, overturns with reasons, verdict, Fable phases used) — REQUIRED before any PASS or CLOSED claim from an efficiency-mode run; mechanical enforcement of that requirement is still open items 2 and 5. This EXTENDS Review-gate availability above — it never relaxes it.
- **Fable re-enters mid-run ONLY for:** a Hard-Rule-6 trigger (money, legal, third-party contact, credentials); a proposed change to Hard Rules, routing, or package versions beyond the ordered scope; a ladder deadlock (the same major bullet contested twice); an accepted-risk auto-reopen; BLOCKED for more than 24h; an Owner summons.
- **CURSOR LANE — ACTIVE since 2026-08-18 (PATCH-NOTES open item 15 CLOSED on evidence: PR #2, CI run 32196858563, critique record 55, gate merge 5ce249f):** Cursor Ultra background agents (bundled at $0 with the Owner's SuperGrok Heavy while Heavy stays active) are a SECOND builder pool, exercised ONCE and therefore not yet proven under load. Their output enters ONLY as pull requests, UNVERIFIED under Hard Rule 3's principle that non-Claude output is UNVERIFIED until a Claude gate verifies it; every dispatch and PR is recorded to `docs/run-journals/run-journal.jsonl` — the system's JSONL Event Bus surface — as a `cursor_dispatch` record (task, branch/PR, outcome), so PR ingress lands on the Event Bus as Hard Rule 3 requires.
- **Branches are STAGING, not canon.** Hard Rule 1's live-write authority protects CANONICAL state — `main`, tags, released docs. A Cursor agent may write only to its own `cursor/*` branches, which serve as Event-Bus staging; the canonical write is the MERGE, and only the Claude surface performs it. Merging requires the full review lane: `verify-docs` CI (which runs on EVERY pull request, unfiltered, so nothing merges green-by-absence), a Grok critique of the diff, then that gate merge.
- **Cursor agents NEVER push to `main`** and never touch money, ledgers, credentials, or third parties: the hard stops apply to every lane. Mechanics: `docs/CURSOR-LANE.md`; the step-by-step run shape: `docs/EFFICIENCY-MODE.md`.
- **This dial is FREQUENCY, not depth.** The ladder, the required `grok_critique` records, and every hard stop are unchanged. An efficiency mode that skips critique is not efficiency, it is a false green.
- **Autopilot lane: one Owner paste; Fable plans, spawns crew, gates; fix-loop max 3 then BLOCK; live Fable phases stay at plan+gate plus one per fix loop.** The crew builds under the unchanged critique ladder and lands via `docs/LANDING-PROTOCOL.md`; a `FIX` verdict routes a fix order back to Opus, the Cursor lane or Grok and RE-GATES, and the conservative overturn rule still forbids turning a FAIL or a missing `grok_critique` record into a PASS without new critique evidence. `BLOCK` is available at ANY gate, not only after the loop is spent, and `RATIFY` is recorded as `verdict` `PASS` while `FIX`/`BLOCK` are recorded as `verdict` `FAIL`. One `gate_ratification` record covers the whole run however many crew agents ran, and it is POST-LAND: the gate stops the bad CLAIM, not the bad commit — the pre-land protection is the crew's own Grok ladder plus the validators. A FIX routed to Grok orders a critique pass, NEVER a write. System surgery is EXEMPT and Fable REFUSES the spawn for it — rule changes stay Fable-live. Mechanics: `docs/EFFICIENCY-MODE.md` → Autopilot lane; the Owner-facing lane map: `docs/OWNER-FLOW.md`; the one-paste prompt: `docs/RUN-TEMPLATE.md` block 5.
- **SPEED PACK (v4.1.16): crews self-brief from the GENERATED `docs/BRIEF-PACK.md` once its staleness check passes; canonical documents WIN on any conflict and surgery-class runs read them directly.** Every run touching `docs/**` or `tools/**` RE-RUNS `tools/gen_brief.py` in the SAME commit — `tools/validate_journal.py` FAILs a stale pack — and that is what keeps the Grok snapshot `docs/GROK-CONTEXT.txt` and the Cursor/agent briefing `AGENTS.md` current on every update instead of whenever someone remembers. Also: the gate SCRIBE verifies only its own `LANDED` line and the validator exit, deferring the Drive CONTENT re-read to the NEXT run's self-brief as a journaled compensating control (the gate may still order full verification); ROUTINE runs may be BATCH-GATED in one sitting with one `gate_ratification` record PER RUN, never merged, while significant and surgery runs are gated individually; and PARALLEL CREWS may fan out only over DISJOINT file sets, with one designated closer/scribe for shared state, fetch-before-finalize serialized landings, one HANDOFF per crew, one gate sweeping the wave and every agent named in the receipt. Mechanics: `docs/EFFICIENCY-MODE.md` → The SPEED PACK.

The copy-ready prompt blocks and the required Grok output shape live in `docs/GROK.md`.

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
- **v4.1.10** — CHANGED: the Grok Heavy critique path now defaults to the local one-shot Grok CLI on the Owner machine (`grok -m grok-4.5 -p "<critique prompt>"`, Grok Build TUI 1.0.3, grok.com login, verified 2026-08-18); volume work may use `-m grok-4.6`; browser grok.com demoted to FALLBACK. Mechanism block mirrored verbatim from the FOR-CLAUDE package into Shared Infrastructure. Grok output still lands UNVERIFIED with no write authority; Hard Rules unchanged
- **v4.1.11** — ADDED: Critique policy (routine = 1 focused Grok Heavy pass; significant = 3-pass ladder defects/false-green/final-adversarial; major-finding definition; apply-or-reject with journaled one-line reasons; LGTM/empty = FAIL; pass non-overlap; significant-definition narrowing only by Owner order; pre-land/post-land artifact modes; nightly is routine-only and never lands significant changes) + interconnect/hygiene doc set (GROK.md, HANDOFF-FORMAT.md, OWNER-QUICK-REFERENCE.md, INTERCONNECT.md, NIGHTLY-HYGIENE.md + nightly-checklist.json, CLAUDE.md update). Version renumbered from a v4.1.10 collision with the Grok-CLI-bridge patch that landed first the same morning; reconciled, no rules lost
- **v4.1.12** — ADDED: Review-gate availability (significant work cannot be marked PASS/CLOSED without its `grok_critique` records; BLOCKED_ON_CRITIQUE when the Grok CLI is unavailable and no browser session is running; the Owner-PC-off honesty clause; an Owner accepted-risk waiver that auto-reopens when significant work waits while that machine is offline; a second independent transport stays Owner-escalated under Hard Rule 6, no paid xAI API) + verification pack (`tools/validate_journal.py`, `.github/workflows/verify.yml` with a committed specguard baseline and a self-non-matching secret scan) + `docs/GROK.md` critique queue and `critique_blocked` record shape + the post-land Drive CONTENT-check invariant; PATCH-NOTES open item 14 CLOSED on the landed c8d8884 evidence stack
- **v4.1.13** — ADDED: Efficiency mode (Fable bookends) — Fable appears at most twice per run (an optional kickoff plus the mandatory end gate), in-run critique dispositions are PROVISIONAL until the gate ratifies them from `docs/LATEST-HANDOFF.md` + the run journal, a closed list of mid-run re-entry triggers, and the CURSOR LANE (Cursor Ultra background agents, bundled at $0 with the Owner's SuperGrok Heavy, as an approved second builder pool whose output enters ONLY as pull requests under Hard Rule 3 and merges only through `verify-docs` CI + a Grok critique of the diff + a Claude gate merge; never a push to `main`, hard stops apply to every lane) + new `docs/EFFICIENCY-MODE.md`, `docs/RUN-TEMPLATE.md`, `docs/CURSOR-LANE.md`, and `docs/LATEST-HANDOFF.md` (overwritten at every landing, per a new LANDING-PROTOCOL invariant). Frequency only, never depth — the ladder, the required `grok_critique` records and all hard stops are unchanged; this mode EXEMPTS today's system-surgery cycles by definition, because rule changes remain Fable-gated ladder work. Cursor lane status: CONNECTED per Owner report 2026-08-18, ACTIVATION PENDING — the pilot PR through the full review lane is the activation evidence (PATCH-NOTES open item 15)
- **v4.1.14** — ADDED: the AUTOPILOT lane — one Owner paste to Fable, which plans, writes a complete standalone work order, SPAWNS the Opus execution crew carrying it, stays out of the room while they build under the unchanged critique ladder, and GATES on return with verdicts RATIFY / FIX / BLOCK; a FIX verdict routes a fix order back to the crew (Opus, the Cursor lane, or Grok) and RE-GATES, looping until ratified to a MAXIMUM of 3 fix loops before it BLOCKS to the Owner; `fable_phases` counts an autopilot run as 2 (plan + gate) plus 1 per fix loop, and every fix loop is journaled. Frequency only, never depth — the ladder, the required `grok_critique` records, the conservative overturn rule (a FAIL or a missing critique record can never become a PASS without new journaled critique evidence) and every hard stop are unchanged, and SYSTEM SURGERY stays EXEMPT: rule changes remain Fable-live ladder work and may not be autopiloted. + new `docs/OWNER-FLOW.md` (the Owner-facing map of all four lanes — routine, plan-touch, autopilot, system surgery — in lay language, with who bills what, the desktop-hands requirement and the parking rule), two new blocks in `docs/RUN-TEMPLATE.md` (4 PLAN, plan-only; 5 AUTOPILOT, the one paste) and a new `### Autopilot lane` section in `docs/EFFICIENCY-MODE.md`. Status: WRITTEN, not PROVEN — no autopilot run has been gated yet; the exit is the first ratified autopilot `gate_ratification` record on `main` (PATCH-NOTES open item 16)
- **v4.1.15** — ADDED: the Owner's standing ROUTING DIRECTIVE (2026-08-19) inside Credit-Aware Routing, identical in both package files (sha256 of the added block matches across the two) — Claude usage is the scarce resource and is conserved first; above-trivial repo-based coding routes to CURSOR background agents BY DEFAULT when it fits the PR lane (zero Claude credit; Cursor Ultra bundled with SuperGrok Heavy); Opus keeps trivial edits, canonical writes and merges, Owner-machine hands, session-tool work and anything Cursor cannot reach; Grok capacity is used LIBERALLY — critique always, plus drafting, research and large-text summarization through the Grok CLI as UNVERIFIED input to a Claude gate (Hard Rule 3 unchanged, Grok never writes to the repo); Fable appears only at bookends and gates. + a MANDATORY per-run USAGE RECEIPT composed by the gate (tokens per spawned agent as reported by the spawn results, Fable phase count, Grok passes with durations, Cursor dispatches), now required by `docs/RUN-TEMPLATE.md` blocks 2 (GATE) and 5 (AUTOPILOT), by `docs/EFFICIENCY-MODE.md` → Autopilot lane, and explained to the Owner in a new lay-language Receipts section in `docs/OWNER-FLOW.md`; the AUTOPILOT plan step must also state the routing split (Cursor / Opus / Grok) and give a one-line reason whenever above-trivial repo coding is NOT routed to Cursor. Routing and receipts only — no Hard Rule, critique-depth, hard-stop or landing rule changes. HONEST LIMITS, recorded not waived: the Anthropic plan meter is NOT machine-readable, so the receipt is a PROXY and the Owner reads the true meter in the Claude app's usage settings; token counts are self-reported by the same surface that composes the receipt; and nothing mechanically enforces receipt presence (PATCH-NOTES open items 2 and 5). Status: WRITTEN, not PROVEN — exit is the directive present and identical in both package files on `main` AND a gate-composed usage receipt delivered on a ratified run (PATCH-NOTES open item 17)
- **v4.1.16** — (this document) ADDED: the SPEED PACK and automatic LANE BRIEFINGS. New `tools/gen_brief.py` (stdlib, deterministic, no wall-clock) reads the canonical documents and generates three files: `docs/BRIEF-PACK.md` (the crew operating brief — Hard Rules and the other authority text extracted VERBATIM, never paraphrased, plus the critique ladder, the record schemas read out of the validator itself, landing tiers, the routing directive, open items, `docs/LATEST-HANDOFF.md` in full, and a MANIFEST of every source with its sha256), `docs/GROK-CONTEXT.txt` (the snapshot prepended to EVERY Grok prompt file, with pure-ASCII / no-double-quote / no-apostrophe / no-dash-led-line / 1500-char constraints ENFORCED by the generator) and repo-root `AGENTS.md` (the standing briefing Cursor and other outside agents read). `tools/validate_journal.py --all` gains a BRIEF-PACK STALENESS CHECK: every manifest source and generated output is re-hashed and any mismatch FAILs naming the stale files, an absent pack skips cleanly, and a `SELF-DIGEST` catches a hand-edited pack; self-test grows from 11 to 17 cases. RULES: crews SELF-BRIEF from the pack and trust it only after that check passes, with canonical documents winning every conflict and surgery-class runs reading them directly; any run touching `docs/**` or `tools/**` REGENERATES in the same commit (the validator FAIL is the mechanical backstop, and this is what keeps Grok and Cursor current on every update); the gate SCRIBE is LEAN (own `LANDED` line + validator exit only, Drive CONTENT re-read deferred to the next run's self-brief as a journaled compensating control, gate may still order full verification); ROUTINE runs may be BATCH-GATED with one `gate_ratification` record PER RUN, never merged, while significant and surgery runs are gated individually; and PARALLEL CREWS may fan out only over DISJOINT file sets with one designated scribe for shared state, serialized fetch-before-finalize landings, one HANDOFF per crew and one gate sweeping the wave. No Hard Rule, model-split, critique-depth, hard-stop or write-authority change. HONEST LIMITS, recorded not waived: a fresh pack proves the SOURCES have not moved, never that the pack summarises them well; deleting the pack makes the check skip rather than fail; the run journal is deliberately outside the manifest; `AGENTS.md` and `tools/**` are NOT mirrored to Drive (docs-only sync), so they are verified in the repo; and whether a Cursor agent reads `AGENTS.md` at all is an assumption, mitigated by naming both files in the dispatch template. Status: WRITTEN, not PROVEN — exit is the generator and the staleness check live on `main` with all three generated files present and fresh, AND the first subsequent run self-briefing via the pack with the lean-scribe compensating control journaled (PATCH-NOTES open item 18)
