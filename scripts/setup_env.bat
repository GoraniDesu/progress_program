@echo off
@chcp 65001 > nul
@setlocal EnableExtensions EnableDelayedExpansion

:: Setup script for ProgressProgram
set "QUIET="
if /I "%~1"=="/quiet" set "QUIET=1"

pushd "%~dp0.." || (
    echo [ERROR] Failed to move to project root!
    goto :finalize_error
)

set "VENV_NAME=progress_env"
set "PY_MIN_MAJOR=3"
set "PY_MIN_MINOR=9"
set "VENV_DIR=.\%VENV_NAME%"

echo.
echo [Setup Start]
echo Root: %CD%

echo.
echo [1/4] Python Version Check
where python > nul 2> nul || (
    echo [ERROR] Python not found
    goto :finalize_error
)
for /f "tokens=2" %%v in ('python --version 2^>^&1') do set "PYTHON_VERSION=%%v"
echo Python Version: !PYTHON_VERSION!
for /f "tokens=1,2 delims=." %%a in ("!PYTHON_VERSION!") do (
    if %%a LSS %PY_MIN_MAJOR% (
        echo [ERROR] Python %PY_MIN_MAJOR%.%PY_MIN_MINOR%+ required
        goto :finalize_error
    ) else if %%a EQU %PY_MIN_MAJOR% if %%b LSS %PY_MIN_MINOR% (
        echo [ERROR] Python %PY_MIN_MAJOR%.%PY_MIN_MINOR%+ required
        goto :finalize_error
    )
)
echo Python version OK

echo.
echo [2/4] Virtual Environment Setup
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo Creating venv...
    python -m venv "%VENV_DIR%" || (
        echo [ERROR] Failed to create venv
        goto :finalize_error
    )
)
set "PY_CMD=%VENV_DIR%\Scripts\python.exe"

echo.
echo [3/4] Package Installation
if not exist "requirements.txt" (
    echo [ERROR] requirements.txt not found
    goto :finalize_error
)
%PY_CMD% -m pip install --upgrade pip || (
    echo [ERROR] Failed to upgrade pip
    goto :finalize_error
)
%PY_CMD% -m pip install -r "requirements.txt" || (
    echo [ERROR] Failed to install packages
    goto :finalize_error
)
echo Packages installed successfully

echo.
echo [4/4] Setup Complete
echo Run 'run.bat' to start the program
set "EXIT_CODE=0"
goto :finalize

:finalize_error
set "EXIT_CODE=1"
goto :finalize

:finalize
popd 2> nul
if not defined QUIET (
    pause
)
endlocal
exit /b %EXIT_CODE% 