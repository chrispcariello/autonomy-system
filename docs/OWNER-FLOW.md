# OWNER-FLOW.md — which prompt to paste, and what it costs

For Chris. You do not write code and you should never have to. This file is the map of the four ways
work gets started, in plain words. The prompts themselves live in one place —
`docs/RUN-TEMPLATE.md` — and this file only tells you which one to reach for.

`docs/OWNER-QUICK-REFERENCE.md` is the one-pager on who is who and where things live. This file is the
one-pager on *how a job starts*.

## The one-card principle

Think of `docs/RUN-TEMPLATE.md` as a small stack of index cards. Every prompt you will ever paste is
on one of those cards, already written. You pick a card, drop your job description into the one blank
line at the bottom, and paste it. Nothing else is expected of you.

If a job does not fit any card, that is the signal to use the PLAN card (lane 2) — not to improvise a
new prompt. A card that keeps getting improvised is a card that needs rewriting, and that is a job in
itself.

## The four lanes

### Lane 1 — Routine (the cheap default)

The job is a shape the system has done before. You paste the **START card** into a fresh Opus task and
walk away. The crew builds, has Grok critique it, runs the checkers, lands it, and hands you a HANDOFF
block. Later — same day, next morning, whenever — you paste the **GATE card** into Fable so the
inspector signs it off.

Fable is in the room twice at most, and never while the work is happening. Those are the bookends.

### Lane 2 — Plan-touch (novel work)

The job is new enough that you do not know how to describe it as one order. You paste the **PLAN
card** into Fable. Fable thinks, and hands back a work order: what the goal is, how many runs it takes,
the exact lines to paste, how deep the critique should go, and what "done" looks like. Then it stops —
it does not build anything.

You take that work order, paste it into a fresh Opus task as the START card's task line, and gate in
the same Fable chat when the crew comes back. Two Fable moments, both short.

### Lane 3 — AUTOPILOT (one paste, hands off)

The job is real work and you would rather not be the courier between rooms. You paste the **AUTOPILOT
card** into Fable — once — and that is the whole of your involvement until a verdict comes back.

What happens after that paste:

1. **Fable plans.** Briefly. It writes a complete, standalone work order — one that assumes the reader
   knows nothing about your conversation.
2. **Fable spawns the crew.** One or more Opus execution agents carry that order. Fable then leaves
   the room: while the crew works, the expensive meter is off.
3. **The crew builds.** They read the repo for themselves, make the change, send it to Grok for
   critique at the required depth, run the checkers, and land it — journal and handoff riding the same
   commit as the change.
4. **The crew returns** a short handoff. Nothing else — no transcript, no essay.
5. **Fable gates.** The inspector reads the handoff and the journal, checks the mirror, and returns
   one of three verdicts:
   - **RATIFY** — it holds. Done, recorded, and you are told so.
   - **FIX** — something is wrong. Fable writes a fix order and routes it back to whichever hand suits
     the problem: Opus for building, Cursor for a reviewable branch, Grok for another look. Then it
     re-gates. That loop repeats until the work is ratified, up to **three fix loops**.
   - **BLOCK** — it cannot be finished safely (a hard stop, no critique transport, three fix loops
     spent). It stops and comes to you with what it knows.
6. **You get one message:** the verdict.

Autopilot is the lane to reach for when the job is well-defined but not trivial. It is not a licence to
skip anything — the same critique depth, the same checkers, the same hard stops apply. It only changes
who does the walking between rooms.

**Two honest things about this lane, so you are not surprised by them:**

- **The inspector arrives after the work has landed, not before.** The crew commits, then Fable reads
  it. What stops bad work reaching the repo is the Grok critique and the automatic checkers the crew
  runs first; what the gate stops is a bad *claim* — it can overturn, re-open and order fixes, but it
  cannot un-commit. If a run ends in BLOCK, whatever already landed stays landed and gets written down
  as unratified rather than quietly rolled back.
- **Nobody is watching between the spawn and the return.** That is the whole point of the meter being
  off, and it means there is no timer and no alarm: a crew that gets stuck is noticed when someone next
  looks. So autopilot a job with a clear edge to it, not an open-ended one.

Grok never writes anything in this lane either. If Fable routes a fix to Grok, it is asking for another
critique — the actual edit is always made by a Claude unit that owns it.

### Lane 4 — System surgery (rare, expensive, worth it)

The job changes the rules themselves — hard stops, routing, who is allowed to do what, a version bump
of the rulebook. Fable stays live in the room for the whole run. This is the most expensive shape the
system has, and it is deliberately so: rule changes get the full attention of the most careful reader.

Do not autopilot a rule change. That exemption is written into the rules
(`docs/EFFICIENCY-MODE.md` → what still costs Fable).

## Who bills what

- **Opus (the crew)** — the same Claude subscription as Fable, on a much cheaper meter. This is where
  almost all the work should happen.
- **Cursor background agents** — free while your SuperGrok Heavy stays active. They never push
  anything straight in: their work arrives as a pull request and gets the CI checks, a Grok critique,
  and a Claude gate before it merges. `docs/CURSOR-LANE.md`.
- **Grok** — bills your Grok subscription, not Claude. Critique costs you zero Claude usage, which is
  exactly why critique depth is never the thing being economised.
- **Fable (the inspector)** — bills only at the moments it actually speaks: the plan, the gate, and one
  more moment per fix loop. Every time it re-enters a chat it re-reads that chat, and re-reading is
  charged at a cached discount rather than full price — which is why one long-running chat with a few
  Fable moments beats a new Fable chat each time.

The honest caveat: nothing in this system meters per-model spend. The number actually tracked is how
many times Fable spoke — `fable_phases` in the gate's record. Treat the cost picture above as the
shape, not as a measured bill.

## What has to be true before you paste

- **The desktop app has to be open and this PC awake.** Two things run as hands on your machine: the
  Grok CLI that performs every critique, and the Tier 2 landing that pushes the commit. No machine, no
  critique and no landing.
- **If the hands are not available, the run parks.** It does not guess and it does not declare
  success: it stages the work, reports `BLOCKED_ON_CRITIQUE`, and writes down what it is waiting for.
  You will see that word in the handoff. It clears when the machine comes back and the critique
  actually runs — never by someone deciding it looked fine.

## Starting a new project

There is no franchise kit yet — that is a roadmap item, not something you have. Say so rather than
expecting a button.

What works today: bootstrap the new project the same way as any other job, by writing its setup as the
task line on a START or AUTOPILOT card ("stand up repo X with the same landing protocol, journal and
critique policy as autonomy-system"). Attach the new repo at session creation so it can land natively,
and clone it beside the standing clone as `<project>-live` for Tier 2 (`docs/LANDING-PROTOCOL.md`).

## Where things live

- **On this PC:** `C:\Users\chris\autonomy-system-live` — the standing clone. This is what the landing
  script fast-forwards and pushes.
- **Drive mirror (public, read-only):** folder `1E-0tL4DGXk-HVYNlWUc6ccF6SzZh60OE`. Refreshed by
  Actions on every push to `main`. This is the copy you send Grok or show anyone; Grok can never open
  the repo itself.
- **GitHub (private, canonical):** `chrispcariello/autonomy-system`. The one true copy. Never hand its
  link to Grok — Grok cannot read it, and a link it cannot open produces confident review of a file it
  never saw.

## Related

`docs/RUN-TEMPLATE.md` (the cards) · `docs/EFFICIENCY-MODE.md` (the run shape and the Fable budget) ·
`docs/OWNER-QUICK-REFERENCE.md` (who is who) · `docs/HANDOFF-FORMAT.md` (the block you get back) ·
`docs/LANDING-PROTOCOL.md` (how a commit reaches the repo).
