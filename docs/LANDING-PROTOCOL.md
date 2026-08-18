# LANDING PROTOCOL

How any Claude session gets a commit onto the canonical GitHub repo with zero Owner effort. Three tiers, best first — use the highest tier available and say which one you used.

## Tier 1 — Session-attached repo (best; the only unattended tier)

**When:** the session/environment was created with `autonomy-system` (or the project's repo) attached. **Mechanics:** commit in the sandbox and `git push origin main` directly — nothing else moves.

This is the only tier that works with the Owner's desktop offline, so **every scheduled or autonomous run MUST use an environment with the repo attached.** Proxy facts, probed 2026-08-18: the sandbox git proxy binds allowed repos at session creation; it refuses anything else *before* reading credentials, so an externally supplied token in the URL is rejected by the proxy (403), not by GitHub (401) — supplying a token does not help. Mid-session attach is not currently possible (the desktop add-repo picker is defective; see PATCH-NOTES). If the repo was not attached at creation, drop to Tier 2.

## Tier 2 — Local-shell landing (default day-to-day)

**When:** the sandbox cannot push but the Owner's desktop app is online. **Mechanics:**

1. Sandbox builds the commit on top of the verified `origin/main`.
2. Sandbox makes a thin bundle: `git bundle create <file> <base>..main`, where `<base>` is the `origin/main` tip you actually fetched and verified this session. `git bundle verify <file>` before handing it over.
3. Write the bundle into the Owner's connected folder via the device bridge (`C:\Users\chris\OneDrive\Desktop\AUTONOMOUS-MULTI-AGENT-SYSTEM`).
4. Claude runs, through the desktop local shell: `powershell -ExecutionPolicy Bypass -File C:\Users\chris\autonomy-system-live\tools\land.ps1 -Bundle "<path to bundle>"`

`land.ps1` fetches, fast-forwards the standing clone `C:\Users\chris\autonomy-system-live` to canonical, fast-forwards the bundle in, pushes, and prints `LANDED <sha>`. Credentials stay in the Owner's Git Credential Manager on his machine. Claude performs this itself — the Owner does nothing.

## Tier 3 — One-click fallback

**When:** tiers 1 and 2 are both unavailable (no attached repo *and* desktop local shell unreachable). **Mechanics:** drop the bundle plus a generated `.bat` wrapper into the connected folder and ask the Owner to double-click it. Retired to fallback by Owner order 2026-08-18 — never the first choice, and always say why the higher tiers failed.

## Invariants

- Fast-forward only, at every step. No force-push, no rebase of landed history, ever. A rejected fast-forward means the bundle base is stale: rebuild the bundle on the current tip, do not override.
- No credentials in the sandbox, the repo, Drive, or memory — Tier 1 uses the proxy's own binding, Tier 2 uses the Owner's local credential store.
- Verify after every landing: `git ls-remote` SHA matches, the Actions run result via the Drive mirror write-through, and the mirror file's `modifiedTime` has advanced. An unverified landing is not a landing.
- **Post-land verification is a Drive CONTENT check, not a timestamp check.** Name, before landing, a heading or exact string that THIS commit introduces (e.g. the new version-history row, or a new section heading), then read the mirrored file and confirm that string is present. A `modifiedTime` advance alone is NOT sufficient — the sync can rewrite a file with stale or partial content and still bump the timestamp. State the string you checked and the file you found it in; if the string is absent, the landing is UNVERIFIED regardless of a green Actions run.
- **Pre-land critique gate (every tier, Tier 2 included).** Before any landing the gate runs `python3 tools/validate_journal.py --all` (it must exit 0) AND confirms that this change's required `grok_critique` records are present in `docs/run-journals/run-journal.jsonl` — 1 for routine, 3 for the ladder. Landing work that was marked `BLOCKED_ON_CRITIQUE` without its critique records is a protocol violation, not a shortcut: `land.ps1` is a dumb fast-forward transport and enforces nothing, so this is the gate's own step. Mechanical enforcement of it remains open items 2 and 5.
- **Consequence, intended:** SIGNIFICANT work cannot land from unattended sessions until a headless critique transport exists (open item 13); routine work may land under the critique-frequency rules. The accepted-risk waiver NEVER authorizes landing significant work without critique — it only covers CLI-only operation while the machine is up; machine off = `BLOCKED_ON_CRITIQUE` regardless of any waiver.
- retrieval_ref discipline is unchanged — every landing still carries its ref.
- Generalizes to any new project repo: same three tiers. Attach that repo at session creation for Tier 1; for Tier 2 pass `land.ps1 -Repo <path>` or clone `<project>-live` beside the standing clone.
