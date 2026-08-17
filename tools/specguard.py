#!/usr/bin/env python3
"""specguard.py - mechanical consistency checks for SYSTEM-vX-FOR-CLAUDE.md
and for CREDIT-CHECK notes written against it.

Read-only, stdlib-only, writes nothing. Exit 0 = clean, 1 = findings, 2 = usage/IO error.

Usage:
  python3 specguard.py --spec PATH [--json] [--strict]
  python3 specguard.py --spec PATH --check-note NOTE [--json]
  python3 specguard.py --self-test
"""

import argparse
import json
import re
import sys

EM = "—"
EN = "–"
ARROW = "→"
DASHCLS = "[" + EM + EN + "\\-]"

VER_RE = re.compile(r"^\s*[-*]\s*(?:\*\*)?\s*v(\d+(?:\.\d+)*)\s*(?:\*\*)?\s*" + DASHCLS)
H2_RE = re.compile(r"^##\s+(\S.*?)\s*$")
H3_RE = re.compile(r"^###\s+(\S.*?)\s*$")
MODE_RE = re.compile(r"\b[A-Z][A-Z0-9]*(?:_[A-Z0-9]+)*\b")
ARROW_MODE_RE = re.compile(r"(?:->|" + ARROW + r")\s*\*{0,2}\s*([A-Z][A-Z0-9]*(?:_[A-Z0-9]+)*)")
REC_RE = re.compile(r"Recommendation:\s*\[([^\]]+)\]")
REC_PLAIN_RE = re.compile(r"^\s*Recommendation:\s*(.+?)\s*$")
TIME_RE = re.compile(r"\b\d{1,2}(?::\d{2})?\s*[AaPp]\.?[Mm]\.?|\b\d{1,2}:\d{2}\b")
TZ_RE = re.compile(
    r"\b(?:UTC|GMT)\b"
    r"|[+-]\d{2}:?\d{2}\b"
    r"|\b(?:Africa|America|Antarctica|Arctic|Asia|Atlantic|Australia|Europe|Indian|Pacific|Etc|US)/[A-Za-z0-9_+-]+"
    r"|\b(?:E[SD]T|C[SD]T|M[SD]T|P[SD]T|BST|CES?T|IST|JST|AE[SD]T|NZ[SD]T|ET|CT|MT|PT)\b"
)
TS_TZ_RE = re.compile(r"\dZ\b|" + TZ_RE.pattern)
ISO_TS_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}")
MODEL_RE = re.compile(r"^\s*[-*]\s*\*\*Claude\s+([A-Z][A-Za-z0-9]*)")
RULE_ITEM_RE = re.compile(r"^\s*(\d+)\.\s+\S")
RULE_REF_RE = re.compile(r"[Hh]ard [Rr]ule\s+(\d+)")

NON_MODES = frozenset(["MODE", "ACTION", "STATE", "NOTE", "TODO", "OWNER", "CLAUDE", "GROK"])
STOPWORDS = frozenset(["this", "that", "with", "from", "only", "when", "what", "does", "team", "claude", "each", "into", "your"])
FAIL = "FAIL"
ADVISORY = "ADVISORY"


def _f(check, severity, lns, message):
    return {"check": check, "severity": severity, "lines": sorted(set(lns)), "message": message}


def read_lines(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read().splitlines()


def fence_map(lines):
    out = []
    inside = False
    for ln in lines:
        if ln.strip().startswith("```"):
            out.append(True)
            inside = not inside
        else:
            out.append(inside)
    return out


def sections(lines):
    fm = fence_map(lines)
    secs = []
    for i, ln in enumerate(lines):
        if fm[i]:
            continue
        m = H2_RE.match(ln)
        if m:
            secs.append({"title": m.group(1), "start": i, "end": len(lines)})
    for j in range(len(secs) - 1):
        secs[j]["end"] = secs[j + 1]["start"]
    return secs


def find_section(secs, needle):
    n = needle.lower()
    for s in secs:
        if s["title"].strip().lower() == n:
            return s
    for s in secs:
        if n in s["title"].lower():
            return s
    return None


def note_template(lines, credit):
    if credit is None:
        return []
    inside = False
    cur = []
    for i in range(credit["start"], credit["end"]):
        if lines[i].strip().startswith("```"):
            if inside:
                if any("CREDIT-CHECK" in lines[j] for j in cur):
                    return cur
                cur = []
                inside = False
            else:
                inside = True
                cur = []
            continue
        if inside:
            cur.append(i)
    return []


def check_version_numbering(lines, hist):
    out = []
    entries = []
    for i in range(hist["start"], hist["end"]):
        m = VER_RE.match(lines[i])
        if m:
            entries.append((i + 1, m.group(1), tuple(int(x) for x in m.group(1).split("."))))
    if not entries:
        return [_f("version-history-empty", FAIL, [hist["start"] + 1], "no parseable version entries under Version History")]
    for (l1, s1, t1), (l2, s2, t2) in zip(entries, entries[1:]):
        if t2 <= t1:
            out.append(_f("version-numbering", FAIL, [l2], "version entries not in ascending order: v%s then v%s" % (s1, s2)))
        elif len(t1) == len(t2) and t1[:-1] == t2[:-1]:
            if t2[-1] != t1[-1] + 1:
                gap = [".".join(str(x) for x in (t1[:-1] + (n,))) for n in range(t1[-1] + 1, t2[-1])]
                out.append(_f("version-numbering", FAIL, [l2],
                              "history jumps v%s -> v%s; no entry for %s (a released version is unlogged or the numbering is wrong)"
                              % (s1, s2, ", ".join("v" + g for g in gap))))
        elif len(t2) == len(t1) + 1 and t2[:-1] == t1:
            if t2[-1] != 1:
                out.append(_f("version-numbering", FAIL, [l2], "first sub-version after v%s is v%s, expected .1" % (s1, s2)))
        else:
            out.append(_f("version-numbering", ADVISORY, [l2], "non-linear version step v%s -> v%s" % (s1, s2)))
    return out


def check_sections_logged(lines, secs, hist):
    hist_text = " ".join(lines[hist["start"]:hist["end"]]).lower()
    cand = []
    for s in secs:
        if s is hist:
            continue
        toks = [t for t in re.split(r"[^A-Za-z0-9]+", s["title"].lower()) if len(t) >= 4 and t not in STOPWORDS]
        if not toks:
            continue
        if not any(t in hist_text for t in toks):
            cand.append((s["end"] - s["start"], s))
    cand.sort(key=lambda p: -p[0])
    return [_f("section-not-in-history", ADVISORY, [s["start"] + 1],
               "section '%s' (%d lines) is not referenced by any Version History entry [keyword heuristic]" % (s["title"], size))
            for size, s in cand]


def mode_sets(lines, credit):
    enum, enum_line = [], None
    for i in range(credit["start"], credit["end"]):
        m = REC_RE.search(lines[i])
        if m:
            enum = [t.strip() for t in m.group(1).split("|") if t.strip()]
            enum_line = i + 1
            break
    declared = {}
    fm = fence_map(lines)
    for i in range(credit["start"], credit["end"]):
        if fm[i]:
            continue
        raw = lines[i].strip()
        if raw.startswith("|"):
            toks = [] if set(raw) <= set("|-: " + EN + EM) else MODE_RE.findall(raw)
        else:
            toks = ARROW_MODE_RE.findall(raw)
        for t in toks:
            if len(t) >= 4 and t not in NON_MODES:
                declared.setdefault(t, i + 1)
    return enum, enum_line, declared


def check_mode_enum(lines, credit):
    enum, enum_line, declared = mode_sets(lines, credit)
    if enum_line is None:
        return [_f("mode-enum-absent", FAIL, [credit["start"] + 1],
                   "no 'Recommendation: [...]' enum found in the Credit-Aware Routing section")]
    out = []
    extra = [t for t in sorted(declared) if t not in enum]
    missing = [t for t in enum if t not in declared]
    if extra:
        out.append(_f("mode-enum-undeclared", FAIL, [enum_line] + [declared[t] for t in extra],
                      "modes defined by the threshold tables but not permitted by the CREDIT-CHECK Recommendation enum: " + ", ".join(extra)))
    if missing:
        out.append(_f("mode-enum-missing", FAIL, [enum_line],
                      "modes offered by the CREDIT-CHECK Recommendation enum but never defined by any threshold row: " + ", ".join(missing)))
    return out


def _norm_time(raw):
    return re.sub(r"[\s.]", "", raw.lower()).replace(":00", "")


def check_reset_timezone(lines):
    out = []
    renders = {}
    for i, ln in enumerate(lines):
        if "reset" not in ln.lower():
            continue
        times = [t.strip().rstrip(".") for t in TIME_RE.findall(ln)]
        if not times:
            continue
        if not TZ_RE.search(ln):
            out.append(_f("reset-timezone", FAIL, [i + 1],
                          "reset time '%s' carries no timezone; a scheduler cannot resolve it" % ", ".join(sorted(set(times)))))
        for t in times:
            k = _norm_time(t)
            renders.setdefault(k, {})
            renders[k].setdefault(t, []).append(i + 1)
    for k in sorted(renders):
        forms = renders[k]
        if len(forms) > 1:
            lns = [n for v in forms.values() for n in v]
            out.append(_f("reset-format", FAIL, lns,
                          "the same reset time is written %d different ways (%s); it is not greppable" % (len(forms), " / ".join(sorted(forms)))))
    return out


def check_hard_rules(lines, secs):
    hr = find_section(secs, "hard rules")
    if hr is None:
        return [_f("hard-rules-missing", FAIL, [1], "no 'Hard rules' section found")]
    nums = []
    for i in range(hr["start"], hr["end"]):
        m = RULE_ITEM_RE.match(lines[i])
        if m:
            nums.append((i + 1, int(m.group(1))))
    out = []
    for idx, (ln, n) in enumerate(nums, start=1):
        if n != idx:
            out.append(_f("hard-rule-numbering", FAIL, [ln], "hard rule list item %d is numbered %d" % (idx, n)))
    top = max([n for _, n in nums] or [0])
    for i, ln in enumerate(lines):
        for m in RULE_REF_RE.finditer(ln):
            n = int(m.group(1))
            if n < 1 or n > top:
                out.append(_f("hard-rule-ref", FAIL, [i + 1], "reference to 'Hard Rule %d' but only rules 1-%d exist" % (n, top)))
    return out


def check_model_budget(lines, secs, credit):
    split = find_section(secs, "model split")
    if split is None or credit is None:
        return []
    names = []
    for i in range(split["start"], split["end"]):
        m = MODEL_RE.match(lines[i])
        if m and m.group(1) not in names:
            names.append(m.group(1))
    if len(names) < 2:
        return []
    scope = list(note_template(lines, credit))
    for i in range(credit["start"], credit["end"]):
        if H3_RE.match(lines[i]):
            scope.append(i)
    out = []
    for i in sorted(set(scope)):
        hit = [n for n in names if n in lines[i]]
        if len(hit) >= 2:
            out.append(_f("model-budget-collapsed", FAIL, [i + 1],
                          "%s are separately-budgeted models with different roles but share one figure/threshold here: %s"
                          % (" + ".join(hit), lines[i].strip()[:90])))
    return out


def run_lint(lines):
    secs = sections(lines)
    hist = find_section(secs, "version history")
    credit = find_section(secs, "credit-aware routing")
    out = []
    if hist is None:
        out.append(_f("version-history-missing", FAIL, [1], "no 'Version History' section found"))
    else:
        out += check_version_numbering(lines, hist)
        out += check_sections_logged(lines, secs, hist)
    if credit is None:
        out.append(_f("credit-section-missing", ADVISORY, [1], "no 'Credit-Aware Routing' section found; mode/enum checks skipped"))
    else:
        out += check_mode_enum(lines, credit)
        out += check_model_budget(lines, secs, credit)
    out += check_reset_timezone(lines)
    out += check_hard_rules(lines, secs)
    return out


def check_note(doc_lines, note_lines):
    secs = sections(doc_lines)
    credit = find_section(secs, "credit-aware routing")
    vocab = set()
    if credit is not None:
        enum, _l, declared = mode_sets(doc_lines, credit)
        vocab = set(enum) | set(declared)
    split = find_section(secs, "model split")
    names = []
    if split is not None:
        for i in range(split["start"], split["end"]):
            m = MODEL_RE.match(doc_lines[i])
            if m and m.group(1) not in names:
                names.append(m.group(1))
    out = []
    body = [ln for ln in note_lines if ln.strip()]
    head = ""
    if not body or not body[0].strip().startswith("CREDIT-CHECK"):
        out.append(_f("note-header", FAIL, [1], "note does not start with a CREDIT-CHECK header line"))
    else:
        head = body[0]
    if head and not ISO_TS_RE.search(head):
        out.append(_f("note-timestamp", FAIL, [1], "CREDIT-CHECK header has no ISO timestamp (placeholder left unfilled?): %s" % head.strip()))
    elif head and not TS_TZ_RE.search(head):
        out.append(_f("note-timestamp", FAIL, [1], "CREDIT-CHECK timestamp has no timezone: %s" % head.strip()))
    rec, rec_ln = None, None
    for i, ln in enumerate(note_lines):
        m = REC_PLAIN_RE.match(ln)
        if m:
            rec, rec_ln = m.group(1).strip(), i + 1
            break
    if rec is None:
        out.append(_f("note-recommendation", FAIL, [1], "note has no 'Recommendation:' line"))
    elif rec.startswith("["):
        out.append(_f("note-recommendation", FAIL, [rec_ln], "Recommendation is still the unfilled template: %s" % rec))
    elif vocab and rec not in vocab:
        out.append(_f("note-recommendation", FAIL, [rec_ln],
                      "Recommendation '%s' is not a mode defined by the spec (allowed: %s)" % (rec, ", ".join(sorted(vocab)))))
    elif not vocab:
        out.append(_f("note-recommendation", ADVISORY, [rec_ln], "spec exposes no mode vocabulary; Recommendation could not be validated"))
    if not any(ln.strip().lower().startswith("grok") for ln in note_lines):
        out.append(_f("note-grok", FAIL, [1], "note has no Grok/xAI line (spec requires both providers be reported; UNKNOWN is allowed)"))
    if names:
        missing = [n for n in names
                   if not any(n in ln and sum(1 for o in names if o in ln) == 1 for ln in note_lines)]
        if missing:
            out.append(_f("note-model-lines", FAIL, [1],
                          "no dedicated budget line for: %s (separately-budgeted models must be reported separately)" % ", ".join(missing)))
    return out


def report(findings, as_json, strict):
    fails = [f for f in findings if f["severity"] == FAIL]
    advs = [f for f in findings if f["severity"] == ADVISORY]
    if as_json:
        print(json.dumps({"findings": findings, "fail": len(fails), "advisory": len(advs)}, indent=2, sort_keys=True))
    else:
        print("specguard: %d finding(s) [%d FAIL, %d ADVISORY]" % (len(findings), len(fails), len(advs)))
        for f in fails + advs:
            loc = ",".join("L%d" % n for n in f["lines"]) or "-"
            print("  %-9s %-24s %-24s %s" % (f["severity"], f["check"], loc, f["message"]))
    return 1 if fails or (strict and advs) else 0


GOOD_SPEC = '''# SYSTEM vGOOD

## Hierarchy

tree text

## Credit-Aware Routing (browser checks)

**Claude weekly reset: Sunday 21:00 America/New_York.**

```
CREDIT-CHECK [2026-08-14T18:36Z]
Fable weekly: ~40% used
Opus weekly: ~40% used
Grok/xAI: UNKNOWN
Recommendation: [NORMAL | CONSERVE_CLAUDE | CLAUDE_CRITICAL | UNKNOWN]
```

### Weekly thresholds (per model)

| Remaining | Mode | Action |
|-----------|------|--------|
| > 20% | NORMAL | go |
| 5-20% | CONSERVE_CLAUDE | slow |
| < 5% | CLAUDE_CRITICAL | stop |
| unreadable | UNKNOWN | conserve |

## Claude model split

- **Claude Fable 5 Max** - orchestration only
- **Claude Opus 5 Max** - all other work

## Hard rules

1. one
2. two

See Hard Rule 2 for details.

## Version History
- v1 - ADDED: hierarchy loop
- v1.1 - ADDED: credit-aware routing browser checks thresholds reset
- v1.2 - ADDED: hard rules; claude model split
'''

BAD_SPEC = '''# SYSTEM vBAD

## Hierarchy

tree text

## Credit-Aware Routing (browser checks)

**Claude weekly reset: Sunday 9:00 PM.**

```
CREDIT-CHECK [timestamp]
Claude Fable/Opus weekly: ~XX% used - reset Sunday 9pm
Grok/xAI: [exact %]
Recommendation: [NORMAL | CONSERVE_CLAUDE | STOP_LONG_RUNS]
```

### Claude thresholds (Fable / Opus weekly)

| Remaining | Mode | Action |
|-----------|------|--------|
| > 20% | NORMAL | go |
| < 5% | CLAUDE_CRITICAL | stop |

## Claude model split

- **Claude Fable 5 Max** - orchestration only
- **Claude Opus 5 Max** - all other work

## Hard rules

1. one
2. two

See Hard Rule 5 for details.

## Version History
- v1 - ADDED: hierarchy
- v1.1 - ADDED: hard rules
- v1.3 - ADDED: model split
'''

GOOD_NOTE = '''CREDIT-CHECK [2026-08-14T18:36Z]
Fable weekly: ~38% used (~62% remaining)
Opus weekly: ~15% used (~85% remaining)
Grok/xAI: plan-level only
Recommendation: NORMAL
'''

BAD_NOTE = '''CREDIT-CHECK [timestamp]
Claude Fable/Opus weekly: ~2% used
Recommendation: CLAUDE_CRITICAL_ISH
'''


def self_test():
    state = {"ok": True}

    def expect(label, cond, detail=""):
        print("  %s %s%s" % ("PASS" if cond else "FAIL", label, ("  <- " + detail) if (detail and not cond) else ""))
        if not cond:
            state["ok"] = False

    print("specguard self-test")
    good = run_lint(GOOD_SPEC.splitlines())
    expect("clean spec produces no findings", not good, repr(good))
    bad = run_lint(BAD_SPEC.splitlines())
    ids = set(f["check"] for f in bad)
    for want in ["version-numbering", "section-not-in-history", "mode-enum-undeclared", "mode-enum-missing",
                 "reset-timezone", "reset-format", "hard-rule-ref", "model-budget-collapsed"]:
        expect("planted defect detected: %s" % want, want in ids, "got " + repr(sorted(ids)))
    gn = check_note(GOOD_SPEC.splitlines(), GOOD_NOTE.splitlines())
    expect("valid CREDIT-CHECK note accepted", not gn, repr(gn))
    bn = set(f["check"] for f in check_note(GOOD_SPEC.splitlines(), BAD_NOTE.splitlines()))
    for want in ["note-timestamp", "note-recommendation", "note-grok", "note-model-lines"]:
        expect("bad note rejected: %s" % want, want in bn, "got " + repr(sorted(bn)))
    print("self-test: %s" % ("PASS" if state["ok"] else "FAIL"))
    return 0 if state["ok"] else 1


def main(argv=None):
    ap = argparse.ArgumentParser(description="Mechanical consistency checks for the SYSTEM spec and CREDIT-CHECK notes.")
    ap.add_argument("--spec", help="path to SYSTEM-vX-FOR-CLAUDE.md")
    ap.add_argument("--check-note", dest="note", help="path to a CREDIT-CHECK note to validate against the spec")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--strict", action="store_true", help="treat ADVISORY findings as failures")
    ap.add_argument("--self-test", action="store_true", help="run built-in fixtures and exit")
    args = ap.parse_args(argv)
    if args.self_test:
        return self_test()
    if not args.spec:
        ap.print_usage(sys.stderr)
        print("error: --spec is required (or --self-test)", file=sys.stderr)
        return 2
    try:
        doc = read_lines(args.spec)
    except OSError as exc:
        print("error: cannot read %s: %s" % (args.spec, exc), file=sys.stderr)
        return 2
    findings = run_lint(doc)
    if args.note:
        try:
            note = read_lines(args.note)
        except OSError as exc:
            print("error: cannot read %s: %s" % (args.note, exc), file=sys.stderr)
            return 2
        findings += check_note(doc, note)
    return report(findings, args.json, args.strict)


if __name__ == "__main__":
    sys.exit(main())
