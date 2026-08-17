#!/usr/bin/env python3
"""setup_drive_oauth.py - one-time LOCAL helper the Owner runs on his own machine.

What it does, in order:
  1. Finds client_secret*.json (this script's folder, then %USERPROFILE%\\Downloads).
  2. Runs the Google OAuth Desktop-app consent flow in your browser (you click
     Allow). The refresh token is held IN MEMORY only.
  3. Stores three GitHub Actions secrets on chrispcariello/autonomy-system:
     GOOGLE_OAUTH_CLIENT_ID, GOOGLE_OAUTH_CLIENT_SECRET, GOOGLE_OAUTH_REFRESH_TOKEN.
     Preferred path is the GitHub CLI (`gh secret set`), with each value piped on
     stdin so it never appears in a command line. If gh is missing or fails, it
     falls back to a clipboard flow: one value at a time on your clipboard, the
     GitHub "New secret" page opened for you, paste + save, press Enter.

No secret value is ever printed, logged, or written anywhere; this script writes
no files. Delete client_secret*.json when it finishes.

Requires: pip install google-auth google-auth-oauthlib
(SETUP-DRIVE-OAUTH.bat in the repo root installs those and runs this for you.)
"""

import glob
import os
import subprocess
import sys
import webbrowser

REPO = "chrispcariello/autonomy-system"
SCOPES = ["https://www.googleapis.com/auth/drive"]
NEW_SECRET_URL = "https://github.com/%s/settings/secrets/actions/new" % REPO
ORDER = ("GOOGLE_OAUTH_CLIENT_ID", "GOOGLE_OAUTH_CLIENT_SECRET",
         "GOOGLE_OAUTH_REFRESH_TOKEN")
CLIP_CMD = ["powershell", "-NoProfile", "-Command",
            "Set-Clipboard -Value ([Console]::In.ReadToEnd())"]
NO_JSON = """error: no client_secret*.json found. Looked in:
  %s
  %s

Create the OAuth client first (README section "Drive sync setup - OAuth"):
  1. console.cloud.google.com -> same project as the Drive API -> APIs & Services
     -> OAuth consent screen: User type External, add yourself as a test user,
     add scope .../auth/drive
  2. Credentials -> Create credentials -> OAuth client ID -> Application type
     Desktop app -> Create -> Download JSON (leave it in Downloads)
Then run this again."""
NO_LIB = """error: google-auth-oauthlib is not installed. Install it with:
  py -m pip install --user google-auth google-auth-oauthlib
or just run SETUP-DRIVE-OAUTH.bat from the repo folder, which does it for you."""


def find_client_secret():
    """Return the path of the OAuth client JSON, or exit with instructions."""
    here = os.path.dirname(os.path.abspath(__file__))
    downloads = os.path.join(os.environ.get("USERPROFILE") or os.path.expanduser("~"),
                             "Downloads")
    for folder in (here, downloads):
        hits = sorted(glob.glob(os.path.join(folder, "client_secret*.json")))
        if hits:
            print("OAuth client file: %s" % hits[0])
            return hits[0]
    sys.exit(NO_JSON % (here, downloads))


def run_consent(client_file):
    """Do the browser consent flow. Returns {SECRET_NAME: value} in memory only."""
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        sys.exit(NO_LIB)
    flow = InstalledAppFlow.from_client_secrets_file(client_file, scopes=SCOPES)
    print("\nOpening your browser. Sign in as the OWNER of the AUTONOMY-SYSTEM Drive")
    print("folder and click Allow. (An 'unverified app' warning is expected: choose")
    print("Advanced -> Go to ... since you are the app's own test user.)\n")
    creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")
    if not creds.refresh_token:
        sys.exit("error: Google returned no refresh token. Re-run this script (it asks "
                 "for offline access with prompt=consent) and make sure the OAuth "
                 "client type is Desktop app.")
    print("consent complete - refresh token captured in memory (never printed)")
    return {"GOOGLE_OAUTH_CLIENT_ID": creds.client_id,
            "GOOGLE_OAUTH_CLIENT_SECRET": creds.client_secret,
            "GOOGLE_OAUTH_REFRESH_TOKEN": creds.refresh_token}


def pipe(cmd, value):
    """Run cmd with value on stdin. shell=False; value never enters argv."""
    try:
        proc = subprocess.run(cmd, input=value.encode("utf-8"), shell=False,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except OSError:
        return False
    return proc.returncode == 0


def store_with_gh(secrets):
    """Try `gh secret set` for all three. True only if every one succeeded."""
    for name in ORDER:
        if not pipe(["gh", "secret", "set", name, "--repo", REPO], secrets[name]):
            print("gh could not set %s (gh missing, not logged in, or no access)" % name)
            return False
        print("gh secret set %s -> OK" % name)
    return True


def store_with_clipboard(secrets):
    """Fallback: one value at a time on the clipboard, pasted into the GitHub UI."""
    print("\nFalling back to clipboard paste - 3 prompts. For each one: the value is")
    print("copied to your clipboard, the GitHub 'New secret' page opens, you type the")
    print("NAME shown, paste the value with Ctrl+V, click 'Add secret', then press")
    print("Enter here. Re-setting a secret that already exists is harmless.\n")
    for name in ORDER:
        if not pipe(CLIP_CMD, secrets[name]):
            sys.exit("error: could not reach the Windows clipboard via PowerShell. Add "
                     "the three secrets by hand at %s - you will need to re-run this "
                     "script to get fresh values." % NEW_SECRET_URL)
        print("  secret %s: value is on your clipboard" % name)
        webbrowser.open(NEW_SECRET_URL)
        input("  paste it as %s at %s, click 'Add secret', then press Enter: "
              % (name, NEW_SECRET_URL))


def main():
    secrets = run_consent(find_client_secret())
    if not store_with_gh(secrets):
        store_with_clipboard(secrets)
    print("\nDone - all three secrets are stored (names only were shown; no value was "
          "printed or saved).")
    print("NOW DELETE client_secret*.json from this folder and from your Downloads "
          "folder - it is a credential.")
    print("Then run the sync: https://github.com/%s/actions/workflows/"
          "sync-docs-to-drive.yml -> Run workflow" % REPO)
    return 0


if __name__ == "__main__":
    sys.exit(main())
