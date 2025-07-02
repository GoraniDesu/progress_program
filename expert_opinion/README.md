# Expert Opinion 폴더 구조

**※ 본 폴더는 Progress Program 개발 과정의 일환으로 작성된 가상의 전문가 의견들을 버전별로 관리합니다.**

---

## 📁 **폴더 구조**

### 🗂️ **v0.1/ - 초기 개발 단계 피드백**
```
v0.1/
├── user_feedback.md                    # 기본 사용자 피드백
├── design_feedback.md                  # 디자인 전문가 피드백
├── project_manager_analysis.md         # 프로젝트 매니저 분석
├── overall_project_analysis.md         # 종합 프로젝트 분석
├── picky_user_feedback.md             # 까다로운 사용자 피드백
└── design_guru_feedback.md            # 디자인 거장 피드백
```

### 🗂️ **v0.2/ - 기능 확장 단계 피드백**
```
v0.2/
├── user_feedback.md                    # v0.2 사용자 피드백
├── design_feedback.md                  # v0.2 디자인 피드백
├── project_manager_analysis.md         # v0.2 프로젝트 매니저 분석
└── scope_analysis.md                   # 범위 분석
```

### 🗂️ **v0.3/ - 고급 기능 단계 피드백**
```
v0.3/
├── user_feedback.md                    # v0.3 사용자 피드백
├── development_checklist.md            # 개발 체크리스트 (v0.3 기준)
└── compatibility_requirements.md       # 호환성 요구사항 (v0.3 기준)
```

---

## 🎯 **사용 방법**

### 📋 **특정 버전 개발 시**
```bash
# v0.3 개발 시 참조할 문서들
expert_opinion/v0.3/development_checklist.md        # 개발 가이드라인
expert_opinion/v0.3/compatibility_requirements.md   # 호환성 요구사항
expert_opinion/v0.3/user_feedback.md               # 사용자 요구사항
```

### 🔄 **버전 간 비교 시**
```bash
# 사용자 피드백 변화 추적
expert_opinion/v0.1/user_feedback.md
expert_opinion/v0.2/user_feedback.md  
expert_opinion/v0.3/user_feedback.md
```

### 📈 **개발 이력 추적**
- 각 버전별로 어떤 요구사항과 제약사항이 있었는지 명확히 추적
- 호환성 문제 발생 시 이전 버전 요구사항 참조
- 기능 진화 과정 문서화

---

## ⚠️ **주의사항**

### 🔒 **버전별 문서 불변성**
- 각 버전의 문서는 해당 버전이 완료된 후 수정하지 않음
- 새로운 피드백은 새 버전 폴더에 추가
- 역사적 기록 보존을 위해 기존 문서 변경 금지

### 📝 **문서 명명 규칙**
```
✅ GOOD: user_feedback.md, design_feedback.md
❌ BAD: v0.1_user_feedback.md (폴더로 버전 구분)
❌ BAD: UserFeedback.md (snake_case 사용)
```

### 🆕 **새 버전 추가 시**
1. 새 버전 폴더 생성 (예: `v0.4/`)
2. 해당 버전의 문서들 추가
3. 본 README.md 업데이트

---

## 📊 **버전별 주요 특징**

| 버전 | 주요 포커스 | 핵심 문서 | 특이사항 |
|------|-------------|-----------|----------|
| v0.1 | 기본 기능 설계 | overall_project_analysis.md | 다양한 전문가 의견 수집 |
| v0.2 | 기능 확장 및 개선 | scope_analysis.md | 범위 분석 추가 |
| v0.3 | 고급 기능 및 호환성 | compatibility_requirements.md | 개발 가이드라인 체계화 |

---

**마지막 업데이트**: 2025년 7월 2일  
**관리자**: Progress Program 개발팀 