#requires -version 5.0
<#
.SYNOPSIS
    ProgressProgram을 실행합니다.
.DESCRIPTION
    1. progress_env 가상환경 존재 여부 확인 (conda 우선)
    2. 가상환경이 없으면 setup_env.ps1을 실행하여 자동 설정
    3. 가상환경의 Python으로 src/main.py 실행
.PARAMETER Quiet
    스크립트 실행 후 종료를 기다리지 않습니다.
#>
param(
    [switch]$Quiet
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

# --- Helper Functions ---
function Write-Log {
    param(
        [string]$Message,
        [string]$ForegroundColor = "White"
    )
    Write-Host "  $Message" -ForegroundColor $ForegroundColor
}

function Write-Section {
    param(
        [string]$Title
    )
    Write-Host "`n[$Title]" -ForegroundColor Cyan
}

function Exit-Script {
    param(
        [string]$Message = "스크립트가 완료되었습니다.",
        [string]$Color = "Green",
        [int]$ExitCode = 0
    )
    Write-Host "`n$Message" -ForegroundColor $Color
    if (-not $Quiet) {
        Read-Host -Prompt "계속하려면 Enter 키를 누르십시오."
    }
    exit $ExitCode
}
# ------------------------

# 스크립트가 있는 디렉토리의 상위 디렉토리(프로젝트 루트)로 이동
Write-Section "ProgressProgram 실행 시작"
try {
    $ProjectRoot = (Get-Item -Path $PSScriptRoot).Parent.FullName
    Set-Location -Path $ProjectRoot -ErrorAction Stop
    Write-Log "프로젝트 루트: $ProjectRoot"
} catch {
    Exit-Script -Message "[오류] 프로젝트 루트로 이동 실패: $($_.Exception.Message)" -Color Red -ExitCode 1
}

$VenvName = "progress_env"
$VenvDir = ".\$VenvName"
$PythonExe = "$VenvDir\Scripts\python.exe"

Write-Log "가상환경: $VenvName"

# 1. 가상환경 확인 및 활성화 (venv 우선)
Write-Section "1/2 가상환경 확인 및 프로그램 실행"

if (Test-Path -Path $PythonExe) {
    Write-Log "venv 환경 사용"
    Write-Log "가상환경의 Python으로 src\main.py 실행"
    try {
        & $PythonExe "src\main.py"
    } catch {
        Exit-Script -Message "[오류] 프로그램 실행 실패: $($_.Exception.Message)" -Color Red -ExitCode 1
    }
} else {
    $condaFound = $false
    try {
        (Get-Command conda -ErrorAction SilentlyContinue | Out-Null)
        $condaFound = $true
    } catch { }

    if ($condaFound) {
        Write-Log "Conda 환경 사용"
        $condaEnvExists = (conda env list | Select-String -Pattern "^$VenvName\s" -ErrorAction SilentlyContinue)
        if (-not $condaEnvExists) {
            Write-Log "conda 가상환경($VenvName)을 찾을 수 없습니다. setup_env.ps1을 실행합니다..." -ForegroundColor Yellow
            try {
                & "$PSScriptRoot\setup_env.ps1" -Quiet
            } catch {
                Exit-Script -Message "[오류] 환경 설정 실패: $($_.Exception.Message)" -Color Red -ExitCode 1
            }
        }
        Write-Log "가상환경의 Python으로 src\main.py 실행"
        try {
            & conda @('run', '-n', $VenvName, 'python', 'src\main.py')
        } catch {
            Exit-Script -Message "[오류] 프로그램 실행 실패: $($_.Exception.Message)" -Color Red -ExitCode 1
        }
    } else {
        Write-Log "venv 가상환경($VenvName)을 찾을 수 없습니다. setup_env.ps1을 실행합니다..." -ForegroundColor Yellow
        try {
            & "$PSScriptRoot\setup_env.ps1" -Quiet
        } catch {
            Exit-Script -Message "[오류] 환경 설정 실패: $($_.Exception.Message)" -Color Red -ExitCode 1
        }
        Write-Log "가상환경의 Python으로 src\main.py 실행"
        try {
            & $PythonExe "src\main.py"
        } catch {
            Exit-Script -Message "[오류] 프로그램 실행 실패: $($_.Exception.Message)" -Color Red -ExitCode 1
        }
    }
}

# 완료
Exit-Script -Message "[성공] ProgressProgram이 종료되었습니다." 