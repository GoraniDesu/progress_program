@echo off
chcp 65001 > nul
setlocal EnableExtensions EnableDelayedExpansion

:: ------------------------------------------------------------
:: ProgressProgram 릴리스 빌드 스크립트 (Rewritten 2025-07)
:: ------------------------------------------------------------

:: 0) 파라미터 처리
set "VERSION=%~1"
if "%VERSION%"=="" set "VERSION=dev"
set "QUIET="
if /I "%~2"=="/quiet" set "QUIET=1"

:: 1) 프로젝트 루트로 이동
pushd "%~dp0.." || (
    echo [오류] 프로젝트 루트로 이동 실패!
    goto :finalize_error
)

:: 2) 변수 정의
set "APP_NAME=ProgressProgram"
set "BUILD_NAME=%APP_NAME%_v%VERSION%"
set "VENV_NAME=progress_env"
set "VENV_DIR=.\%VENV_NAME%"
set "PY_EXE=%VENV_DIR%\Scripts\python.exe"
set "ICON_FILE=.\resources\icon.ico"

call :section "ProgressProgram 릴리스 빌드 시작"
call :log "빌드 이름: %BUILD_NAME%"

:: === [1/3] PyInstaller 준비 ===
call :section "1/3 PyInstaller 확인"
where conda > nul 2> nul
if %errorlevel%==0 (
    set "PY_CMD=conda run -n %VENV_NAME% python"
    conda env list | findstr /b /c:"%VENV_NAME%" > nul 2> nul || (
        call :error "conda 가상환경을 찾을 수 없습니다. 먼저 setup_env.bat 실행 필요"
        goto :finalize_error
    )
) else (
    set "PY_CMD=%PY_EXE%"
    if not exist "%PY_EXE%" (
        call :error "venv 가상환경을 찾을 수 없습니다. 먼저 setup_env.bat 실행 필요"
        goto :finalize_error
    )
)

%PY_CMD% -m pip show pyinstaller > nul 2> nul || (
    call :log "PyInstaller 미설치. 설치 진행"
    %PY_CMD% -m pip install pyinstaller || (
        call :error "PyInstaller 설치 실패"
        goto :finalize_error
    )
)

:: === [2/3] 이전 빌드 폴더 정리 ===
call :section "2/3 이전 빌드 정리"
if exist build rd /s /q build
if exist dist rd /s /q dist
call :log "정리 완료"

:: === [3/3] PyInstaller 빌드 ===
call :section "3/3 PyInstaller 실행"
set "PYI_OPTS=--noconfirm --clean src/main.py --onedir --name %BUILD_NAME% --windowed"
set "DATA_OPTS=--add-data \"config;config\" --add-data \"resources;resources\""
set "ICON_OPT="
if exist "%ICON_FILE%" set "ICON_OPT=--icon \"%ICON_FILE%\""

%PY_CMD% -m PyInstaller %PYI_OPTS% %DATA_OPTS% %ICON_OPT% || (
    call :error "PyInstaller 빌드 실패"
    goto :finalize_error
)

call :section "완료"
call :log "출력 폴더: dist\%BUILD_NAME%"
set "EXIT_CODE=0"
 goto :finalize

:: ------------------------------------------------------------
:: Helper 함수
:: ------------------------------------------------------------
:log
    echo   %~1
    goto :eof

:section
    echo.
    echo [%~1]
    goto :eof

:error
    echo.
    echo [오류] %~1
    set "EXIT_CODE=1"
    goto :eof

:finalize_error
    set "EXIT_CODE=1"

:finalize
    popd 2> nul
    if not defined QUIET (
        timeout /t -1 > nul
    )
    endlocal
    exit /b %EXIT_CODE% 