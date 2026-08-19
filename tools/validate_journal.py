#!/usr/bin/env python3
"""validate_journal.py — mechanical checks the run journal and the open-items list must pass.

Stdlib only, no network, no dependencies. Companion to tools/specguard.py, which lints the
package documents; this one lints the EVIDENCE surfaces: the run journal (critique records),
the authoritative open-items list, and the presence of the two governance sections that the
whole critique/routing contract hangs off.

Checks
------
C1  --journal      every line of the run journal is valid JSON; every `grok_critique` record
                   carries the required keys; len(applied) + len(rejected) == bullets_count;
                   an empty critique (bullets_count 0) on a ladder pass is a FAIL unless the
                   record honestly says status == "FAIL" (then ADVISORY — recorded, not swallowed).
C4  --open-items   in the LAST "## REMAINING OPEN ITEMS" section, every numbered item names an
                   Owner and an Exit (struck-through closed items are exempt from that), and every
                   struck-through CLOSED item cites evidence that lives in the repo: a journal
                   record number, a grok_critique record, or a commit SHA. Both are ADVISORY by
                   default and FAIL under --strict — a CLOSED claim backed only by prose is the
                   false-green this check exists to surface.
C5  --sections     both package files contain "## Critique policy" and "## Credit-Aware Routing".
                   PRESENCE ONLY — this check does not read the body or compare the two files.
C6  --brief-pack   docs/BRIEF-PACK.md is FRESH: every source in its MANIFEST still hashes to the
                   recorded sha256, the two other generated files still hash to their recorded
                   values, the MANIFEST-DIGEST agrees with the rows, and the pack's own
                   SELF-DIGEST proves it was not hand-edited. Any mismatch is a FAIL naming the
                   stale files. An ABSENT pack is a clean skip, not a failure — see the honest
                   limit in the check itself.

Exit code: 0 when no FAIL was raised, 1 otherwise (ADVISORY never fails the build unless --strict).
"""

import argparse
import hashlib
import json
import os
import re
import sys

DEFAULT_JOURNAL = os.path.join("docs", "run-journals", "run-journal.jsonl")
DEFAULT_OPEN_ITEMS = os.path.join("docs", "PATCH-NOTES-CURRENT.md")
DEFAULT_PACKAGE_FILES = (
    os.path.join("docs", "SYSTEM-CURRENT.md"),
    os.path.join("docs", "SYSTEM-SPEC-CURRENT.md"),
)
DEFAULT_BRIEF_PACK = os.path.join("docs", "BRIEF-PACK.md")

CRITIQUE_REQUIRED_KEYS = (
    "ts",
    "type",
    "target",
    "pass",
    "model",
    "transport",
    "exit_code",
    "duration_s",
    "bullets_count",
    "applied",
    "rejected",
    "retrieval_ref",
)

# Efficiency mode (v4.1.13) adds two record types with their own minimum shapes:
# a Cursor-lane dispatch, and the Fable gate's ratification of an execution run.
CURSOR_DISPATCH_REQUIRED_KEYS = ("ts", "type", "task", "branch_or_pr", "outcome")
GATE_RATIFICATION_REQUIRED_KEYS = (
    "ts",
    "type",
    "target",
    "dispositions_reviewed",
    "overturns",
    "verdict",
)

REQUIRED_SECTIONS = ("## Critique policy", "## Credit-Aware Routing")

FAIL = "FAIL"
ADVISORY = "ADVISORY"


class Report(object):
    def __init__(self):
        self.findings = []

    def add(self, severity, check, where, message):
        self.findings.append(
            {"severity": severity, "check": check, "where": where, "message": message}
        )

    @property
    def fails(self):
        return [f for f in self.findings if f["severity"] == FAIL]

    @property
    def advisories(self):
        return [f for f in self.findings if f["severity"] == ADVISORY]


def _read(path, report, check):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read()
    except OSError as exc:
        report.add(FAIL, check, path, "cannot read file: %s" % exc)
        return None


# ---------------------------------------------------------------- C1: journal


def check_journal(path, report):
    text = _read(path, report, "C1-journal")
    if text is None:
        return
    lines = text.split("\n")
    seen_records = 0
    critiques = 0
    dispatches = 0
    ratifications = 0
    for number, raw in enumerate(lines, start=1):
        if not raw.strip():
            continue
        seen_records += 1
        where = "%s:%d" % (path, number)
        try:
            record = json.loads(raw)
        except ValueError as exc:
            report.add(FAIL, "journal-json", where, "line is not valid JSON: %s" % exc)
            continue
        if not isinstance(record, dict):
            report.add(FAIL, "journal-json", where, "line is valid JSON but not an object")
            continue
        record_type = record.get("type")
        if record_type == "cursor_dispatch":
            dispatches += 1
            missing = [k for k in CURSOR_DISPATCH_REQUIRED_KEYS if k not in record]
            if missing:
                report.add(
                    FAIL,
                    "cursor-dispatch-missing-keys",
                    where,
                    "cursor_dispatch record missing required key(s): %s — a Cursor PR with no "
                    "complete Event Bus record has not entered the bus" % ", ".join(missing),
                )
            continue
        if record_type == "gate_ratification":
            ratifications += 1
            missing = [k for k in GATE_RATIFICATION_REQUIRED_KEYS if k not in record]
            if missing:
                report.add(
                    FAIL,
                    "gate-ratification-missing-keys",
                    where,
                    "gate_ratification record missing required key(s): %s — without it an "
                    "efficiency-mode run has no ratification artifact and cannot claim PASS/CLOSED"
                    % ", ".join(missing),
                )
            continue
        if record_type != "grok_critique":
            continue
        critiques += 1
        missing = [key for key in CRITIQUE_REQUIRED_KEYS if key not in record]
        if missing:
            report.add(
                FAIL,
                "critique-missing-keys",
                where,
                "grok_critique record missing required key(s): %s" % ", ".join(missing),
            )
            continue

        applied = record.get("applied")
        rejected = record.get("rejected")
        if not isinstance(applied, list) or not isinstance(rejected, list):
            report.add(
                FAIL,
                "critique-shape",
                where,
                "applied and rejected must both be lists (got %s / %s)"
                % (type(applied).__name__, type(rejected).__name__),
            )
            continue

        bullets = record.get("bullets_count")
        if not isinstance(bullets, int) or isinstance(bullets, bool):
            report.add(
                FAIL,
                "critique-shape",
                where,
                "bullets_count must be an int (got %r)" % (bullets,),
            )
            continue

        dispositioned = len(applied) + len(rejected)
        if dispositioned != bullets:
            report.add(
                FAIL,
                "critique-bullets-unaccounted",
                where,
                "len(applied)+len(rejected)=%d != bullets_count=%d — every bullet must land in "
                "applied or rejected (minors may share one batched reason, still one entry each)"
                % (dispositioned, bullets),
            )

        pass_number = record.get("pass")
        if bullets == 0 and isinstance(pass_number, int) and pass_number >= 1:
            if record.get("status") == "FAIL":
                report.add(
                    ADVISORY,
                    "critique-empty-pass",
                    where,
                    "empty critique on ladder pass %d, correctly recorded status FAIL — it does "
                    "not count as a pass; re-scope, re-ask, write a second record" % pass_number,
                )
            else:
                report.add(
                    FAIL,
                    "critique-empty-pass",
                    where,
                    "bullets_count 0 on ladder pass %d with status %r — an empty or LGTM critique "
                    "on significant work is a FAIL, not a pass"
                    % (pass_number, record.get("status")),
                )
    report.add(
        ADVISORY,
        "journal-summary",
        path,
        "%d journal records parsed, %d grok_critique / %d cursor_dispatch / %d gate_ratification "
        "records checked" % (seen_records, critiques, dispatches, ratifications),
    )


# ------------------------------------------------------------- C4: open items

OPEN_ITEMS_HEADING = re.compile(r"^##\s+REMAINING OPEN ITEMS", re.IGNORECASE)
NUMBERED_ITEM = re.compile(r"^(\d+)\.\s+(.*)$")

# A CLOSED item must point at evidence that lives in the repo: a journal record number,
# a grok_critique record, or a commit SHA. Prose alone is an assertion, not evidence.
CLOSURE_CITATIONS = (
    re.compile(r"records?\s*#?\s*\d+", re.IGNORECASE),
    re.compile(r"grok_critique"),
    re.compile(r"\b[0-9a-f]{7,40}\b"),
)


def check_open_items(path, report, strict):
    text = _read(path, report, "C4-open-items")
    if text is None:
        return
    lines = text.split("\n")
    starts = [i for i, line in enumerate(lines) if OPEN_ITEMS_HEADING.match(line)]
    if not starts:
        report.add(
            FAIL,
            "open-items-missing",
            path,
            'no "## REMAINING OPEN ITEMS" section found — the authoritative list is the surface '
            "nightly hygiene step d and the HANDOFF open-items count both read",
        )
        return
    start = starts[-1]
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break
    heading = lines[start].strip()
    severity = FAIL if strict else ADVISORY
    items = 0
    closed = 0
    for offset in range(start + 1, end):
        line = lines[offset]
        match = NUMBERED_ITEM.match(line)
        if not match:
            continue
        items += 1
        number, body = match.group(1), match.group(2)
        if "~~" in body:
            closed += 1
            if not any(pattern.search(body) for pattern in CLOSURE_CITATIONS):
                report.add(
                    severity,
                    "closed-item-no-evidence",
                    "%s:%d" % (path, offset + 1),
                    "closed item %s cites no journal record number, no grok_critique record and no "
                    "commit SHA — a CLOSED claim must point at evidence in the repo, not prose"
                    % number,
                )
            continue
        missing = []
        if "Owner" not in body:
            missing.append("Owner")
        if "Exit" not in body:
            missing.append("Exit")
        if missing:
            report.add(
                severity,
                "open-item-no-owner-exit",
                "%s:%d" % (path, offset + 1),
                "open item %s does not name %s (struck-through closed items are exempt)"
                % (number, " and ".join(missing)),
            )
    report.add(
        ADVISORY,
        "open-items-summary",
        "%s:%d" % (path, start + 1),
        '"%s": %d numbered items, %d closed-on-record (struck through), %d open'
        % (heading, items, closed, items - closed),
    )


# --------------------------------------------------------------- C5: sections


def check_sections(paths, report):
    for path in paths:
        text = _read(path, report, "C5-sections")
        if text is None:
            continue
        headings = [line for line in text.split("\n") if line.startswith("## ")]
        for wanted in REQUIRED_SECTIONS:
            if not any(head.startswith(wanted) for head in headings):
                report.add(
                    FAIL,
                    "package-section-missing",
                    path,
                    'required section "%s" is absent from this package file' % wanted,
                )
    report.add(
        ADVISORY,
        "sections-scope",
        ", ".join(paths),
        "PRESENCE-ONLY check: heading exists in each package file. This does NOT read the section "
        "body and does NOT compare the two files for content drift (that is PATCH-NOTES open "
        "item 2, specguard cross-file sync — still unbuilt).",
    )


# ------------------------------------------------------------- C6: brief pack

# The MANIFEST FLOOR: paths that MUST appear in the pack's manifest whatever
# tools/gen_brief.py currently lists. Without this, "manifest amputation" beats the whole
# check — drop a binding source from the generator's SOURCES tuple, regenerate, and C6
# re-hashes only what remains, passing green while the briefing permanently omits a rule
# surface. Two files now have to agree before that can happen. Kept deliberately short: it is
# a floor, not a copy of SOURCES, so the generator may add sources freely but not remove these.
REQUIRED_MANIFEST_PATHS = (
    "CLAUDE.md",
    "docs/SYSTEM-CURRENT.md",
    "docs/SYSTEM-SPEC-CURRENT.md",
    "docs/EFFICIENCY-MODE.md",
    "docs/RUN-TEMPLATE.md",
    "docs/GROK.md",
    "docs/LANDING-PROTOCOL.md",
    "docs/HANDOFF-FORMAT.md",
    "docs/CURSOR-LANE.md",
    "docs/PATCH-NOTES-CURRENT.md",
    "docs/LATEST-HANDOFF.md",
    "tools/validate_journal.py",
)

MANIFEST_ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*`([0-9a-f]{64})`\s*\|\s*$")
SOURCE_TABLE_HEADER = "| source | sha256 |"
OUTPUT_TABLE_HEADER = "| generated file | sha256 |"
SELF_DIGEST_LINE = re.compile(r"^SELF-DIGEST: ([0-9a-f]{64})$", re.MULTILINE)
MANIFEST_DIGEST_LINE = re.compile(r"^MANIFEST-DIGEST: ([0-9a-f]{64})$", re.MULTILINE)
ZERO_DIGEST = "0" * 64


def _sha256_file(path):
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def check_brief_pack(pack_path, root, report):
    """Recompute the pack's MANIFEST and fail on drift.

    This is the mechanical backstop behind the regeneration rule: a run that edits docs/**
    or tools/** without re-running tools/gen_brief.py leaves the pack pointing at hashes the
    sources no longer have, and this check names the files that moved.

    HONEST LIMITS, stated rather than implied. (a) An ABSENT pack skips cleanly — this check
    catches DRIFT, not DELETION, so removing the pack removes the check with it, and only a
    human or a gate notices that. (b) A fresh pack proves the sources have not moved since
    generation; it proves nothing about whether the pack's PROSE summarises them well, nor
    anything about the run journal, which is deliberately not a manifest source. (c) It
    cannot tell an honest regeneration from a regeneration that also quietly rewrote a
    canonical source — it compares the pack to the tree, never the tree to its history."""
    if not os.path.isfile(pack_path):
        report.add(
            ADVISORY,
            "brief-pack-absent",
            pack_path,
            "no BRIEF-PACK.md — staleness check SKIPPED (clean skip by design). This check "
            "catches drift, not deletion: with the pack gone nothing here notices.",
        )
        if os.path.isfile(os.path.join(root, "tools", "gen_brief.py")):
            report.add(
                ADVISORY,
                "brief-pack-absent-but-generator-present",
                pack_path,
                "tools/gen_brief.py IS installed but its pack is missing — this is the known "
                "no-op path: deleting the generated files removes the staleness check with "
                "them. The detector is `python3 tools/gen_brief.py --check` (exit 1 when any "
                "output is missing or would change); run it in the pre-land step. Left as an "
                "ADVISORY rather than a FAIL because a clean skip on an absent pack is the "
                "ordered semantic (v4.1.16); the residual is recorded on PATCH-NOTES item 18.",
            )
        return
    text = _read(pack_path, report, "C6-brief-pack")
    if text is None:
        return

    self_match = SELF_DIGEST_LINE.search(text)
    if not self_match:
        report.add(
            FAIL,
            "brief-pack-malformed",
            pack_path,
            "no SELF-DIGEST line — this file does not look like a tools/gen_brief.py output; "
            "regenerate it rather than hand-repairing it",
        )
        return
    normalised = text.replace("SELF-DIGEST: " + self_match.group(1), "SELF-DIGEST: " + ZERO_DIGEST)
    recomputed_self = hashlib.sha256(normalised.encode("utf-8")).hexdigest()
    if recomputed_self != self_match.group(1):
        report.add(
            FAIL,
            "brief-pack-hand-edited",
            pack_path,
            "SELF-DIGEST does not match this file's own content — BRIEF-PACK.md has been "
            "hand-edited or partially regenerated. It is a generated file: run "
            "python3 tools/gen_brief.py and commit the result.",
        )

    lines = text.split("\n")
    sources = []
    outputs = []
    bucket = None
    for line in lines:
        stripped = line.rstrip()
        if stripped == SOURCE_TABLE_HEADER:
            bucket = sources
            continue
        if stripped == OUTPUT_TABLE_HEADER:
            bucket = outputs
            continue
        if stripped.startswith("#"):
            bucket = None
            continue
        if bucket is None:
            continue
        row = MANIFEST_ROW.match(stripped)
        if row:
            bucket.append((row.group(1), row.group(2)))
        elif stripped.startswith("| :") or not stripped:
            continue  # alignment row, or a blank line between the header and the rows
        else:
            bucket = None  # anything else ends the table

    if not sources:
        report.add(
            FAIL,
            "brief-pack-malformed",
            pack_path,
            "MANIFEST source table is empty or unparseable — a pack with no manifest cannot be "
            "checked for staleness, which is indistinguishable from an unchecked pack",
        )
        return

    stale = []
    missing = []
    for rel, recorded in sources + outputs:
        path = os.path.join(root, rel)
        if not os.path.isfile(path):
            missing.append(rel)
            continue
        if _sha256_file(path) != recorded:
            stale.append(rel)
    if missing:
        report.add(
            FAIL,
            "brief-pack-source-missing",
            pack_path,
            "listed in the BRIEF-PACK MANIFEST but absent from the tree: %s — the pack is "
            "describing a repo that no longer exists" % ", ".join(sorted(missing)),
        )
    if stale:
        report.add(
            FAIL,
            "brief-pack-stale",
            pack_path,
            "BRIEF-PACK.md is STALE — these files changed since it was generated: %s. Any run "
            "that touches docs/** or tools/** must re-run python3 tools/gen_brief.py in the "
            "SAME commit." % ", ".join(sorted(stale)),
        )

    listed = {rel for rel, _ in sources}
    amputated = [rel for rel in REQUIRED_MANIFEST_PATHS if rel not in listed]
    if amputated:
        report.add(
            FAIL,
            "brief-pack-manifest-amputated",
            pack_path,
            "the BRIEF-PACK MANIFEST omits required source(s): %s. Re-hashing only what a "
            "manifest still lists proves nothing if the manifest itself shrank, so this floor "
            "lives in the validator rather than in tools/gen_brief.py — restore the source to "
            "the generator SOURCES tuple and regenerate." % ", ".join(amputated),
        )

    digest_match = MANIFEST_DIGEST_LINE.search(text)
    if digest_match:
        recomputed = hashlib.sha256(
            "\n".join("%s %s" % (rel, sha) for rel, sha in sources).encode("utf-8")
        ).hexdigest()
        if recomputed != digest_match.group(1):
            report.add(
                FAIL,
                "brief-pack-digest-mismatch",
                pack_path,
                "MANIFEST-DIGEST does not match the manifest rows in this same file — the "
                "table or the digest was edited by hand; regenerate the pack",
            )
    report.add(
        ADVISORY,
        "brief-pack-summary",
        pack_path,
        "%d manifest sources + %d generated outputs re-hashed; %d stale, %d missing. Scope: "
        "this proves the sources have not moved since generation, nothing about the journal "
        "(deliberately not a source) or about the quality of the pack's prose."
        % (len(sources), len(outputs), len(stale), len(missing)),
    )


# ---------------------------------------------------------------------- main


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Validate the run journal, the open-items list, and package-section presence."
    )
    parser.add_argument("--journal", action="store_true", help="C1 only: run-journal records")
    parser.add_argument("--open-items", action="store_true", help="C4 only: owner/exit on open items")
    parser.add_argument("--sections", action="store_true", help="C5 only: package section presence")
    parser.add_argument("--brief-pack", action="store_true", help="C6 only: BRIEF-PACK freshness")
    parser.add_argument("--all", action="store_true", help="run every check (default)")
    parser.add_argument("--strict", action="store_true", help="treat ADVISORY findings as failures")
    parser.add_argument("--root", default=".", help="repo root the default paths resolve against")
    parser.add_argument("--journal-path", default=None)
    parser.add_argument("--open-items-path", default=None)
    parser.add_argument("--package-file", action="append", default=None)
    parser.add_argument("--brief-pack-path", default=None)
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument("--self-test", action="store_true", help="run built-in fixtures and exit")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    run_all = args.all or not (
        args.journal or args.open_items or args.sections or args.brief_pack
    )
    root = args.root
    journal_path = args.journal_path or os.path.join(root, DEFAULT_JOURNAL)
    open_items_path = args.open_items_path or os.path.join(root, DEFAULT_OPEN_ITEMS)
    package_files = args.package_file or [os.path.join(root, p) for p in DEFAULT_PACKAGE_FILES]
    brief_pack_path = args.brief_pack_path or os.path.join(root, DEFAULT_BRIEF_PACK)

    report = Report()
    if run_all or args.journal:
        check_journal(journal_path, report)
    if run_all or args.open_items:
        check_open_items(open_items_path, report, args.strict)
    if run_all or args.sections:
        check_sections(package_files, report)
    if run_all or args.brief_pack:
        check_brief_pack(brief_pack_path, root, report)

    if args.json:
        print(
            json.dumps(
                {
                    "fail": len(report.fails),
                    "advisory": len(report.advisories),
                    "findings": report.findings,
                },
                indent=2,
                sort_keys=True,
            )
        )
    else:
        for finding in report.findings:
            print(
                "%-8s %-28s %s\n         %s"
                % (finding["severity"], finding["check"], finding["where"], finding["message"])
            )
        print(
            "\n%d finding(s) [%d FAIL, %d ADVISORY]"
            % (len(report.findings), len(report.fails), len(report.advisories))
        )

    failed = bool(report.fails) or (args.strict and bool(report.advisories))
    return 1 if failed else 0


# ------------------------------------------------------------------ self-test

GOOD_CRITIQUE = {
    "ts": "2026-08-18T12:00:00Z",
    "type": "grok_critique",
    "status": "VERIFIED",
    "target": "fixture",
    "pass": 1,
    "model": "grok-4.5",
    "transport": "cli",
    "exit_code": 0,
    "duration_s": 10,
    "bullets_count": 2,
    "applied": [{"b": 1, "reason": "x"}],
    "rejected": [{"b": 2, "reason": "minor style, batched"}],
    "retrieval_ref": "LM-RET-EXAMPLE-0000",
}


def _fixture(report_kwargs):
    record = dict(GOOD_CRITIQUE)
    record.update(report_kwargs)
    return record


def self_test():
    import tempfile

    cases = [
        ("valid record", _fixture({}), []),
        (
            "dropped bullet",
            _fixture({"bullets_count": 6}),
            ["critique-bullets-unaccounted"],
        ),
        (
            "empty pass, dishonest status",
            _fixture({"bullets_count": 0, "applied": [], "rejected": []}),
            ["critique-empty-pass"],
        ),
        (
            "missing key",
            {k: v for k, v in GOOD_CRITIQUE.items() if k != "retrieval_ref"},
            ["critique-missing-keys"],
        ),
        (
            "cursor_dispatch without branch_or_pr or outcome",
            {
                "ts": "2026-08-18T23:00:00Z",
                "type": "cursor_dispatch",
                "status": "UNVERIFIED",
                "task": "generate a LATEST-HANDOFF history index page",
                "retrieval_ref": "LM-RET-EXAMPLE-0000",
            },
            ["cursor-dispatch-missing-keys"],
        ),
        (
            "gate_ratification without overturns or verdict",
            {
                "ts": "2026-08-18T23:05:00Z",
                "type": "gate_ratification",
                "status": "VERIFIED",
                "target": "v4.1.x execution run",
                "dispositions_reviewed": 8,
                "retrieval_ref": "LM-RET-EXAMPLE-0000",
            },
            ["gate-ratification-missing-keys"],
        ),
    ]
    passed = 0
    total = 0
    workdir = tempfile.mkdtemp(prefix="validate-journal-selftest-")
    for name, record, expected in cases:
        total += 1
        path = os.path.join(workdir, "j.jsonl")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(record) + "\n")
        report = Report()
        check_journal(path, report)
        got = sorted({f["check"] for f in report.fails})
        if got == sorted(expected):
            passed += 1
            print("PASS  %s" % name)
        else:
            print("FAIL  %s — expected %s, got %s" % (name, expected, got))

    total += 1
    path = os.path.join(workdir, "bad.jsonl")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("{not json}\n")
    report = Report()
    check_journal(path, report)
    if [f["check"] for f in report.fails] == ["journal-json"]:
        passed += 1
        print("PASS  unparseable line")
    else:
        print("FAIL  unparseable line — got %s" % [f["check"] for f in report.fails])

    open_items_cases = [
        (
            "closed item citing a SHA + records",
            "## REMAINING OPEN ITEMS\n\n1. ~~thing~~ — CLOSED on records 43-45, landed c8d8884.\n",
            [],
        ),
        (
            "closed item citing only prose",
            "## REMAINING OPEN ITEMS\n\n1. ~~thing~~ — CLOSED because it works now.\n",
            ["closed-item-no-evidence"],
        ),
        (
            "open item with no owner or exit",
            "## REMAINING OPEN ITEMS\n\n1. thing that nobody owns.\n",
            ["open-item-no-owner-exit"],
        ),
    ]
    for name, body, expected in open_items_cases:
        total += 1
        path = os.path.join(workdir, "items.md")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(body)
        report = Report()
        check_open_items(path, report, strict=False)
        advisories = sorted({f["check"] for f in report.advisories if f["check"] != "open-items-summary"})
        strict_report = Report()
        check_open_items(path, strict_report, strict=True)
        strict_fails = sorted({f["check"] for f in strict_report.fails})
        if advisories == sorted(expected) and strict_fails == sorted(expected) and not report.fails:
            passed += 1
            print("PASS  %s (ADVISORY by default, FAIL under --strict)" % name)
        else:
            print(
                "FAIL  %s — expected %s, got advisories %s / strict fails %s"
                % (name, expected, advisories, strict_fails)
            )

    total += 1
    path = os.path.join(workdir, "empty_fail.jsonl")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(
            json.dumps(
                _fixture(
                    {"bullets_count": 0, "applied": [], "rejected": [], "status": "FAIL"}
                )
            )
            + "\n"
        )
    report = Report()
    check_journal(path, report)
    if not report.fails and any(f["check"] == "critique-empty-pass" for f in report.advisories):
        passed += 1
        print("PASS  empty pass honestly recorded as status FAIL -> ADVISORY")
    else:
        print("FAIL  empty-pass advisory case")

    # ---------------------------------------------------------- C6 fixtures
    #
    # A synthetic repo with two "sources" and one "generated output", plus a pack whose
    # MANIFEST is built the same way tools/gen_brief.py builds it. Fresh must pass, and
    # every way of going stale must FAIL — a staleness check that only passes is a check
    # nobody has proven can fail.
    def _write_pack(packdir, rows, outputs):
        digest = hashlib.sha256(
            "\n".join("%s %s" % (rel, sha) for rel, sha in rows).encode("utf-8")
        ).hexdigest()
        body = [
            "# BRIEF-PACK.md — fixture",
            "",
            "SELF-DIGEST: %s",
            "MANIFEST-DIGEST: " + digest,
            "",
            "## MANIFEST",
            "",
            "| source | sha256 |",
            "| :-- | :-- |",
        ]
        body += ["| `%s` | `%s` |" % (rel, sha) for rel, sha in rows]
        body += ["", "| generated file | sha256 |", "| :-- | :-- |"]
        body += ["| `%s` | `%s` |" % (rel, sha) for rel, sha in outputs]
        body.append("")
        template = "\n".join(body)
        self_digest = hashlib.sha256((template % ZERO_DIGEST).encode("utf-8")).hexdigest()
        path = os.path.join(packdir, "BRIEF-PACK.md")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(template % self_digest)
        return path

    def _pack_fixture(root_dir, source_body="alpha\n", output_body="gamma\n"):
        os.makedirs(root_dir, exist_ok=True)
        # Every fixture satisfies the MANIFEST FLOOR, so only the amputation case below trips
        # it and the other fixtures keep testing exactly the one thing each is named for.
        files = {"a.md": source_body, "b.md": "beta\n"}
        for required in REQUIRED_MANIFEST_PATHS:
            files[required] = "floor fixture for %s\n" % required
        rows = []
        for name, body in sorted(files.items()):
            target = os.path.join(root_dir, name)
            parent = os.path.dirname(target)
            if parent:
                os.makedirs(parent, exist_ok=True)
            with open(target, "w", encoding="utf-8") as handle:
                handle.write(body)
            rows.append((name, hashlib.sha256(body.encode("utf-8")).hexdigest()))
        with open(os.path.join(root_dir, "OUT.txt"), "w", encoding="utf-8") as handle:
            handle.write(output_body)
        outputs = [("OUT.txt", hashlib.sha256(output_body.encode("utf-8")).hexdigest())]
        return _write_pack(root_dir, rows, outputs), rows, outputs

    pack_cases = []

    fresh_root = os.path.join(workdir, "pack-fresh")
    fresh_pack, _, _ = _pack_fixture(fresh_root)
    pack_cases.append(("fresh pack passes", fresh_pack, fresh_root, []))

    stale_root = os.path.join(workdir, "pack-stale")
    stale_pack, _, _ = _pack_fixture(stale_root)
    with open(os.path.join(stale_root, "a.md"), "w", encoding="utf-8") as handle:
        handle.write("alpha EDITED after generation\n")
    pack_cases.append(("stale source fails", stale_pack, stale_root, ["brief-pack-stale"]))

    out_root = os.path.join(workdir, "pack-out")
    out_pack, _, _ = _pack_fixture(out_root)
    with open(os.path.join(out_root, "OUT.txt"), "w", encoding="utf-8") as handle:
        handle.write("gamma EDITED by hand\n")
    pack_cases.append(("hand-edited generated output fails", out_pack, out_root, ["brief-pack-stale"]))

    gone_root = os.path.join(workdir, "pack-gone")
    gone_pack, _, _ = _pack_fixture(gone_root)
    os.remove(os.path.join(gone_root, "b.md"))
    pack_cases.append(("manifest source deleted fails", gone_pack, gone_root, ["brief-pack-source-missing"]))

    edit_root = os.path.join(workdir, "pack-edited")
    edit_pack, _, _ = _pack_fixture(edit_root)
    with open(edit_pack, "r", encoding="utf-8") as handle:
        edited = handle.read()
    with open(edit_pack, "w", encoding="utf-8") as handle:
        handle.write(edited.replace("# BRIEF-PACK.md — fixture", "# BRIEF-PACK.md — tampered"))
    pack_cases.append(("hand-edited pack body fails", edit_pack, edit_root, ["brief-pack-hand-edited"]))

    amp_root = os.path.join(workdir, "pack-amputated")
    os.makedirs(amp_root, exist_ok=True)
    body = "alpha\n"
    with open(os.path.join(amp_root, "a.md"), "w", encoding="utf-8") as handle:
        handle.write(body)
    with open(os.path.join(amp_root, "OUT.txt"), "w", encoding="utf-8") as handle:
        handle.write("gamma\n")
    amp_pack = _write_pack(
        amp_root,
        [("a.md", hashlib.sha256(body.encode("utf-8")).hexdigest())],
        [("OUT.txt", hashlib.sha256(b"gamma\n").hexdigest())],
    )
    # This fixture's manifest lists a single file, so every REQUIRED_MANIFEST_PATHS entry is
    # missing: exactly the amputation case, and the fixture proves the floor can fire.
    pack_cases.append(
        ("amputated manifest fails", amp_pack, amp_root, ["brief-pack-manifest-amputated"])
    )

    for name, pack_path, pack_root, expected in pack_cases:
        total += 1
        report = Report()
        check_brief_pack(pack_path, pack_root, report)
        got = sorted({f["check"] for f in report.fails})
        if got == sorted(expected):
            passed += 1
            print("PASS  %s" % name)
        else:
            print("FAIL  %s — expected %s, got %s" % (name, expected, got))

    total += 1
    report = Report()
    check_brief_pack(os.path.join(workdir, "no-such-pack.md"), workdir, report)
    if not report.fails and any(f["check"] == "brief-pack-absent" for f in report.advisories):
        passed += 1
        print("PASS  absent pack skips cleanly (ADVISORY, not FAIL)")
    else:
        print("FAIL  absent-pack clean-skip case")

    print("\nself-test %d/%d PASS" % (passed, total))
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
