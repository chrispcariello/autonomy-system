@echo off
REM SETUP-DRIVE-OAUTH.bat - one-time Owner setup for the Drive sync (OAuth owner auth).
REM Installs two Google libraries, then runs tools\setup_drive_oauth.py, which opens the
REM browser consent flow and stores the three GOOGLE_OAUTH_* GitHub secrets.
REM No credential value is printed or written by any of this. See README section
REM "Drive sync setup - OAuth (current)".
cd /d %~dp0

if not exist "tools\setup_drive_oauth.py" (
  echo Could not find tools\setup_drive_oauth.py next to this file.
  echo Run SETUP-DRIVE-OAUTH.bat from inside the autonomy-system repo folder.
  pause
  exit /b 1
)

REM Pick whichever launcher this machine has: the py launcher, else python.
set "PYEXE="
py -c "import sys" >nul 2>nul && set "PYEXE=py"
if not defined PYEXE (python -c "import sys" >nul 2>nul && set "PYEXE=python")
if not defined PYEXE (
  echo Python 3 was not found. Install it from https://www.python.org/downloads/
  echo and tick "Add python.exe to PATH", then run this file again.
  pause
  exit /b 1
)

echo Installing google-auth and google-auth-oauthlib (quiet, user-level)...
%PYEXE% -m pip install --quiet --user google-auth google-auth-oauthlib || py -m pip install --quiet --user google-auth google-auth-oauthlib || python -m pip install --quiet --user google-auth google-auth-oauthlib

echo.
echo Starting the one-time OAuth consent flow - a browser window will open, click Allow.
echo.
%PYEXE% tools\setup_drive_oauth.py || (py tools\setup_drive_oauth.py || python tools\setup_drive_oauth.py)
pause
