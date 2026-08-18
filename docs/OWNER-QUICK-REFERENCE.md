# OWNER QUICK REFERENCE — one page

For Chris. Everything you need to run the system without reading the full package.

## The two links

- **Canonical repo (private, yours):** https://github.com/chrispcariello/autonomy-system
  The one true copy. Claude writes here. Grok cannot open it — it is private.
- **Drive mirror (public, read-only link):** https://drive.google.com/drive/folders/1E-0tL4DGXk-HVYNlWUc6ccF6SzZh60OE
  Auto-updated from the repo on every push. This is what you send Grok, or anyone else you want to
  show the system to. Anyone with the link can read; nobody can edit.

## Who does what

- **Claude Fable 5 Max/Ultracode** — orchestrates and gates. Decides, routes, verifies, says done.
- **Claude Opus 5 Max/Ultracode** — does the work. All other Claude execution: edits, builds, sweeps.
- **Grok Heavy** — critique and advice only. Never writes. Output is UNVERIFIED until Claude verifies it.
- **Grok Build** — volume work (drafts, bulk edits). Same rule: UNVERIFIED, never authority.
- **Cowork** — hands: browser, desktop, activation. Not a source of truth, no live-write authority,
  cannot approve its own output.

## How to start a run

1. Claude app → **Code** tab → **new session** → **Select repo: `autonomy-system` AT CREATION.**
   The repo must be attached when the session is created. Adding it mid-session is broken right now
   (desktop picker defect, logged as an open item) and an unattached session cannot push.
2. Paste your order into that session. Fable orchestrates it; Opus units execute.
3. Use Cowork for hands-only jobs — clicking, browsing, screenshots, checking credits. Never as the
   place where files get written.

## Efficiency with quality

- Cheap runs come from doing critique **less often**, never from doing it **less well**.
- **Routine work → 1 Grok Heavy pass.** Small edits, formatting, journal appends.
- **Significant work → 3-pass ladder:** Pass 1 Defects → Pass 2 False-green → Pass 3 Final adversarial.
  Significant = system rules, routing, safety or hard stops, multi-file package changes, or anything
  you name significant.
- Claude must apply or explicitly reject each major Grok finding, with a one-line reason in the journal.
  A bare "LGTM" from Grok counts as a FAIL on significant work, not a pass.
- If credits are too low to run the full ladder, the significant change waits. It does not land on
  one thin pass.
- **PC off = critique queues.** Both Grok paths (CLI and browser) need your machine, so when it is off
  the work stages and reports `BLOCKED_ON_CRITIQUE` — it never false-greens, and it clears when a
  critique actually runs.
- Prompts to paste into Grok: `docs/GROK.md`.

## Nightly hygiene (runs itself)

- Fires **01:30 UTC daily = 9:30 PM ET** (during EST months this lands at 8:30 PM ET unless you move it).
  Created as a Claude scheduled task — free, capped at 20 minutes, docs only.
- What it does: credit check (if the browser is reachable) → read the lessons + journal tail → run
  specguard on both package docs → make sure every open item has an owner and an exit criterion →
  one small cleanup → write a nightly journal record → push, so Drive updates.
- Where to look the next morning: `docs/run-journals/run-journal.jsonl` (record type `nightly_hygiene`),
  mirrored to Drive. If a step failed it says so; it never reports green for something it could not do.
- Full detail: `docs/NIGHTLY-HYGIENE.md`.

## Landing (getting work onto the repo)

Three tiers, best first: Tier 1 native push from a repo-attached session · Tier 2 local-shell landing
through your desktop · Tier 3 one-click fallback. Claude uses the highest tier available and tells you
which one it used. Detail: `docs/LANDING-PROTOCOL.md`.

## End of every run

Claude gives you a HANDOFF block: SHA · Drive · Changed · Significant · Grok passes requested · Open
items · Ask Grok. If the SHA line says `STAGED (unpushed)`, nothing landed yet and the reason is on
that line. Format: `docs/HANDOFF-FORMAT.md`.

## Hard stops (never, without you)

No money. No ledger, inventory, or order writes. No third-party contact. No credentials, tokens, or
secrets — not in the repo, not in Drive, not in chat. Anything irreversible escalates to you first.
