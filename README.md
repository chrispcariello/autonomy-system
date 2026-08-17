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
| `.github/workflows/sync-docs-to-drive.yml` | Runs the sync on any `docs/**` push and on demand |

## Shared visibility + version control

- Canonical store: private GitHub repo `autonomy-system`
- Shared mirror: Google Drive AUTONOMY-SYSTEM folder for external review
- A run is incomplete until: (1) docs committed + tagged on version change, (2) Drive mirror updated via Actions or explicit sync, (3) Summary Report includes commit SHA and Drive folder link
- /root/staging remains temporary only
- Never commit secrets, OAuth client secrets, service-account keys, or .env files

## Drive sync setup

The workflow is wired and will run, but it **fails fast with
`BLOCKED_ON_OWNER_SECRETS`** until the Owner completes these steps. Nothing here needs
to be done by an agent — steps 1–4 require Owner-held credentials.

1. Create or choose a Google Cloud project, then enable the **Google Drive API** for it
   (APIs & Services → Library → Google Drive API → Enable).
2. Create a **service account** in that project (IAM & Admin → Service Accounts). No
   project roles are needed. Open the service account → Keys → Add key → Create new key →
   **JSON**, and download the key file.
3. Share the Drive folder **AUTONOMY-SYSTEM** (id `1E-0tL4DGXk-HVYNlWUc6ccF6SzZh60OE`)
   with the service account's `client_email` address (found in the key file), granting
   **Editor**. Drive access is per-folder — without this share the sync sees nothing.
4. Add the repo secret **`GOOGLE_SERVICE_ACCOUNT_JSON`** containing the full JSON key
   content, via GitHub → Settings → Secrets and variables → Actions → New repository
   secret, or from a terminal:

   ```sh
   gh secret set GOOGLE_SERVICE_ACCOUNT_JSON < key.json
   ```

5. Trigger a sync: push any change under `docs/`, or run it manually via
   Actions → **sync-docs-to-drive** → Run workflow.
6. **Delete the local key file** once the secret is stored. It must never live in this
   repo or in a shared folder.

### Alternative: OAuth client (fallback only)

If the Google Workspace org policy blocks service-account key creation, the fallback is
an OAuth client (Desktop app) plus a long-lived refresh token stored as a repo secret,
with a token-refresh step added ahead of the sync step to exchange it for an access
token. This is documented as a fallback only — the service-account path above is the
supported one, because an OAuth refresh token is bound to a human account and silently
breaks when that account's password or grants change.

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
