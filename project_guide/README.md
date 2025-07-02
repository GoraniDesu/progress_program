# Project Guide

**Progress Program LLM 개발 요청 가이드라인**

이 폴더는 Progress Program 프로젝트에서 LLM(AI 어시스턴트)에게 개발 요청을 할 때 사용할 수 있는 실용적인 가이드라인과 템플릿을 제공합니다.

---

## 📁 **폴더 구성**

```
project_guide/
├── README.md                           # 이 파일 (폴더 소개)
├── llm_request_guide.md               # LLM 개발 요청 가이드라인 (메인 문서)
├── project_context_template.md        # 프로젝트 컨텍스트 템플릿
├── request_templates.md               # 요청 유형별 템플릿
└── best_practices.md                  # 실제 경험 기반 베스트 프랙티스
```

---

## 🎯 **가이드 목적**

### 📋 **해결하려는 문제**
- LLM에게 개발 요청 시 **일관성 부족**
- **호환성 문제** (기존 코드와 맞지 않는 구현)
- **프로젝트 컨텍스트 누락**으로 인한 잘못된 구현
- **문서 업데이트 누락**
- **품질 기준 불일치**

### ✅ **기대 효과**
- **일관된 코드 품질** 보장
- **호환성 문제** 사전 방지
- **개발 생산성** 향상
- **프로젝트 목표 준수**
- **문서 동기화** 자동화

---

## 🚀 **빠른 시작**

### 1단계: 메인 가이드 읽기
👉 **[`llm_request_guide.md`](./llm_request_guide.md)** - 가장 중요한 문서

### 2단계: 프로젝트 컨텍스트 준비
👉 **[`project_context_template.md`](./project_context_template.md)** - 요청 시 포함할 기본 정보

### 3단계: 적절한 템플릿 선택
👉 **[`request_templates.md`](./request_templates.md)** - 상황별 요청 템플릿

### 4단계: 베스트 프랙티스 확인
👉 **[`best_practices.md`](./best_practices.md)** - 실전 팁과 주의사항

---

## 💡 **핵심 원칙**

### 🔑 **Progress Program 개발 철학**
1. **간단함 우선**: "복잡한 기능에 지친 사용자를 위한 간단한 도구"
2. **실용성 극대화**: 꼭 필요한 기능만 추가
3. **호환성 보장**: 기존 기능이 깨지지 않아야 함
4. **사용자 경험 일관성**: 기존 워크플로우 유지

### 📊 **품질 기준**
- ✅ 모든 기존 기능 정상 동작
- ✅ 새 기능 버그 없음
- ✅ 사용자 경험 일관성 유지
- ✅ 성능 회귀 없음
- ✅ 문서 업데이트 완료

---

## 🔄 **사용 방법**

### 💻 **기본 사용법**
```markdown
1. llm_request_guide.md를 읽고 기본 원칙 이해
2. project_context_template.md를 복사해서 현재 상황에 맞게 수정
3. request_templates.md에서 적절한 템플릿 선택
4. 템플릿을 채워서 LLM에게 요청
5. best_practices.md의 체크리스트로 최종 검토
```

### 🎯 **고급 사용법**
```markdown
1. expert_opinion/development_checklist.md와 함께 사용
2. expert_opinion/compatibility_requirements.md 참조
3. 복잡한 요청 시 단계별로 나누어 진행
4. 요청 후 결과 검토 및 피드백 반영
```

---

## 📚 **관련 문서**

### 🏗️ **기술 문서**
- [`expert_opinion/development_checklist.md`](../expert_opinion/development_checklist.md) - 상세 개발 체크리스트
- [`expert_opinion/compatibility_requirements.md`](../expert_opinion/compatibility_requirements.md) - 호환성 요구사항

### 📋 **프로젝트 문서**
- [`README.md`](../README.md) - 프로젝트 개요
- [`reff/DEVELOPMENT_GUIDE.md`](../reff/DEVELOPMENT_GUIDE.md) - 개발 가이드
- [`CHANGELOG.md`](../CHANGELOG.md) - 변경 이력

### 📊 **버전 정보**
- [`changelog/v0.3.0_development_plan.md`](../changelog/v0.3.0_development_plan.md) - 현재 개발 계획

---

## ⚡ **효율적인 LLM 명령 방법**

### 🚀 **빠른 작업 명령어 모음**

#### 📁 **폴더/파일 생성 작업**
```markdown
✅ 좋은 명령 (구체적이고 일괄 처리):
"expert_opinion을 버전별로 폴더 재구성해줘. v0.1, v0.2, v0.3 폴더 만들고 파일들 이동시켜줘"

✅ 더 좋은 명령 (PowerShell 효율화 포함):
"폴더 재구성해줘. PowerShell 세미콜론이나 배열 사용해서 한 번에 처리해줘"

❌ 비효율적인 명령:
"v0.1 폴더 만들어줘" (하나씩 개별 요청)
```

#### 🔄 **파일 이동/이름 변경**
```markdown
✅ 효율적인 방법:
"expert_opinion 파일들을 버전별로 정리하고 파일명도 수정해줘"
"PowerShell 한 줄 명령으로 여러 파일 한번에 이동시켜줘"

✅ 패턴 기반 요청:
"v0.1_으로 시작하는 모든 파일을 v0.1 폴더로 이동하고 접두사 제거해줘"
```

#### 📝 **문서 작성/수정**
```markdown
✅ 구조적 요청:
"README.md에 효율적인 명령 방법 섹션을 추가해줘. PowerShell 활용법 포함해서"

✅ 컨텍스트 포함:
"project_guide/README.md에 LLM 명령 효율화 방법 추가. 기존 구조 유지하면서"
```

### ⚡ **시간 단축 키워드**

#### 🔥 **마법의 키워드들**
```markdown
"한 번에" - 여러 작업을 일괄 처리
"PowerShell로" - 효율적인 명령어 사용  
"배열 사용해서" - 반복 작업 자동화
"세미콜론으로" - 여러 명령 연결
"패턴 매칭으로" - 와일드카드 활용
"스크립트 블록으로" - 복잡한 로직 처리
```

#### 📊 **구체성 레벨**
```markdown
🥇 Level 3 (최고): "expert_opinion을 v0.1/v0.2/v0.3 폴더로 재구성하고 파일명에서 버전 접두사 제거, PowerShell 효율화 사용"

🥈 Level 2 (좋음): "expert_opinion 폴더를 버전별로 재구성해줘"

🥉 Level 1 (기본): "폴더 만들어줘"
```

### 🎯 **상황별 최적 명령**

#### 🏗️ **프로젝트 구조 변경**
```markdown
✅ "프로젝트 구조를 [원하는 형태]로 재구성해줘. 기존 파일들 적절히 이동시키고 README도 업데이트해줘"
✅ "폴더 구조 변경하고 관련 문서들도 함께 수정해줘"
```

#### 📄 **문서 작업**
```markdown
✅ "[파일명]에 [내용] 섹션 추가해줘. 기존 구조 유지하면서"
✅ "여러 파일에 동일한 섹션 추가해줘. 배열 사용해서 한 번에"
```

#### 🔧 **코드 작업**
```markdown
✅ "[기능명] 구현해줘. expert_opinion/v0.3/development_checklist.md 참조해서"
✅ "호환성 확인하고 [기능] 추가해줘. compatibility_requirements.md 따라서"
```

### 💡 **Pro Tips**

#### 🎨 **명령 최적화 팁**
```markdown
1. 🎯 구체적 목표 명시: "무엇을 어떻게"
2. 🔗 관련 문서 참조: "@expert_opinion", "@project_guide"  
3. ⚡ 효율화 키워드: "한 번에", "PowerShell로"
4. 📋 결과 확인: "완료 후 구조 보여줘"
5. 🔄 연관 작업: "관련 문서도 함께 업데이트"
```

#### 🚫 **피해야 할 명령**
```markdown
❌ 너무 모호한 명령: "파일 정리해줘"
❌ 하나씩 개별 요청: "파일1 이동해줘, 그다음 파일2 이동해줘"  
❌ 컨텍스트 누락: "README 수정해줘" (어떤 README?)
❌ 결과 불확실: "적당히 만들어줘"
```

#### 📈 **효율성 측정**
```markdown
🔥 최고 효율 (1분 내): 구체적 + PowerShell + 일괄처리
⚡ 높은 효율 (3분 내): 명확한 목표 + 구조적 접근
✅ 기본 효율 (5분 내): 단계별 명령
⏳ 낮은 효율 (10분+): 개별 작업 반복
```

---

## 🔧 **업데이트 및 기여**

### 📝 **문서 업데이트**
이 가이드는 Progress Program의 발전과 함께 지속적으로 업데이트됩니다:
- **새로운 베스트 프랙티스** 발견 시 추가
- **실패 사례** 분석 및 예방법 추가
- **템플릿 개선** 및 새 유형 추가

### 💡 **개선 제안**
실제 사용 경험을 바탕으로 한 개선 제안을 환영합니다:
- 더 효과적인 요청 방법
- 놓치기 쉬운 주의사항
- 자주 사용되는 패턴

---

**이 가이드를 활용하여 Progress Program을 더욱 안정적이고 일관되게 발전시켜 나가세요! 🚀** 