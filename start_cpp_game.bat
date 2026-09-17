@echo off
cd /d "%~dp0"
if not exist "cpp_game\bin\VimanaWars.exe" (
    echo [INFO] Vimana Wars C++ executable not found. Building now...
    call cpp_game\build.bat
)
echo [LAUNCHING] Starting Vimana Wars C++ Desktop Game...
cd /d "%~dp0cpp_game"
start "" "bin\VimanaWars.exe"
