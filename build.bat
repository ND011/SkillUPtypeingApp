@echo off
echo ========================================
echo SPEED Executable Builder
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or later
    pause
    exit /b 1
)

echo Checking and installing dependencies...
pip install PyQt6 pyinstaller

echo.
echo Starting build process...
python build_speed.py

echo.
echo ========================================
echo Build process completed!
echo Check the SPEED_Distribution folder for your executable
echo ========================================
pause