#requires -version 5.0
<#
.SYNOPSIS
    ProgressProgram의 릴리스 빌드를 생성합니다.
.DESCRIPTION
    1. progress_env 가상환경 및 PyInstaller 확인 (conda 우선)
    2. 이전 빌드 폴더(build, dist) 정리
    3. PyInstaller를 사용하여 onedir (기본값) 또는 onefile 배포판 생성
.PARAMETER Version
    빌드할 버전 문자열 (예: 1.0.0). 생략 시 'dev'로 설정됩니다.
#>
param(
    [string]$Version = 'dev'
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

# 스크립트가 있는 디렉토리의 상위 디렉토리(프로젝트 루트)로 이동
$ProjectRoot = (Get-Item -Path $PSScriptRoot).Parent.FullName
Set-Location -Path $ProjectRoot

$AppName = "ProgressProgram"
$BuildName = "${AppName}_v${Version}"
$VenvName = "progress_env"
$VenvDir = ".\$VenvName"
$IconFile = ".\resources\icon.ico"

Write-Host "[ProgressProgram] 릴리스 빌드를 시작합니다." -ForegroundColor Cyan
Write-Host "  - 빌드 버전: $Version"
Write-Host "  - 빌드 이름: $BuildName"
Write-Host "  - 가상환경: $VenvName"

# 1. 가상환경 확인 및 PyInstaller 설치
Write-Host "`n[1/3] 가상환경 및 PyInstaller 확인..."
$condaFound = $false
try {
    (Get-Command conda -ErrorAction SilentlyContinue | Out-Null)
    $condaFound = $true
} catch { }

if ($condaFound) {
    Write-Host "  - conda 환경을 사용합니다."
    $condaEnvExists = (conda env list | Select-String -Pattern "^$VenvName\s" -ErrorAction SilentlyContinue)
    if (-not $condaEnvExists) {
        throw "conda 가상환경($VenvName)을 찾을 수 없습니다. 먼저 'setup_env.ps1'을 실행하여 환경을 설정해주세요."
    }
    $PythonCmd = "conda run -n $VenvName python"
}
else {
    Write-Host "  - venv 환경을 사용합니다."
    if (-not (Test-Path -Path "$VenvDir\Scripts\python.exe")) {
        throw "venv 가상환경($VenvName)을 찾을 수 없습니다. 먼저 'setup_env.ps1'을 실행하여 환경을 설정해주세요."
    }
    $PythonCmd = "$VenvDir\Scripts\python.exe"
}

$pyinstallerCheck = & $PythonCmd -m pip show pyinstaller 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "  - PyInstaller가 설치되어 있지 않아 새로 설치합니다..."
    & $PythonCmd -m pip install pyinstaller
}
Write-Host "  - PyInstaller가 준비되었습니다."

# 2. 이전 빌드 폴더 정리
Write-Host "`n[2/3] 이전 빌드 폴더 정리 (build, dist)..."
Remove-Item -Path "build", "dist" -Recurse -Force -ErrorAction SilentlyContinue
Write-Host "  - 정리 완료."

# 3. PyInstaller 빌드 실행
Write-Host "`n[3/3] PyInstaller 빌드를 실행합니다..."
$CommonOpts = @(
    "--name", $BuildName,
    "--windowed"
)
$DataOpts = @(
    "--add-data", "config;config",
    "--add-data", "resources;resources"
)
if (Test-Path -Path $IconFile) {
    $IconOpt = @("--icon", $IconFile)
}
else {
    $IconOpt = @()
    Write-Host "  [경고] 아이콘 파일($IconFile)을 찾을 수 없어 기본 아이콘으로 빌드합니다." -ForegroundColor Yellow
}

# Onedir 빌드 (기본값)
Write-Host "  - 빌드 모드: onedir (폴더 형태)"
& $PythonCmd -m PyInstaller --noconfirm --clean "src/main.py" --onedir $CommonOpts $DataOpts $IconOpt

# Onefile 빌드가 필요할 경우 아래 주석 해제
# Write-Host "  - 빌드 모드: onefile (단일 실행 파일)"
# & $PythonCmd -m PyInstaller --noconfirm --clean "src/main.py" --onefile $CommonOpts $DataOpts $IconOpt

Write-Host "`n[성공] 릴리스 빌드가 완료되었습니다!" -ForegroundColor Green
Write-Host "  - 출력 폴더: dist\$BuildName"

Read-Host -Prompt "`nPress Enter to exit" 