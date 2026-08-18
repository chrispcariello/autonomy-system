# EFFICIENCY-MODE.md — the bookend run shape

Owner order, 2026-08-18: *"use Fable 5 just as the bookends/orchestrator."* This file is the
operational version of `## Critique policy` → `### Efficiency mode (Fable bookends)` in both package
files. The package block is the rule; this file is how a run actually executes it.

## The flow, step by step (who runs each step)

1. **Owner — one paste.** The whole order goes in at once, into a FRESH session, using the activation
   text in `docs/RUN-TEMPLATE.md`. No drip-feeding: each follow-up message re-sends the conversation.
2. **Fable kickoff — OPTIONAL, short.** Only when the task shape is not covered by `RUN-TEMPLATE.md`
   (new class of work, unclear routing, Owner asked for a plan first). A covered task skips this
   entirely and the Owner pastes straight to the execution session.
3. **Execution session (Opus) — the whole build.** Reads `CLAUDE.md`, records its `retrieval_ref`,
   checks PATCH-NOTES open items, edits, and runs to a finished HANDOFF block without checking in.
4. **Validators and scripts — free, always run.** `python3 tools/validate_journal.py --all`,
   `python3 tools/specguard.py --spec <file>` before AND after, secret scan. These cost no model
   tokens; there is never a reason to skip them.
5. **Critique — per `docs/GROK.md`.** Routine = 1 pass, significant = the 3-pass ladder. Grok is a
   separate credit tank, so critique depth is NOT what efficiency mode is dialling down. No transport
   reachable ⇒ `BLOCKED_ON_CRITIQUE`, stage the work, journal `critique_blocked`.
6. **Land — best available tier** (`docs/LANDING-PROTOCOL.md`), journal record in the same commit.
7. **Write `docs/LATEST-HANDOFF.md` in that same commit** — this is the gate's inbox. A landing that
   does not refresh it leaves the gate reading stale facts. It is not a second format: `docs/HANDOFF-FORMAT.md`
   remains the canonical FORMAT of the baton, and `LATEST-HANDOFF.md` is only the machine-findable CURRENT
   COPY of that same baton, refreshed each landing. The gate reads the copy plus the journal.
8. **Fable gate — MANDATORY, the end bookend.** Reads `docs/LATEST-HANDOFF.md` + the journal tail,
   ratifies or overturns the execution unit's dispositions, verifies the Drive CONTENT string, and
   returns a verdict plus one surplus note. It appends a `gate_ratification` record (below) — that
   record, not the verdict prose, is what makes the ratification checkable later.

## The Fable budget

Fable appears at most TWICE per run: optional kickoff, mandatory gate. Target ≤5% of a run's tokens —
a target on the RUN SHAPE, never a ceiling on the gate: when ratification needs depth, the end gate
spends whatever it needs and the percentage loses, every time. Everything between the bookends is Opus
or the Cursor lane.

**The 5% has no meter — say so rather than imply one.** Nothing in this system reads per-model token
spend, so the token share is currently UNMEASURABLE and no run may report it as met. The measurable
proxy is the **Fable phase count** — 0, 1 or 2 — recorded as `fable_phases` in each run's
`gate_ratification` record: 2 means kickoff plus gate, 1 means gate only (the efficient shape), and any
count above 2 means a mid-run re-entry happened and its trigger should be named. Until token accounting
exists, the 5% figure is a GOAL, not a claim; the phase count is the number that gets reported.

**What PROVISIONAL means, precisely.** The execution unit journals each critique bullet as APPLIED or
REJECTED with its one-line reason at the moment it decides — the critique journal contract in
`docs/GROK.md` is unchanged and `PROVISIONAL` is NOT a new disposition value in any record. What is
provisional is the RATIFICATION layer above those records: the gate reads them and may OVERTURN any
disposition; an overturn re-opens that item and is itself journaled. Nothing is PASS or CLOSED until
the gate has ratified.

**Ratification leaves an artifact, or it did not happen.** The gate appends one `gate_ratification`
record to `docs/run-journals/run-journal.jsonl` per run it gates, and no efficiency-mode run may claim
PASS or CLOSED without it. Fields: `ts` · `type` `"gate_ratification"` · `target` (the run or work
gated) · `dispositions_reviewed` (count) · `overturns` (a list of `{"b": <bullet>, "reason": "one
line"}`, empty list when the gate ratified everything) · `verdict` (`PASS` or `FAIL`) · `fable_phases`
(0, 1 or 2) · `retrieval_ref`. `tools/validate_journal.py` fails the build when a `gate_ratification`
record is missing `ts`, `type`, `target`, `dispositions_reviewed`, `overturns` or `verdict` — but
nothing yet forces the record to EXIST for a given run, or checks that its counts match the critique
records. That enforcement is PATCH-NOTES open items 2 and 5; until then this is gate discipline, and
saying otherwise would be exactly the false green this file exists to prevent.

**Overturns move outcomes in the CONSERVATIVE direction only.** Ratification can turn a PASS into a
FAIL or re-open a closed item; it can NEVER turn a FAIL, or work with a missing critique record, into
a PASS. Upgrading an outcome requires a new critique record — a fresh pass, journaled — not a gate
opinion. A thin, late ratification therefore cannot wash a ladder: the worst it can do is be too
lenient about what it leaves standing, and it can never manufacture the review that did not happen.

## Mid-run re-entry — the ONLY six triggers

(a) a Hard-Rule-6 trigger: money, legal, third-party contact, credentials · (b) a proposed change to
Hard Rules, routing, or package versions beyond the ordered scope · (c) a ladder deadlock — the same
major bullet contested twice · (d) an accepted-risk auto-reopen (open item 13) · (e) anything BLOCKED
more than 24h · (f) an Owner summons. Nothing else. "I want a second opinion" is not on the list;
that is what Grok is for.

## The Cursor lane, in one paragraph

Cursor Ultra background agents come bundled at $0 with the Owner's SuperGrok Heavy while Heavy stays
active. They are a second BUILDER pool, not a second gate — approved but ACTIVATION PENDING (accounts
connected 2026-08-18 per Owner report; nothing dispatched, no PR, open item 15). They work a branch and
open a pull request, which enters UNVERIFIED under Hard Rule 3's principle and is recorded to the JSONL
Event Bus as a `cursor_dispatch` record, then merges only through `verify-docs` CI + a Grok critique of
the diff + a Claude gate merge. They never push `main` and never touch money, ledgers, credentials, or
third parties. Mechanics, setup state and pilot: `docs/CURSOR-LANE.md`.

## What still costs Fable — be honest about it

The end gate every single run (that is the point of a gate, and it is not negotiable). Odd-shaped
kickoffs, which get cheaper as `RUN-TEMPLATE.md` covers more task shapes. And rule surgery: cycles
that change Hard Rules, routing, or package versions are Fable-gated ladder work by definition and are
EXEMPT from this mode — including the cycle that wrote this file. Efficiency mode reduces how often
Fable is in the room, not how carefully the room is checked.

## Credit notes (they apply to every model, not just Fable)

- **A long conversation makes every following message cost more** — the whole history is re-sent each
  turn. Start a FRESH session per job; do not reuse yesterday's thread.
- **One session per job, one paste.** Hand over the entire order at the start rather than in pieces.
- **Grok is a separate tank.** Spending Grok passes does not spend Claude credit — never cut critique
  to save Claude tokens.
- **Scripts are free.** Validators, specguard, CI, and the secret scan cost zero model tokens; run
  them every time rather than reasoning about whether they would pass.
