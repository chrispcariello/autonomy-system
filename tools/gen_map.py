#!/usr/bin/env python3
"""gen_map.py — generate docs/SYSTEM-MAP.html, the Owner-facing living system map.

Stdlib only, no network, DETERMINISTIC: same tree in, byte-identical page out. There is no
wall-clock timestamp anywhere in what this script writes, so re-running it on an unchanged
tree is a no-op and `git status` stays clean — the same property that makes the staleness
check in `tools/validate_journal.py` meaningful for `docs/BRIEF-PACK.md`.

WHAT THIS IS. One self-contained HTML page (inline CSS + a few lines of inline JS, no
external fetches, no network, no localStorage, no cookies) that explains the system in lay
language to a NON-CODER Owner: who is on the team and which bill each one drains, what the
one-paste loop does, what gauntlet every change walks, how the briefings keep themselves
current, and where the system stands right now. It is the FOURTH generated output of the
regeneration rule in `docs/EFFICIENCY-MODE.md`, alongside the three `tools/gen_brief.py`
writes.

WHAT THIS IS NOT. It is not a rule source and never resolves a disagreement in its own
favour. Canonical documents win, always; this page is a picture OF them.

THE ANTI-DRIFT DEVICE, because a picture is exactly the artifact that quietly goes stale:
every lay-language claim on the page is ANCHORED to a phrase that must be present in a named
canonical source (`require_phrase`). Delete or reword the rule and generation FAILS LOUDLY
with exit 2 naming the claim and the file — the map cannot outlive the rule it describes.
Anchors prove the phrase is still THERE; they cannot prove the surrounding paragraph still
MEANS what the panel says it means. That residual is stated on the page itself rather than
hidden here.

SOURCES AND FRESHNESS. The manifest is `gen_brief.SOURCES`, imported rather than copied, so
the two generators cannot drift apart on what "the rulebook" is. The page carries the same
`SELF-DIGEST` / `MANIFEST-DIGEST` / manifest-table footer shape the pack carries, and
`tools/validate_journal.py --all` re-hashes it through the SAME code path (C6), not a fork.

THE ONE FIGURE OUTSIDE THE MANIFEST, named rather than buried: the journal RECORD COUNT is
read from `docs/run-journals/run-journal.jsonl`, which is deliberately NOT a manifest source
(it is append-only evidence and grows on every landing). So a journal append makes this page's
record count LAG without making it STALE by C6 — the detector for that is
`python3 tools/gen_map.py --check` in the pre-land step, and the practical rule is: regenerate
AFTER the journal appends, last thing before the commit. The page says so where it prints the
number.
"""

import argparse
import hashlib
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gen_brief  # noqa: E402  - sibling module, imported for its SOURCES and helpers

GenError = gen_brief.GenError

OUT_MAP = os.path.join("docs", "SYSTEM-MAP.html")

# Display-only, deliberately OUTSIDE the manifest. See the module docstring.
JOURNAL_REL = os.path.join("docs", "run-journals", "run-journal.jsonl")

ZERO_DIGEST = gen_brief.ZERO_DIGEST
SELF_DIGEST_LINE = re.compile(r"^SELF-DIGEST: [0-9a-f]{64}$", re.MULTILINE)


# --------------------------------------------------------------- anchoring


def require_phrase(texts, rel, phrase, claim):
    """Assert that a canonical source still contains the phrase a lay claim rests on.

    This is the whole anti-drift mechanism. A map that keeps asserting "Grok never writes"
    after that rule was deleted is worse than no map, because it is confidently wrong in the
    Owner's own words. Honest limit: presence of a phrase is not preservation of a meaning —
    a rule can be reversed in the sentence AROUND an intact phrase and this will not notice.
    """
    if rel not in texts:
        raise GenError("anchor names a file outside SOURCES: %s" % rel)
    if phrase not in texts[rel]:
        raise GenError(
            "ANCHOR BROKEN — the map claims %r on the strength of the phrase %r in %s, and "
            "that phrase is no longer there. Either the rule changed (fix the map) or the "
            "wording moved (fix the anchor). Refusing to publish a picture of a rulebook "
            "that no longer says this." % (claim, phrase, rel)
        )
    return phrase


def one_match(pattern, text, rel, what):
    found = re.search(pattern, text)
    if not found:
        raise GenError("cannot read %s out of %s (pattern %r)" % (what, rel, pattern))
    return found


# ------------------------------------------------------------------ gather


def gather(root):
    texts = {}
    sources = {}
    for rel in gen_brief.SOURCES:
        text = gen_brief.read_source(root, rel)
        texts[rel] = text
        sources[rel] = gen_brief.sha256_text(text)

    sc = texts["docs/SYSTEM-CURRENT.md"]
    pn = texts["docs/PATCH-NOTES-CURRENT.md"]
    landing = texts["docs/LANDING-PROTOCOL.md"]
    handoff_file = texts["docs/LATEST-HANDOFF.md"]

    version = gen_brief.current_version(sc, "docs/SYSTEM-CURRENT.md")
    items, counts = gen_brief.open_items(pn, "docs/PATCH-NOTES-CURRENT.md")
    if not counts:
        raise GenError(
            "no '**N listed, M open**' count line in the authoritative open-items section of "
            "docs/PATCH-NOTES-CURRENT.md — the map will not invent one"
        )
    listed, still_open = counts
    closed = sum(1 for _, _, state in items if state == "CLOSED")

    # Critique depth, read out of the ladder rather than asserted.
    ladder = gen_brief.extract_section(sc, "### Critique ladder", "docs/SYSTEM-CURRENT.md")
    routine_passes = one_match(
        r"\*\*Routine\s*(?:→|->)\s*(\d+)\s+focused", ladder, "docs/SYSTEM-CURRENT.md",
        "the routine critique pass count").group(1)
    significant_passes = one_match(
        r"\*\*Significant\s*(?:→|->)\s*(\d+)-pass", ladder, "docs/SYSTEM-CURRENT.md",
        "the significant critique pass count").group(1)
    pass_titles = [t.strip() for t in
                   re.findall(r"\*\*Pass\s+\d+\s+[-—]+\s+([^:*]+)", ladder)]
    if len(pass_titles) != int(significant_passes):
        raise GenError(
            "the ladder advertises %s passes but names %d of them in docs/SYSTEM-CURRENT.md"
            % (significant_passes, len(pass_titles))
        )

    owner_flow = texts["docs/OWNER-FLOW.md"]
    lanes = [m.strip() for m in re.findall(r"^###\s+(Lane\s+\d+\s*[-—]+\s*.+?)\s*$",
                                          owner_flow, re.MULTILINE)]
    if len(lanes) != 4:
        raise GenError(
            "expected four '### Lane N' headings in docs/OWNER-FLOW.md (its own '## The four "
            "lanes' section), found %d — the map will not describe a lane map it cannot read"
            % len(lanes)
        )
    autopilot = [lane for lane in lanes if "AUTOPILOT" in lane.upper()]
    if len(autopilot) != 1:
        raise GenError(
            "docs/OWNER-FLOW.md does not name exactly one AUTOPILOT lane — the one-paste panel "
            "describes that lane specifically and must not guess which one it is"
        )

    fix_loops = one_match(
        r"fix-loop max (\d+) then BLOCK", sc, "docs/SYSTEM-CURRENT.md",
        "the autopilot fix-loop bound").group(1)

    tiers = []
    for line in landing.split("\n"):
        found = re.match(r"^##\s+(Tier\s+\d+\s*[-—]+\s*[^*]+?)\s*$", line)
        if found:
            tiers.append(found.group(1).strip())
    if len(tiers) != 3:
        raise GenError(
            "expected exactly three '## Tier N' headings in docs/LANDING-PROTOCOL.md, found %d"
            % len(tiers)
        )

    # The last landed commit AS RECORDED IN THE BATON. Not a git call: this generator never
    # shells out, and a SHA read from the file is a claim the file already makes.
    sha_match = re.search(r"^SHA:\s*([0-9a-f]{40})", handoff_file, re.MULTILINE)
    if sha_match:
        sha_short = sha_match.group(1)[:7]
        sha_full = sha_match.group(1)
        sha_note = "as recorded in the run baton"
    else:
        # The newest baton says STAGED whenever the run that wrote it has not been gated yet:
        # a file cannot contain its own landing SHA. Print that rather than a plausible number.
        sha_short = "not yet"
        sha_full = "the current baton records no pushed SHA (STAGED)"
        sha_note = "the newest baton is still STAGED; the gate commit fills this in"

    # The Changed: field is a hard-wrapped multi-line block, so take it whole (up to the next
    # HANDOFF field) and collapse it. Reading only the first physical line would cut the
    # sentence mid-clause and print a fragment as if it were the summary.
    changed_block = re.search(
        r"^Changed:\s*(.+?)(?=\n[A-Z][A-Za-z ]*:\s)", handoff_file, re.MULTILINE | re.DOTALL)
    last_changed = re.sub(r"\s+", " ", changed_block.group(1)).strip() if changed_block else ""
    last_changed = re.sub(r"[`*]", "", last_changed)
    if len(last_changed) > 260:
        last_changed = last_changed[:257].rsplit(" ", 1)[0] + "..."

    history_row = gen_brief.newest_history_row(sc, "docs/SYSTEM-CURRENT.md")
    last_land = re.sub(r"^- \*\*(v[0-9.]+)\*\*\s*[-—]+\s*", r"\1 — ", history_row)
    last_land = re.sub(r"\(this document\)\s*", "", last_land)
    last_land = re.sub(r"[`*]", "", last_land)
    if len(last_land) > 320:
        last_land = last_land[:317].rstrip() + "..."

    # Journal record count — display only, outside the manifest. See the module docstring.
    journal_path = os.path.join(root, JOURNAL_REL)
    if not os.path.isfile(journal_path):
        raise GenError("the run journal is missing: %s" % JOURNAL_REL)
    with open(journal_path, "r", encoding="utf-8") as handle:
        journal_records = sum(1 for line in handle if line.strip())
    if journal_records == 0:
        raise GenError("the run journal has no records: %s" % JOURNAL_REL)

    validator = gen_brief.load_validator(root)
    if not hasattr(validator, "SELF_TEST_CASE_COUNT"):
        raise GenError(
            "tools/validate_journal.py does not export SELF_TEST_CASE_COUNT — the map will not "
            "hardcode a self-test count it cannot read from the checker itself"
        )
    self_tests = int(validator.SELF_TEST_CASE_COUNT)

    generated_outputs = [
        (gen_brief.OUT_PACK.replace(os.sep, "/"), "the Opus build crews",
         "the operating brief a crew self-briefs from before it touches anything"),
        (gen_brief.OUT_GROK.replace(os.sep, "/"), "Grok, the outside inspector",
         "the snapshot pasted at the top of every critique prompt"),
        (gen_brief.OUT_AGENTS.replace(os.sep, "/"), "Cursor and other outside agents",
         "the standing briefing an agent reads when it opens the repo"),
        (OUT_MAP.replace(os.sep, "/"), "you, the Owner",
         "this page"),
    ]

    facts = {
        "version": version,
        "listed": listed,
        "open": still_open,
        "closed": closed,
        "items": items,
        "routine_passes": routine_passes,
        "significant_passes": significant_passes,
        "pass_titles": pass_titles,
        "fix_loops": fix_loops,
        "tiers": tiers,
        "lanes": lanes,
        "autopilot_lane": autopilot[0],
        "sha_short": sha_short,
        "sha_full": sha_full,
        "sha_note": sha_note,
        "last_changed": last_changed,
        "last_land": last_land,
        "journal_records": journal_records,
        "self_tests": self_tests,
        "source_count": len(gen_brief.SOURCES),
        "generated_outputs": generated_outputs,
    }

    # ------------------------------------------------------------- anchors
    # Every lay claim below is checked against the rulebook before it is drawn.
    anchor_log = []

    def a(rel, phrase, claim):
        require_phrase(texts, rel, phrase, claim)
        anchor_log.append((claim, rel, phrase))
        return phrase

    facts["anchors"] = {
        "fable_role": a("docs/SYSTEM-CURRENT.md", "highest-level orchestration only",
                        "Fable only architects and inspects"),
        "fable_cost": a("docs/SYSTEM-CURRENT.md", "Fable is priced higher than Opus on token rates",
                        "Fable is the expensive seat"),
        "fable_bookends": a("docs/SYSTEM-CURRENT.md", "Fable appears only at bookends and gates.",
                            "Fable shows up only at the start and the end"),
        "opus_role": a("docs/SYSTEM-CURRENT.md", "all other Claude work",
                       "Opus crews do the building"),
        "grok_nowrite": a("docs/GROK.md", "Grok has no write path, permanently.",
                          "Grok never writes"),
        "grok_liberal": a("docs/SYSTEM-CURRENT.md", "Grok capacity is used liberally",
                          "Grok is used freely because it is a different bill"),
        "cursor_free": a("docs/SYSTEM-CURRENT.md", "Cursor usage draws zero Claude credit",
                         "Cursor does not spend Claude credit"),
        "cursor_pr": a("docs/SYSTEM-CURRENT.md", "Their output enters ONLY as pull requests",
                       "Cursor work comes in through the PR door"),
        "owner_paste": a("docs/SYSTEM-CURRENT.md", "one Owner paste",
                         "the Owner pastes once to start the autopilot lane"),
        "four_lanes": a("docs/OWNER-FLOW.md", "The four lanes",
                        "there are four lanes and only one of them is a single paste"),
        "fable_fixloop": a("docs/SYSTEM-CURRENT.md", "plus one per fix loop",
                           "Fable also returns once per fix loop"),
        "receipt_limit": a("docs/OWNER-FLOW.md", "nothing in this system meters per-model spend",
                           "the receipt is a proxy, not a bill"),
        "lean_scribe": a("docs/EFFICIENCY-MODE.md", "LEAN SCRIBE",
                         "the post-land read may be deferred to the next run"),
        "lgtm_fail": a("CLAUDE.md", "is a FAIL on significant work",
                       "an empty critique fails a significant pass"),
        "claude_scarce": a("docs/SYSTEM-CURRENT.md", "Claude usage is the scarce resource",
                           "the Claude meter is the scarce one"),
        "receipt": a("docs/SYSTEM-CURRENT.md", "Every run ends with a USAGE RECEIPT",
                     "every run ends with a receipt"),
        "fix_loop": a("docs/SYSTEM-CURRENT.md", "fix-loop max 3 then BLOCK",
                      "the fix loop is bounded, then it blocks"),
        "hr1": a("docs/SYSTEM-CURRENT.md", "Only Claude Code may perform live system writes",
                 "only Claude Code writes to the live system"),
        "hr3": a("docs/SYSTEM-CURRENT.md", "Everything else → Event Bus as UNVERIFIED",
                 "everything else arrives UNVERIFIED"),
        "postland": a("docs/LANDING-PROTOCOL.md",
                      "Post-land verification is a Drive CONTENT check, not a timestamp check.",
                      "after landing we read the words, not the clock"),
        "preland": a("docs/LANDING-PROTOCOL.md", "Pre-land critique gate (every tier",
                     "nothing lands before critique and the validators"),
        "regen": a("docs/EFFICIENCY-MODE.md", "docs/SYSTEM-MAP.html",
                   "this page is named in the regeneration rule as a required output"),
        "regen_rule": a("docs/EFFICIENCY-MODE.md",
                        "Any run that changes `docs/**` or `tools/**` MUST re-run",
                        "any change to the docs or the tools rebuilds the briefings"),
        "stale_fail": a("docs/EFFICIENCY-MODE.md", "is a `brief-pack-stale` FAIL",
                        "a stale briefing fails the run"),
        # Anchor phrases are kept SHORT and free of line breaks on purpose: the sources are
        # hard-wrapped prose, so a long phrase can straddle a newline and break an anchor for a
        # reflow that changed no rule at all. Short phrase, real signal.
        "canonical_wins": a("docs/EFFICIENCY-MODE.md", "canonical document wins",
                            "the canonical document always wins"),
    }
    # The anchor set is PUBLISHED on the page (collapsed) rather than kept in the source.
    # Ladder pass 2 b1/b5: presence of a phrase cannot prove the surrounding paragraph still
    # MEANS what the panel says, and one crew wrote both the generator and the page it checks.
    # Neither is fixable from inside the generator; what IS cheap is making every claim and its
    # exact evidence pointer readable by an outside reviewer in one place, so the check a
    # machine cannot do costs a human about a minute.
    facts["anchor_log"] = sorted(set(anchor_log))
    return texts, sources, facts


# -------------------------------------------------------------------- HTML

ESCAPES = (("&", "&amp;"), ("<", "&lt;"), (">", "&gt;"), ('"', "&quot;"))


def esc(value):
    text = str(value)
    for raw, encoded in ESCAPES:
        text = text.replace(raw, encoded)
    return text


# Palette: the reference instance from the dataviz skill, used by ROLE through CSS custom
# properties so light and dark swap in one place. Only the first THREE categorical slots are
# used for the meters, which is the documented all-pairs-safe cap for that palette; the
# fourth encoding is a neutral, not a fourth hue. Identity is never carried by colour alone —
# every meter chip is a coloured dot NEXT TO its written name.
STYLE = """
:root{
  color-scheme: light;
  --surface-0:#f4f3f0; --surface-1:#fcfcfb; --surface-2:#eceae5;
  --line:#d7d4cd; --line-strong:#b9b5ab;
  --ink:#0b0b0b; --ink-2:#52514e; --ink-3:#6f6d67;
  --meter-claude:#2a78d6; --meter-grok:#eb6834; --meter-free:#1baf7a; --meter-none:#6f6d67;
  --accent:#2a78d6; --good:#1baf7a; --warn:#eda100;
  --shadow:0 1px 2px rgba(11,11,11,.06),0 6px 18px rgba(11,11,11,.05);
}
@media (prefers-color-scheme: dark){
  :root:where(:not([data-theme="light"])){
    color-scheme: dark;
    --surface-0:#121211; --surface-1:#1a1a19; --surface-2:#232322;
    --line:#3a3a37; --line-strong:#55554f;
    --ink:#ffffff; --ink-2:#c3c2b7; --ink-3:#a3a299;
    --meter-claude:#3987e5; --meter-grok:#d95926; --meter-free:#199e70; --meter-none:#a3a299;
    --accent:#3987e5; --good:#199e70; --warn:#c98500;
    --shadow:0 1px 2px rgba(0,0,0,.4),0 6px 18px rgba(0,0,0,.35);
  }
}
:root[data-theme="dark"]{
  color-scheme: dark;
  --surface-0:#121211; --surface-1:#1a1a19; --surface-2:#232322;
  --line:#3a3a37; --line-strong:#55554f;
  --ink:#ffffff; --ink-2:#c3c2b7; --ink-3:#a3a299;
  --meter-claude:#3987e5; --meter-grok:#d95926; --meter-free:#199e70; --meter-none:#a3a299;
  --accent:#3987e5; --good:#199e70; --warn:#c98500;
  --shadow:0 1px 2px rgba(0,0,0,.4),0 6px 18px rgba(0,0,0,.35);
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; background:var(--surface-0); color:var(--ink);
  font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
}
.wrap{max-width:1080px;margin:0 auto;padding:28px 20px 72px}
header.top{display:flex;flex-wrap:wrap;gap:14px;align-items:flex-end;justify-content:space-between;margin-bottom:6px}
h1{font-size:30px;line-height:1.2;margin:0;letter-spacing:-.01em}
.sub{color:var(--ink-2);margin:8px 0 0;max-width:62ch}
.btn{
  font:inherit;font-size:13px;color:var(--ink-2);background:var(--surface-1);
  border:1px solid var(--line-strong);border-radius:999px;padding:7px 14px;cursor:pointer;
}
.btn:hover{color:var(--ink);border-color:var(--ink-3)}
.btn:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.panel{
  background:var(--surface-1);border:1px solid var(--line);border-radius:14px;
  padding:22px 22px 24px;margin:22px 0;box-shadow:var(--shadow);
}
.panel > h2{
  font-size:12px;letter-spacing:.10em;text-transform:uppercase;color:var(--ink-3);
  margin:0 0 4px;font-weight:700;
}
.panel > .lede{font-size:19px;font-weight:650;margin:0 0 16px;line-height:1.35}
.note{font-size:13px;color:var(--ink-3);margin:16px 0 0;line-height:1.5}
.grid{display:grid;gap:12px}
@media(min-width:720px){.cols-2{grid-template-columns:1fr 1fr}}
/* ---- team table ---- */
.team{display:grid;gap:10px}
.role{
  display:grid;grid-template-columns:minmax(0,1fr);gap:6px;
  border:1px solid var(--line);border-left:5px solid var(--meter);
  border-radius:10px;padding:13px 15px;background:var(--surface-2);
}
@media(min-width:760px){.role{grid-template-columns:200px minmax(0,1fr) 190px;align-items:baseline;gap:14px}}
.role .who{font-weight:700}
.role .what{color:var(--ink-2);font-size:14.5px}
.meter{display:inline-flex;align-items:center;gap:8px;font-size:13px;font-weight:650;white-space:nowrap}
.dot{width:11px;height:11px;border-radius:50%;background:var(--meter);flex:0 0 auto;
     box-shadow:0 0 0 2px var(--surface-2)}
.m-claude{--meter:var(--meter-claude)} .m-grok{--meter:var(--meter-grok)}
.m-free{--meter:var(--meter-free)} .m-none{--meter:var(--meter-none)}
/* ---- flow ---- */
.flow{display:grid;gap:10px}
.step{
  display:grid;grid-template-columns:34px minmax(0,1fr);gap:14px;align-items:start;
  padding:12px 14px;border:1px solid var(--line);border-radius:10px;background:var(--surface-2);
}
.step .n{
  width:30px;height:30px;border-radius:50%;display:grid;place-items:center;
  background:var(--accent);color:#fff;font-weight:700;font-size:14px;
}
.step .t{font-weight:650}
.step .d{color:var(--ink-2);font-size:14.5px;margin-top:2px}
.step .tag{
  display:inline-block;margin-top:6px;font-size:12px;font-weight:650;padding:2px 9px;
  border-radius:999px;border:1px solid var(--line-strong);color:var(--ink-2);background:var(--surface-1);
}
.fork{display:grid;gap:8px;margin-top:4px}
@media(min-width:720px){.fork{grid-template-columns:repeat(3,1fr)}}
.outcome{border:1px solid var(--line-strong);border-radius:10px;padding:11px 13px;background:var(--surface-2)}
.outcome b{display:block;font-size:14px;letter-spacing:.04em}
.outcome span{font-size:13.5px;color:var(--ink-2)}
.outcome.ok{border-left:5px solid var(--good)}
.outcome.fix{border-left:5px solid var(--warn)}
.outcome.stop{border-left:5px solid var(--meter-grok)}
/* ---- gauntlet ---- */
.gate{display:grid;gap:0}
.gate li{
  list-style:none;display:grid;grid-template-columns:26px minmax(0,1fr);gap:14px;
  padding:12px 2px 12px 0;border-bottom:1px solid var(--line);
}
.gate li:last-child{border-bottom:0}
.gate .mark{
  width:22px;height:22px;border-radius:6px;background:var(--surface-2);
  border:1px solid var(--line-strong);display:grid;place-items:center;
  font-size:12px;font-weight:700;color:var(--ink-2);margin-top:2px;
}
.gate .h{font-weight:650}
.gate .p{color:var(--ink-2);font-size:14.5px;margin-top:2px}
.count{font-variant-numeric:tabular-nums;font-weight:700;color:var(--ink)}
/* ---- stat tiles ---- */
.tiles{display:grid;gap:12px;grid-template-columns:repeat(2,minmax(0,1fr))}
@media(min-width:760px){.tiles{grid-template-columns:repeat(4,minmax(0,1fr))}}
.tile{border:1px solid var(--line);border-radius:11px;padding:14px 15px;background:var(--surface-2)}
.tile .k{font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3);font-weight:700}
.tile .v{font-size:27px;font-weight:700;line-height:1.15;margin-top:5px;font-variant-numeric:tabular-nums;
         overflow-wrap:anywhere}
.tile .s{font-size:12.5px;color:var(--ink-3);margin-top:4px}
/* ---- misc ---- */
table.items{width:100%;border-collapse:collapse;font-size:14px;margin-top:6px}
table.items th,table.items td{text-align:left;padding:7px 10px;border-bottom:1px solid var(--line)}
table.items th{font-size:11.5px;letter-spacing:.07em;text-transform:uppercase;color:var(--ink-3)}
table.items td.n{width:44px;font-variant-numeric:tabular-nums;color:var(--ink-3)}
.state{font-size:12px;font-weight:700;padding:2px 8px;border-radius:999px;border:1px solid var(--line-strong)}
.state.open{color:var(--ink);background:var(--surface-1)}
.state.closed{color:var(--ink-2);background:var(--surface-1);text-decoration:none}
details{margin-top:14px;border-top:1px solid var(--line);padding-top:12px}
summary{cursor:pointer;font-size:13.5px;font-weight:650;color:var(--ink-2)}
summary:focus-visible{outline:3px solid var(--accent);outline-offset:3px}
details p,details li{font-size:13.5px;color:var(--ink-2)}
code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.9em;
     background:var(--surface-2);border:1px solid var(--line);border-radius:5px;padding:1px 5px}
footer.foot{margin-top:34px;padding-top:18px;border-top:1px solid var(--line);
            font-size:13px;color:var(--ink-3);line-height:1.6}
.warnstrip{
  border:1px solid var(--line-strong);border-left:5px solid var(--warn);border-radius:10px;
  padding:12px 15px;background:var(--surface-2);font-size:14px;color:var(--ink-2);margin:18px 0 0;
}
a{color:var(--accent)}
@media print{.btn{display:none} .panel{break-inside:avoid;box-shadow:none}}
@media(prefers-reduced-motion:no-preference){.panel{transition:none}}
"""

SCRIPT = """
(function(){
  var b=document.getElementById('themeBtn');
  if(!b){return;}
  b.addEventListener('click',function(){
    var root=document.documentElement;
    var now=root.getAttribute('data-theme');
    var next=(now==='dark')?'light':'dark';
    root.setAttribute('data-theme',next);
    b.setAttribute('aria-pressed', next==='dark' ? 'true':'false');
    b.textContent = next==='dark' ? 'Light mode' : 'Dark mode';
  });
})();
"""


def panel_team(f):
    rows = [
        ("Fable", "m-claude", "Claude meter",
         "The architect and the inspector. Plans the run at the start and rules on it at the "
         "end &mdash; RATIFY, FIX or BLOCK. It is the priciest seat, so it appears at the "
         "bookends and, when it sends work back, once more per fix loop &mdash; never while "
         "the crews are building."),
        ("Opus crews", "m-claude", "Claude meter",
         "The builders. They do all the actual writing, on the cheaper Claude seat, with the "
         "expensive seat switched off while they work."),
        ("Grok", "m-grok", "Grok bill (separate)",
         "The outside inspector. It attacks the work before it lands, and drafts bulk text on "
         "request. It never writes to the system &mdash; every word it produces arrives "
         "UNVERIFIED and has to survive a Claude gate."),
        ("Cursor", "m-free", "Free (bundled)",
         "A second pool of builders that costs nothing extra. Its work only enters through the "
         "pull-request door and is merged by a Claude gate, never pushed straight in."),
        ("You, the Owner", "m-none", "One or two pastes",
         "One paste starts an autopilot run and you are not needed again until the verdict. "
         "In the other lanes you paste a second card to open the gate. Beyond that you are "
         "needed only for a true hard stop &mdash; money, legal, a third party, or "
         "credentials."),
    ]
    out = ['<section class="panel" aria-labelledby="p1">',
           '<h2 id="p1">Panel 1</h2>',
           '<p class="lede">The team, and which bill each one drains</p>',
           '<div class="team">']
    for who, cls, meter, what in rows:
        out.append(
            '<div class="role %s"><div class="who">%s</div>'
            '<div class="what">%s</div>'
            '<div class="meter"><span class="dot" aria-hidden="true"></span>%s</div></div>'
            % (cls, esc(who), what, esc(meter))
        )
    out.append('</div>')
    out.append(
        '<p class="note"><strong>Why the split matters:</strong> the Claude meter is the '
        'scarce one, so the design spends the other two first &mdash; the outside inspector '
        'runs on a separate bill and the second builder pool is bundled at no extra cost. '
        'Colour here is a convenience only: every row also says its meter in words.</p>'
    )
    out.append(
        '<details><summary>Show the rules this panel is drawn from</summary>'
        '<p>Anchored phrases, checked at generation time in <code>docs/SYSTEM-CURRENT.md</code> '
        'and <code>docs/GROK.md</code>: &ldquo;%s&rdquo; &middot; &ldquo;%s&rdquo; &middot; '
        '&ldquo;%s&rdquo; &middot; &ldquo;%s&rdquo; &middot; &ldquo;%s&rdquo; &middot; '
        '&ldquo;%s&rdquo; &middot; &ldquo;%s&rdquo;. If any of them disappears from the '
        'rulebook this page refuses to build.</p></details>'
        % (esc(f["anchors"]["fable_role"]), esc(f["anchors"]["fable_cost"]),
           esc(f["anchors"]["opus_role"]), esc(f["anchors"]["grok_nowrite"]),
           esc(f["anchors"]["cursor_free"]), esc(f["anchors"]["claude_scarce"]),
           esc(f["anchors"]["owner_paste"]))
    )
    out.append('</section>')
    return "\n".join(out)


def panel_loop(f):
    steps = [
        ("You paste once", "One message starts everything. Nothing else is asked of you until "
         "the run reports back.", "Owner"),
        ("Fable plans", "The architect reads the current state, decides the shape of the work "
         "and hands out the orders.", "Claude meter &mdash; short"),
        ("The crews build", "Opus crews (and, when the job fits the PR door, Cursor) do the "
         "work. The expensive seat is off for this whole stretch.",
         "Claude meter &mdash; cheap seat"),
        ("Grok attacks it", "The outside inspector tries to break the work before it lands: "
         "%s pass for a ROUTINE change, %s for a SIGNIFICANT one."
         % (esc(f["routine_passes"]), esc(f["significant_passes"])), "Grok bill"),
        ("Validators run", "Machine checks: the journal, the open-items board, the package "
         "sections, and whether every generated briefing is out of date. Note the gap: they "
         "catch a STALE briefing, not a DELETED one. Catching a deleted briefing is a "
         "separate step the builder runs by hand.", "Free"),
        ("It lands", "The change is committed to the private repo and mirrored out to the "
         "read-only Drive folder the inspector reads.", "Free"),
        ("Fable gates it", "The architect returns once, reads the baton and the journal, and "
         "rules.", "Claude meter &mdash; short"),
    ]
    lane_items = "".join("<li>%s</li>" % esc(lane) for lane in f["lanes"])
    out = ['<section class="panel" aria-labelledby="p2">',
           '<h2 id="p2">Panel 2</h2>',
           '<p class="lede">The one-paste loop &mdash; what happens after you hit send</p>',
           '<p class="note" style="margin:0 0 14px"><strong>Which lane this is.</strong> There '
           'are four, and only one of them is a single paste. The loop below is '
           '<strong>%s</strong>. In the routine and plan-touch lanes the same machinery runs, '
           'but you paste a second card to open the gate. The four:<ul>%s</ul></p>'
           % (esc(f["autopilot_lane"]), lane_items),
           '<div class="flow">']
    for index, (title, detail, tag) in enumerate(steps, start=1):
        out.append(
            '<div class="step"><div class="n" aria-hidden="true">%d</div><div>'
            '<div class="t">%s</div><div class="d">%s</div>'
            '<span class="tag">%s</span></div></div>' % (index, esc(title), detail, tag)
        )
    out.append('</div>')
    out.append(
        '<div class="fork" role="group" aria-label="The three ways a run can end">'
        '<div class="outcome ok"><b>RATIFY</b><span>The work is accepted and the run is '
        'closed on the record.</span></div>'
        '<div class="outcome fix"><b>FIX</b><span>A fix order goes back to the crews and the '
        'gate runs again &mdash; at most %s times, then it stops.</span></div>'
        '<div class="outcome stop"><b>BLOCK</b><span>Available at any gate, not just at the '
        'end. Nothing is marked done that is not done.</span></div></div>'
        % esc(f["fix_loops"])
    )
    out.append(
        '<p class="note">Then a scorecard comes back to you: what changed, which agents ran, '
        'and what is still open. Every run ends with one. Read the cost line for what it is '
        '&mdash; nothing here meters per-model spend, so the numbers are an honest proxy, not '
        'a bill. The real meter is in your Claude account settings.</p>'
    )
    out.append('</section>')
    return "\n".join(out)


def panel_gauntlet(f):
    pass_list = ", ".join(esc(title) for title in f["pass_titles"])
    tiers = "".join('<li>%s</li>' % esc(tier) for tier in f["tiers"])
    gates = [
        ("1", "The critique ladder",
         "A ROUTINE change takes <span class=\"count\">%s</span> inspection pass. A SIGNIFICANT "
         "one takes <span class=\"count\">%s</span>, in a fixed order: %s. On significant work "
         "an empty critique or an &ldquo;LGTM&rdquo; is a FAILED pass, not a cheap win."
         % (esc(f["routine_passes"]), esc(f["significant_passes"]), pass_list)),
        ("2", "The machine validators",
         "<span class=\"count\">%s</span> self-tests must pass, and the whole-repo check must "
         "come back clean, before anything is allowed to land. Those two run again "
         "automatically on the server after the push &mdash; but only those two. The extra "
         "pre-landing step that catches a DELETED briefing runs on the builder&rsquo;s machine "
         "only, so it is discipline, not a server guarantee."
         % esc(f["self_tests"])),
        ("3", "A named landing route",
         "Three routes exist and the run says which one it used:<ul>%s</ul>" % tiers),
        ("4", "The post-landing read-back",
         "Someone reads the actual words of the mirrored file to confirm the change arrived. A "
         "newer timestamp is not evidence &mdash; a broken sync can update the clock and keep "
         "the old text. Read the timing honestly: the gate is allowed to DEFER that read to the "
         "next run, so the gap between landing and confirmation can be one run wide, and a next "
         "run that never happens never discovers a broken sync. The deferral is not a waiver: "
         "the next run MUST read the mirror and write down what it found, and a gate may refuse "
         "to defer at all whenever a bad sync would be expensive to find late. If you want it "
         "checked immediately, say so &mdash; that instruction is always available to you."),
        ("5", "The gate",
         "The architect rules RATIFY, FIX or BLOCK and can overturn any decision the crew made."),
        ("6", "The permanent record",
         "Every pass, every dispatch and every ruling is written to the run journal, which "
         "held <span class=\"count\">%s</span> records when this page was built and only ever "
         "grows. Claims that cannot point at a record do not count." % esc(f["journal_records"])),
    ]
    out = ['<section class="panel" aria-labelledby="p3">',
           '<h2 id="p3">Panel 3</h2>',
           '<p class="lede">The gauntlet every change walks &mdash; six checkpoints, in order</p>',
           '<ul class="gate">']
    for mark, head, body in gates:
        out.append('<li><span class="mark" aria-hidden="true">%s</span><div>'
                   '<div class="h">%s</div><div class="p">%s</div></div></li>'
                   % (mark, esc(head), body))
    out.append('</ul>')
    out.append(
        '<div class="tiles" style="margin-top:16px">'
        '<div class="tile"><div class="k">Version</div><div class="v">%s</div>'
        '<div class="s">from the package title</div></div>'
        '<div class="tile"><div class="k">Journal records</div><div class="v">%s</div>'
        '<div class="s">read at build time; the file only grows</div></div>'
        '<div class="tile"><div class="k">Open items</div><div class="v">%s</div>'
        '<div class="s">of %s listed &middot; %s closed on record</div></div>'
        '<div class="tile"><div class="k">Validator self-tests</div><div class="v">%s</div>'
        '<div class="s">read out of the checker itself</div></div></div>'
        % (esc(f["version"]), esc(f["journal_records"]), esc(f["open"]),
           esc(f["listed"]), esc(f["closed"]), esc(f["self_tests"]))
    )
    out.append('</section>')
    return "\n".join(out)


def panel_briefings(f):
    rows = "".join(
        '<div class="role m-free"><div class="who"><code>%s</code></div>'
        '<div class="what">%s</div><div class="meter">'
        '<span class="dot" aria-hidden="true"></span>for %s</div></div>'
        % (esc(path), esc(what), esc(audience))
        for path, audience, what in f["generated_outputs"]
    )
    out = ['<section class="panel" aria-labelledby="p4">',
           '<h2 id="p4">Panel 4</h2>',
           '<p class="lede">The self-briefing loop &mdash; no briefing is allowed to go '
           'quietly out of date</p>',
           '<p class="note" style="margin:0 0 14px">Every change to the documents or the tools '
           'rebuilds all four briefings below, in the same commit as the change. Nobody has to '
           'remember to brief anyone.</p>',
           '<div class="team">%s</div>' % rows]
    out.append(
        '<div class="warnstrip"><strong>The enforcement, not the intention:</strong> if a '
        'briefing is out of date the run FAILS the validator and names the files that moved. '
        'That is what stops a briefing from rotting in place. Two limits stated plainly rather '
        'than glossed: a fresh briefing '
        'proves the sources have not moved since it was built &mdash; not that it summarises '
        'them well; and DELETING a briefing outright makes the freshness check skip rather '
        'than fail, so deletion is the one way a briefing can go quiet without a red light. '
        'The detector for that is <code>--check</code> on both generators, which runs on the '
        'builder&rsquo;s machine as a separate pre-landing step and is not repeated by the '
        'server.</div>'
    )
    out.append(
        '<p class="note">Precedence is fixed and one-directional: <strong>the canonical '
        'document always wins</strong>. These four files are a fast path to the current state, '
        'never an authority, and nothing may be closed, ratified or landed on one of them '
        'alone.</p>'
    )
    out.append('</section>')
    return "\n".join(out)


def panel_state(f):
    item_rows = "".join(
        '<tr><td class="n">%d</td><td>%s</td><td><span class="state %s">%s</span></td></tr>'
        % (number, esc(title), state.lower(), state)
        for number, title, state in f["items"]
    )
    out = ['<section class="panel" aria-labelledby="p5">',
           '<h2 id="p5">Panel 5</h2>',
           '<p class="lede">Where the system stands right now</p>',
           '<div class="tiles">'
           '<div class="tile"><div class="k">Version</div><div class="v">%s</div>'
           '<div class="s">package title</div></div>'
           '<div class="tile"><div class="k">Last landed commit</div><div class="v">%s</div>'
           '<div class="s">%s</div></div>'
           '<div class="tile"><div class="k">Open items</div><div class="v">%s</div>'
           '<div class="s">%s listed in total</div></div>'
           '<div class="tile"><div class="k">Journal records</div><div class="v">%s</div>'
           '<div class="s">at build time</div></div></div>'
           % (esc(f["version"]), esc(f["sha_short"]), esc(f["sha_note"]), esc(f["open"]),
              esc(f["listed"]), esc(f["journal_records"]))]
    out.append(
        '<div class="warnstrip"><strong>Read these as a snapshot, not as live state.</strong> '
        'Every figure here was frozen when this page was built. Before acting on any of them '
        '&mdash; deciding what is still open, whether something landed, or whether to start a '
        'run &mdash; open the sources: <code>docs/LATEST-HANDOFF.md</code> for the newest run, '
        '<code>docs/run-journals/run-journal.jsonl</code> for the record, and '
        '<code>docs/PATCH-NOTES-CURRENT.md</code> for the open items. Nothing is closed, '
        'ratified or landed on the strength of this page.</div>'
    )
    out.append(
        '<p class="note" style="margin-top:16px"><strong>What landed last:</strong> %s</p>'
        % esc(f["last_land"])
    )
    if f["last_changed"]:
        out.append('<p class="note"><strong>Files that run touched:</strong> %s</p>'
                   % esc(f["last_changed"]))
    out.append(
        '<details><summary>Show all %s tracked items (%s still open)</summary>'
        '<p><strong>Snapshot, not the board.</strong> These states were frozen when the page '
        'was built and an item may have opened or closed since. Never close, re-open or '
        'renumber an item from this table.</p>'
        '<table class="items"><thead><tr><th>#</th><th>Item</th><th>State</th></tr></thead>'
        '<tbody>%s</tbody></table>'
        '<p>Titles are shortened for scanning. The authoritative list, with the full text, the '
        'owner and the exit condition for each item, is the last '
        '<code>REMAINING OPEN ITEMS</code> section of '
        '<code>docs/PATCH-NOTES-CURRENT.md</code>.</p></details>'
        % (esc(f["listed"]), esc(f["open"]), item_rows)
    )
    out.append('</section>')
    return "\n".join(out)


def build_manifest_block(sources, manifest_digest, self_digest):
    rows = "\n".join(
        "| `%s` | `%s` |" % (rel, sources[rel]) for rel in gen_brief.SOURCES
    )
    return (
        "<!--\n"
        "SYSTEM-MAP MANIFEST - generated by tools/gen_map.py. Do not hand-edit this file.\n"
        "The two digests and the table below are re-computed by tools/validate_journal.py --all\n"
        "(check C6) through the same code path that checks docs/BRIEF-PACK.md.\n"
        "\n"
        "SELF-DIGEST: " + self_digest + "\n"
        "MANIFEST-DIGEST: " + manifest_digest + "\n"
        "\n"
        "| source | sha256 |\n"
        "| :-- | :-- |\n"
        + rows + "\n"
        "-->\n"
    )


def build_html(facts, sources, manifest_digest, self_digest):
    anchor_rows = "".join(
        "<tr><td>%s</td><td><code>%s</code></td><td>%s</td></tr>"
        % (esc(claim), esc(rel), esc(phrase))
        for claim, rel, phrase in facts["anchor_log"]
    )
    head = (
        "<!DOCTYPE html>\n"
        '<html lang="en" data-theme="">\n<head>\n'
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<meta name="color-scheme" content="light dark">\n'
        "<title>Living system map &mdash; autonomy-system " + esc(facts["version"]) + "</title>\n"
        "<style>" + STYLE + "</style>\n</head>\n<body>\n"
    )
    top = (
        '<div class="wrap">\n<header class="top">\n<div>\n'
        "<h1>How this system works</h1>\n"
        '<p class="sub">A picture of the autonomy-system in plain language. It is rebuilt from '
        'the rulebook itself every time anything lands, so it cannot drift away from what the '
        'system actually does.</p>\n</div>\n'
        '<button class="btn" id="themeBtn" type="button" aria-pressed="false">Dark mode</button>\n'
        "</header>\n"
        '<p class="note">Reading order: who is on the team &rarr; what one paste sets off '
        '&rarr; what every change has to survive &rarr; how the briefings keep themselves '
        'current &rarr; where things stand today.</p>\n'
    )
    body = "\n".join([
        panel_team(facts),
        panel_loop(facts),
        panel_gauntlet(facts),
        panel_briefings(facts),
        panel_state(facts),
    ])
    foot = (
        '\n<footer class="foot">\n'
        "<p><strong>Generated file &mdash; do not hand-edit.</strong> "
        "<code>tools/gen_map.py</code> writes this page from " + esc(facts["source_count"]) +
        " canonical documents, listed with their fingerprints in the manifest comment at the "
        "end of this file. Hand edits are overwritten at the next landing, and the "
        "<code>SELF-DIGEST</code> in that manifest is what makes such an edit detectable. "
        "It rebuilds itself at every landing: any change under <code>docs/</code> or "
        "<code>tools/</code> must regenerate it in the same commit, and "
        "<code>tools/validate_journal.py --all</code> fails a run that leaves it stale.</p>\n"
        "<p><strong>Canonical documents win.</strong> This page is a picture of the rules, "
        "never the rules themselves. On any disagreement between this page and a canonical "
        "document, the document is right and this page is stale. Nothing may be closed, "
        "ratified or landed on the strength of this file.</p>\n"
        "<p><strong>What the freshness check does and does not prove.</strong> It proves the "
        "source documents have not changed since this page was built. It does not prove the "
        "page describes them well. Every lay claim above is additionally anchored to an exact "
        "phrase that must still be present in a named document, and generation fails loudly if "
        "one goes missing &mdash; but a phrase can survive inside a paragraph whose meaning was "
        "reversed, and no check here would notice that. One figure sits outside the manifest on "
        "purpose: the journal record count, because the journal is append-only evidence that "
        "grows after this page is built, so that number is a floor read at build time rather "
        "than a live reading. The last landed commit "
        "(<code>" + esc(facts["sha_full"]) + "</code>) is read from the run baton, not from git.</p>\n"
        "<details><summary>Show every claim on this page and the exact rule it is anchored "
        "to (%d anchors)</summary>"
        "<p>Each row is a lay claim, the canonical file it was checked against, and the exact "
        "phrase that had to be present for this page to build at all. This table exists so the "
        "check a machine cannot do &mdash; does the surrounding paragraph still MEAN this "
        "&mdash; costs a reviewer about a minute instead of a re-read of the whole rulebook.</p>"
        "<table class=\"items\"><thead><tr><th>Claim on this page</th><th>Checked in</th>"
        "<th>Exact phrase required</th></tr></thead><tbody>" + anchor_rows +
        "</tbody></table></details>\n"
        "<p>No network requests, no tracking, no stored state: this file is inert HTML and "
        "renders offline. The one control on the page is a light/dark toggle that lasts only "
        "as long as the tab is open.</p>\n"
        "</footer>\n</div>\n"
    )
    script = "<script>" + SCRIPT + "</script>\n</body>\n</html>\n"
    manifest = build_manifest_block(sources, manifest_digest, self_digest)
    return head + top + body + foot + script + manifest


def generate(root):
    _texts, sources, facts = gather(root)
    manifest_digest = gen_brief.sha256_text(
        "\n".join("%s %s" % (rel, sources[rel]) for rel in gen_brief.SOURCES)
    )
    provisional = build_html(facts, sources, manifest_digest, ZERO_DIGEST)
    self_digest = gen_brief.sha256_text(provisional)
    final = build_html(facts, sources, manifest_digest, self_digest)
    # Belt and braces: the digest is over the page with a zeroed SELF-DIGEST, exactly the
    # normalisation tools/validate_journal.py performs. Prove it here rather than assume it.
    normalised = final.replace("SELF-DIGEST: " + self_digest, "SELF-DIGEST: " + ZERO_DIGEST)
    if gen_brief.sha256_text(normalised) != self_digest:
        raise GenError(
            "internal error: the SELF-DIGEST does not survive its own normalisation. The page "
            "must contain the digest string exactly once and nowhere else."
        )
    return {OUT_MAP: final}


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Generate docs/SYSTEM-MAP.html, the Owner-facing living system map."
    )
    parser.add_argument("--root", default=".", help="repo root")
    parser.add_argument("--check", action="store_true",
                        help="do not write; exit 1 if the output would change (CI/idempotency)")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    try:
        outputs = generate(args.root)
    except GenError as exc:
        sys.stderr.write("gen_map: FAIL - %s\n" % exc)
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

    if not args.quiet:
        print("gen_map: %s | SYSTEM-MAP %d bytes | %d manifest sources"
              % ("no change" if not changed else "wrote " + ", ".join(changed),
                 len(outputs[OUT_MAP]), len(gen_brief.SOURCES)))
    if args.check and changed:
        sys.stderr.write("gen_map: --check FAIL - would rewrite: %s\n" % ", ".join(changed))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
