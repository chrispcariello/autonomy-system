#!/usr/bin/env python3
"""drive_sync.py - upsert a local directory tree into a Google Drive folder.

Credentials are read from the GOOGLE_SERVICE_ACCOUNT_JSON environment variable
(the full JSON key). The value is never printed or logged. Subfolders under the
destination folder are found-or-created by name; each file is upserted by
(name, parent). Prints one "CREATE|UPDATE <path>" line per file.

Exit 0 = synced, 1 = usage/IO error or Drive API error.

Usage:
  python3 drive_sync.py --src docs --folder <DRIVE_FOLDER_ID>
"""

import argparse
import json
import os
import sys

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/drive"]
FOLDER_MIME = "application/vnd.google-apps.folder"
TEXT_TYPES = {".md": "text/markdown", ".jsonl": "text/plain", ".txt": "text/plain"}
DEFAULT_MIME = "application/octet-stream"
SHARED = {"supportsAllDrives": True}


def mime_for(name):
    return TEXT_TYPES.get(os.path.splitext(name)[1].lower(), DEFAULT_MIME)


def credentials():
    raw = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "").strip()
    if not raw:
        sys.exit("error: GOOGLE_SERVICE_ACCOUNT_JSON is not set (value is never printed)")
    try:
        info = json.loads(raw)
    except ValueError:
        sys.exit("error: GOOGLE_SERVICE_ACCOUNT_JSON is not valid JSON (value is never printed)")
    return service_account.Credentials.from_service_account_info(info, scopes=SCOPES)


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
    return svc.files().create(body=body, fields="id", **SHARED).execute()["id"]


def upsert_file(svc, parent, path):
    name = os.path.basename(path)
    media = MediaFileUpload(path, mimetype=mime_for(name), resumable=False)
    existing = find_child(svc, parent, name)
    if existing:
        svc.files().update(fileId=existing, media_body=media, fields="id", **SHARED).execute()
        return "UPDATE"
    svc.files().create(body={"name": name, "parents": [parent]}, media_body=media,
                       fields="id", **SHARED).execute()
    return "CREATE"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Upsert a local tree into a Google Drive folder.")
    ap.add_argument("--src", required=True, help="local directory to mirror")
    ap.add_argument("--folder", required=True, help="destination Drive folder id")
    args = ap.parse_args(argv)

    src = os.path.abspath(args.src)
    if not os.path.isdir(src):
        sys.exit("error: --src is not a directory: %s" % args.src)

    svc = build("drive", "v3", credentials=credentials(), cache_discovery=False)
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
                print("%s %s" % (upsert_file(svc, folders[rel], os.path.join(root, fname)), shown))
                count += 1
    except HttpError as exc:
        sys.exit("error: Drive API call failed: %s" % exc)
    print("synced %d file(s) into Drive folder %s" % (count, args.folder))
    return 0


if __name__ == "__main__":
    sys.exit(main())
