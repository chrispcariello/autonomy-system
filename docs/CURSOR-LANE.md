# CURSOR-LANE.md — the second builder pool

**What it is.** Cursor Ultra background agents, working this repo on branches and opening pull
requests — approved, ACTIVATION PENDING (nothing dispatched yet; see Status below). It is a BUILDER
pool for volume — never a gate, never an authority, and never a replacement
for a Claude execution session on rule work.

**Evidence for the $0 claim, stated so it can be checked.** Two independent sources: (1) Cursor's own
documentation at `cursor.com/help/grok-bot/supergrok-heavy` — Cursor Ultra is included at $0 while a
SuperGrok Heavy subscription stays active, and one Grok account pairs to one Cursor account; anyone
can verify this at that URL. (2) Owner report, 2026-08-18 — Chris found the bundle and paired the
accounts the same day. Source (2) is OWNER-REPORTED and unverified by this system; source (1) is
independently verifiable. If Heavy lapses, the $0 assumption dies with it.

**Status: CONNECTED, ACTIVATION PENDING.** Accounts are paired and GitHub is connected per Owner
report (2026-08-18). No dispatch has been made and no Cursor PR exists, so the lane has still never
been exercised: connection is not activation. It becomes active when a pilot PR clears the full review
lane — PATCH-NOTES open item 15, whose Exit is unchanged by the connection.

## Owner setup checklist (Owner-hands only — Hard Rule 6: accounts and credentials)

- [x] **Pair Grok → Cursor** at cursor.com with the SuperGrok Heavy account. *DONE per Owner report,
  2026-08-18.*
- [x] **Connect Cursor's GitHub access** to `chrispcariello/autonomy-system`. *DONE per Owner report,
  2026-08-18 — one transient "Could not resolve default branch" error during the connect, which then
  resolved.* No Claude session performed either step: both are account/credential actions.
- [ ] **URGENT — verify in Cursor settings that its GitHub access is scoped to branches and PRs**; if
  it can push `main` directly, restrict it. *Owner, about one minute.* Urgent because **the grant is
  LIVE NOW while the lane is unactivated — the wire is not dark.** "No dispatch yet" limits what the
  lane has DONE, not what the credential CAN do, and this repo has NO branch protection, so this
  scoping is currently the only thing standing between a misconfigured agent and `main`.
- [ ] **Owner decision — branch protection.** Part of activation, not a detail: either (a) a GitHub
  ruleset requiring pull requests, with a bypass allowance for the Owner's own landing paths (Tier 1
  and Tier 2 both push `main` directly), or (b) keep manual-gate merging plus a strictly scoped
  Cursor grant. PENDING — nothing was configured this cycle and no protection is claimed.
- [ ] **Pilot dispatch + PR through the full review lane.** NOT DONE — this is the activation
  evidence, not the connection above.

## Dispatch procedure

1. The gate (or an execution session under the gate's order) writes a dispatch from the CURSOR
   DISPATCH template in `docs/RUN-TEMPLATE.md`: task, `cursor/<slug>` branch, definition of done,
   constraints, "open a PR — never push main", and the PR-description requirements. **Scope is
   `docs/**` and `tools/**` only**, set by the template; a PR that touches anything else is
   OUT OF SCOPE and is closed without merge, not fixed up by the reviewer.
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

## Pilot (defined, NOT yet run)

First dispatch is one bounded, low-risk, docs-only task — e.g. generating a history index page of
past `LATEST-HANDOFF` blocks from the run journal. **Success = that PR passes all three legs and
merges.** Measure three things: output quality against the definition of done, turnaround time, and
whatever usage limits Ultra actually reveals under load. Those limits are UNKNOWN today; they stay
recorded as unknown until a run measures them.

## Honest limits

Usage caps are unmeasured, and the $0 bundle lasts only as long as Heavy stays active — if Heavy
lapses, the lane's cost assumption dies with it. A third brand adds coordination surface, mitigated
by keeping the interchange GitHub-only: branches and PRs, no shared session state, no second source
of truth. If the lane underperforms, retiring it costs one doc edit and zero refactoring — nothing
else in the system depends on it.
