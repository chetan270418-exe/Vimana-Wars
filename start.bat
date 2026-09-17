@echo off
cd /d "%~dp0"
echo ========================================================
echo   VIMANA WARS // CELESTIAL COMBAT LAUNCHER
echo ========================================================
echo.
echo   [1] Vimana Wars C++ Engine (Native Desktop, 60 FPS)
echo   [2] Vimana Wars Python Edition (Original Arcade)
echo   [3] Exit
echo.
set choice=1
set /p choice="Select game edition to launch [1, 2, or 3, default=1]: "
if "%choice%"=="2" (
    call start_python_game.bat
) else if "%choice%"=="3" (
    exit /b 0
) else (
    call start_cpp_game.bat
)
