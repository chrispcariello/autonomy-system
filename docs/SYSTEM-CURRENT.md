# SYSTEM v4.1.14 — PACKAGE FOR CLAUDE

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


## Critique policy (quality-preserving efficiency)

**Non-negotiable quality rule:** "Efficiency may reduce the FREQUENCY of expensive steps, never the DEPTH required for significant work."

### Routine vs significant
- **Routine** — low-risk work that triggers none of the significant conditions: typo and formatting fixes, single-file non-rule edits, journal appends, restatements of existing rules.
- **Significant** — any change to system rules; any change to routing; any change to safety rules or hard stops; any multi-file package change; anything an Owner order names significant. The Hard Rule 7 significance test still applies in full. When unsure → significant.

### Critique ladder
- **Routine → 1 focused Grok Heavy pass.**
- **Significant → 3-pass Grok Heavy ladder, in this order:**
  1. **Pass 1 — Defects:** defects, contradictions, missing evidence.
  2. **Pass 2 — False-green:** false-green risks, process holes, "looks done but isn't".
  3. **Pass 3 — Final adversarial:** what makes this unsafe, incomplete, or drifted from Owner vision.

### Handling findings
- Claude must APPLY or explicitly REJECT every major Grok finding, each with a one-line reason recorded in the run journal.
- An "LGTM" or an empty critique is a **FAIL** for significant work: re-scope and re-ask, never proceed on it.
- Grok output stays UNVERIFIED until a Claude gate verifies it. Grok has no write path.
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
- **CURSOR LANE — approved, ACTIVATION PENDING (PATCH-NOTES open item 15):** Cursor Ultra background agents (bundled at $0 with the Owner's SuperGrok Heavy while Heavy stays active) are an approved SECOND builder pool that has not yet been exercised. Their output enters ONLY as pull requests, UNVERIFIED under Hard Rule 3's principle that non-Claude output is UNVERIFIED until a Claude gate verifies it; every dispatch and PR is recorded to `docs/run-journals/run-journal.jsonl` — the system's JSONL Event Bus surface — as a `cursor_dispatch` record (task, branch/PR, outcome), so PR ingress lands on the Event Bus as Hard Rule 3 requires.
- **Branches are STAGING, not canon.** Hard Rule 1's live-write authority protects CANONICAL state — `main`, tags, released docs. A Cursor agent may write only to its own `cursor/*` branches, which serve as Event-Bus staging; the canonical write is the MERGE, and only the Claude surface performs it. Merging requires the full review lane: `verify-docs` CI (which runs on EVERY pull request, unfiltered, so nothing merges green-by-absence), a Grok critique of the diff, then that gate merge.
- **Cursor agents NEVER push to `main`** and never touch money, ledgers, credentials, or third parties: the hard stops apply to every lane. Mechanics: `docs/CURSOR-LANE.md`; the step-by-step run shape: `docs/EFFICIENCY-MODE.md`.
- **This dial is FREQUENCY, not depth.** The ladder, the required `grok_critique` records, and every hard stop are unchanged. An efficiency mode that skips critique is not efficiency, it is a false green.
- **Autopilot lane: one Owner paste; Fable plans, spawns crew, gates; fix-loop max 3 then BLOCK; live Fable phases stay at plan+gate plus one per fix loop.** The crew builds under the unchanged critique ladder and lands via `docs/LANDING-PROTOCOL.md`; a `FIX` verdict routes a fix order back to Opus, the Cursor lane or Grok and RE-GATES, and the conservative overturn rule still forbids turning a FAIL or a missing `grok_critique` record into a PASS without new critique evidence. `BLOCK` is available at ANY gate, not only after the loop is spent, and `RATIFY` is recorded as `verdict` `PASS` while `FIX`/`BLOCK` are recorded as `verdict` `FAIL`. One `gate_ratification` record covers the whole run however many crew agents ran, and it is POST-LAND: the gate stops the bad CLAIM, not the bad commit — the pre-land protection is the crew's own Grok ladder plus the validators. A FIX routed to Grok orders a critique pass, NEVER a write. System surgery is EXEMPT and Fable REFUSES the spawn for it — rule changes stay Fable-live. Mechanics: `docs/EFFICIENCY-MODE.md` → Autopilot lane; the Owner-facing lane map: `docs/OWNER-FLOW.md`; the one-paste prompt: `docs/RUN-TEMPLATE.md` block 5.

Copy-ready prompt blocks and the required Grok output shape: `docs/GROK.md`.

---

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
- **v4.1.10** — CHANGED: the Grok Heavy critique path now defaults to the local one-shot Grok CLI on the Owner machine (`grok -m grok-4.5 -p "<critique prompt>"`, Grok Build TUI 1.0.3, grok.com login, verified 2026-08-18); volume work may use `-m grok-4.6`; browser grok.com demoted to FALLBACK. Grok output still lands UNVERIFIED with no write authority; Hard Rules unchanged
- **v4.1.11** — ADDED: Critique policy (routine = 1 focused Grok Heavy pass; significant = 3-pass ladder defects/false-green/final-adversarial; major-finding definition; apply-or-reject with journaled one-line reasons; LGTM/empty = FAIL; pass non-overlap; significant-definition narrowing only by Owner order; pre-land/post-land artifact modes; nightly is routine-only and never lands significant changes) + interconnect/hygiene doc set (GROK.md, HANDOFF-FORMAT.md, OWNER-QUICK-REFERENCE.md, INTERCONNECT.md, NIGHTLY-HYGIENE.md + nightly-checklist.json, CLAUDE.md update). Version renumbered from a v4.1.10 collision with the Grok-CLI-bridge patch that landed first the same morning; reconciled, no rules lost
- **v4.1.12** — ADDED: Review-gate availability (significant work cannot be marked PASS/CLOSED without its `grok_critique` records; BLOCKED_ON_CRITIQUE when the Grok CLI is unavailable and no browser session is running; the Owner-PC-off honesty clause; an Owner accepted-risk waiver that auto-reopens when significant work waits while that machine is offline; a second independent transport stays Owner-escalated under Hard Rule 6, no paid xAI API) + verification pack (`tools/validate_journal.py`, `.github/workflows/verify.yml` with a committed specguard baseline and a self-non-matching secret scan) + `docs/GROK.md` critique queue and `critique_blocked` record shape + the post-land Drive CONTENT-check invariant; PATCH-NOTES open item 14 CLOSED on the landed c8d8884 evidence stack
- **v4.1.13** — ADDED: Efficiency mode (Fable bookends) — Fable appears at most twice per run (an optional kickoff plus the mandatory end gate), in-run critique dispositions are PROVISIONAL until the gate ratifies them from `docs/LATEST-HANDOFF.md` + the run journal, a closed list of mid-run re-entry triggers, and the CURSOR LANE (Cursor Ultra background agents, bundled at $0 with the Owner's SuperGrok Heavy, as an approved second builder pool whose output enters ONLY as pull requests under Hard Rule 3 and merges only through `verify-docs` CI + a Grok critique of the diff + a Claude gate merge; never a push to `main`, hard stops apply to every lane) + new `docs/EFFICIENCY-MODE.md`, `docs/RUN-TEMPLATE.md`, `docs/CURSOR-LANE.md`, and `docs/LATEST-HANDOFF.md` (overwritten at every landing, per a new LANDING-PROTOCOL invariant). Frequency only, never depth — the ladder, the required `grok_critique` records and all hard stops are unchanged; this mode EXEMPTS today's system-surgery cycles by definition, because rule changes remain Fable-gated ladder work. Cursor lane status: CONNECTED per Owner report 2026-08-18, ACTIVATION PENDING — the pilot PR through the full review lane is the activation evidence (PATCH-NOTES open item 15)
- **v4.1.14** — (this document) ADDED: the AUTOPILOT lane — one Owner paste to Fable, which plans, writes a complete standalone work order, SPAWNS the Opus execution crew carrying it, stays out of the room while they build under the unchanged critique ladder, and GATES on return with verdicts RATIFY / FIX / BLOCK; a FIX verdict routes a fix order back to the crew (Opus, the Cursor lane, or Grok) and RE-GATES, looping until ratified to a MAXIMUM of 3 fix loops before it BLOCKS to the Owner; `fable_phases` counts an autopilot run as 2 (plan + gate) plus 1 per fix loop, and every fix loop is journaled. Frequency only, never depth — the ladder, the required `grok_critique` records, the conservative overturn rule (a FAIL or a missing critique record can never become a PASS without new journaled critique evidence) and every hard stop are unchanged, and SYSTEM SURGERY stays EXEMPT: rule changes remain Fable-live ladder work and may not be autopiloted. + new `docs/OWNER-FLOW.md` (the Owner-facing map of all four lanes — routine, plan-touch, autopilot, system surgery — in lay language, with who bills what, the desktop-hands requirement and the parking rule), two new blocks in `docs/RUN-TEMPLATE.md` (4 PLAN, plan-only; 5 AUTOPILOT, the one paste) and a new `### Autopilot lane` section in `docs/EFFICIENCY-MODE.md`. Status: WRITTEN, not PROVEN — no autopilot run has been gated yet; the exit is the first ratified autopilot `gate_ratification` record on `main` (PATCH-NOTES open item 16)
