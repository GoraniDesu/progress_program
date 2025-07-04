#requires -version 5.0
<#!
.SYNOPSIS
    ProgressProgram 빌드/실행 통합 스크립트 (PowerShell)
.DESCRIPTION
    PyInstaller 를 이용하여 onedir 패키지를 빌드하고(버전 인수 선택),
    빌드 성공 시 exe 를 즉시 실행합니다.

.PARAMETER Version
    빌드할 버전 문자열 (예: 1.0.0). 생략 시 'dev' 로 빌드.
#>
param(
    [string]$Version = 'dev'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# ---------------------------------------------
# 1. 변수 설정
# ---------------------------------------------
$NAME = "ProgressProgram_$Version"

Write-Host "[Info] Cleaning previous build folders..." -ForegroundColor Cyan
Remove-Item -Recurse -Force build, dist -ErrorAction SilentlyContinue

# ---------------------------------------------
# 2. PyInstaller onedir 빌드
# ---------------------------------------------
Write-Host "[Info] Building ONEDIR package $NAME ..." -ForegroundColor Cyan
$pyCmd = @(
    'pyinstaller','--clean','--noconfirm','--onedir','--windowed',
    '--name', $NAME,
    '--paths','src',
    '--add-data','config;config',
    '--add-data','resources;resources',
    '--add-data','data\progress.db;data',
    'src\main.py'
)

& $pyCmd 2>&1 | Write-Host

if (!(Test-Path "dist/$NAME/progress_program.exe")) {
    Write-Host "[Error] Build failed." -ForegroundColor Red
    exit 1
}

Write-Host "[Success] Build complete! Output: dist/$NAME" -ForegroundColor Green

# ---------------------------------------------
# 3. EXE 실행 여부 질의
# ---------------------------------------------
$run = Read-Host '빌드한 프로그램을 바로 실행할까요? (Y/N)'
if ($run -match '^[Yy]') {
    & "dist/$NAME/progress_program.exe"
} 