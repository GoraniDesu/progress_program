@echo off
echo Progress Program을 시작합니다...
echo.

REM conda 환경 활성화 및 프로그램 실행
call conda run -n progress_env python src/main.py

echo.
echo 프로그램이 종료되었습니다. 아무 키나 누르세요...
pause > nul 