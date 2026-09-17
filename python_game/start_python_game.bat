@echo off
cd /d "%~dp0"
echo ========================================================
echo   VIMANA WARS // PYTHON ARCADE EDITION
echo ========================================================
python main.py
if %ERRORLEVEL% neq 0 (
    echo.
    echo If Arcade is not installed, run: pip install -r requirements.txt
    pause
)
