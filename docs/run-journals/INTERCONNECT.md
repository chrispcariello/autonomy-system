# INTERCONNECT — how Claude and Grok share files and hand off

Plain language, no diagram needed. This is the whole loop, in the order it actually happens.

## The loop

1. **GitHub is the one true copy.** The private repo `https://github.com/chrispcariello/autonomy-system`
   holds the real docs. Only Claude writes to it, from a session that had the repo attached at creation.
   If a fact is not in the repo, it is not a fact yet.

2. **Every push mirrors itself to Drive.** The Actions workflow `.github/workflows/sync-docs-to-drive.yml`
   copies `docs/` into the Drive folder `1E-0tL4DGXk-HVYNlWUc6ccF6SzZh60OE` on every push to `main`.
   Nobody syncs by hand. The mirror is downstream of the repo, never the other way round: editing a file
   in Drive changes nothing and will be overwritten on the next push.

3. **Drive is public-read, so Grok reads the same files.** The mirror folder and its files are shared
   anyone-with-the-link, read-only (verified 2026-08-18). Claude gives Grok the Drive links and Grok
   opens the exact text that just landed — not a paraphrase, not a stale paste. The repo itself is
   private and Grok cannot open it, which is precisely why the mirror exists. Per-file links and the
   ready-made prompts are in `docs/GROK.md`.

4. **Grok's bullets come back as UNVERIFIED.** Grok returns blunt numbered bullets with evidence
   pointers, either straight into the Claude session or pasted in by the Owner. Either way the status is
   the same: UNVERIFIED. Grok has no write path — it cannot change a file, close an item, or approve
   anything.

5. **A Claude gate applies or rejects, in writing.** Fable 5 (or the gating Claude for that run) takes
   each major finding and either applies it or rejects it, with a one-line reason recorded in the run
   journal. Silence is not a decision. An "LGTM" or an empty critique is a FAIL on significant work, so
   the pass gets re-scoped and re-asked rather than banked. Routine work gets 1 pass; significant work
   gets the 3-pass ladder (Defects → False-green → Final adversarial).

6. **The result lands per the landing protocol.** Best available tier from `docs/LANDING-PROTOCOL.md`
   (Tier 1 native push → Tier 2 local-shell → Tier 3 one-click fallback), the push fires Actions, Actions
   refreshes Drive, and Grok's next read is already the new version. Loop closed.

## The baton

Every run ends with the same block, so the next session (or the Owner, or Grok) can pick up cold:

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

`SHA` is a pushed commit or exactly `STAGED (unpushed)` — never a prediction. `Significant` decides
whether the next critique is 1 pass or 3. `Ask Grok` is a concrete question, not a topic. Field rules
and a filled example: `docs/HANDOFF-FORMAT.md`.

## What has no authority here

Cowork is hands — browser, desktop, activation, screenshots. It is not a git source of truth and holds
no live-write authority, so nothing it produces enters the loop except as UNVERIFIED evidence. Grok
Build is the same: volume in, verification by Claude before anything lands.

## Phase 2 interconnect (deferred — $0 tiers available, none required now)

Nothing was installed this patch and nothing needs to be: the core interconnect is docs + GitHub +
Actions + Drive, all already live and free. For the record, the free options considered and deliberately
deferred are — **Cursor**: NO LONGER DEFERRED. Ordered into the system by Owner order 2026-08-18
("implement cursor now to this system") as a second BUILDER pool on the Ultra tier bundled with
SuperGrok Heavy, not as the hand-edit surface described here — accounts connected per Owner report,
but ACTIVATION PENDING until a pilot PR clears the review lane; mechanics in `docs/CURSOR-LANE.md`,
activation evidence tracked as PATCH-NOTES open item 15. Still deferred: **Composio + a Grok bot free tier**: the path to a
*toolized* Grok that could fetch and act instead of only reading and critiquing, worth activating when
Grok genuinely needs to DO things, not before; **LangGraph (free)**: a real orchestrator graph if the
flows ever outgrow docs + Actions, which they have not; and **GraphQL**: unnecessary for a docs and
Event-Bus architecture with no queryable API surface — do not introduce it. Those three stay unbuilt until
an Owner order says otherwise; Cursor is the one that got such an order.
