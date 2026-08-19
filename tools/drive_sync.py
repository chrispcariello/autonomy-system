#!/usr/bin/env python3
"""drive_sync.py - upsert a local directory tree into a Google Drive folder.

Auth order (no credential value is ever printed or logged): (1) OAuth owner auth
when GOOGLE_OAUTH_CLIENT_ID + GOOGLE_OAUTH_CLIENT_SECRET +
GOOGLE_OAUTH_REFRESH_TOKEN are all set - created files are Owner-owned, so CREATE
and UPDATE both work on My Drive; (2) else GOOGLE_SERVICE_ACCOUNT_JSON - UPDATEs
of Owner-owned files work but CREATE fails 403 storageQuotaExceeded, because a
service account holds no Drive storage quota; (3) else exit 1 with
BLOCKED_ON_OWNER_SECRETS.

Subfolders under the destination folder are found-or-created by name; each file
is upserted by (name, parent). Prints one "CREATE|UPDATE <path>" line per file.
Exit 0 = synced, 1 = usage/IO error, missing secrets, or Drive API error.

Usage: python3 drive_sync.py --src docs --folder <DRIVE_FOLDER_ID>
"""

import argparse
import json
import os
import sys

from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive"]
TOKEN_URI = "https://oauth2.googleapis.com/token"
FOLDER_MIME = "application/vnd.google-apps.folder"
TEXT_TYPES = {".md": "text/markdown", ".jsonl": "text/plain", ".txt": "text/plain",
              # docs/SYSTEM-MAP.html is a generated docs/** file and therefore mirrors.
              # Without this row it would upload as application/octet-stream, which Drive
              # neither indexes nor renders - and the post-land CONTENT check (read the
              # words, not the clock) would have nothing to read.
              ".html": "text/html"}
DEFAULT_MIME = "application/octet-stream"
SHARED = {"supportsAllDrives": True}
OAUTH_VARS = ("GOOGLE_OAUTH_CLIENT_ID", "GOOGLE_OAUTH_CLIENT_SECRET",
              "GOOGLE_OAUTH_REFRESH_TOKEN")
SA_MODE = "auth: service-account (fallback - updates only; creates will fail on My Drive)"
SA_CREATE_HELP = (
    "error: CREATE of %s was refused with 403 storageQuotaExceeded.\n"
    "Cause: this run used service-account auth, and a service account has no Drive\n"
    "storage quota, so it cannot own a new file in a consumer My Drive folder.\n"
    "Updating files the Owner already owns works; creating new ones never will.\n"
    "Fix: set repo secrets GOOGLE_OAUTH_CLIENT_ID, GOOGLE_OAUTH_CLIENT_SECRET and\n"
    "GOOGLE_OAUTH_REFRESH_TOKEN by running SETUP-DRIVE-OAUTH.bat - see README\n"
    "section \"Drive sync setup - OAuth\"."
)


class CreateQuotaError(Exception):
    """A create call was refused for lack of storage quota (carries the item path)."""


def env(name):
    return os.environ.get(name, "").strip()


def credentials():
    """Resolve credentials; returns (creds, mode). No env value is ever printed."""
    if all(env(name) for name in OAUTH_VARS):
        creds = Credentials(token=None, token_uri=TOKEN_URI, scopes=SCOPES,
                            client_id=env("GOOGLE_OAUTH_CLIENT_ID"),
                            client_secret=env("GOOGLE_OAUTH_CLIENT_SECRET"),
                            refresh_token=env("GOOGLE_OAUTH_REFRESH_TOKEN"))
        print("auth: oauth (owner)")
        return creds, "oauth"
    raw = env("GOOGLE_SERVICE_ACCOUNT_JSON")
    if raw:
        try:
            info = json.loads(raw)
        except ValueError:
            sys.exit("error: GOOGLE_SERVICE_ACCOUNT_JSON is not valid JSON (never printed)")
        print(SA_MODE)
        return service_account.Credentials.from_service_account_info(info, scopes=SCOPES), \
            "service-account"
    sys.exit("BLOCKED_ON_OWNER_SECRETS: set GOOGLE_OAUTH_CLIENT_ID/SECRET/REFRESH_TOKEN "
             "(preferred) or GOOGLE_SERVICE_ACCOUNT_JSON")


def create_item(svc, body, media, shown):
    try:
        return svc.files().create(body=body, media_body=media, fields="id",
                                  **SHARED).execute()["id"]
    except HttpError as exc:
        if "storageQuotaExceeded" in "%s|%s" % (getattr(exc, "content", "") or "", exc):
            raise CreateQuotaError(shown)
        raise


def find_child(svc, parent, name, folder_only=False):
    esc = name.replace("\\", "\\\\").replace("'", "\\'")
    q = "name = '%s' and '%s' in parents and trashed = false" % (esc, parent)
    if folder_only:
        q += " and mimeType = '%s'" % FOLDER_MIME
    res = svc.files().list(q=q, spaces="drive", fields="files(id,name)", pageSize=10,
                           includeItemsFromAllDrives=True, **SHARED).execute()
    hits = res.get("files", [])
    return hits[0]["id"] if hits else None


def ensure_folder(svc, parent, name):
    found = find_child(svc, parent, name, folder_only=True)
    if found:
        return found
    body = {"name": name, "mimeType": FOLDER_MIME, "parents": [parent]}
    return create_item(svc, body, None, name + "/")


def upsert_file(svc, parent, path, shown):
    name = os.path.basename(path)
    mime = TEXT_TYPES.get(os.path.splitext(name)[1].lower(), DEFAULT_MIME)
    media = MediaFileUpload(path, mimetype=mime, resumable=False)
    existing = find_child(svc, parent, name)
    if existing:
        svc.files().update(fileId=existing, media_body=media, fields="id", **SHARED).execute()
        return "UPDATE"
    create_item(svc, {"name": name, "parents": [parent]}, media, shown)
    return "CREATE"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Upsert a local tree into a Google Drive folder.")
    ap.add_argument("--src", required=True, help="local directory to mirror")
    ap.add_argument("--folder", required=True, help="destination Drive folder id")
    args = ap.parse_args(argv)

    src = os.path.abspath(args.src)
    if not os.path.isdir(src):
        sys.exit("error: --src is not a directory: %s" % args.src)

    creds, mode = credentials()
    svc = build("drive", "v3", credentials=creds, cache_discovery=False)
    folders = {"": args.folder}
    count = 0
    try:
        for root, dirs, files in os.walk(src):
            dirs.sort()
            rel = os.path.relpath(root, src)
            rel = "" if rel == "." else rel.replace(os.sep, "/")
            if rel and rel not in folders:
                parent_rel, _, leaf = rel.rpartition("/")
                folders[rel] = ensure_folder(svc, folders[parent_rel], leaf)
            for fname in sorted(files):
                shown = "%s/%s" % (rel, fname) if rel else fname
                print("%s %s" % (upsert_file(svc, folders[rel],
                                             os.path.join(root, fname), shown), shown))
                count += 1
    except CreateQuotaError as exc:
        if mode == "service-account":
            sys.exit(SA_CREATE_HELP % exc)
        sys.exit("error: CREATE of %s refused: 403 storageQuotaExceeded (Drive full)" % exc)
    except HttpError as exc:
        sys.exit("error: Drive API call failed: %s" % exc)
    print("synced %d file(s) into Drive folder %s" % (count, args.folder))
    return 0


if __name__ == "__main__":
    sys.exit(main())
