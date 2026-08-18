# NIGHTLY HYGIENE

**Scope rule (non-negotiable):** nightly hygiene is ROUTINE by construction — appends and one reversible cleanup only. It never edits the SYSTEM-CURRENT / SYSTEM-SPEC-CURRENT bodies or any system rule; anything significant it finds is recorded and deferred to an attended run.

## Purpose

A 15–20 minute unattended pass that keeps the system honest while nobody is watching: credits noted,
lessons re-read, both package docs linted, open items given an owner and an exit criterion, one small
piece of surplus cleaned up, and the whole thing written down and landed.

**Docs only.** This run never touches money, ledgers, inventory, third parties, or credentials, and it
never invents a rule. It reports; it does not decide. If it cannot do something, it says so.

## Schedule

- Fires **01:30 UTC daily** (cron `30 1 * * *`).
- That is **9:30 PM EDT**. Honest note: the task is pinned to UTC, so in EST months (roughly November
  through March) the same firing lands at **8:30 PM ET**. It does not drift with daylight saving on its
  own — the Owner moves it if he wants 9:30 PM year-round.
- Created as a Claude scheduled task (free tier, no new dependency). **Hard cap: 20 minutes.** If the
  cap is reached, stop where you are, write the journal record with what got done, and report.
- The session must be created with the `autonomy-system` repo attached — an unattached session cannot
  push (see `docs/LANDING-PROTOCOL.md`).

## Steps (a–g, in order)

**a) CREDIT-CHECK.** Via browser if reachable: read Claude weekly Fable/Opus usage and Grok/xAI usage,
then write a CREDIT-CHECK note in the format defined in `docs/SYSTEM-CURRENT.md` → Credit-Aware Routing.
The note is an Event Bus / journal note and is **UNVERIFIED**. If the browser is not reachable or the
page is unreadable, record `UNKNOWN` — never invent a number, never skip silently. Unattended firings will usually record UNKNOWN: that is expected and honest, not a failure — the credit gate for significant work lives in attended runs.

**b) Retrieve lessons and journal tail.** Read **all** of `docs/lessons/lessons.jsonl` (all records, not
a sample) and the tail of `docs/run-journals/run-journal.jsonl`. Record the `retrieval_ref` on the run —
this is a significant-task retrieval under Hard Rule 7 and a missing ref is a self-test failure.

**c) Run specguard.** `python3 tools/specguard.py --spec docs/SYSTEM-CURRENT.md` and
`python3 tools/specguard.py --spec docs/SYSTEM-SPEC-CURRENT.md`. Record both finding counts
(`N findings [X FAIL, Y ADVISORY]`) and compare them to the previous night's counts. New FAILs are the
headline of the report; do not fix rules to make the linter quiet — report the delta.

**d) Refresh open items.** Re-read REMAINING OPEN ITEMS in `docs/PATCH-NOTES-CURRENT.md`. **Every item
must carry an owner and an exit criterion.** Add the missing ones. Do not close an item without
evidence, do not re-open a closed one silently, and do not renumber the list to hide a change.

**e) One surplus cleanup.** Exactly one, small and reversible: move an obviously superseded file to
`delete-me/`, drop a dead draft, fix a stale path in a doc. **No aggressive deletion.** If nothing is
obviously safe to clean, say "no safe cleanup found" and move on — that is a valid outcome.

**f) Append the nightly journal record.** One JSON line to `docs/run-journals/run-journal.jsonl`, schema
below. Every step gets its real outcome, including failures.

**g) Land it.** Commit and push the docs using the best available tier in `docs/LANDING-PROTOCOL.md`
(Tier 1 native push → Tier 2 local-shell → Tier 3 one-click fallback), which triggers Actions and the
Drive mirror. Say which tier you used. **If no landing tier is available, stage the work and report
`BLOCKED` with the reason.** Never write a green result for a push that did not happen, and never claim
a Drive sync you did not observe. A BLOCKED first firing is a valid honest outcome (open item 12); Tier 2 may be available to unattended runs when the Owner's desktop app is online.

## Credit rule for this run

If Claude credits are **CLAUDE_CRITICAL**, **skip Grok on the nightly** — unless specguard fails, in
which case run one focused Grok Heavy pass on the failure. This is a frequency cut, not a depth cut:
"Efficiency may reduce the FREQUENCY of expensive steps, never the DEPTH required for significant work."
Nightly hygiene is routine by definition; if the run turns up something significant, it does not fix it
tonight — it opens an item with an owner and an exit criterion and leaves it for a gated run.

## Hard stops (unchanged)

No money. No ledger, inventory, or order writes. No third-party contact. No credentials or secrets in
the repo, in Drive, or in logs. No live system writes outside docs. No architecture changes, no new
dependencies, no activating deferred layers (Grok Bots, Event Bus collapse rule). Anything irreversible
escalates to the Owner instead of happening.

## Failure behaviour

Any step may fail. When one does: **record it and continue** to the next step, then still write the
journal record (f) and the report. Never silent-skip, never substitute a guess for an observation,
never mark a step done because the next step worked. A nightly run that completes three of seven steps
and says so is a success; one that reports green on unobserved work is a failure.

## Journal record schema

Record type `nightly_hygiene`, appended to `docs/run-journals/run-journal.jsonl`:

```json
{
  "ts": "2026-08-19T01:47:00Z",
  "type": "nightly_hygiene",
  "status": "VERIFIED",
  "retrieval_ref": "LM-RET-2026-08-19T01:32Z-N",
  "steps": {
    "a": "OK — CREDIT-CHECK posted UNVERIFIED, Recommendation: NORMAL",
    "b": "OK — lessons.jsonl read in full (6 records), run-journal tail read",
    "c": "OK — SYSTEM-CURRENT 3 [2 FAIL, 1 ADVISORY] (unchanged); SPEC 1 [0 FAIL, 1 ADVISORY] (unchanged)",
    "d": "OK — 12 open items, 2 lacked an exit criterion, both added",
    "e": "OK — moved superseded draft to delete-me/",
    "f": "OK — this record",
    "g": "OK — Tier 1 native push <sha>, Actions green, Drive modifiedTime advanced"
  },
  "grok": "skipped — routine nightly, specguard clean",
  "minutes": 14,
  "detail": "One-paragraph plain summary: what changed, what failed, what the Owner should look at."
}
```

`status` is `VERIFIED` only for what was observed; use `UNVERIFIED` for browser reads and anything not
confirmed, and `BLOCKED` when landing was impossible. Failed steps read `FAIL — <what happened>`.
Machine-readable mirror of these steps: `docs/nightly-checklist.json`.
