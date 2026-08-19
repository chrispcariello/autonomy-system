#!/usr/bin/env python3
"""gen_brief.py — generate the three lane briefings from the canonical documents.

Stdlib only, no network, DETERMINISTIC: the same inputs produce byte-identical outputs.
There is no wall-clock timestamp anywhere in what this script writes, so re-running it on an
unchanged tree is a no-op and `git status` stays clean. That property is what makes the
staleness check in `tools/validate_journal.py` meaningful — a diff after regeneration means an
INPUT changed, never that the clock moved.

Outputs (all three are GENERATED; none may be hand-edited):

  docs/BRIEF-PACK.md    the condensed crew operating brief. Hard Rules and the other
                        authority text are EXTRACTED VERBATIM from their canonical
                        sections — never paraphrased, because paraphrase is the drift
                        vector this pack would otherwise introduce.
  docs/GROK-CONTEXT.txt the system snapshot prepended to every Grok prompt file. Hard
                        constraints (pure ASCII, no double quotes, no apostrophes, no
                        dash-led line, <= 1500 chars) are ENFORCED here, not hoped for.
  AGENTS.md             the repo-root briefing Cursor and other outside agents read.

Design notes that a reader should not have to reverse-engineer:

* The MANIFEST covers the RULE SOURCES, not the evidence surfaces. `docs/run-journals/`
  is deliberately excluded: it is append-only evidence, it grows on every landing, and
  including it would force a regeneration for a journal append that changed no rule.
  The cost of that choice is stated in the pack itself rather than hidden here.
* `tools/validate_journal.py` IS a source, because the pack's record-schema summary is
  read out of that module's own constants. The summary therefore cannot drift from the
  checker; changing the checker forces a regeneration, which is the intended coupling.
* Missing or unreadable source = loud failure and a non-zero exit. A brief generated from
  a hole is worse than no brief, because it looks current.
"""

import argparse
import hashlib
import importlib.util
import os
import re
import sys

# ------------------------------------------------------------------ constants

# Order is FIXED and is part of the output contract: the manifest digest is a hash over
# this sequence, so re-ordering it would change every generated file for no reason.
SOURCES = (
    "CLAUDE.md",
    "docs/SYSTEM-CURRENT.md",
    "docs/SYSTEM-SPEC-CURRENT.md",
    "docs/EFFICIENCY-MODE.md",
    "docs/RUN-TEMPLATE.md",
    "docs/GROK.md",
    "docs/LANDING-PROTOCOL.md",
    "docs/HANDOFF-FORMAT.md",
    "docs/CURSOR-LANE.md",
    "docs/OWNER-FLOW.md",
    "docs/NIGHTLY-HYGIENE.md",
    "docs/lessons/lessons.jsonl",
    "docs/PATCH-NOTES-CURRENT.md",
    "docs/LATEST-HANDOFF.md",
    "tools/validate_journal.py",
)

OUT_PACK = os.path.join("docs", "BRIEF-PACK.md")
OUT_GROK = os.path.join("docs", "GROK-CONTEXT.txt")
OUT_AGENTS = "AGENTS.md"

GROK_MAX_CHARS = 1500
# The variable last-land summary is capped well below the remaining budget on purpose: the
# fixed authority lines and the pointer to the full pack are worth more to a critique pass
# than another 200 characters of a run-on history row.
GROK_SUMMARY_MAX = 260
PACK_TARGET_LINES = 350
ZERO_DIGEST = "0" * 64
SELF_DIGEST_RE = re.compile(r"^SELF-DIGEST: [0-9a-f]{64}$", re.MULTILINE)


class GenError(Exception):
    """A condition that must stop generation loudly rather than produce a plausible file."""


def sha256_text(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_source(root, rel):
    path = os.path.join(root, rel)
    if not os.path.isfile(path):
        raise GenError("canonical source missing: %s" % rel)
    try:
        with open(path, "r", encoding="utf-8") as handle:
            text = handle.read()
    except OSError as exc:
        raise GenError("canonical source unreadable: %s (%s)" % (rel, exc))
    if not text.strip():
        raise GenError("canonical source is empty: %s" % rel)
    return text


# ------------------------------------------------------------ text extraction


def extract_section(text, heading, rel):
    """Return a heading and its body VERBATIM, up to the next heading of the same or
    higher level. Verbatim is the whole point: a summariser here would reintroduce the
    paraphrase drift the pack exists to remove."""
    lines = text.split("\n")
    level = len(heading) - len(heading.lstrip("#"))
    start = None
    for index, line in enumerate(lines):
        if line.strip() == heading:
            start = index
            break
    if start is None:
        raise GenError("section %r not found in %s" % (heading, rel))
    end = len(lines)
    for index in range(start + 1, len(lines)):
        line = lines[index]
        if line.startswith("#"):
            found = len(line) - len(line.lstrip("#"))
            if found <= level and line[found:found + 1] == " ":
                end = index
                break
    body = "\n".join(lines[start:end]).rstrip()
    if not body:
        raise GenError("section %r in %s is empty" % (heading, rel))
    return body


def extract_lines_matching(text, pattern, rel, what):
    found = [line.rstrip() for line in text.split("\n") if pattern.search(line)]
    if not found:
        raise GenError("no %s lines found in %s" % (what, rel))
    return found


def current_version(system_current, rel):
    match = re.search(r"^#\s+SYSTEM\s+(v[0-9][0-9A-Za-z.\-]*)\s", system_current, re.MULTILINE)
    if not match:
        raise GenError("cannot read the version from the %s title line" % rel)
    return match.group(1)


def newest_history_row(system_current, rel):
    rows = [
        line for line in system_current.split("\n")
        if re.match(r"^- \*\*v[0-9]", line)
    ]
    if not rows:
        raise GenError("no version-history rows found in %s" % rel)
    return rows[-1]


OPEN_ITEMS_HEADING = re.compile(r"^##\s+REMAINING OPEN ITEMS", re.IGNORECASE)
NUMBERED_ITEM = re.compile(r"^(\d+)\.\s+(.*)$")
COUNT_LINE = re.compile(r"\*\*(\d+) listed, (\d+) open\*\*")


def open_items(patch_notes, rel):
    """Numbers, titles and open/closed state from the LAST open-items section — the same
    section `validate_journal.py --open-items` treats as authoritative."""
    lines = patch_notes.split("\n")
    starts = [i for i, line in enumerate(lines) if OPEN_ITEMS_HEADING.match(line)]
    if not starts:
        raise GenError('no "## REMAINING OPEN ITEMS" section in %s' % rel)
    start = starts[-1]
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    items = []
    counts = None
    for index in range(start + 1, end):
        line = lines[index]
        found = COUNT_LINE.search(line)
        if found:
            counts = (int(found.group(1)), int(found.group(2)))
        match = NUMBERED_ITEM.match(line)
        if not match:
            continue
        number, body = match.group(1), match.group(2)
        closed = body.lstrip().startswith("~~")
        title = re.sub(r"[*~`]", "", body)
        title = title.split(" — ")[0].split(" - ")[0].split(". ")[0].strip()
        if len(title) > 78:
            title = title[:75].rstrip() + "..."
        items.append((int(number), title, "CLOSED" if closed else "OPEN"))
    if not items:
        raise GenError("open-items section in %s has no numbered items" % rel)
    return items, counts


# --------------------------------------------------------- ASCII enforcement

ASCII_MAP = {
    "—": "-", "–": "-", "‒": "-", "−": "-",
    "‘": "", "’": "", "‚": ",", "‛": "",
    "“": "", "”": "", "„": "", "‟": "",
    "…": "...", "·": "|", "•": "*", " ": " ",
    "→": "->", "←": "<-", "⇒": "=>", "≤": "<=",
    "≥": ">=", "≠": "!=", "×": "x", "✓": "yes",
    "✗": "no", "£": "GBP ", "€": "EUR ", "″": "",
    "′": "", "«": "", "»": "", "﻿": "",
}


def to_grok_ascii(text):
    """TRANSFORM until the hard constraints hold. Every rule here is enforced, not
    documented and hoped for: the Grok CLI rejects or mangles double quotes, apostrophes
    and dash-led lines in a prompt file, so a prompt that violates them is a failed pass."""
    for source, target in ASCII_MAP.items():
        text = text.replace(source, target)
    text = text.replace('"', "").replace("'", "")
    text = "".join(ch if (32 <= ord(ch) < 127 or ch == "\n") else " " for ch in text)
    cleaned = []
    for line in text.split("\n"):
        stripped = line.lstrip()
        if stripped.startswith("-"):
            line = line[:len(line) - len(stripped)] + "*" + stripped[1:]
        cleaned.append(line.rstrip())
    text = "\n".join(cleaned)
    while "\n\n\n" in text:
        text = text.replace("\n\n\n", "\n\n")
    return text.strip() + "\n"


def assert_grok_constraints(text):
    problems = []
    try:
        text.encode("ascii")
    except UnicodeEncodeError as exc:
        problems.append("non-ASCII byte survived the transform: %s" % exc)
    if '"' in text:
        problems.append("double quote survived the transform")
    if "'" in text:
        problems.append("apostrophe survived the transform")
    for number, line in enumerate(text.split("\n"), start=1):
        if line.lstrip().startswith("-"):
            problems.append("line %d starts with a dash" % number)
    if len(text) > GROK_MAX_CHARS:
        problems.append("%d chars exceeds the %d-char ceiling" % (len(text), GROK_MAX_CHARS))
    if problems:
        raise GenError("GROK-CONTEXT constraint failure: " + "; ".join(problems))


# ------------------------------------------------------- record-schema import


def load_validator(root):
    """Read the record schemas out of the checker itself, so the pack's summary cannot
    drift from what actually fails the build."""
    path = os.path.join(root, "tools", "validate_journal.py")
    if not os.path.isfile(path):
        raise GenError("canonical source missing: tools/validate_journal.py")
    spec = importlib.util.spec_from_file_location("_vj_for_brief", path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as exc:  # noqa: BLE001 - any import failure must be loud
        raise GenError("cannot import tools/validate_journal.py for schemas: %s" % exc)
    for name in ("CRITIQUE_REQUIRED_KEYS", "CURSOR_DISPATCH_REQUIRED_KEYS",
                 "GATE_RATIFICATION_REQUIRED_KEYS"):
        if not hasattr(module, name):
            raise GenError("tools/validate_journal.py no longer defines %s" % name)
    return module


SCHEMA_OWNERS = {
    "grok_critique": "docs/GROK.md",
    "cursor_dispatch": "docs/CURSOR-LANE.md",
    "gate_ratification": "docs/EFFICIENCY-MODE.md",
}


def assert_no_schema_fork(validator, texts):
    """The pack reads its record schemas from the CHECKER, while `docs/GROK.md` states the
    contract in prose. Those two can fork: change the validator, regenerate, and a green
    staleness check would certify a pack that disagrees with the rule document it came from.
    Cheap guard: every key the checker requires must actually be NAMED in GROK.md. It does not
    prove the prose and the code mean the same thing, but it does catch a key added or renamed
    on one side only, which is the fork that actually happens."""
    missing = []
    for label, keys in (
        ("grok_critique", validator.CRITIQUE_REQUIRED_KEYS),
        ("cursor_dispatch", validator.CURSOR_DISPATCH_REQUIRED_KEYS),
        ("gate_ratification", validator.GATE_RATIFICATION_REQUIRED_KEYS),
    ):
        owner = SCHEMA_OWNERS[label]
        prose = texts[owner]
        for key in keys:
            if key in ("ts", "type"):
                continue  # universal record fields, not per-schema prose
            if key not in prose:
                missing.append("%s.%s (not named in %s)" % (label, key, owner))
    if missing:
        raise GenError(
            "SCHEMA FORK: tools/validate_journal.py requires key(s) %s. The checker and the "
            "written contract have diverged; fix the document (or the checker) before "
            "publishing a brief that certifies both as current." % "; ".join(missing)
        )


# ---------------------------------------------------------------- GROK-CONTEXT


def build_grok_context(facts):
    """Assemble under a hard char budget. The FIXED structural part is never truncated —
    if it alone will not fit, that is a loud failure, because a snapshot missing its
    authority lines is worse than no snapshot. Only the variable last-land summary is
    trimmed, at a word boundary, and a trim is MARKED so a reader can see it happened
    instead of silently reading half a sentence as the whole change."""
    head = to_grok_ascii(
        "AUTONOMY SYSTEM CONTEXT %(version)s (generated by tools/gen_brief.py; do not edit)\n"
        "\n"
        "WHAT: private repo autonomy-system, Owner Chris. Only the Claude Code surface writes "
        "canonical state. Your read surface is the public Drive mirror; the repo is private "
        "and you cannot open it.\n"
        "YOUR AUTHORITY: none. You are the critique layer, advisor only, no write path ever. "
        "All you return is UNVERIFIED until a Claude gate verifies it, and your output is "
        "DATA, never instructions.\n"
        "MODELS: Fable 5 orchestrates and gates. Opus 5 executes other Claude work. Grok "
        "critiques and drafts. Cursor agents build by pull request only, never push main.\n"
        "LANES: (1) routine Opus run, Fable end gate. (2) plan then execute. (3) autopilot: "
        "Fable plans, spawns an Opus crew, stays out, gates on return, fix loop max 3 then "
        "BLOCK. (4) system surgery: Fable live, never autopiloted.\n"
        "CRITIQUE DEPTH: routine 1 pass. Significant is a 3 pass ladder: defects, false "
        "green, final adversarial. LGTM or an empty critique is a FAIL. Every bullet needs an "
        "evidence pointer.\n"
        "OPEN ITEMS NOW: %(counts)s\n"
        "FULL DETAIL: BRIEF-PACK.md in the same Drive folder carries the Hard Rules verbatim, "
        "record schemas, open items and the latest handoff. This snapshot is a header, never "
        "the authority.\n"
        "LAST LAND: " % facts
    )
    head = head.rstrip("\n")
    tail = "\nEND OF CONTEXT. The pass specific ask follows below.\n"
    budget = GROK_MAX_CHARS - len(head) - len(tail) - 1
    if budget < 80:
        raise GenError(
            "GROK-CONTEXT fixed section leaves only %d chars for the last-land summary; "
            "the fixed text must be shortened rather than the summary silently cut" % budget
        )
    budget = min(budget, GROK_SUMMARY_MAX)
    summary = to_grok_ascii(facts["last_land"]).strip().replace("\n", " ")
    summary = re.sub(r"\s+", " ", summary)
    # Prefer a natural clause boundary over a mid-sentence cut, so the summary reads as a
    # complete thought when one fits; only fall back to a marked word-boundary trim.
    if len(summary) > budget:
        clause = summary.split(";")[0].strip()
        if len(clause) <= budget and len(clause) >= 60:
            summary = clause
        else:
            cut = summary[:budget - 14].rsplit(" ", 1)[0]
            summary = cut + " [TRUNCATED]"
    text = head + " " + summary + tail
    text = to_grok_ascii(text)
    assert_grok_constraints(text)
    return text


# -------------------------------------------------------------------- AGENTS


def build_agents(facts, manifest_digest):
    return """# AGENTS.md — briefing for agents working this repository

> **GENERATED FILE — do not hand-edit.** `tools/gen_brief.py` writes this file from the
> canonical documents. Hand edits are overwritten on the next regeneration and are invisible
> to review. If this file and a canonical document disagree, **the canonical document wins**
> and this file is stale: run `python3 tools/gen_brief.py` and commit the result.

Current version: **%(version)s**. Manifest stamp: `%(digest)s`
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
""" % {"version": facts["version"], "digest": manifest_digest}


# ---------------------------------------------------------------- BRIEF-PACK

PACK_HEADER = """# BRIEF-PACK.md — generated crew operating brief (%(version)s)

> **GENERATED FILE — do not hand-edit.** `tools/gen_brief.py` writes it from the canonical
> documents listed in the MANIFEST at the foot of this file. Hand edits are overwritten on the
> next regeneration, and the `SELF-DIGEST` line below is what makes such an edit detectable.
> **On any conflict between this pack and a canonical document, THE CANONICAL DOCUMENT WINS**
> and this pack is stale. This is a fast path to current state, never an authority: no rule
> lives here first, and nothing may be closed, ratified or landed on this file alone.
>
> **Trust it only after the freshness check passes.** `python3 tools/validate_journal.py --all`
> recomputes every MANIFEST hash and FAILS naming any source that moved. If you cannot run it,
> spot-check the hashes yourself. Read the canonical documents in full on ANY conflict, gap or
> staleness — and read the gate and authority documents directly, always, on surgery-class runs.

SELF-DIGEST: %(self_digest)s
MANIFEST-DIGEST: %(manifest_digest)s
"""


def build_pack(facts, sources, manifest_digest, out_digests):
    sc = facts["system_current"]
    parts = []
    add = parts.append

    add("## Current state at a glance\n")
    add("- Version: **%s** (both package files carry it; the SPEC also carries the date)." % facts["version"])
    add("- Canonical repo: private GitHub `chrispcariello/autonomy-system`; `main` is canon.")
    add("- Public read-only Drive mirror of `docs/**` only — that is Grok's read surface, and")
    add("  `AGENTS.md` plus `tools/**` are NOT mirrored there. Verify those in the repo/clone.")
    add("- Open items: %s." % facts["counts_text"])
    add("- Newest version-history row, verbatim from `docs/SYSTEM-CURRENT.md`:\n")
    add("> " + facts["history_row"].strip())
    add("")

    add("## Roles and model split — VERBATIM from `docs/SYSTEM-CURRENT.md`\n")
    add("```")
    add(facts["model_split"])
    add("```\n")

    add("## HARD RULES — VERBATIM from `docs/SYSTEM-CURRENT.md`, never paraphrased\n")
    add("A paraphrase of a Hard Rule is the drift vector this pack exists to remove, so these")
    add("are copied byte-for-byte by the generator. `CLAUDE.md` carries a condensed restatement")
    add("for session start; where the two differ in wording, the package text below governs.\n")
    add("```")
    add(facts["hard_rules"])
    add("```\n")

    add("## Critique ladder — VERBATIM from `docs/SYSTEM-CURRENT.md`\n")
    add("```")
    add(facts["routine_vs_significant"])
    add("")
    add(facts["critique_ladder"])
    add("")
    add(facts["review_gate"])
    add("```\n")
    add("Prompt blocks, the required output shape, and the transport rules: `docs/GROK.md`.")
    add("Every critique or drafting prompt file begins with the current `docs/GROK-CONTEXT.txt`.\n")

    add("## Journal record schemas — read out of `tools/validate_journal.py` itself\n")
    add("These are the keys whose ABSENCE fails the build, generated from the checker's own")
    add("constants so this summary cannot drift from the check. They are a MINIMUM shape, not")
    add("the full contract: the field semantics live in `docs/GROK.md` (critique + blocked),")
    add("`docs/CURSOR-LANE.md` (dispatch) and `docs/EFFICIENCY-MODE.md` (ratification).\n")
    for label, keys in facts["schemas"]:
        add("- `%s` — required: %s" % (label, ", ".join("`%s`" % k for k in keys)))
    add("- Arithmetic also enforced on `grok_critique`: `len(applied) + len(rejected) ==")
    add("  bullets_count`, always; `bullets_count` 0 on a ladder pass is a FAIL unless the")
    add("  record honestly carries `status` `\"FAIL\"`.")
    add("- **All `ts` values are MACHINE-MEASURED at write time, never estimated** (lesson")
    add("  `L-20260819-01`). Nothing in the validator can catch an invented timestamp.")
    add("- **Schema-fork guard:** generation FAILS when the checker requires a key `docs/GROK.md`")
    add("  never names, so the code and the written contract cannot silently diverge. It does not")
    add("  prove they MEAN the same thing — read `docs/GROK.md` for the semantics.\n")

    add("## Landing tiers — VERBATIM headings and triggers from `docs/LANDING-PROTOCOL.md`\n")
    for line in facts["tier_lines"]:
        add("- " + line.lstrip("# ").strip() if line.startswith("#") else "  " + line.strip())
    add("")
    add("The two invariants runs most often get wrong, verbatim:\n")
    add("```")
    add(facts["landing_invariants"])
    add("```\n")

    add("## Routing directive and the usage receipt — VERBATIM from `docs/SYSTEM-CURRENT.md`\n")
    add("```")
    add(facts["routing_directive"])
    add("```\n")

    add("## Efficiency mode, autopilot and the fix loop — VERBATIM shared block\n")
    add("This block is byte-identical in both package files; it is the authority on run shape.")
    add("The step-by-step mechanics, the fix-loop bound and the receipt rules: `docs/EFFICIENCY-MODE.md`.\n")
    add("```")
    add(facts["efficiency_block"])
    add("```\n")

    add("## HANDOFF block — the eight fields, in this order\n")
    add("```")
    add(facts["handoff_block"])
    add("```")
    add("Field rules: `docs/HANDOFF-FORMAT.md`. `SHA` is a pushed commit or exactly")
    add("`STAGED (unpushed)` — never a prediction.\n")

    add("## The SPEED PACK rules — VERBATIM from `docs/EFFICIENCY-MODE.md`\n")
    add("These are the rules that govern READING THIS PACK, so they are carried here in full")
    add("rather than pointed at: a brief that omits the rules for using briefs installs a")
    add("control nobody in the lane can see.\n")
    add("```")
    add(facts["speed_pack"])
    add("```\n")

    add("## Mid-run re-entry — VERBATIM from `docs/EFFICIENCY-MODE.md`\n")
    add("```")
    add(facts["reentry"])
    add("```\n")

    add("## Where the rules this pack does NOT extract actually live\n")
    add("This pack extracts the package-file authority text verbatim. Whole rule sets live only")
    add("in their own documents and are NOT reproduced here — reading the pack is not reading the")
    add("rules. Go to the document itself before acting on any of these:\n")
    add("| document | what only it carries |")
    add("| :-- | :-- |")
    add("| `docs/EFFICIENCY-MODE.md` | run shape, the SPEED PACK rules (self-brief via pack, regeneration, lean scribe, batch gating, parallel crews), autopilot mechanics, the six re-entry triggers, receipt rules |")
    add("| `docs/RUN-TEMPLATE.md` | the five copy-paste blocks: activation, gate, Cursor dispatch, plan, autopilot |")
    add("| `docs/GROK.md` | prompt blocks, transport, the GROK CONTEXT rule, critique journal contract, queue + `critique_blocked` |")
    add("| `docs/LANDING-PROTOCOL.md` | the three tiers in full and every landing invariant |")
    add("| `docs/HANDOFF-FORMAT.md` | the per-field rules for the eight HANDOFF fields |")
    add("| `docs/CURSOR-LANE.md` | dispatch procedure, the three review legs, `AGENTS.md` assumptions and their limits |")
    add("| `docs/OWNER-FLOW.md` | the Owner-facing lane map and receipts, in lay language |")
    add("| `docs/NIGHTLY-HYGIENE.md` | the unattended nightly steps and their caps |")
    add("| `AGENTS.md` | the standing briefing outside agents read (generated; repo root, NOT mirrored to Drive) |")
    add("")

    add("## Open items — numbers, titles and state\n")
    add("Authoritative list: the LAST `## REMAINING OPEN ITEMS` section of")
    add("`docs/PATCH-NOTES-CURRENT.md`. Titles below are shortened for scanning; never close,")
    add("re-open or renumber an item from this pack — read the section itself.\n")
    add("| # | State | Title |")
    add("| --: | :-- | :-- |")
    for number, title, state in facts["open_items"]:
        add("| %d | %s | %s |" % (number, state, title.replace("|", "/")))
    add("")
    add("Count line in force: %s\n" % facts["counts_text"])

    add("## docs/LATEST-HANDOFF.md — copied in full\n")
    add(facts["latest_handoff"].rstrip())
    add("")

    add("## MANIFEST\n")
    add("Each canonical source with the sha256 of its content at generation time.")
    add("`tools/validate_journal.py --all` recomputes these; any mismatch is a FAIL naming the")
    add("stale files, and that failure is the mechanical backstop behind the regeneration rule.\n")
    add("Cross-file guard: the shared `### Efficiency mode (Fable bookends)` block was verified")
    add("BYTE-IDENTICAL across both package files at generation, sha256 `%s`." % facts["shared_block_sha"])
    add("Generation FAILS when it is not — the one cross-file consistency check that exists today.\n")
    add("| source | sha256 |")
    add("| :-- | :-- |")
    for rel in SOURCES:
        add("| `%s` | `%s` |" % (rel, sources[rel]))
    add("")
    add("Generated outputs, hashed so a hand-edit of them is detectable too:\n")
    add("| generated file | sha256 |")
    add("| :-- | :-- |")
    for rel in (OUT_GROK, OUT_AGENTS):
        add("| `%s` | `%s` |" % (rel.replace(os.sep, "/"), out_digests[rel]))
    add("")
    add("**What the MANIFEST deliberately does NOT cover, so nobody reads more into it:**")
    add("(1) `docs/run-journals/**` — append-only evidence, not a rule source; including it would")
    add("force a regeneration per journal append. (2) The source list is a CLOSED SET: a")
    add("rule-bearing file outside it can change with every hash still matching, so the pack stays")
    add("FRESH and wrong. (3) The pack reproduces its sources faithfully, CONTRADICTIONS INCLUDED —")
    add("if two canonical documents disagree it ships both claims and flags neither, except for the")
    add("one shared block guarded above (cross-file consistency generally is open item 2, unbuilt).")
    add("(4) DELETION beats this check: an absent pack skips cleanly, so")
    add("`python3 tools/gen_brief.py --check` is the deletion detector and belongs in the pre-land")
    add("step. (5) Nothing here proves the rules are good, that Drive synced, or that any outside")
    add("agent read `AGENTS.md` at all.")
    return "\n".join(parts).rstrip() + "\n"


# ---------------------------------------------------------------------- main


def shared_block(text, rel, end_marker):
    """The `### Efficiency mode (Fable bookends)` block, which must be byte-identical in both
    package files. Extracting it here lets the generator FAIL on cross-file drift — the exact
    class of defect L-20260817-06 recorded and PATCH-NOTES open item 2 is still unbuilt for."""
    lines = text.split("\n")
    heading = "### Efficiency mode (Fable bookends)"
    if heading not in lines:
        raise GenError("%s: %r not found" % (rel, heading))
    start = lines.index(heading)
    end = start + 1
    while end < len(lines) and not lines[end].startswith(end_marker):
        end += 1
    if end >= len(lines):
        raise GenError("%s: end marker %r for the shared block not found" % (rel, end_marker))
    return "\n".join(lines[start:end])


def gather(root):
    sources = {}
    texts = {}
    for rel in SOURCES:
        text = read_source(root, rel)
        texts[rel] = text
        sources[rel] = sha256_text(text)

    sc = texts["docs/SYSTEM-CURRENT.md"]
    spec = texts["docs/SYSTEM-SPEC-CURRENT.md"]
    block_sc = shared_block(sc, "docs/SYSTEM-CURRENT.md", "Copy-ready prompt blocks")
    block_spec = shared_block(spec, "docs/SYSTEM-SPEC-CURRENT.md", "The copy-ready prompt blocks")
    if block_sc != block_spec:
        raise GenError(
            "CROSS-FILE DRIFT: the shared '### Efficiency mode (Fable bookends)' block is NOT "
            "byte-identical across the two package files (SYSTEM-CURRENT sha256 %s, SPEC sha256 "
            "%s). Generating a brief over a rulebook that disagrees with itself would publish "
            "the disagreement; fix the package files first."
            % (sha256_text(block_sc), sha256_text(block_spec))
        )
    pn = texts["docs/PATCH-NOTES-CURRENT.md"]
    validator = load_validator(root)
    assert_no_schema_fork(validator, texts)
    items, counts = open_items(pn, "docs/PATCH-NOTES-CURRENT.md")
    if counts:
        counts_text = "**%d listed, %d open**" % counts
    else:
        counts_text = "count line absent from the open-items section — read it directly"

    landing = texts["docs/LANDING-PROTOCOL.md"]
    tier_lines = []
    for line in landing.split("\n"):
        if re.match(r"^##\s+Tier\s+\d", line) or line.startswith("**When:**"):
            tier_lines.append(line.split(" **Mechanics:**")[0].rstrip())
    if len(tier_lines) < 6:
        raise GenError("expected three Tier headings with a When line in docs/LANDING-PROTOCOL.md")
    invariants = [
        line.rstrip() for line in landing.split("\n")
        if line.startswith("- **Post-land verification") or line.startswith("- **Pre-land critique gate")
    ]
    if len(invariants) != 2:
        raise GenError("the two named LANDING-PROTOCOL invariants were not both found")

    handoff = texts["docs/HANDOFF-FORMAT.md"]
    block = re.search(r"```\n(HANDOFF\n.*?)```", handoff, re.DOTALL)
    if not block:
        raise GenError("the HANDOFF block was not found in docs/HANDOFF-FORMAT.md")

    facts = {
        "version": current_version(sc, "docs/SYSTEM-CURRENT.md"),
        "history_row": newest_history_row(sc, "docs/SYSTEM-CURRENT.md"),
        "hard_rules": extract_section(sc, "## Hard rules", "docs/SYSTEM-CURRENT.md"),
        "model_split": extract_section(sc, "## Claude model split (Owner rule)", "docs/SYSTEM-CURRENT.md"),
        "routine_vs_significant": extract_section(sc, "### Routine vs significant", "docs/SYSTEM-CURRENT.md"),
        "critique_ladder": extract_section(sc, "### Critique ladder", "docs/SYSTEM-CURRENT.md"),
        "review_gate": extract_section(sc, "### Review-gate availability", "docs/SYSTEM-CURRENT.md"),
        "routing_directive": extract_section(
            sc, "### Owner routing directive (standing, 2026-08-19)", "docs/SYSTEM-CURRENT.md"),
        "efficiency_block": extract_section(sc, "### Efficiency mode (Fable bookends)", "docs/SYSTEM-CURRENT.md"),
        "tier_lines": tier_lines,
        "landing_invariants": "\n".join(invariants),
        "handoff_block": block.group(1).rstrip(),
        "latest_handoff": texts["docs/LATEST-HANDOFF.md"],
        "open_items": items,
        "counts_text": counts_text,
        "counts": ("%d listed, %d open" % counts) if counts else "count line absent, read PATCH-NOTES",
        "system_current": sc,
        "shared_block_sha": sha256_text(block_sc),
        "reentry": extract_section(
            texts["docs/EFFICIENCY-MODE.md"],
            "## Mid-run re-entry — the ONLY six triggers",
            "docs/EFFICIENCY-MODE.md"),
        "speed_pack": extract_section(
            texts["docs/EFFICIENCY-MODE.md"],
            "## The SPEED PACK — self-brief from the generated brief, then verify it",
            "docs/EFFICIENCY-MODE.md"),
        "schemas": [
            ("grok_critique", validator.CRITIQUE_REQUIRED_KEYS),
            ("cursor_dispatch", validator.CURSOR_DISPATCH_REQUIRED_KEYS),
            ("gate_ratification", validator.GATE_RATIFICATION_REQUIRED_KEYS),
        ],
    }
    facts["last_land"] = re.sub(r"^- \*\*(v[0-9.]+)\*\*\s*[-—]+\s*", r"\1 ", facts["history_row"])
    facts["last_land"] = re.sub(r"\(this document\)\s*", "", facts["last_land"])
    return texts, sources, facts


def generate(root):
    texts, sources, facts = gather(root)
    manifest_digest = sha256_text("\n".join("%s %s" % (rel, sources[rel]) for rel in SOURCES))

    grok_text = build_grok_context(facts)
    agents_text = build_agents(facts, manifest_digest)
    out_digests = {OUT_GROK: sha256_text(grok_text), OUT_AGENTS: sha256_text(agents_text)}

    header_args = {
        "version": facts["version"],
        "self_digest": ZERO_DIGEST,
        "manifest_digest": manifest_digest,
    }
    body = build_pack(facts, sources, manifest_digest, out_digests)
    provisional = PACK_HEADER % header_args + "\n" + body
    header_args["self_digest"] = sha256_text(provisional)
    pack_text = PACK_HEADER % header_args + "\n" + body
    return {OUT_PACK: pack_text, OUT_GROK: grok_text, OUT_AGENTS: agents_text}


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Generate docs/BRIEF-PACK.md, docs/GROK-CONTEXT.txt and AGENTS.md."
    )
    parser.add_argument("--root", default=".", help="repo root")
    parser.add_argument("--check", action="store_true",
                        help="do not write; exit 1 if any output would change (CI/idempotency)")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    try:
        outputs = generate(args.root)
    except GenError as exc:
        sys.stderr.write("gen_brief: FAIL — %s\n" % exc)
        return 2

    changed = []
    for rel, text in sorted(outputs.items()):
        path = os.path.join(args.root, rel)
        existing = None
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as handle:
                existing = handle.read()
        if existing == text:
            continue
        changed.append(rel)
        if not args.check:
            with open(path, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(text)

    pack_lines = outputs[OUT_PACK].count("\n")
    grok_chars = len(outputs[OUT_GROK])
    if not args.quiet:
        print("gen_brief: %s | BRIEF-PACK %d lines | GROK-CONTEXT %d chars | AGENTS.md %d lines"
              % ("no change" if not changed else "wrote " + ", ".join(changed),
                 pack_lines, grok_chars, outputs[OUT_AGENTS].count("\n")))
    if pack_lines > PACK_TARGET_LINES:
        sys.stderr.write(
            "gen_brief: NOTE — BRIEF-PACK is %d lines, above the ~%d-line target. It is still "
            "correct; trim a source or the pack layout if crews stop reading it.\n"
            % (pack_lines, PACK_TARGET_LINES))
    if args.check and changed:
        sys.stderr.write("gen_brief: --check FAIL — would rewrite: %s\n" % ", ".join(changed))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
