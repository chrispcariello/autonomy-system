# AGENTS.md — briefing for agents working this repository

> **GENERATED FILE — do not hand-edit.** `tools/gen_brief.py` writes this file from the
> canonical documents. Hand edits are overwritten on the next regeneration and are invisible
> to review. If this file and a canonical document disagree, **the canonical document wins**
> and this file is stale: run `python3 tools/gen_brief.py` and commit the result.

Current version: **v4.1.16**. Manifest stamp: `e405e08feca76293a8d205095d68d9c8a7d81fff40e8a5fef78dc1421a2cc643`
(the digest over the canonical sources this briefing was generated from — it must match the
MANIFEST in `docs/BRIEF-PACK.md`).

## What this repo is

The rulebook and evidence trail of Chris Cariello's autonomous multi-agent system. It is
DOCUMENTATION AND TOOLING, not an application: Markdown rules under `docs/`, stdlib-Python
checkers under `tools/`, a GitHub Actions workflow that verifies both and mirrors `docs/` to a
public read-only Drive folder. There is no build, no test suite beyond the checkers, and no
runtime. Changing a sentence here changes how live agents behave, which is why the review
lane below is heavier than the file sizes suggest.

## Read this first

1. `docs/BRIEF-PACK.md` — the current-state brief: version, roles, Hard Rules verbatim,
   critique ladder, record schemas, landing tiers, open items, and the latest handoff.
2. Confirm the pack is fresh before you trust it: `python3 tools/validate_journal.py --all`
   runs a BRIEF-PACK staleness check that recomputes every manifest hash. A stale pack is a
   FAIL naming the files that moved.
3. Only then read the canonical documents themselves, and always read them directly for
   anything you are about to change.

## Your scope, if you are not the Claude surface

- **`docs/**` and `tools/**` ONLY, and by PULL REQUEST only.** Never push to `main`. A PR that
  touches anything else is OUT OF SCOPE and gets CLOSED without merge, not tidied up by the
  reviewer. This has already happened once (PR #1) — it is enforced, not advisory.
- Your PR is UNVERIFIED input under Hard Rule 3. It merges only after `verify-docs` CI, a Grok
  critique of the diff, and a Claude gate merge. Nothing you write is landed until a Claude
  unit merges it.
- Hard stops bind every lane: never touch money, ledgers, credentials, or third-party
  accounts, and never contact anyone. If a task appears to require one of those, stop and say
  so in the PR instead of improvising around it.
- Do not edit `CLAUDE.md`, the two package files (`docs/SYSTEM-CURRENT.md`,
  `docs/SYSTEM-SPEC-CURRENT.md`), or the Hard Rules unless your task names them explicitly.

## Conventions

- **The run journal is Claude-only.** Never append to, edit, or reformat
  `docs/run-journals/run-journal.jsonl`. Never edit `docs/PATCH-NOTES-CURRENT.md` or
  `docs/LATEST-HANDOFF.md` from the PR lane either: those are the gate's evidence surfaces and
  the Claude unit that owns a run writes them in the same commit as its change.
- **Generated files are outputs, not documents.** `docs/BRIEF-PACK.md`, `docs/GROK-CONTEXT.txt`
  and this file are written by `tools/gen_brief.py`. Never hand-edit them. If your change
  touches `docs/**` or `tools/**`, RERUN the generator and commit its three outputs in the same
  commit — the staleness check in `tools/validate_journal.py --all` fails the build otherwise.
  If you cannot run Python in your environment, say so in the PR description; the Claude gate
  regenerates before merging and your PR is expected to fail that check until it does.
- **Style:** plain Markdown, no HTML, no emoji. Keep prose lines wrapped near 100 characters to
  match the existing files. State honest limits rather than rounding them off — "not verified
  this run" is a correct sentence here and a preferred one.
- **Evidence over assertion.** Do not write that something passed, synced, or landed unless you
  observed it. Anything you could not check is named as unchecked, with the reason.
- Your PR description must carry the task statement verbatim plus your own self-review notes:
  what you changed, what you deliberately did not change, and what you are unsure about.

## Honest limits of this briefing

This file is a briefing, not a permission system. Nothing here can stop an agent that ignores
it: the enforcement is the PR scope check, CI, the Grok critique and the Claude gate merge —
this file only makes the rules legible before the work starts instead of after. It also assumes
outside agents read repo-root `AGENTS.md` at all; that assumption is why the Cursor dispatch
template in `docs/RUN-TEMPLATE.md` names this file and `docs/BRIEF-PACK.md` explicitly, rather
than relying on the convention alone.
