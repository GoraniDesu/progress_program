@echo off
echo [ProgressProgram] 환경을 설정합니다...
echo.

REM ------------------------------------------------------
REM 1. conda 존재 여부 확인
REM    - conda가 없으면 venv를 사용
REM ------------------------------------------------------
where conda >nul 2>nul
if %errorlevel%==0 (
    goto :CREATE_CONDA
) else (
    goto :CREATE_VENV
)

:CREATE_CONDA
echo [1/3] conda 가상환경(progress_env) 생성 / 업데이트...
call conda env list | findstr "progress_env" >nul 2>nul
if %errorlevel% neq 0 (
    call conda create -n progress_env python=3.9 -y
)
echo [2/3] 패키지 설치(requirements.txt)...
call conda run -n progress_env pip install -r requirements.txt
goto :DONE

:CREATE_VENV
echo [1/3] venv 가상환경(progress_env) 생성 / 업데이트...
if not exist progress_env (
    python -m venv progress_env
)
echo [2/3] 패키지 설치(requirements.txt)...
call progress_env\Scripts\pip.exe install --upgrade pip
call progress_env\Scripts\pip.exe install -r requirements.txt
goto :DONE

:DONE
echo.
echo [3/3] 환경 설정이 완료되었습니다!
echo run.bat 파일을 실행하여 프로그램을 시작하세요.
echo.
if not "%1"=="/quiet" pause
exit /b 