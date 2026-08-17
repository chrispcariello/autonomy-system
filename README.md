# autonomy-system

Canonical store for the **Autonomous Multi-Agent System** documentation — currently **SYSTEM v4.1.8**.

This private repo is the source of truth. The Google Drive folder `AUTONOMY-SYSTEM`
(id `1E-0tL4DGXk-HVYNlWUc6ccF6SzZh60OE`) is a **shared mirror** for external review, kept up to
date by the `sync-docs-to-drive` GitHub Actions workflow. Any product-local sandbox
(`/root/staging/...`) is temporary scratch and is never authoritative.

## Layout

| Path | What it is |
|------|------------|
| `docs/SYSTEM-CURRENT.md` | FOR-CLAUDE package — the operating document agents read |
| `docs/SYSTEM-SPEC-CURRENT.md` | Full specification (layers, rules, routing) |
| `docs/PATCH-NOTES-CURRENT.md` | Per-version patch notes, changelog, and open items |
| `docs/lessons/lessons.jsonl` | Learning Memory lessons (one JSON object per line) |
| `docs/run-journals/run-journal.jsonl` | Structured run journal events |
| `docs/run-journals/SMOKE-*.md` | Smoke-test run records |
| `tools/specguard.py` | Mechanical consistency linter for the SYSTEM docs |
| `tools/drive_sync.py` | Upserts `docs/` into the Drive mirror folder |
| `tools/setup_drive_oauth.py` | Owner's one-time local OAuth helper (browser consent → repo secrets) |
| `SETUP-DRIVE-OAUTH.bat` | Windows double-click wrapper for the helper above |
| `.github/workflows/sync-docs-to-drive.yml` | Runs the sync on any `docs/**` push and on demand |

## Shared visibility + version control

- Canonical store: private GitHub repo `autonomy-system`
- Shared mirror: Google Drive AUTONOMY-SYSTEM folder for external review
- A run is incomplete until: (1) docs committed + tagged on version change, (2) Drive mirror updated via Actions or explicit sync, (3) Summary Report includes commit SHA and Drive folder link
- /root/staging remains temporary only
- Never commit secrets, OAuth client secrets, service-account keys, or .env files

## Drive sync setup — OAuth (current)

The sync authenticates **as the Owner** via an OAuth refresh token, so files it uploads
are Owner-owned. That is what makes CREATE work: a service account has no Drive storage
quota and cannot own a new file in a consumer My Drive folder (see the legacy note
below). Until the three `GOOGLE_OAUTH_*` secrets exist the workflow fails fast with
`BLOCKED_ON_OWNER_SECRETS`. All five steps are Owner-only — no agent can do them, and no
credential value is ever printed, logged, or committed.

1. **OAuth consent screen.** [console.cloud.google.com](https://console.cloud.google.com)
   → the **same project** where the Google Drive API is enabled → APIs & Services →
   **OAuth consent screen**: User type **External**, add **yourself as a test user**, and
   add the scope `.../auth/drive` (`https://www.googleapis.com/auth/drive`).
   While the app's publishing status stays **Testing**, Google expires the refresh token
   after **7 days** — click **Publish app** on that same screen to keep it long-lived
   (staying unverified is fine; you are the only user). If the sync ever fails with
   `invalid_grant`, the token died: re-run `SETUP-DRIVE-OAUTH.bat` to mint a fresh one.
2. **OAuth client.** Credentials → Create credentials → **OAuth client ID** →
   Application type **Desktop app** → Create → **Download JSON**. Leave the downloaded
   `client_secret*.json` in your **Downloads** folder.
3. **Run `SETUP-DRIVE-OAUTH.bat`** (double-click it in the repo folder). It finds
   `client_secret*.json` in either the repo folder or Downloads, opens your browser —
   click **Allow** (the "unverified app" warning is expected; you are your own test
   user) — and then stores the three repo secrets `GOOGLE_OAUTH_CLIENT_ID`,
   `GOOGLE_OAUTH_CLIENT_SECRET`, `GOOGLE_OAUTH_REFRESH_TOKEN`. If the **GitHub CLI**
   (`gh`) is installed and logged in, this is silent — zero prompts. Otherwise it walks
   you through **3 clipboard-paste prompts**: each value lands on your clipboard, the
   GitHub "New secret" page opens, you type the name shown, paste, save, press Enter.
   The refresh token is held in memory only; nothing is written to disk.
4. **Delete `client_secret*.json`** from Downloads (and the repo folder if you copied it
   there). It is a credential — it must never live in this repo or a shared folder.
5. **Run the sync:** Actions → **sync-docs-to-drive** → Run workflow, or push any change
   under `docs/`. The run logs `MODE=oauth` and `auth: oauth (owner)`, never a value.

### Legacy: service account (updates only)

The original setup used a service-account JSON key in `GOOGLE_SERVICE_ACCOUNT_JSON`, and
`drive_sync.py` still falls back to it when no OAuth secrets are present. It is not
sufficient on its own: a service account has **no Drive storage quota**, so any CREATE
into the Owner's My Drive folder is rejected with `403 storageQuotaExceeded`
("Service Accounts do not have storage quota"). UPDATEs of files the Owner already owns
do succeed, which is why the fallback is kept — but new files, including new subfolders,
require the OAuth path above. The fallback prints
`auth: service-account (fallback - updates only; creates will fail on My Drive)` and, on
that 403, an error pointing back to this section. The folder must also be shared with
the service account's `client_email` as **Editor** for even updates to work.

## specguard

Lint the SYSTEM docs for mechanical inconsistencies (version-history gaps, unattributed
sections, mode-enum drift, timezone-less reset times, hard-rule numbering):

```sh
python3 tools/specguard.py --spec docs/SYSTEM-CURRENT.md
```

Exit 0 = clean, 1 = findings, 2 = usage error. Add `--json` for machine-readable output,
`--strict` to treat advisories as failures, `--self-test` to run built-in fixtures.

## Never commit secrets

No credential of any kind belongs in this repo — no service-account JSON keys, no OAuth
client secret, no refresh tokens, no API keys, no `.env` files, no `.pem` files. Those
paths are in `.gitignore`, but `.gitignore` is a safety net, not the rule. Credentials
live in GitHub Actions secrets or in the Owner's password manager. If one is ever
committed, treat it as compromised: rotate it first, then rewrite history.
