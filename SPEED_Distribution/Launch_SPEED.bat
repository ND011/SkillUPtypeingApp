@echo off
echo Starting SPEED - Keyboard Speed Training...
echo.

REM Check if executable exists
if not exist "SPEED.exe" (
    echo Error: SPEED.exe not found!
    echo Make sure this file is in the same folder as SPEED.exe
    pause
    exit /b 1
)

REM Launch SPEED
echo Launching application...
start "" "SPEED.exe"

REM Optional: Close this window after launch
timeout /t 2 /nobreak >nul
echo SPEED started successfully!
echo You can close this window now.
