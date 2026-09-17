@echo off
cd /d "%~dp0"

echo ========================================================
echo   VIMANA WARS // NATIVE C++ RUNTIME & SANGHA CLOUD
echo ========================================================

:: Check if PostgreSQL backend service is running on port 5000
netstat -ano | findstr :5000 >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Starting Vimana Wars PostgreSQL Backend Server...
    start /min "Vimana Wars Cloud Backend" python python_game/backend/app.py
    timeout /t 2 /nobreak >nul
)

if not exist "cpp_game\bin\VimanaWars.exe" (
    echo [INFO] Vimana Wars C++ executable not found. Building now...
    call cpp_game\build.bat
)
echo [LAUNCHING] Starting Vimana Wars C++ Desktop Game...
cd /d "%~dp0cpp_game"
start "" "bin\VimanaWars.exe"
