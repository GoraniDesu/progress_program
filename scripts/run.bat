@echo off
echo Starting Progress Program...
echo.

REM Change to project root directory
cd /d "%~dp0.."

REM ------------------------------------------------------
REM 1. 가상환경 존재 여부 확인 – 없으면 자동 생성
REM ------------------------------------------------------
where conda >nul 2>nul
if %errorlevel%==0 (
    REM conda 사용
    conda env list | findstr "progress_env" >nul 2>nul
    if %errorlevel% neq 0 (
        echo conda 가상환경이 없으므로 setup_env.bat 를 실행합니다...
        call "%~dp0setup_env.bat" /quiet
    )
    echo Running with conda environment...
    conda run -n progress_env python src/main.py
) else (
    REM venv 사용
    if not exist progress_env\Scripts\python.exe (
        echo venv 가상환경이 없으므로 setup_env.bat 를 실행합니다...
        call "%~dp0setup_env.bat" /quiet
    )
    echo Running with venv environment...
    progress_env\Scripts\python.exe src/main.py
)

echo.
echo Program terminated. Press any key to exit...
pause > nul 