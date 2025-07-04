# ProgressProgram 배포 패키지 안내

이 문서는 **`dist/ProgressProgram_<버전>/`** (onedir) 또는 **`dist/`** (onefile) 내에 포함되어 사용자에게 전달되는 배포 파일들의 목적과 구조를 설명합니다.

---

## 1. 폴더/파일 구조 (onedir 기준)

```
ProgressProgram_1.0.0/
├─ progress_program.exe          # 런처 실행 파일 (GUI)
├─ config/                       # 사용자/테마 설정
│    └─ theme_settings.json
├─ resources/                    # 폰트·아이콘 등 정적 리소스
│    ├─ fonts/영양군_음식디미방.ttf
│    └─ icons/... (아이콘 추가 시)
├─ data/                         # 사용자 데이터(SQLite DB)
│    └─ progress.db              # 첫 실행 시 자동 생성/확장
├─ PySide6/                      # Qt DLL & plugins (자동 포함)
│    └─ plugins/platforms/qwindows.dll
└─ 기타 DLL                      # 파이썬 런타임·OpenSSL 등 의존 라이브러리
```

> **onefile** 패키지를 받으신 경우 `progress_program.exe` 한 파일만 제공됩니다. 실행 시 위 구조가 임시 폴더로 자동 추출되므로 사용자는 신경 쓸 필요가 없습니다.

---

## 2. 실행 방법

1. 폴더(또는 EXE 파일)를 원하는 위치에 복사합니다.
2. `progress_program.exe` 더블클릭 → 프로그램 실행.
3. 데이터베이스(`data/progress.db`)는 동일 폴더 안에서 관리되므로 다른 PC로 옮길 때 함께 복사하면 됩니다.

> Windows Defender SmartScreen 경고가 발생할 수 있습니다. "추가 정보 → 계속 실행"을 선택하면 됩니다.

---

## 3. 업데이트/마이그레이션

새 버전 패키지를 받은 경우:
1. 기존 폴더를 백업하거나 덮어쓰기 전에 `data/progress.db` 를 안전한 위치에 복사합니다.
2. 새 폴더/EXE 로 교체한 뒤 `data` 폴더에 DB 파일을 다시 넣습니다.
3. 프로그램을 실행하여 데이터가 정상 표시되는지 확인합니다.

DB 스키마가 변경되는 경우 애플리케이션이 자동으로 마이그레이션합니다.

---

## 4. 문제 해결 FAQ

| 증상 | 해결책 |
|-----|---------|
| 실행 시 "failed to start embedded python interpreter" | 백신 또는 권한 문제일 수 있습니다. 1) 실시간 보호 잠시 해제 2) 관리자 권한으로 실행 |
| `utils` 모듈을 찾을 수 없다는 오류 | 배포 패키지를 수정했거나 손상된 경우입니다. 최신 압축본을 다시 받아 풀어 주세요. |
| 폰트가 기본 글꼴로 보임 | `resources/fonts/영양군_음식디미방.ttf` 가 없는지 확인 후 다시 복사하십시오. |

---

## 5. 라이선스

본 소프트웨어는 MIT 라이선스로 배포되며, 폰트/아이콘 등 제3자 리소스는 각 라이선스를 따릅니다.

> © 2025 Progress Team 