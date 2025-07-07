# Progress Program v1.1.0

**복잡한 기능에 지친 당신을 위한, 가장 간단하고 직관적인 진척도 관리 도구**

> 🤖 **AI와 함께 개발되었습니다**
> 본 프로젝트는 **Cursor AI** 환경에서 다양한 LLM 모델과의 페어프로그래밍을 통해 기획·개발·문서화를 진행했습니다.
> **주의**: AI 모델의 특성상, 코드, 문서 등에 부정확하거나 모호한 표현, 또는 사실과 다른 정보(할루시네이션)가 포함될 수 있습니다. 중요 정보는 교차 검증을 권장하며, 모든 정보가 100% 정확하다고 보장할 수 없으므로 사용에 주의를 기울여 주시기 바랍니다.

---

## ✨ 주요 기능 (Key Features)

- **🌊 살아 움직이는 진척도**: `Fluid ProgressBar`가 물결 애니메이션으로 당신의 진행 상황을 시각적으로 보여줍니다.
- **🎉 목표 달성 축하 효과**: 100%를 달성하면 나타나는 `스탬프(Stamp)`와 `파티클 효과`가 성취의 즐거움을 더합니다.
- **🎨 사용자 맞춤 테마**: 눈이 편안한 `라이트/다크 모드`를 지원합니다.
- **💾 안전한 데이터 백업**: `백업/복원 관리자`를 통해 언제든 데이터를 안전하게 보관하고 원하는 시점으로 되돌릴 수 있습니다.
- **⚡️ 빠른 작업 효율**: `더블클릭 편집`, `키보드 단축키`(`Ctrl+N`, `Ctrl+S` 등)로 반복 작업을 최소화합니다.
- **📝 스마트 노트 기능**: 프로젝트별 노트를 자유롭게 작성하고, 저장 버튼(💾)으로 명시적 저장이 가능합니다. 프로젝트 전환 시 자동 저장 확인으로 작성 내용이 안전하게 보호됩니다.

## 📦 다운로드 및 빠른 시작

### 1. 다운로드
- **최신 버전 (v1.1.0)**: [Google Drive에서 다운로드](https://drive.google.com/drive/folders/1CtZWaGRnM2i6Qb8AaCVfb74cQuh1625K?usp=sharing)
- **과거 버전 및 상세 변경 이력**: [전체 변경 로그(CHANGELOG)](docs/changelog/CHANGELOG.md) 참고

### 2. 실행 방법
- **Windows 사용자**: 
  1. 구글 드라이브 링크로 다운로드한 zip 파일의 `progress_program.exe`를 더블클릭하여 실행
  2. 또는 `scripts` 폴더의 `run.bat` 실행

- **소스 코드로 직접 실행**:
  1. `scripts` 폴더의 `setup_env.bat` 실행 (최초 1회)
  2. `scripts` 폴더의 `run.bat` 실행

> **참고**: 실행 스크립트는 자동으로 가상환경을 감지하고 필요한 의존성을 설치합니다.

## 📖 문서
프로그램 사용법, 개발 가이드 등 더 자세한 정보는 아래 문서들을 참고하세요.

- **[사용자 가이드](docs/guides/reference/user_guide.md)**: 프로그램의 모든 기능에 대한 상세한 사용법 안내
- **[전체 변경 로그](docs/changelog/CHANGELOG.md)**: v0.1.0부터 현재까지의 모든 버전별 상세 변경 기록
- **[개발 가이드](docs/guides/reference/DEVELOPMENT_GUIDE.md)**: 개발 환경 설정 및 프로젝트 구조, 기여 방법 안내

## 👨‍💻 개발자 안내

### 기술 스택
- **언어**: Python 3.9+
- **GUI**: PySide6 (LGPL)
- **데이터베이스**: SQLite
- **배포**: PyInstaller

### 📁 프로젝트 구조
```
progress_program/
├── README.md                    # (이 파일) 프로젝트 소개
├── docs/                        # 모든 문서
│   ├── changelog/              # 버전별 상세 변경이력
│   └── guides/                 # 각종 가이드 (사용자, 개발)
├── src/                         # 애플리케이션 소스 코드
│   ├── main.py                 # 애플리케이션 진입점
│   ├── database/               # 데이터베이스 관리
│   ├── ui/                     # UI 위젯 및 로직
│   └── utils/                  # 핵심 유틸리티 (테마, 애니메이션, 백업 등)
├── scripts/                     # 빌드 및 실행 스크립트
│   ├── build_release.bat       # CMD용 빌드 스크립트
│   └── build_release.ps1       # PowerShell용 빌드 스크립트
├── config/                      # 설정 파일
│   └── theme_settings.json     # 테마 설정 저장
├── resources/                   # 폰트, 아이콘 등 리소스
├── data/                        # (프로그램 실행 시 생성) 데이터베이스 파일
├── dist/                        # (빌드 시 생성) 배포 패키지
└── requirements.txt             # Python 의존성 목록
```

### 원-클릭 빌드 스크립트
Windows 환경에서는 아래 스크립트로 직접 빌드할 수 있습니다.
```powershell
# PowerShell 스크립트 실행 (버전 번호 지정)
scripts\build_release.ps1 1.1.0

# 또는 CMD에서 실행
scripts\build_release.bat 1.1.0
```

#### 빌드 스크립트 개선사항 (v1.1.0)
- 가상환경(venv/conda) 자동 감지
- 필요한 의존성 패키지 자동 설치
- Python 경로 자동 감지 및 설정
- 상세한 오류 메시지 제공
- 실행 파일 호환성 강화

### 실행 파일 호환성 (v1.1.0)
- PyInstaller 패키지 경로 자동 감지
- 모듈 import 오류 해결
- 리소스 파일 접근 개선
- 다양한 Python 환경 지원

### 폰트 라이선스
이 프로그램은 '영양군 음식디미방체' 폰트를 사용하며, 공공누리 제1유형(출처표시) 라이선스를 준수합니다.

## 💡 핵심 원칙

**간단하게, 꾸준히, 시각적으로! 📊✨**

복잡한 기능보다는 직관적인 사용성에, 사용자의 부담을 줄이는 자동화에, 그리고 시각적 피드백을 통한 성취감에 집중합니다.

## 📜 라이선스

이 프로젝트는 Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0) 하에 배포됩니다.

### 사용 허가 범위
✅ 허용되는 사용:
- 개인적인 사용
- 교육 목적 사용
- 비영리 단체 사용
- 연구 및 개발 목적 사용 (비상업적)
- 소스코드 수정 및 재배포 (비상업적 목적)

❌ 금지되는 사용:
- 소프트웨어 판매
- 광고를 통한 수익 창출
- 기업/영리 목적 사용
- 상업적 제품/서비스에 포함
- 영리 목적의 배포

### 필수 표시 사항
사용 시 반드시 다음을 포함해야 합니다:
1. 원작자 표시: "pollux (GoraniDesu)" (GitHub: [@GoraniDesu](https://github.com/GoraniDesu))
2. 원본 프로젝트 링크
3. 라이선스 문구
4. 수정 시 수정 내용 명시

자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

### 제3자 라이선스
이 프로젝트는 다음과 같은 제3자 소프트웨어와 리소스를 사용합니다:
- PySide6 (LGPL v3)
- Python (PSF License)
- SQLite (Public Domain)
- 영양군 음식디미방체 (공공누리 제1유형)

자세한 라이선스 정보는 [THIRD_PARTY_LICENSES](THIRD_PARTY_LICENSES) 파일을 참조하세요.

---

**Progress Program v1.1.0으로 여러분의 프로젝트를 더욱 효율적이고 즐겁게 관리해보세요! 🚀**
