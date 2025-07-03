@echo off
echo Starting Progress Program v0.3.2...
echo.

REM Change to project root directory
cd /d "%~dp0.."

REM Check Python environment
echo Checking Python environment...
python --version
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)
echo.

REM Run the program
echo Starting the application...
python src/main.py

echo.
echo Program terminated. Press any key to exit...
pause > nul 