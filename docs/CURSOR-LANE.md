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
`tools/**`, which is what keeps a dispatched agent current without a human re-briefing it — **with
one exception the Harvest procedure below creates and this sentence must not paper over: an agent
dispatched EARLY, before its own wave has landed, is briefed on the PRE-WAVE state by construction.**
Regeneration keeps the briefing current with `main`; it cannot make it current with a wave still in
flight. That case is handled in Harvest procedure (a), not here.

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

## Harvest procedure (pipelined lane)

The three legs above say WHAT must clear before a merge. This section says WHEN each leg runs, and
it exists because the lane's wall-clock cost so far has been mostly WAITING rather than checking: a
dispatch written after the Claude work was already done, then a pull request sitting green while
everyone's attention was somewhere else. Pipelining removes that waiting. It removes nothing else —
the floor in (d) is restated here precisely so speed cannot be spent out of the review budget.

**HARVEST-READY, defined before it is used, because an undefined readiness test is where the whole
procedure would leak.** A pull request is HARVEST-READY when all three hold: it is open and IN SCOPE
(`docs/**` and `tools/**` only); `verify-docs` is green **on the branch as it stands now, against
the current `main`**; and a Grok critique exists that covers THAT diff, or is about to be run
against it. Green alone is not ready — green is the trigger to START the harvest, not a licence to
finish it — and a critique taken against an earlier diff does not make a later diff ready.

**(a) DISPATCH EARLY — the Cursor dispatch is the FIRST thing out the door, not the last.** In any
wave that contains Cursor work, the dispatch is written and sent BEFORE the Claude crews start
building, so Cursor's build time overlaps Claude work instead of following it. A dispatch sent after
the Claude work is finished has paid the lane's entire latency cost and bought none of its
parallelism, which is how a lane that draws zero Claude credit still ends up feeling slower than
doing it in Opus. THREE failure modes come with dispatching first. All three are the planner's to
handle rather than the reviewer's to discover, and none of them is mechanised — they are gate
discipline, in the same unmechanised class as `fable_phases` and the receipt (open items 2 and 5):
- **The agent reads the briefing that exists AT DISPATCH TIME.** `AGENTS.md` and
  `docs/BRIEF-PACK.md` are regenerated by the wave that is still running, so an early-dispatched
  agent is briefed on the PRE-WAVE state by construction — and per the `AGENTS.md` assumptions
  above, a re-used agent may be working from an even older cached copy. That is acceptable when the
  dispatched task does not depend on text the wave is still writing, and it is a planning DEFECT
  when it does. Dispatch early only what is independent of the wave's own unlanded edits; when the
  task does depend on them, either hold the dispatch or carry the needed text INLINE in the dispatch
  statement, where it arrives through the one channel the agent certainly reads.
- **The base moves under the open PR.** The wave lands on `main` while the branch is still open, so
  a check that went green against the dispatch-time base may be green against a base that no longer
  exists. CI green is only evidence on the CURRENT base: before merging, the gate confirms the
  branch is up to date with `main` and that `verify-docs` passed on that updated base, re-running it
  if the update was not itself a run. A stale green is the green-by-absence problem in new clothes.
  **Stated as the limit it is:** ruleset `protect-main-cursor-lane` today requires only that `main`
  take pull requests — it does NOT require branches to be up to date before merging, so this is a
  gate READING and not a merge CONDITION. Turning on that requirement (and making `verify-docs` a
  required status check) would mechanise it, and is the standing next step for whoever next has
  repository-settings hands; until then, a gate that skips this check leaves no trace.
- **The wave and the early PR regenerate the SAME four files.** An early-dispatched PR that touches
  `docs/**` or `tools/**` must carry regenerated briefings to pass CI, while the wave regenerates
  `docs/BRIEF-PACK.md`, `docs/GROK-CONTEXT.txt`, `AGENTS.md` and `docs/SYSTEM-MAP.html` onto `main`
  underneath it — so the PR arrives stale, or conflicted, or both, and its CI can go red through no
  fault of its content. This is expected, not a defect in the PR. It is resolved exactly as
  `docs/EFFICIENCY-MODE.md` → PARALLEL CREWS already requires for the GENERATED SET: **a generated
  file is NEVER conflict-resolved by hand.** The gate takes either side to make the merge complete
  and then RE-RUNS both generators over the merged tree before the merge commit is final. Prefer
  dispatching early work that does NOT need to carry the generated set at all; where it must, expect
  the red check and read it as staleness rather than as failure.

**(b) POUNCE — a green PR is picked up, not remembered.** The responsible unit polls the pull
request and begins the review THE MOMENT CI goes green: the Grok diff critique runs immediately, and
its evidence is staged for the gate rather than reconstructed later. **WHO polls is named at
dispatch, and it is never Fable mid-run.** Polling a pull request is not supervising a crew — it is
crew work, written into the dispatching unit's own work order, so it does not touch the autopilot
rule that Fable stays out of the room between spawn and return (`docs/EFFICIENCY-MODE.md` →
Autopilot lane). The poller is therefore the dispatching CREW unit, or the GATE at its own sitting;
if a plan names Fable as the poller it has misread both rules. The dispatching unit owns the poll
from the moment the dispatch goes out and holds it until it either harvests the PR itself or hands
the duty on — **and a hand-off is only real when it is written in the baton**, naming the unit that
holds it now. A duty handed on in conversation has been dropped, because the next run reads the file
and not the conversation.

**If a run ends with a green unharvested PR, the baton NAMES it** — PR number, branch, what it was
dispatched to do, the `verify-docs` run id with the time it was observed, and who holds the poll
now. Two things that naming is NOT. It is **not a harvest**: a sitting that names PRs instead of
merging them has recorded an outstanding obligation, not discharged one, and it says WHY each named
PR was not harvested rather than letting the naming stand as the outcome. And the CI line in the
baton is **evidence of an observation, not of current state** — the next run RE-QUERIES the check
before acting on it, because a PR can go red or gain commits between two runs and a copied string
would merge on a receipt for a build that no longer exists. Say plainly what all of this is: there
is no watcher and no webhook in this system, so pouncing is a unit doing it or a run reading the
baton, and an unnamed PR is one nobody is polling. The named-in-the-baton rule is the whole
mechanism, and it fails exactly the way the lean-scribe deferral fails — a run that never happens
never harvests anything.

**(c) BATCH HARVEST — several ready PRs may be swept in one gate sitting; the RECORDS never merge.**
When more than one pull request is harvest-ready, one gate sitting may review and merge them
together. What may NOT be pooled is the evidence: **each PR keeps its OWN `cursor_dispatch` record
and outcome, and its OWN diff critique at its own depth.** A single critique covering four diffs is
one critique, not four, and a merged record cannot be overturned per PR — the same reasoning that
gives `docs/EFFICIENCY-MODE.md` → BATCH GATING one `gate_ratification` record per run. This TIGHTENS
the lane's own precedent rather than restating it, and the precedent is named rather than quietly
dropped: the pilot took ONE batched routine critique across BOTH open pull requests (journal record
55). That is superseded here. One scribe landing may still carry several records in one commit —
that is a transport saving, never a review saving.

**The two record shapes that would still PARSE, named so a gate can refuse them rather than
discover them.** `tools/validate_journal.py` checks that the required keys are PRESENT; it cannot
count PRs. So both of these pass the validator and are nonetheless violations of this rule: a single
`grok_critique` whose `target` lists several pull requests (exactly record 55's shape), and a single
`cursor_dispatch` whose `branch_or_pr` names more than one PR. **One record, one PR, both types** —
if the field would have to name two, the record should have been two records.

**BATCH-HARVEST ELIGIBILITY is a hard test, not appetite** — the same discipline
`docs/EFFICIENCY-MODE.md` → BATCH ELIGIBILITY applies to batched gating, and for the same reason. A
PR is INELIGIBLE for batch harvest and is harvested ALONE if any of these hold: its diff is
SIGNIFICANT by the standing test (rule text, routing, safety or hard stops, or a multi-file rule
change), in which case it takes the full 3-pass ladder on its own rather than a batched routine
pass; it touches anything outside `docs/**` and `tools/**`; its scope or its quality is contested by
anyone in the sitting; or it carries the generated set while the same wave regenerated those files,
per (a). When unsure → not batchable, the same direction the significance test already runs in.
**Out-of-scope PRs are still CLOSED UNMERGED, exactly as PR #1 was**, and scope is judged per PR: a
batch is not a bundle, and a PR does not inherit its siblings' compliance. The abuse to name so a
gate can refuse it, and it is the same one batch gating names: a batch used to carry a marginal PR
through on the attention its siblings are absorbing. Reviewing four diffs in one sitting is less
adversarial than reviewing one, which is why these tests are drawn tight rather than left to
judgement. **And when a batch harvest happens inside an autopilot gate, the one
`gate_ratification` record that lane writes must ENUMERATE each PR's critique record in
`dispositions_reviewed`** — one run-level record may cover the sitting, but it may not blur which
PR got which read.

**(d) THE INSPECTION FLOOR IS NON-COMPRESSIBLE.** Every pull request merges on `verify-docs` CI
green **plus** a Grok critique of the diff **plus** a Claude gate merge — every PR, at every batch
size, under every credit state and against every deadline. This is a restatement of the routing
directive's own scope paragraph in both package files, not a new rule and not a softer one: no
credit state, `CLAUDE_CRITICAL` included, authorizes skipping or thinning a Claude gate, a critique
pass, or the Cursor merge review, because scarcity buys fewer and shorter runs and never cheaper
reviews.

**The one credit exception that exists, reconciled here rather than left to be discovered as a
loophole.** Both package files carry, under Critique policy: *"Credit exception (frequency only,
never depth): under CLAUDE_CRITICAL, ROUTINE critiques may be deferred or batched."* That exception
is real and is not amended here — but read against the routing directive's scope paragraph in the
same files, which names **the Cursor merge review** among the things no credit state may skip or
thin, it means exactly two things in this lane and nothing else. DEFERRED means **the MERGE waits**,
not that the merge proceeds on a critique that has not happened: a deferred critique is an unmerged
PR, not a merged one with an IOU. BATCHED means the SITTING is batched, which is precisely what (c)
permits and bounds — one sitting, still one critique per PR. A reading under which `CLAUDE_CRITICAL`
lets a Cursor PR merge with no diff critique, or with one critique shared across several, has used
a frequency exception to buy depth, which its own parenthesis forbids.

**Pipelining removes WAITING, never CHECKING.** Any reading of (a), (b) or (c) that ends in one
fewer critique, one skipped CI conclusion, or a merge performed by something other than a Claude
gate has misread this section, and the correct response to being behind schedule is a smaller batch,
not a thinner one. **A critique is evidence for the diff it was taken against.** If the base moved
or the branch gained commits after the critique ran, the staged critique is stale for merge purposes
and the diff is re-critiqued before the merge — reusing it would let a review of an older tip stand
as the receipt for a newer one, which is the same defect as a stale CI green wearing a fresh face.

**(e) Timing expectation, on the record so it can be checked rather than felt.** Run this way, the
lane's cost for a dispatched task is roughly CURSOR BUILD TIME plus the inspection — the inspection
being the diff critique and the gate merge, which are the only parts this system performs. **Be
precise about "the inspection", because a single number here would be an overpromise.** A ROUTINE
single-diff harvest is minutes: the lane's own pilot critique ran 150s (record 55) and the merge is
one action. A SIGNIFICANT diff is not: it takes the full 3-pass ladder, and this system's observed
ladders have run 210s/344s/294s and 218s/40s/97s per pass, so the honest figure there is tens of
minutes, not "a few". Three further caveats, none waived. Cursor build time runs on Cursor's servers
and is OUTSIDE this system's control: it is not a commitment, nothing may be cut to meet it, and
Ultra's usage limits are still UNMEASURED (see Honest limits), so a queue or a cap on that side
makes build time arbitrary and nothing here would even observe it. The inspection figure assumes a
unit is actually polling; a PR nobody is polling costs whatever the gap to the next run is, which is
the cost (b) exists to remove and the reason the baton names it. And every number above is a
RECORDED OBSERVATION from past runs, not a measurement of this procedure — which has never been
run. Nothing in this section may be quoted as a deadline, and a run that finds itself behind the
expectation takes the extra minutes rather than the shortcut.

### What this procedure COSTS — the part a speed rule usually leaves out

Written from the ladder's own adversarial pass, because a procedure that only lists its benefits has
not been reviewed.

**It removes the only accidental throttle the lane had.** Work skips Cursor today because Cursor is
slow. That latency was never a control, but it FUNCTIONED as one: it kept volume low in a lane whose
review culture has never once said no on QUALITY. Take the latency away and the Cursor-first default
in `docs/EFFICIENCY-MODE.md` — where ties already break TOWARD Cursor — delivers materially more
Cursor commits to `main` with no new quality brake anywhere. That is the price of this section, it
is not hypothetical, and it is stated here so nobody can say it was sold as free. **The evidence
base under it is thin and stays thin:** one merged pilot (PR #2, a docs-only self-introduction), one
scope rejection (PR #1), and ZERO quality rejections ever. Scaling throughput on that record is a
deliberate policy choice taken on the Owner's order, not a conclusion the evidence supports.

**The exact sequence that would let a bad merge through, written down so a gate can watch for it
rather than discover it.** Plan dispatches Cursor first against a pre-wave briefing → the agent
opens the PR early → `verify-docs` greens on the dispatch-time base → the poller pounces and stages
a routine diff critique immediately → the Claude wave lands and moves `main` under the branch → the
end-of-run sitting, already busy ratifying the wave, sweeps several ready PRs at once → the gate
merges → the merged tip is now concurrent with in-flight Claude changes the agent never authored
against, reviewed under batch attention, with a docs/tools CI pack as the only mechanical check.
Every arrow in that chain is permitted by (a) through (c). The defences against it are the
current-base requirement in (a), the re-critique rule in (d), the eligibility test in (c) and the
HARVEST-READY definition — **all four of which are gate readings, none of which is mechanical.**

**`verify-docs` is not an integration check, and this procedure leans on it harder than anything
before it.** CI here runs the validator self-test, `--all`, specguard and the secret scan; it says
nothing about whether a Cursor diff and a concurrent Claude diff mean the same thing after both
land. Early dispatch maximises exactly that divergence, so the integration judgement is human, at
harvest time, in the sitting that is already the busiest turn of the run.

**Attention is zero-sum, and HARVEST LAST concentrates it.** Sweeping every ready PR into the same
sitting that ratifies the Claude wave puts all of the lane's merge judgement on the most loaded
turn. So: **the gate MAY split the harvest into its own sitting, and SHOULD when the wave's
ratification is heavy or the batch is more than small.** Harvest-last is about not blocking the
wave; it is not a requirement to merge everything while tired. Splitting costs a turn and buys the
adversarial reading the merges actually need.

**Two things this section does NOT do, said plainly so its own text cannot be quoted as proof of
safety.** Part (d) is a RESTATEMENT of rules that already exist; it is an anchor for a gate, not a
control, and quoting (d) is never evidence that the floor was honoured — the evidence is the
records: a CI conclusion, a `grok_critique` record per PR, a merge by a Claude gate. And this
procedure FORBIDS the lane's only practiced critique shape (the record-55 batched critique) while
replacing it with discipline nothing checks, which is the same unmechanised class as open items 2
and 5. Forbidding the practiced thing, installing the unexercised thing, and then scaling volume on
top is a real risk ordering, recorded here rather than discovered later.

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
