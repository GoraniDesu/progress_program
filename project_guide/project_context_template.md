# Progress Program 프로젝트 컨텍스트 템플릿

**LLM 요청 시 포함할 기본 정보 템플릿**

---

## 📋 **기본 프로젝트 정보**

```markdown
## 프로젝트 컨텍스트
**프로젝트명**: Progress Program v0.3.0
**목표**: "복잡한 기능에 지친 사용자를 위한 간단한 진척도 관리 도구"
**기술 스택**: Python, PySide6, SQLite
**현재 상태**: v0.3.0 개발 중
```

## 🏗️ **핵심 구조 정보**

```markdown
## 주요 파일 구조
- src/main.py: 애플리케이션 진입점
- src/ui/main_window.py: 메인 UI 윈도우
- src/ui/project_widget.py: 프로젝트 관리 위젯
- src/ui/task_widget.py: 할 일 관리 위젯
- src/database/database.py: SQLite 데이터베이스 관리
- src/database/models.py: 데이터 모델 정의
- src/utils/progress.py: 진척도 계산 로직
- src/utils/theme_manager.py: 테마 시스템
- theme_settings.json: 사용자 설정 파일
```

## 🔒 **필수 준수사항**

```markdown
## 반드시 확인해야 할 문서
1. expert_opinion/development_checklist.md - 개발 체크리스트
2. expert_opinion/compatibility_requirements.md - 호환성 요구사항
3. project_guide/llm_request_guide.md - 요청 가이드라인

## 절대 금지사항
❌ 기존 API 시그니처 변경
❌ 데이터베이스 스키마 무단 변경
❌ 복잡한 기능 추가 (간단함 원칙 위배)
❌ main.py 진입점 변경
❌ 기존 사용자 워크플로우 파괴
```

## ✅ **품질 기준**

```markdown
## 완료 기준 체크리스트
- [ ] 모든 기존 기능 정상 동작
- [ ] 새 기능 버그 없음
- [ ] 호환성 테스트 통과
- [ ] "간단함" 원칙 위반 없음
- [ ] 관련 문서 업데이트 완료
```

---

**이 템플릿을 복사해서 현재 요청에 맞게 수정하여 사용하세요.** 