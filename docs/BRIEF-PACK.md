# BRIEF-PACK.md — generated crew operating brief (v4.1.16)

> **GENERATED FILE — do not hand-edit.** `tools/gen_brief.py` writes it from the canonical
> documents listed in the MANIFEST at the foot of this file. Hand edits are overwritten on the
> next regeneration, and the `SELF-DIGEST` line below is what makes such an edit detectable.
> **On any conflict between this pack and a canonical document, THE CANONICAL DOCUMENT WINS**
> and this pack is stale. This is a fast path to current state, never an authority: no rule
> lives here first, and nothing may be closed, ratified or landed on this file alone.
>
> **Trust it only after the freshness check passes.** `python3 tools/validate_journal.py --all`
> recomputes every MANIFEST hash and FAILS naming any source that moved. If you cannot run it,
> spot-check the hashes yourself. Read the canonical documents in full on ANY conflict, gap or
> staleness — and read the gate and authority documents directly, always, on surgery-class runs.

SELF-DIGEST: f45ded30c1d7233d6cf6004533f6dcfe8077228caace9ee7c8d81ed2cecfdefe
MANIFEST-DIGEST: 9a2131b73da4bfedbff9e194ffb97845824455185d793ddc4a1428e46b4bc78b

## Current state at a glance

- Version: **v4.1.16** (both package files carry it; the SPEC also carries the date).
- Canonical repo: private GitHub `chrispcariello/autonomy-system`; `main` is canon.
- Public read-only Drive mirror of `docs/**` only — that is Grok's read surface, and
  `AGENTS.md` plus `tools/**` are NOT mirrored there. Verify those in the repo/clone.
- Open items: **19 listed, 13 open**.
- Newest version-history row, verbatim from `docs/SYSTEM-CURRENT.md`:

> - **v4.1.16** — (this document) ADDED: the SPEED PACK and automatic LANE BRIEFINGS. New `tools/gen_brief.py` (stdlib, deterministic, no wall-clock) reads the canonical documents and generates three files: `docs/BRIEF-PACK.md` (the crew operating brief — Hard Rules and the other authority text extracted VERBATIM, never paraphrased, plus the critique ladder, the record schemas read out of the validator itself, landing tiers, the routing directive, open items, `docs/LATEST-HANDOFF.md` in full, and a MANIFEST of every source with its sha256), `docs/GROK-CONTEXT.txt` (the snapshot prepended to EVERY Grok prompt file, with pure-ASCII / no-double-quote / no-apostrophe / no-dash-led-line / 1500-char constraints ENFORCED by the generator) and repo-root `AGENTS.md` (the standing briefing Cursor and other outside agents read). `tools/validate_journal.py --all` gains a BRIEF-PACK STALENESS CHECK: every manifest source and generated output is re-hashed and any mismatch FAILs naming the stale files, an absent pack skips cleanly, and a `SELF-DIGEST` catches a hand-edited pack; self-test grows from 11 to 17 cases. RULES: crews SELF-BRIEF from the pack and trust it only after that check passes, with canonical documents winning every conflict and surgery-class runs reading them directly; any run touching `docs/**` or `tools/**` REGENERATES in the same commit (the validator FAIL is the mechanical backstop, and this is what keeps Grok and Cursor current on every update); the gate SCRIBE is LEAN (own `LANDED` line + validator exit only, Drive CONTENT re-read deferred to the next run's self-brief as a journaled compensating control, gate may still order full verification); ROUTINE runs may be BATCH-GATED with one `gate_ratification` record PER RUN, never merged, while significant and surgery runs are gated individually; and PARALLEL CREWS may fan out only over DISJOINT file sets with one designated scribe for shared state, serialized fetch-before-finalize landings, one HANDOFF per crew and one gate sweeping the wave. No Hard Rule, model-split, critique-depth, hard-stop or write-authority change. HONEST LIMITS, recorded not waived: a fresh pack proves the SOURCES have not moved, never that the pack summarises them well; deleting the pack makes the check skip rather than fail; the run journal is deliberately outside the manifest; `AGENTS.md` and `tools/**` are NOT mirrored to Drive (docs-only sync), so they are verified in the repo; and whether a Cursor agent reads `AGENTS.md` at all is an assumption, mitigated by naming both files in the dispatch template. Status: WRITTEN, not PROVEN — exit is the generator and the staleness check live on `main` with all three generated files present and fresh, AND the first subsequent run self-briefing via the pack with the lean-scribe compensating control journaled (PATCH-NOTES open item 18)

## Roles and model split — VERBATIM from `docs/SYSTEM-CURRENT.md`

```
## Claude model split (Owner rule)

- **Claude Fable 5 Max / Ultracode** — highest-level orchestration only (decompose, route, verify, final quality gate, Meta-Improvement process critique).
- **Claude Opus 5 Max / Ultracode** — all other Claude work (implementation, drafts, revisions, most team execution).
- **Live writes** still only through Claude Code, under system hard stops + Snapshot → Verify → Rollback.
- **Note:** Fable is priced higher than Opus on token rates; this split is capability/role based by Owner choice, not cost savings.
```

## HARD RULES — VERBATIM from `docs/SYSTEM-CURRENT.md`, never paraphrased

A paraphrase of a Hard Rule is the drift vector this pack exists to remove, so these
are copied byte-for-byte by the generator. `CLAUDE.md` carries a condensed restatement
for session start; where the two differ in wording, the package text below governs.

```
## Hard rules

1. Only Claude Code may perform live system writes (orchestrator model: Fable 5 Max/Ultracode; other Claude work: Opus 5 Max/Ultracode)
2. Cowork holds NO live-write authority of any duration
3. Everything else → Event Bus as UNVERIFIED
4. No live write without Snapshot → Verify → Rollback
5. Owner only for true hard stops / irreversible decisions
6. Money, legal, third-party, credentials always escalate
7. Significant tasks require Learning Memory retrieval recorded on the task. A missing retrieval reference is a self-test failure
```

## Critique ladder — VERBATIM from `docs/SYSTEM-CURRENT.md`

```
### Routine vs significant
- **Routine** — low-risk work that triggers none of the significant conditions: typo and formatting fixes, single-file non-rule edits, journal appends, restatements of existing rules.
- **Significant** — any change to system rules; any change to routing; any change to safety rules or hard stops; any multi-file package change; anything an Owner order names significant. The Hard Rule 7 significance test still applies in full. When unsure → significant.

### Critique ladder
- **Routine → 1 focused Grok Heavy pass.**
- **Significant → 3-pass Grok Heavy ladder, in this order:**
  1. **Pass 1 — Defects:** defects, contradictions, missing evidence.
  2. **Pass 2 — False-green:** false-green risks, process holes, "looks done but isn't".
  3. **Pass 3 — Final adversarial:** what makes this unsafe, incomplete, or drifted from Owner vision.

### Review-gate availability
- Significant work MUST NOT be marked PASS or CLOSED without its required `grok_critique` records in `docs/run-journals/run-journal.jsonl` — 1 record for routine, 3 for the ladder. Missing records = the work is not reviewed, whatever the prose says.
- If the Grok CLI is unavailable AND no browser session is running, the status is **BLOCKED_ON_CRITIQUE**: the work stages, nothing false-greens, and the queue clears only when critique actually runs and its dispositions are journaled.
- HONESTY: the browser fallback still requires a running Owner session on a running Owner machine. Owner PC off = BOTH default paths are down = BLOCKED_ON_CRITIQUE is the only honest status; "fallback exists" is not availability.
- The Owner may journal an accepted-risk line for temporary CLI-only operation (PATCH-NOTES open item 13). That waiver AUTO-REOPENS the moment significant work waits for critique while the Owner machine is offline.
- A second independent critique transport stays Owner-escalated: any transport needing credentials or spend is Hard Rule 6 — proposed to the Owner, never self-activated. No paid xAI API is adopted here.
```

Prompt blocks, the required output shape, and the transport rules: `docs/GROK.md`.
Every critique or drafting prompt file begins with the current `docs/GROK-CONTEXT.txt`.

## Journal record schemas — read out of `tools/validate_journal.py` itself

These are the keys whose ABSENCE fails the build, generated from the checker's own
constants so this summary cannot drift from the check. They are a MINIMUM shape, not
the full contract: the field semantics live in `docs/GROK.md` (critique + blocked),
`docs/CURSOR-LANE.md` (dispatch) and `docs/EFFICIENCY-MODE.md` (ratification).

- `grok_critique` — required: `ts`, `type`, `target`, `pass`, `model`, `transport`, `exit_code`, `duration_s`, `bullets_count`, `applied`, `rejected`, `retrieval_ref`
- `cursor_dispatch` — required: `ts`, `type`, `task`, `branch_or_pr`, `outcome`
- `gate_ratification` — required: `ts`, `type`, `target`, `dispositions_reviewed`, `overturns`, `verdict`
- Arithmetic also enforced on `grok_critique`: `len(applied) + len(rejected) ==
  bullets_count`, always; `bullets_count` 0 on a ladder pass is a FAIL unless the
  record honestly carries `status` `"FAIL"`.
- **All `ts` values are MACHINE-MEASURED at write time, never estimated** (lesson
  `L-20260819-01`). Nothing in the validator can catch an invented timestamp.
- **Schema-fork guard:** generation FAILS when the checker requires a key `docs/GROK.md`
  never names, so the code and the written contract cannot silently diverge. It does not
  prove they MEAN the same thing — read `docs/GROK.md` for the semantics.

## Landing tiers — VERBATIM headings and triggers from `docs/LANDING-PROTOCOL.md`

- Tier 1 — Session-attached repo (best; the only unattended tier)
  **When:** the session/environment was created with `autonomy-system` (or the project's repo) attached.
- Tier 2 — Local-shell landing (default day-to-day)
  **When:** the sandbox cannot push but the Owner's desktop app is online.
- Tier 3 — One-click fallback
  **When:** tiers 1 and 2 are both unavailable (no attached repo *and* desktop local shell unreachable).

The two invariants runs most often get wrong, verbatim:

```
- **Post-land verification is a Drive CONTENT check, not a timestamp check.** Name, before landing, a heading or exact string that THIS commit introduces (e.g. the new version-history row, or a new section heading), then read the mirrored file and confirm that string is present. A `modifiedTime` advance alone is NOT sufficient — the sync can rewrite a file with stale or partial content and still bump the timestamp. State the string you checked and the file you found it in; if the string is absent, the landing is UNVERIFIED regardless of a green Actions run.
- **Pre-land critique gate (every tier, Tier 2 included).** Before any landing the gate runs `python3 tools/validate_journal.py --all` (it must exit 0) AND confirms that this change's required `grok_critique` records are present in `docs/run-journals/run-journal.jsonl` — 1 for routine, 3 for the ladder. Landing work that was marked `BLOCKED_ON_CRITIQUE` without its critique records is a protocol violation, not a shortcut: `land.ps1` is a dumb fast-forward transport and enforces nothing, so this is the gate's own step. Mechanical enforcement of it remains open items 2 and 5.
```

## Routing directive and the usage receipt — VERBATIM from `docs/SYSTEM-CURRENT.md`

```
### Owner routing directive (standing, 2026-08-19)

Claude usage is the scarce resource — conserve it first. Repo-based coding routes to Cursor background agents BY DEFAULT when the change is above trivial size and fits the PR lane; Cursor usage draws zero Claude credit (Owner holds Cursor Ultra, bundled with SuperGrok Heavy). Opus handles trivial edits, canonical writes and merges, Owner-machine hands, session-tool work, and anything Cursor cannot reach. Grok capacity is used liberally: critique always, plus drafting, research, and large-text summarization through the Grok CLI as UNVERIFIED input to a Claude gate — HR3 unchanged, Grok never writes to the repo. Fable appears only at bookends and gates.

Every run ends with a USAGE RECEIPT composed by the gate: tokens per spawned agent as reported by the spawn results (only the gating surface sees them), Fable phase count, Grok passes with durations, Cursor dispatches. The Anthropic plan meter is not machine-readable; token receipts are the honest proxy, and the Owner reads the true meter in the Claude app's usage settings.

Scope of this directive, so it cannot be over-read: it changes ROUTING PREFERENCE ONLY. The Hard Rules are unchanged, the Fable/Opus model split is unchanged, Claude Code remains the sole live-write authority, and Grok gains no write path — a routing preference cannot amend an authority rule, and a session that reads this section as a builder charter overriding the model split or Hard Rule 1 has misread it. Cursor-first IS the standard routing at every threshold mode above: the mode table governs HOW MUCH Claude work runs, never whether coding goes to Cursor. No credit state, `CLAUDE_CRITICAL` included, authorizes skipping or thinning a Claude gate, a critique pass, or the Cursor merge review — scarcity means fewer and shorter runs, never cheaper reviews. The Cursor default does not reach system surgery, package-file work, canonical merges, or a hot-path repair where `main` is red or the lane's own tooling is what broke; those stay with Opus, and when speed is the reason the reason recorded is speed.
```

## Efficiency mode, autopilot and the fix loop — VERBATIM shared block

This block is byte-identical in both package files; it is the authority on run shape.
The step-by-step mechanics, the fix-loop bound and the receipt rules: `docs/EFFICIENCY-MODE.md`.

```
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

Copy-ready prompt blocks and the required Grok output shape: `docs/GROK.md`.

---
```

## HANDOFF block — the eight fields, in this order

```
HANDOFF
SHA:
Drive:
Changed:
Significant: yes|no
Grok passes requested: 1|3
Open items:
Ask Grok:
```
Field rules: `docs/HANDOFF-FORMAT.md`. `SHA` is a pushed commit or exactly
`STAGED (unpushed)` — never a prediction.

## The SPEED PACK rules — VERBATIM from `docs/EFFICIENCY-MODE.md`

These are the rules that govern READING THIS PACK, so they are carried here in full
rather than pointed at: a brief that omits the rules for using briefs installs a
control nobody in the lane can see.

```
## The SPEED PACK — self-brief from the generated brief, then verify it

Two generators read the canonical documents and write FOUR GENERATED files, one per audience.
`tools/gen_brief.py` writes three: `docs/BRIEF-PACK.md` (the crew brief), `docs/GROK-CONTEXT.txt`
(the snapshot that heads every Grok prompt) and `AGENTS.md` (the repo-root briefing outside agents
read). `tools/gen_map.py` writes the fourth, `docs/SYSTEM-MAP.html` (the Owner-facing living system
map — one self-contained page, no network, no stored state, explaining the system in lay language).
None of the four is a rule source. They are a fast path to current state, and the rules below are
what keep them from becoming a slow path to confident wrongness.

**SELF-BRIEF VIA PACK.** A crew reads `docs/BRIEF-PACK.md` FIRST, and may trust it only after
the freshness check passes — `python3 tools/validate_journal.py --all` (its BRIEF-PACK staleness
check recomputes every manifest hash) or, where the validator cannot run, a manual spot-check of
the MANIFEST hashes. A pack that has not been checked is an unverified summary, and reading one
is not a self-brief. On ANY conflict between the pack and a canonical document, ANY gap the pack
does not cover, or ANY staleness signal, the crew reads the canonical documents in full and the
canonical document wins — the pack never resolves a disagreement in its own favour. **Surgery-class
runs read the gate and authority documents DIRECTLY regardless**: `CLAUDE.md`, both package
files, this file, `docs/GROK.md`, `docs/LANDING-PROTOCOL.md`, `docs/HANDOFF-FORMAT.md`. A change
to the rules is exactly the case where reading a summary of the rules is the wrong move, and the
pack's own header says so. Honest limit, not waived: freshness proves the SOURCES have not moved
since generation. It proves nothing about whether the pack summarises them WELL, and nothing
about the run journal, which is deliberately not a manifest source.

**REGENERATION RULE.** Any run that changes `docs/**` or `tools/**` MUST re-run
`python3 tools/gen_brief.py` AND `python3 tools/gen_map.py` and commit all FOUR outputs IN THE
SAME COMMIT as the change. This
is the mechanism that keeps Grok, Cursor and the Owner briefed on every update without anyone
remembering to brief them. The mechanical backstop is the validator: a changed source with an
unregenerated pack is a `brief-pack-stale` FAIL naming the files that moved, an unregenerated map
is the identical `system-map-stale` FAIL through the same check, and `verify-docs` CI runs both on
every push to `main` and every pull request. **Ordering matters and is not optional:**
both generators read `docs/PATCH-NOTES-CURRENT.md` and `docs/LATEST-HANDOFF.md`, so regenerate
AFTER those are final and before the commit. The run journal is excluded from BOTH manifests on
purpose, so journal appends may follow — with ONE named consequence for the map, which PRINTS the
journal record count: an append after generation leaves that number a build-time FLOOR rather than
a live reading, so it lags without going stale, `--all` stays green by design, and the detector is
`python3 tools/gen_map.py --check` in the pre-land step. Where a run wants the printed count exact,
regenerate the map LAST, after the journal appends. Two limits stated rather than implied: deleting the pack
makes the check SKIP cleanly rather than fail — it catches drift, not deletion — and a
regeneration is only as honest as the sources it ran against, so it certifies currency, never
correctness. Three loopholes named rather than papered over. (i) **Deletion beats the check** — an
absent pack skips cleanly — and an absent MAP skips cleanly the same way, for the same reason — so
the detector for a deleted or never-generated output is
`python3 tools/gen_brief.py --check` AND `python3 tools/gen_map.py --check` (exit 1 when any output
is missing or would change), which
belongs in the pre-land step alongside the validator, not in the validator. (ii) **The source list
is a closed set** — a rule-bearing file outside the MANIFEST can change with every hash still
matching, so adding a new rule document means adding it to `SOURCES` in the generator in the same
run that creates it. That tuple lives in `tools/gen_brief.py` and `tools/gen_map.py` IMPORTS it
rather than copying it, so the two manifests cannot drift apart on what the rulebook is — the cost
of that coupling, named: `gen_map.py` cannot run if `gen_brief.py` is broken or missing, and both
fail loudly rather than half-generating. (iii) **A fresh pack reproduces contradictions faithfully** — if two canonical
documents disagree, the pack ships both claims and flags neither; cross-file consistency is
PATCH-NOTES open item 2 and is still unbuilt, so a green staleness check is not a green rulebook.

**GROK CONTEXT RULE.** Every Grok prompt file — critique pass, drafting, research,
summarization — BEGINS with the current contents of `docs/GROK-CONTEXT.txt`, then the
pass-specific ask. Mechanics and the failure modes: `docs/GROK.md`.

**LEAN SCRIBE.** The gate scribe that lands a `gate_ratification` record verifies exactly two
things about its own landing: that `land.ps1` printed `LANDED <sha>` and that
`validate_journal.py` exited 0. Re-verifying the Drive-mirror CONTENT of what it just landed
moves to the NEXT run's self-brief, which reads the mirror and journals the result as the
COMPENSATING CONTROL for the deferral. Say plainly what this trades: the gap between landing and
verification is now one run wide instead of one turn wide, so a broken sync is discovered later
than it used to be, and a run that never happens never discovers it. That is accepted to buy
gate speed, and the gate MAY still order full verification at landing whenever it judges the
stakes warrant — a version bump, a rule change, or any landing whose failure would be expensive
to find late. The compensating control is only real when the next run actually journals it;
a next-run self-brief that skips the mirror read has quietly removed the check rather than
deferred it. **Effective only once the v4.1.16 run that wrote this rule is itself RATIFIED** —
that run's own scribe follows the law in force when it landed and verifies its Drive content at
the gate, because a rule cannot license the run that is still asking for permission to exist.

**BATCH GATING.** Fable may gate several ROUTINE runs in one sitting. What may NOT be batched is
the record: ONE `gate_ratification` record PER RUN, never merged, each naming its own target,
its own `dispositions_reviewed` and its own verdict — a merged record cannot be overturned per
run, and a wave that fails halfway would otherwise be recorded as one indivisible outcome. One
scribe landing may CARRY several such records in a single commit; that is a transport saving,
not a review saving. SIGNIFICANT and SURGERY-class runs are ALWAYS gated individually, and
batching never lowers the bar for any run in the batch: each still needs its own critique records
at its own depth, and one failing run in a batch fails alone rather than dragging the others or
being dragged by them. The abuse to watch for, named so a gate can refuse it: a batch used to
push a borderline-significant run through on routine attention. When a run's classification is
contested, it leaves the batch and is gated alone.

**BATCH ELIGIBILITY is a hard test, not a judgement call, precisely because "routine" is the word
this rule can be evaded through.** A run is INELIGIBLE for batching — gated individually,
whatever it calls itself — if it changed any of: a Hard Rule, routing, safety rules or hard
stops; either package file; `CLAUDE.md`; anything under `tools/**`; the run journal's schema; or
this file, `docs/RUN-TEMPLATE.md`, `docs/GROK.md`, `docs/LANDING-PROTOCOL.md`,
`docs/CURSOR-LANE.md`, `docs/HANDOFF-FORMAT.md` or `docs/lessons/lessons.jsonl`. **The path list
is a FLOOR, not the test** — a denylist can always be walked around by editing something not on
it, so the governing rule is semantic and sits above it: **any run whose HANDOFF says
`Significant: yes` is ineligible for batching, full stop**, and so is any run that changed the
MEANING of a control regardless of which file carried it. "Restatement of an existing rule" is a
routine category for CRITIQUE DEPTH; it is not a licence to batch a rule document's edit, and
relabelling a control change as a restatement to buy one pass and a batched gate is the exact
evasion these two tests exist to block. When unsure → not batchable, the same direction the
significance test already runs in. **The SPLIT-RUN evasion is named too**, because it defeats a
per-run test by construction: a set of runs that TOGETHER change a control is batch-ineligible
even when each one looks routine alone, and the gate applies the test to the BATCH as a whole
before it applies it run by run. Honest limit: nothing mechanically classifies a run or notices
that three runs add up to one rule change, so this is gate discipline like `fable_phases` and the
receipt — open items 2 and 5. And be precise about what batching costs: one record per run
preserves the RECORD, not the attention. Reading four runs in one sitting is less adversarial than
reading one, which is why the eligibility tests are drawn tight rather than left to appetite. And a batch NEVER pools deferred verification: if the runs in it deferred Drive
CONTENT reads under LEAN SCRIBE, each deferral is named separately and the next run reads all of
them — one read does not discharge N landings.

**PARALLEL CREWS (fan-out).** One plan may spawn N crews at once, under conditions that are
requirements, not preferences:
- **DISJOINT file sets.** Each crew's scope is declared in its work order and no two overlap.
  Overlap is not resolved later; it is a planning error caught before the spawn.
- **Shared state has ONE writer — with the journal exception stated exactly, because the
  unqualified version contradicts an older rule.** `docs/PATCH-NOTES-CURRENT.md` and
  `docs/LATEST-HANDOFF.md` are written ONLY by the designated closer/scribe, whose landing is
  LAST. The run journal is different: the standing contract requires each unit's `grok_critique`
  records to ride the SAME commit as the fixes they produced, so each crew DOES append its own
  records — but only inside its OWN landing commit, never into a working copy a sibling is also
  editing. Because landings serialize, those appends serialize too; a crew that has not landed
  holds its records rather than writing them early. The closer appends the run-level record last.
  Any crew touching PATCH-NOTES or LATEST-HANDOFF is racing a sibling it cannot see.
  **Journal appends are APPEND-ONLY AT END OF FILE, and "rebase" here means one specific thing.**
  A crew whose base moved rebuilds its own UNLANDED commit on the fetched tip and re-appends its
  lines at EOF; it never rewrites landed history, which `docs/LANDING-PROTOCOL.md` forbids
  outright ("No force-push, no rebase of landed history, ever"). Because the appends are at EOF
  and the landings serialize, the merge is deterministic — but nothing MECHANICALLY prevents a
  crew from resolving a conflict by dropping a sibling's line, so the closer's last job before
  the baton is to check the journal's record count and numbering against the crews it dispatched.
  A wave whose record count does not reconcile is not closed.
- **`docs/LATEST-HANDOFF.md` is ONE file and stays one file.** It holds the CLOSER's baton, and
  because it is the gate's only inbox that baton MUST ENUMERATE every crew — each crew's landed
  SHA, its file set and its critique records — or the gate reads the last crew's facts and
  silently gates a wave it cannot see. Each crew still returns its own HANDOFF block to the
  orchestrator; the file carries the consolidated one.
- **The GENERATED SET is shared state too, and only the CLOSER regenerates it.**
  `docs/BRIEF-PACK.md`, `docs/GROK-CONTEXT.txt`, `AGENTS.md` and `docs/SYSTEM-MAP.html` are
  rewritten by every run that
  touches `docs/**` or `tools/**`, so under the regeneration rule as written EVERY crew in a wave
  would rewrite the same four files — a guaranteed collision even when the task file sets are
  perfectly disjoint. The fan-out carve-out is exact: crews in a wave do NOT regenerate; the
  designated closer runs `tools/gen_brief.py` and then `tools/gen_map.py` once each, in the
  CLOSING commit, after every sibling has
  landed. **A generated file is NEVER conflict-resolved by hand.** If a wave leaves one of the
  four conflicted, the closer takes either side to make the merge complete and then RE-RUNS both
  generators over the merged tree; picking ours or theirs on a generated file can keep every
  digest green while a real source edit is silently dropped, which is the one merge outcome this
  rule exists to make impossible. The intervening commits are knowingly stale and the validator will say so on any of
  them; the wave is not finished until the closer's commit clears the check. Single-crew runs are
  unaffected — they regenerate in their own commit, as the rule says.
- **Landings SERIALIZE, and the CLOSER lands LAST.** Every crew fetches `origin/main` immediately
  before finalizing and rebases onto the current tip; the landing protocol is fast-forward-only,
  so a stale bundle base is rejected rather than forced. Two crews landing from the same base is
  the collision this rule exists to prevent, and the rejection is the detector of last resort —
  it fires after the work, not before. A crew landing AFTER the closer is a protocol violation,
  not a late arrival: the closer's baton and the gate's sweep both describe a wave that is
  already complete, so the wave stays OPEN and unratified until that commit is accounted for.
- **Each crew returns its OWN HANDOFF block**, and ONE gate sweeps the whole wave with one
  `gate_ratification` record per RUN in it, enumerating every crew agent and every critique
  record it reviewed.
- **The receipt lists EVERY agent**, per the routing directive; a receipt naming one agent for a
  wave of four is a receipt that has already lost track of the run.

**Fan-out is the WRONG shape for dependent steps and for trivial jobs**, and this run is the
worked example: v4.1.16 changed a generator, a validator, four rule documents, both package files
and the open-items board, all of which read each other, so it ran as ONE Opus crew and said so on
the run record. Splitting interdependent edits across crews that cannot see each other buys
parallelism and pays for it in merge conflicts and half-consistent rules; splitting a ten-minute
job buys nothing and pays a spawn, a work order and a gate sweep. Fan out for VOLUME over
independent surfaces, never to look busy.
```

## Mid-run re-entry — VERBATIM from `docs/EFFICIENCY-MODE.md`

```
## Mid-run re-entry — the ONLY six triggers

(a) a Hard-Rule-6 trigger: money, legal, third-party contact, credentials · (b) a proposed change to
Hard Rules, routing, or package versions beyond the ordered scope · (c) a ladder deadlock — the same
major bullet contested twice · (d) an accepted-risk auto-reopen (open item 13) · (e) anything BLOCKED
more than 24h · (f) an Owner summons. Nothing else. "I want a second opinion" is not on the list;
that is what Grok is for.
```

## Where the rules this pack does NOT extract actually live

This pack extracts the package-file authority text verbatim. Whole rule sets live only
in their own documents and are NOT reproduced here — reading the pack is not reading the
rules. Go to the document itself before acting on any of these:

| document | what only it carries |
| :-- | :-- |
| `docs/EFFICIENCY-MODE.md` | run shape, the SPEED PACK rules (self-brief via pack, regeneration, lean scribe, batch gating, parallel crews), autopilot mechanics, the six re-entry triggers, receipt rules |
| `docs/RUN-TEMPLATE.md` | the five copy-paste blocks: activation, gate, Cursor dispatch, plan, autopilot |
| `docs/GROK.md` | prompt blocks, transport, the GROK CONTEXT rule, critique journal contract, queue + `critique_blocked` |
| `docs/LANDING-PROTOCOL.md` | the three tiers in full and every landing invariant |
| `docs/HANDOFF-FORMAT.md` | the per-field rules for the eight HANDOFF fields |
| `docs/CURSOR-LANE.md` | dispatch procedure, the three review legs, `AGENTS.md` assumptions and their limits |
| `docs/OWNER-FLOW.md` | the Owner-facing lane map and receipts, in lay language |
| `docs/NIGHTLY-HYGIENE.md` | the unattended nightly steps and their caps |
| `AGENTS.md` | the standing briefing outside agents read (generated; repo root, NOT mirrored to Drive) |

## Open items — numbers, titles and state

Authoritative list: the LAST `## REMAINING OPEN ITEMS` section of
`docs/PATCH-NOTES-CURRENT.md`. Titles below are shortened for scanning; never close,
re-open or renumber an item from this pack — read the section itself.

| # | State | Title |
| --: | :-- | :-- |
| 1 | OPEN | Pooled Fable/Opus budget |
| 2 | OPEN | specguard cross-file version-sync check |
| 3 | OPEN | SPEC team table (L48–52) still uses pre-split phrasing ("Claude Code (Opus/... |
| 4 | OPEN | v4.1.5 condensation drops remain unrestored in FOR-CLAUDE (UNVERIFIED→verif... |
| 5 | OPEN | Write-safety auditability |
| 6 | OPEN | Self-test pass criteria and the 3-fail counter scope remain undefined in bo... |
| 7 | OPEN | Grok "low" is unquantified, so the CONSERVE_BOTH trigger stays a judgement... |
| 8 | OPEN | Heuristic advisories |
| 9 | OPEN | Deferred by directive, unchanged |
| 10 | CLOSED | Actions sync BLOCKED_ON_OWNER_SECRETS |
| 11 | OPEN | Desktop add-repo-to-existing-session picker defect |
| 12 | OPEN | NEW |
| 13 | OPEN | NEW |
| 14 | CLOSED | CLI critique path independent validation |
| 15 | CLOSED | Cursor lane activation |
| 16 | CLOSED | Autopilot lane (one-paste bookends with gate fix-loop) |
| 17 | CLOSED | Owner routing directive + mandatory usage receipts |
| 18 | CLOSED | Speed pack + lane auto-briefings (v4.1.16), extended by the LIVING SYSTEM MAP |
| 19 | OPEN | NEW |

Count line in force: **19 listed, 13 open**

## docs/LATEST-HANDOFF.md — copied in full

# LATEST-HANDOFF.md

This file always holds the NEWEST run's HANDOFF block and is overwritten at every landing, in the same
commit as the change — it is the Fable gate's inbox, not an archive. History lives in
`docs/run-journals/run-journal.jsonl` and `docs/PATCH-NOTES-CURRENT.md`.

It is NOT a second format. `docs/HANDOFF-FORMAT.md` remains the canonical FORMAT of the baton — the
eight fields, their order, and the rules per field. This file is only the machine-findable CURRENT COPY
of that same baton, so the gate can read one path instead of scrolling a run report. Gate input = this
copy + the journal tail; the format authority is HANDOFF-FORMAT.md.

---

**GATE STATUS: PENDING — awaiting the Fable end gate.** This is the CREW's baton for the CURSOR HARVEST
PROCEDURE run, written before ratification. Nothing below is PASS or CLOSED: the crew's critique
dispositions (journal records **80, 81, 82**) are PROVISIONAL until a `gate_ratification` record exists,
and PATCH-NOTES item **19** was deliberately ADDED OPEN rather than self-closed — its exit requires a
real harvested PR that this run did not perform. The run classified itself **SIGNIFICANT, non-surgery**
and is **batch-INELIGIBLE** on both tests (`Significant: yes`, and it edited three files on the
eligibility floor list), so it is gated individually.

```
HANDOFF
SHA: STAGED (unpushed) at write time — a file cannot contain its own landing SHA. Landing via Tier 2
  (local-shell land.ps1 into the standing clone C:\Users\chris\autonomy-system-live), base/parent
  78f5e253ead6b3898da0757edfd2e14ddc128ea1 (the ratified record-79 gate commit), fast-forward only.
  No tag: this run carries no version bump. GATE: fill in the landed SHA here from git log -1 in the
  clone rather than from the crew's report.
Drive: NOT VERIFIED THIS RUN for this run's own landing — deferred under LEAN SCRIBE, which is the
  standing law now that the v4.1.16 run that wrote it is ratified (record 79). The scribe verifies its
  own LANDED line and the validator exit only.
  DEFERRED TO THE NEXT RUN, named separately so one read cannot silently discharge three: (a) the exact
  string "Harvest procedure (pipelined lane)" in the mirrored docs/CURSOR-LANE.md — the word
  "pipelined" is the one-word check; (b) the exact string "NAMING IS NOT HARVESTING" in the mirrored
  docs/RUN-TEMPLATE.md; (c) the exact string "19 listed, 13 open" in the mirrored
  docs/PATCH-NOTES-CURRENT.md. Three strings, three files, one next run.
  DISCHARGED BY THIS RUN, the compensating control for f13b1e5, all three strings read by CONTENT and
  not by modifiedTime (journal record 83): the mirrored docs/EFFICIENCY-MODE.md (Drive id
  1s42VvKYAqgrMJgw05htM38DkdJVi5V6y, text/markdown, 41349 bytes) CONTAINS "docs/SYSTEM-MAP.html" inside
  the sentence "writes the fourth" AND CONTAINS "system-map-stale"; the mirrored docs/LATEST-HANDOFF.md
  (Drive id 1kTmQYp3_D2ICLnocaY_SD0esgAOXXzym, text/markdown, 12714 bytes) CONTAINS "record 79", three
  times as a literal single-line string. No deferral aged out.
  NOT CHECKABLE ON DRIVE by construction: AGENTS.md and tools/** never reach the mirror (docs/** only) —
  verify those in the standing clone at the landed SHA.
Changed: docs/CURSOR-LANE.md (NEW section "Harvest procedure (pipelined lane)" — a HARVEST-READY
  definition, (a) DISPATCH EARLY with THREE named failure modes, (b) POUNCE, (c) BATCH HARVEST with an
  eligibility test, (d) the non-compressible inspection floor with the CLAUDE_CRITICAL credit exception
  reconciled, (e) a split routine/significant timing expectation, plus a "What this procedure COSTS"
  subsection carrying the bad-merge sequence; ALSO one amended sentence under Standing briefing, which
  claimed regeneration keeps a dispatched agent current and is false under early dispatch) ·
  docs/RUN-TEMPLATE.md (block 5 ORDER THE WAVE; block 2 BATCH HARVEST; block 3 HARVEST EXPECTATION) ·
  docs/EFFICIENCY-MODE.md (ONE cross-reference paragraph in the Autopilot routing area, pointing at
  CURSOR-LANE.md as the owner, no duplication) · docs/PATCH-NOTES-CURRENT.md (item 19 ADDED at the end,
  OPEN, plus a superseding count line; nothing renumbered, reordered or closed) · docs/BRIEF-PACK.md,
  docs/GROK-CONTEXT.txt, AGENTS.md, docs/SYSTEM-MAP.html (all four regenerated in this same commit,
  both generators, map LAST after the journal appends) · docs/LATEST-HANDOFF.md (this baton) ·
  docs/run-journals/run-journal.jsonl (records 80-82 grok_critique passes 1-3, record 83 patch).
  NO package files, no version bump, no tag, no .github/**, no tools/** code, no routing or authority
  text.
Significant: yes
Grok passes requested: 3 — full ladder run BEFORE landing via the Grok CLI on the Owner machine, each
  prompt file headed by docs/GROK-CONTEXT.txt per the GROK CONTEXT RULE. Pass 1 defects 8 bullets
  (exit 0, 149s, PROMPT_CHARS 10876), Pass 2 false-green 8 (exit 0, 133s, PROMPT_CHARS 11197), Pass 3
  adversarial 8 (exit 0, 151s, PROMPT_CHARS 11823). 24 bullets, 23 APPLIED, 1 REJECTED with a reason
  preserved for the gate. The ladder changed the artifact materially: it produced the HARVEST-READY
  definition, the reconciliation of the CLAUDE_CRITICAL credit exception (docs/SYSTEM-CURRENT.md line
  207) that (d) had flatly contradicted, the THIRD dispatch-early failure mode (an early PR and its own
  wave regenerating the same four generated files), the poller-is-never-Fable resolution of a real
  collision with the autopilot stay-out-of-the-room rule, the batch-harvest eligibility test, the two
  record shapes that still pass the validator, NAMING IS NOT HARVESTING, the re-critique-on-base-move
  rule, the ordered-artifact exit on item 19, and the entire "What this procedure COSTS" subsection.
  EXCEPTIONS, recorded not waived, all on record 83: (1) a self-reported PROMPT HYGIENE DEFECT — the
  pass 1 prompt file was transferred with ONE line of the generated snapshot omitted (the LAST LAND
  history row, itself already [TRUNCATED]), which breaks the GROK CONTEXT RULE instruction not to
  substitute the snapshot; passes 2 and 3 carry it verbatim, the pass returned full depth, and the pass
  was NOT re-run — the gate may order it; (2) all three prompts exceed the 1900-char guideline, echoed
  PROMPT_CHARS is the standing compensating control; (3) --all --strict still exits 1 at base and after
  on legacy item 10, unchanged, while --all (what CI runs) exits 0 both times; (4) no Python on the
  Owner machine, so the verify-docs conclusion is NOT observed at write time.
Open items: 19 listed, 13 open. ADDED: item 19 (Cursor harvest procedure — pounce + batch), OPEN, owner
  Claude, exit = the FIRST REAL PR harvested under the procedure and closing on ORDERED ARTIFACTS rather
  than narrative: a cursor_dispatch record whose ts predates that wave's Claude build, the verify-docs
  Actions run id for the merged tip, a grok_critique record covering that PR alone cited by number, and
  the gate merge SHA, with dispatch < critique < merge in time. Nothing renumbered, reordered or closed;
  item 18 stays closed-on-record with its residuals as standing limits; item 13 (Review-gate SPOF) stays
  open and unwaived. THE CREW DID NOT SELF-CLOSE ANYTHING. What this run does NOT claim: the procedure
  has never been RUN — no PR was dispatched early, pounced on, or batch-harvested under it — and the
  recorded price is on the item: the lane's latency was never a control but throttled volume in a lane
  that has never rejected a PR on quality, so removing it makes the Cursor-first default bite harder,
  and all four of the procedure's defences (HARVEST-READY, current base, re-critique, eligibility) are
  gate readings with no mechanical enforcement, the same gap as open items 2 and 5.
Ask Grok: pass 3 argued this procedure should not exist yet — one merged pilot, one scope rejection,
  zero quality rejections — and that removing the lane's latency unlocks Cursor-first volume with no new
  quality brake. That was REJECTED as a conclusion on the Owner order and APPLIED as recorded price, so
  the question is now the Owner's, not the crew's: what OBSERVABLE in this repo would show that the lane
  has started merging work it should have rejected, given that a quality rejection has never once
  happened and its absence reads identically to a lane producing only good PRs? Second: every defence
  this procedure adds is a gate reading performed on the busiest turn of the run. Which ONE of them
  would buy the most safety if it were made mechanical instead — a required up-to-date-before-merge
  branch rule, verify-docs as a required status check, or a validator check that no grok_critique target
  names two PRs — and what would break the first time it fired?
```

## MANIFEST

Each canonical source with the sha256 of its content at generation time.
`tools/validate_journal.py --all` recomputes these; any mismatch is a FAIL naming the
stale files, and that failure is the mechanical backstop behind the regeneration rule.

Cross-file guard: the shared `### Efficiency mode (Fable bookends)` block was verified
BYTE-IDENTICAL across both package files at generation, sha256 `b4fb9e89f78f5655a3b3b8d964fe331da4d59a851f07e93d0bec151ea830bfcc`.
Generation FAILS when it is not — the one cross-file consistency check that exists today.

| source | sha256 |
| :-- | :-- |
| `CLAUDE.md` | `cc9eed20ad0469081fb335d234940820d999b6c5c02019f6c3c13d24e90d4162` |
| `docs/SYSTEM-CURRENT.md` | `ecd943a1db9ce51c6a33b2f339ad21ab6516657bf7a134f5f5676815ddfda200` |
| `docs/SYSTEM-SPEC-CURRENT.md` | `f99b5f4a12da6952839a0ed9ea19295e4380174a2d9657ef0a87021c88f026a0` |
| `docs/EFFICIENCY-MODE.md` | `fece2ea7e145eaaa84cd12438053cd3f1fb2fcb8529c0e25f3b06456c679b876` |
| `docs/RUN-TEMPLATE.md` | `f110afdde95a6e92f89b3e5f6e41f0480b89c899ea3b1639487e2f460e829117` |
| `docs/GROK.md` | `7635de9b23ccc1c06761a7b551f22487501d6690a4f07fe863ad1ef0448a897f` |
| `docs/LANDING-PROTOCOL.md` | `9388e37a57a4736483b60c073fccd2fb62abb2925437cf82953e64b15fa1178a` |
| `docs/HANDOFF-FORMAT.md` | `4db1a9a489ec090b3ce555fa4e2f537c8401662501736c172a58b4d254eb88e1` |
| `docs/CURSOR-LANE.md` | `241f44fa35de93e35d6dd9e43e64190c1d778ddfd8da7929bbe7238f4762e70e` |
| `docs/OWNER-FLOW.md` | `1caa25201c04a47c46c23d14421c9218101c107e06e9cf76f7e74ffd1cd2fcb0` |
| `docs/NIGHTLY-HYGIENE.md` | `464ee705a33a71c764b102798bd6fa93fd0b9c9cdf90d4345509599288eed3d6` |
| `docs/lessons/lessons.jsonl` | `99c3a9df776fbda5159ae5211daede50f9069e62601b5db2ab0434e1649f1aae` |
| `docs/PATCH-NOTES-CURRENT.md` | `929277ada1dca466ffa55d6b8ca4b27898f9acfb2761953dc1c45b3384048978` |
| `docs/LATEST-HANDOFF.md` | `4fc1489d8e61d651307c511a1d3e715afa4a688557c4e55ada31e8423a36fe90` |
| `tools/validate_journal.py` | `816ea1c1f33f29c5d91950bc540bf6f5d802b27458276f633e082bae918f7ded` |

Generated outputs, hashed so a hand-edit of them is detectable too:

| generated file | sha256 |
| :-- | :-- |
| `docs/GROK-CONTEXT.txt` | `ca83d9b1b8739004a9c6dbaaa1a6c597cb613c55131c208a089ccadd7fc87e1d` |
| `AGENTS.md` | `1c66558f69a4e405ad72885b682216b962949f78c9ca480420ec1b5a791fa8d9` |

**What the MANIFEST deliberately does NOT cover, so nobody reads more into it:**
(1) `docs/run-journals/**` — append-only evidence, not a rule source; including it would
force a regeneration per journal append. (2) The source list is a CLOSED SET: a
rule-bearing file outside it can change with every hash still matching, so the pack stays
FRESH and wrong. (3) The pack reproduces its sources faithfully, CONTRADICTIONS INCLUDED —
if two canonical documents disagree it ships both claims and flags neither, except for the
one shared block guarded above (cross-file consistency generally is open item 2, unbuilt).
(4) DELETION beats this check: an absent pack skips cleanly, so
`python3 tools/gen_brief.py --check` is the deletion detector and belongs in the pre-land
step. (5) Nothing here proves the rules are good, that Drive synced, or that any outside
agent read `AGENTS.md` at all.
