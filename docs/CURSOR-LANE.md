# CURSOR-LANE.md — the second builder pool

**What it is.** Cursor Ultra background agents, working this repo on branches and opening pull
requests — ACTIVE since 2026-08-18 (see Status below). It is a BUILDER
pool for volume — never a gate, never an authority, and never a replacement
for a Claude execution session on rule work.

**Evidence for the $0 claim, stated so it can be checked.** Two independent sources: (1) Cursor's own
documentation at `cursor.com/help/grok-bot/supergrok-heavy` — Cursor Ultra is included at $0 while a
SuperGrok Heavy subscription stays active, and one Grok account pairs to one Cursor account; anyone
can verify this at that URL. (2) Owner report, 2026-08-18 — Chris found the bundle and paired the
accounts the same day. Source (2) is OWNER-REPORTED and unverified by this system; source (1) is
independently verifiable. If Heavy lapses, the $0 assumption dies with it.

**Status: ACTIVE — activated 2026-08-18 on evidence.** The pilot cleared the complete lane: agent
`bc-88581fe2-6b2c-4b2c-b6d0-eae91640652a` opened **PR #2** (`docs/CURSOR-PILOT.md`, in scope);
`verify-docs` **SUCCEEDED on the PR, Actions run 32196858563** — the first CI conclusion this lane
produced; Grok gave a batched routine critique (cli, exit 0, 150s, 6 bullets, all applied, journal
record 55); and a Claude gate merged it as **5ce249f**. PATCH-NOTES open item 15 is CLOSED on that
stack, with dispatch records 56 and 57. **PR #1 was CLOSED, not merged** — out of scope
(`.cursor/environment.json`) with zero completed checks; its content was re-landed Claude-authored.
The lane's first live decision enforced its own rules. ACTIVE means exercised once, not proven: see
Honest limits below.

## Owner setup checklist (Owner-hands only — Hard Rule 6: accounts and credentials)

- [x] **Pair Grok → Cursor** at cursor.com with the SuperGrok Heavy account. *DONE per Owner report,
  2026-08-18.*
- [x] **Connect Cursor's GitHub access** to `chrispcariello/autonomy-system`. *DONE per Owner report,
  2026-08-18 — one transient "Could not resolve default branch" error during the connect, which then
  resolved.* No Claude session performed either step: both are account/credential actions.
- [x] **Scope the Cursor GitHub app** — DONE 2026-08-18 by the gate courier: narrowed from ALL
  repositories to `autonomy-system` only. The grant was live from the moment it was created, so this
  was closed before the first dispatch, not after.
- [x] **Branch protection — DECIDED and CONFIGURED 2026-08-18:** option (a). Ruleset
  **protect-main-cursor-lane** is Active — `main` requires pull requests; bypass = Repository admin +
  Claude app, always-allow; only that one rule, with the deletion and force-push toggles deliberately
  left off. The gate merge 5ce249f is itself the proof that the bypass works, so Tier 1/Tier 2
  landings are not blocked.
- [x] **Pilot dispatch + PR through the full review lane** — DONE 2026-08-18: PR #2, CI run
  32196858563 green, Grok critique record 55, gate merge 5ce249f.

## Standing briefing: `AGENTS.md` + `docs/BRIEF-PACK.md` (v4.1.16)

Cursor background agents read a repo-root `AGENTS.md` when one exists, so `tools/gen_brief.py`
generates one: what this repo is, the lane's scope, the conventions, and a pointer to
`docs/BRIEF-PACK.md` for current state. It is regenerated on every run that touches `docs/**` or
`tools/**`, which is what keeps a dispatched agent current without a human re-briefing it.

**That convention is an assumption, so it is not relied on alone.** Three separate things are
assumed and NONE of them is observable from this surface: that a Cursor agent loads `AGENTS.md` at
all; that it loads it before rather than after the dispatch text; and that a long-running or
re-used agent RE-READS it after a regeneration rather than working from the copy it cached when
its session began. That third one is the quiet one — a briefing that updates on every land is only
current to an agent that re-reads it, so a stale in-agent copy is invisible here and the freshness
machinery does nothing about it. Belt and braces: the CURSOR DISPATCH template in
`docs/RUN-TEMPLATE.md` NAMES both files explicitly in its first line, so the instruction arrives
through the one channel we know the agent reads. Neither file is a permission system either; the
enforcement is unchanged and mechanical — the scope check on the PR, `verify-docs` CI, the Grok
diff critique, and the Claude gate merge. A briefing makes the rules legible before the work
starts; it never makes an out-of-scope PR mergeable.

**A Cursor PR that touches `docs/**` or `tools/**` must also carry regenerated briefings.** The
regeneration rule (`docs/EFFICIENCY-MODE.md`) is enforced by `validate_journal.py`, which
`verify-docs` runs on EVERY pull request, so a PR with a stale `docs/BRIEF-PACK.md` fails CI. The
dispatch template tells the agent to run `python3 tools/gen_brief.py` and commit the three
outputs; where the agent's environment cannot run Python it says so in the PR description and the
Claude gate regenerates before merging. The failure mode is a red check and a slower merge, never
a silently stale briefing.

## Dispatch procedure

1. The gate (or an execution session under the gate's order) writes a dispatch from the CURSOR
   DISPATCH template in `docs/RUN-TEMPLATE.md`: the "read AGENTS.md and docs/BRIEF-PACK.md first"
   line, task, `cursor/<slug>` branch, definition of done,
   constraints, "open a PR — never push main", and the PR-description requirements. **Scope is
   `docs/**` and `tools/**` only**, set by the template; a PR that touches anything else is
   OUT OF SCOPE and is closed without merge, not fixed up by the reviewer. The journal,
   `docs/PATCH-NOTES-CURRENT.md` and `docs/LATEST-HANDOFF.md` are never touched from this lane —
   they are the gate's evidence surfaces and the Claude unit that owns a run writes them.
2. Journal it — one record per dispatch, `type` `"cursor_dispatch"`, with `task`, `branch_or_pr`
   (the `cursor/<slug>` branch, replaced by the PR number or URL once it opens), `outcome`
   (`opened` | `merged` | `closed` | `abandoned`), and the run's `retrieval_ref`.
   `tools/validate_journal.py` FAILS on a record missing `ts`, `type`, `task`, `branch_or_pr` or
   `outcome`. A dispatch with no record did not happen as far as the system is concerned.
3. The agent works the branch and opens the PR. That PR is UNVERIFIED input under Hard Rule 3's
   principle — non-Claude output is UNVERIFIED until a Claude gate verifies it — and the
   `cursor_dispatch` record is how that ingress reaches the Event Bus: `run-journal.jsonl` is this
   system's JSONL Event Bus surface, so a PR with no record has not entered the bus at all.

## The PR review lane (three legs, all required before merge)

- **CI leg — ALREADY BUILT, now unfiltered for PRs.** `.github/workflows/verify.yml` (job
  `verify-docs`) already triggered on `pull_request` before this lane existed — validator self-test,
  `validate_journal.py --all`, specguard against the committed baseline, and the secret scan. The one
  change made for this lane: the PR trigger's path filter was REMOVED (pushes to `main` keep theirs),
  so every PR runs the checks whatever it touches. Before that, a PR touching only paths outside
  `docs/**`, `tools/**`, `.github/workflows/**` would have merged green-by-absence with no checks run.
- **Critique leg.** A Grok pass over the PR diff, using the standard prompt blocks in `docs/GROK.md`
  — 1 pass routine, the 3-pass ladder if the diff is significant. Same journal contract as any other
  critique: one `grok_critique` record per call.
- **Gate leg.** A Claude gate merges, or closes. **Branches are STAGING, not canon:** Hard Rule 1's
  live-write authority protects CANONICAL state — `main`, tags, released docs — so a Cursor agent
  writing to its own `cursor/*` branch is Event-Bus staging, not a live write, while **the merge IS
  the canonical write** and only the Claude surface performs it. Cursor agents never push to `main`,
  and the hard stops — money, ledgers, credentials, third parties — bind every lane, not only
  Claude's.

## Pilot — RUN AND MERGED 2026-08-18

The first dispatch was one bounded, low-risk, docs-only task: a lane self-introduction,
`docs/CURSOR-PILOT.md`. It passed all three legs — CI run 32196858563 green, Grok batched routine
critique (record 55), gate merge 5ce249f — so the success condition set before the run was met, not
redefined after it. Of the three things the pilot was meant to measure: **output quality** was good
(in scope, correct rules restated in the agent's own words, its own retrieval_ref included);
**turnaround** was same-day; **usage limits stay UNKNOWN** — Cursor ran this pilot on Auto with its
usage-limits banner showing, so nothing here measures what Ultra actually allows under load. That
third measurement is still owed.

## Honest limits

Usage caps are unmeasured, and the $0 bundle lasts only as long as Heavy stays active — if Heavy
lapses, the lane's cost assumption dies with it. One merged pilot is not a track record: no Cursor PR
has yet been rejected on QUALITY (PR #1 was closed on SCOPE), so the lane's failure modes are still
untested. A third brand adds coordination surface, mitigated by keeping the interchange GitHub-only:
branches and PRs, no shared session state, no second source of truth. If the lane underperforms,
retiring it costs one doc edit and zero refactoring — nothing else in the system depends on it.
