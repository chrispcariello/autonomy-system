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

Exit code: 0 when no FAIL was raised, 1 otherwise (ADVISORY never fails the build unless --strict).
"""

import argparse
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
        if record.get("type") != "grok_critique":
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
        "%d journal records parsed, %d grok_critique records checked" % (seen_records, critiques),
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


# ---------------------------------------------------------------------- main


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Validate the run journal, the open-items list, and package-section presence."
    )
    parser.add_argument("--journal", action="store_true", help="C1 only: run-journal records")
    parser.add_argument("--open-items", action="store_true", help="C4 only: owner/exit on open items")
    parser.add_argument("--sections", action="store_true", help="C5 only: package section presence")
    parser.add_argument("--all", action="store_true", help="run every check (default)")
    parser.add_argument("--strict", action="store_true", help="treat ADVISORY findings as failures")
    parser.add_argument("--root", default=".", help="repo root the default paths resolve against")
    parser.add_argument("--journal-path", default=None)
    parser.add_argument("--open-items-path", default=None)
    parser.add_argument("--package-file", action="append", default=None)
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument("--self-test", action="store_true", help="run built-in fixtures and exit")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    run_all = args.all or not (args.journal or args.open_items or args.sections)
    root = args.root
    journal_path = args.journal_path or os.path.join(root, DEFAULT_JOURNAL)
    open_items_path = args.open_items_path or os.path.join(root, DEFAULT_OPEN_ITEMS)
    package_files = args.package_file or [os.path.join(root, p) for p in DEFAULT_PACKAGE_FILES]

    report = Report()
    if run_all or args.journal:
        check_journal(journal_path, report)
    if run_all or args.open_items:
        check_open_items(open_items_path, report, args.strict)
    if run_all or args.sections:
        check_sections(package_files, report)

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

    print("\nself-test %d/%d PASS" % (passed, total))
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
