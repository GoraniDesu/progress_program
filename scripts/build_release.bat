@echo off
:: ProgressProgram 빌드/패키징 스크립트 (고급 전문가용)
:: 사용법: build_release.bat [version]
:: 예) build_release.bat 1.0.0

setlocal enableextensions

:: -------------------------------------------------------------
:: 1. 버전 파라미터 처리 / 기본값
:: -------------------------------------------------------------
if "%1"=="" (
    set VERSION=dev
) else (
    set VERSION=%1
)

set NAME=ProgressProgram_%VERSION%

:: -------------------------------------------------------------
:: 0. 가상환경 활성화/생성
:: -------------------------------------------------------------
where conda >nul 2>nul
if %errorlevel%==0 (
    echo Activating conda environment progress_env ...
    call conda env list | findstr "progress_env" >nul 2>nul
    if %errorlevel% neq 0 (
        echo progress_env 가상환경이 없으므로 setup_env.bat 를 실행합니다...
        call "%~dp0setup_env.bat" /quiet
    )
    set "PYTHON_CMD=conda run -n progress_env python"
) else (
    echo Using venv environment ...
    if not exist "%~dp0..\progress_env\Scripts\python.exe" (
        echo venv 가상환경이 없으므로 setup_env.bat 를 실행합니다...
        call "%~dp0setup_env.bat" /quiet
    )
    set "PYTHON_CMD=%~dp0..\progress_env\Scripts\python.exe"
)

:: PyInstaller(존재 여부) 확인
%PYTHON_CMD% -m pip show pyinstaller >nul 2>nul
if %errorlevel% neq 0 (
    echo Installing PyInstaller...
    %PYTHON_CMD% -m pip install pyinstaller
)

:: -------------------------------------------------------------
:: 2. 환경 정리
:: -------------------------------------------------------------
echo Cleaning previous build folders...
rd /s /q build 2>nul
rd /s /q dist 2>nul

:: -------------------------------------------------------------
:: 3. PyInstaller onedir 빌드 (권장 배포)
:: -------------------------------------------------------------
echo Building ONEDIR package %NAME% ...
%PYTHON_CMD% -m PyInstaller --clean --noconfirm --onedir --windowed ^
  --name %NAME% ^
  --paths src ^
  --add-data "config;config" ^
  --add-data "resources;resources" ^
  --add-data "data\progress.db;data" ^
  src\main.py
if errorlevel 1 (
    echo PyInstaller onedir build failed.
    goto :error
)

:: -------------------------------------------------------------
:: 4. PyInstaller onefile 빌드 (옵션) - 주석 해제 시 활성화
:: -------------------------------------------------------------
:: echo Building ONEFILE executable %NAME%.exe ...
:: pyinstaller --clean --noconfirm --onefile --windowed ^
::   --name %NAME% ^
::   --paths src ^
::   --add-data "config;config" ^
::   --add-data "resources;resources" ^
::   --add-data "data\progress.db;data" ^
::   src\main.py

:: -------------------------------------------------------------
:: 5. 완료 메시지
:: -------------------------------------------------------------
echo Build complete! Output: dist\%NAME%\
pause
exit /b 0

:error
pause
exit /b 1 