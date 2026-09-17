@echo off
cd /d "%~dp0"
if not exist "bin\VimanaWars.exe" (
    echo [INFO] Executable not found. Compiling first...
    call build.bat
)
echo [LAUNCHING] Starting Vimana Wars Desktop Game...
start "" "bin\VimanaWars.exe"
