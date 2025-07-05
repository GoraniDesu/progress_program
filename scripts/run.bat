@echo off
@chcp 65001 > nul
@setlocal EnableExtensions EnableDelayedExpansion

:: Run script for ProgressProgram
set "QUIET="
if /I "%~1"=="/quiet" set "QUIET=1"

echo [ProgressProgram] Starting...
pushd "%~dp0.." || (
    echo [ERROR] Failed to move to project root! Current dir: %CD%
    goto :finalize_error
)

set "VENV_NAME=progress_env"
set "VENV_DIR=.\%VENV_NAME%"
set "PY_EXE=%VENV_DIR%\Scripts\python.exe"

echo [ProgressProgram] Checking virtual environment: %VENV_NAME%

if not exist "%PY_EXE%" (
    echo [ProgressProgram] Virtual environment not found, running setup_env.bat...
    call "%~dp0setup_env.bat" /quiet
    if %errorlevel% neq 0 (
        echo [ERROR] setup_env.bat failed!
        goto :finalize_error
    )
)

echo [ProgressProgram] Running main.py...
"%PY_EXE%" src\main.py
if %errorlevel% neq 0 (
    echo [ERROR] Program execution failed
    goto :finalize_error
)

echo.
echo [ProgressProgram] Program terminated successfully
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