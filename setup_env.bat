@echo off
echo Progress Program 환경을 설정합니다...
echo.

REM conda 환경 생성
echo 1. conda 가상환경 생성 중...
call conda create -n progress_env python=3.9 -y

REM PySide6 설치
echo.
echo 2. PySide6 설치 중...
call conda run -n progress_env pip install PySide6

echo.
echo 환경 설정이 완료되었습니다!
echo run.bat 파일을 실행하여 프로그램을 시작하세요.
echo.
pause 