# Progress Program 폴더 구조 개편 완료 보고서

**개편 일시:** 2025년 7월 3일  
**버전:** v0.3.1 구조 개편

## 📋 개편 결과

### ✅ **새로운 폴더 구조**

```
progress_program/
├── 📁 src/                          # 소스 코드
├── 📁 data/                         # 런타임 데이터 (progress.db)
├── 📁 scripts/                      # 실행 스크립트들
│   ├── run.bat
│   └── setup_env.bat
├── 📁 docs/                         # 모든 문서 통합
│   ├── 📁 planning/                 # 계획 문서들
│   │   ├── 📁 v0.3.1/              # 현재 버전 계획
│   │   │   ├── v0.3.1_상세수정계획.md
│   │   │   └── v0.3.1_수정점.md
│   │   └── 📁 archive/              # 이전 버전 계획들 (향후 사용)
│   ├── 📁 changelog/                # 변경 로그
│   │   ├── README.md
│   │   ├── CHANGELOG.md
│   │   └── 📁 archive/              # 이전 버전 릴리즈 노트들
│   │       ├── v0.1.0_release_notes.md
│   │       ├── v0.2.0_release_notes.md
│   │       ├── v0.3.0_release_notes.md
│   │       └── v0.3.0_development_plan.md
│   ├── 📁 expert_opinion/           # 전문가 의견
│   │   ├── README.md
│   │   └── 📁 archive/              # 버전별 피드백들
│   │       ├── 📁 v0.1/
│   │       ├── 📁 v0.2/
│   │       └── 📁 v0.3/
│   ├── 📁 guides/                   # 가이드 통합
│   │   ├── 📁 project_guide/        # 프로젝트 가이드
│   │   └── 📁 reference/            # 참조 문서
│   └── README_실행방법.md            # 실행 방법 안내
├── 📁 config/                       # 설정 파일들
│   └── theme_settings.json
├── 📁 dist/                         # 빌드 결과물
├── 📁 .git/                         # Git 관리
├── 📄 README.md                     # 메인 문서
├── 📄 CHANGELOG.md                  # 주요 변경사항
├── 📄 requirements.txt              # 패키지 목록
└── 📄 .gitignore                    # Git 설정
```

## 🔄 **주요 변경사항**

### 1. **문서화 체계 통합**
- 모든 문서가 `docs/` 하위로 이동
- 버전별 아카이브 구조 도입 (일관성 확보)
- 계획, 변경로그, 피드백, 가이드 등 목적별 분류

### 2. **Archive 체계 도입**
- `docs/planning/archive/` - 이전 버전 계획들
- `docs/changelog/archive/` - 이전 버전 릴리즈 노트들  
- `docs/expert_opinion/archive/` - 버전별 피드백들

### 3. **루트 폴더 정리**
- 핵심 파일들만 루트에 유지
- 실행 스크립트들 → `scripts/`
- 설정 파일들 → `config/`
- 문서들 → `docs/`

### 4. **현재 버전 관리**
- `docs/planning/v0.3.1/` 생성
- v0.3.1 수정 계획서들 버전별 관리 시작

## 🎯 **개편 효과**

### ✅ **장점**
1. **명확한 구조**: 개발, 문서, 설정이 목적별로 분리
2. **버전 관리 개선**: 모든 문서에 일관된 아카이브 체계 적용
3. **신규 팀원 친화적**: 문서 위치가 직관적으로 파악 가능
4. **유지보수성 향상**: 체계적인 문서 관리로 장기 프로젝트에 적합

### 📊 **파일 이동 현황**
- **이동된 폴더**: 6개 (plan, expert_opinion, changelog, project_guide, reff, 기타)
- **생성된 구조**: docs/ 하위 4개 주요 카테고리
- **아카이브된 항목**: 15개 파일/폴더

## 📝 **주의사항**

### 🔧 **경로 참조 업데이트 필요**
- 스크립트에서 설정 파일 경로 변경: `theme_settings.json` → `config/theme_settings.json`
- 문서 링크들 업데이트 필요
- README 파일들의 상대경로 확인 필요

### 🔄 **향후 관리 방침**
- 새로운 버전 계획은 `docs/planning/v{version}/`에 생성
- 완료된 버전 계획은 `docs/planning/archive/`로 이동
- 모든 문서는 일관된 버전별 아카이브 체계 유지

## ✨ **완료 확인**

모든 폴더 구조 개편이 성공적으로 완료되었습니다. 
v0.3.1 개발 작업은 새로운 구조에서 진행하시면 됩니다.

---
*이 문서는 폴더 구조 개편 완료 후 자동 생성되었습니다.* 