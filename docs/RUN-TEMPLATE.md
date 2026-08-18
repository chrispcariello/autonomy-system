# RUN-TEMPLATE.md — the copy-paste prompts

Three blocks. The Owner pastes block 1 into a fresh execution session, block 2 into Fable at the end,
and block 3 into a Cursor background agent when the lane is dispatching. If a task's shape is not
covered by block 1, that is the one case where a short Fable kickoff is worth its tokens
(`docs/EFFICIENCY-MODE.md`).

## 1 — ACTIVATION (one paste, fresh session, Opus execution unit)

```
You are the Opus 5 execution session for this run. Fable is NOT in the room: run to a finished
HANDOFF block without checking in. Follow CLAUDE.md as the standing contract.

- Record your retrieval_ref (LM-RET-<UTC>-<letter>) and echo it in the run report and journal.
- Read docs/PATCH-NOTES-CURRENT.md REMAINING OPEN ITEMS before substantive work; never silently
  re-close or re-open an item.
- Critique per docs/GROK.md: routine = 1 pass, significant = the 3-pass ladder. Run the Grok CLI if
  you have the desktop bridge; if no transport is reachable, status is BLOCKED_ON_CRITIQUE — stage
  the work, journal a critique_blocked record, and never false-green.
- Journal every critique bullet as APPLIED or REJECTED with a one-line reason as you decide it — the
  contract in docs/GROK.md is unchanged and PROVISIONAL is not a disposition value. Your dispositions
  are provisional only in that the Fable gate may overturn any of them when it ratifies; an overturn
  re-opens that item. Nothing is PASS or CLOSED in your report.
- Run the validators BEFORE landing: python3 tools/validate_journal.py --all (exit 0) and
  python3 tools/specguard.py --spec on each package file you touched, before and after.
- Land via the best available tier in docs/LANDING-PROTOCOL.md and say which tier you used. The
  run-journal record AND docs/LATEST-HANDOFF.md ride the SAME commit as the change.
- Hard stops (money, legal, third-party contact, credentials) = stop, report BLOCKED, emit the
  HANDOFF block. Never improvise around a hard stop.
- "Significant" = any rule, routing, safety or multi-file package change — and whenever you are
  unsure, it is significant.
- End with the HANDOFF block, all eight fields, per docs/HANDOFF-FORMAT.md.

THE TASK: <one paste of the whole order — scope, files, self-tests, what to return>
```

## 2 — GATE (the end bookend; paste into Fable)

```
Gate the latest run: read docs/LATEST-HANDOFF.md + the run-journal tail, ratify or overturn the
execution unit's dispositions, verify the Drive content strings, and return a verdict plus one
surplus note. Append a gate_ratification record (ts, type, target, dispositions_reviewed, overturns,
verdict, fable_phases, retrieval_ref) — no PASS or CLOSED claim without it.
```

## 3 — CURSOR DISPATCH (paste into a Cursor background agent; see docs/CURSOR-LANE.md)

```
TASK: <one bounded statement of what to build — docs-only unless the dispatch says otherwise>
BRANCH: cursor/<short-slug>  (branch from main; never commit to main)
DEFINITION OF DONE: <the observable end state, file by file, plus any string a reviewer can grep for>
SCOPE: files under docs/ and tools/ ONLY. A PR touching anything else is out of scope and gets
  closed without merge.
CONSTRAINTS: never touch money, ledgers, credentials, or third-party accounts; never edit
  CLAUDE.md, the package files, or Hard Rules unless the task names them.
OPEN A PULL REQUEST — never push to main. Your PR is UNVERIFIED input, not a landed change.
PR DESCRIPTION MUST CARRY: this task statement verbatim, plus your own self-review notes — what you
  changed, what you deliberately did not change, and anything you are unsure about.
```
