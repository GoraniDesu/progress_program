# Progress Program v0.5 호환성 요구사항

**작성자**: 홍길동 (Senior System Architect, 14년 경력)
**작성일**: 2025-05-01 
**버전**: 1.0 (Progress Program v0.4.2 → v0.5.0 호환성 기준)

---

## 🎯 v0.5 호환성 보장 원칙

1. **기존 기능 100% 보존**: v0.4.2의 모든 기능이 그대로 작동해야 함
2. **데이터 무손실**: 기존 백업 파일·데이터베이스 완전 호환
3. **API 일관성**: 기존 메서드 시그니처 100% 유지 (추가 매개변수는 선택적)
4. **UI 레이아웃 유지**: 컴포넌트 위치·크기 변경 최소화, 기존 단축키·워크플로우 보존
5. **성능 보장**: 새 기능 추가에도 기존 성능 수준 유지(±5% 이내)

---

## 🔧 v0.5 주요 변경사항별 호환성 분석

### 1. QTableWidget 폰트 사이즈 통일

| 항목 | 호환성 보장책 |
|------|--------------|
| 스타일시트 수정 | `src/utils/theme_manager.py` 내 CSS 확장 방식으로 기존 스타일 덮어쓰지 않음 |
| 메서드 시그니처 | 기존 `apply_theme()` 시그니처 유지, 내부 로직만 추가 |
| 리스크 | 다크/라이트 테마 전환 시 폰트 누락 → 단위 테스트로 검증 |

```python
# ❌ 시그니처 변경 금지
# ✅ 기존 구조 유지 + CSS 추가
LIGHT_TABLE_STYLE = """
    QTableWidget::item { font-size: 14px; }
"""
```

---

### 2. 노트 QTextEdit 기본 스타일 개선

* **Placeholder**·**폰트 크기**를 코드 레벨에서 주입하되, 객체 생성 방식 그대로 유지해 호출부 수정 無.
* 다국어 입력기 호환 테스트 필요(IME).

```python
# src/ui/project_widget.py
self.note_text.setPlaceholderText("메모를 입력하세요…")  # ✅ 기존 API 사용
self.note_text.setStyleSheet("font-size: 15px;")          # ✅ CSS 확장
```

---

### 3. 프로젝트 목록 타이틀 여백 확보

* 텍스트 앞 FIGURE SPACE(U+2007) 한 칸 추가 → 레이아웃 재계산 無.
* 접근성(스크린리더) 무영향 확인.

---

### 4. 프로젝트 제목 아이콘 변경

* 제목 형식 `⭐ {title} ⭐` 변경. 문자열 가공만 수행, 시그널·슬롯 유지.
* 기존 테스트케이스(제목 길이 1~100자) 통과 필수.

---

### 5. 백업 파일 이름 중복 처리 개선

| 요구 | 호환성 고려 |
|------|-------------|
| 파일 덮어쓰기 방지 | 동일 경로 존재 시 `name (n).ext` 자동 부여 |
| 내부 타임스탬프 유지 | restore 로직 영향 無, DB 스키마 변경 無 |
| **표시 이름 고정** | 타임스탬프 제거 후 `사용자 지정 이름 (+ (n))` 형태로 UI에 표시, 복원 자동 백업(`before_restore`) 포함 |
| 역호환성 | v0.4 백업도 그대로 복원 가능해야 함 |

```python
# src/utils/backup_manager.py (추가)
while os.path.exists(candidate_path):
    n += 1
    candidate_path = f"{stem} ({n}){suffix}"
```

---

### 6. Fluid Progress Animation 1차 도입

* `AnimationManager.animate_fluid_progress()` 새로 도입 (선택적 실행)
* 애니메이션 전역 ON/OFF 설정(`animation_enabled`) 기본값 **True** – 기존 설정 파일에 기본값 자동 주입
* 저사양 환경: FPS < 30 시 자동 비활성화 로직 포함 → 성능 역-저하 방지
* ProgressBar 값 직접 설정 API(`setValue`) 기존대로 사용 가능

```python
if not self.animation_enabled or low_fps():
    progress_bar.setValue(static_value)  # ✅ 기존 방식 fallback
```

---

## 🔒 호환성 검증 체크리스트

### 📊 데이터·설정
- [ ] v0.4.2 데이터베이스로 v0.5 구동 시 모든 뷰·CRUD 정상 동작
- [ ] 기존 theme_settings.json 로드 → 새 필드 `animation_enabled` 자동 삽입
- [ ] v0.4 백업 파일 복원 성공률 100%

### 🧪 기능 동작
- [ ] 테마 전환 후 QTableWidget 폰트 동일
- [ ] 노트 영역 Placeholder 및 폰트 반영
- [ ] 프로젝트 목록 타이틀 좌측 여백 4px 유지
- [ ] 제목 아이콘 ⭐ 표시 일관성(다국어 포함)
- [ ] 동일 이름 연속 백업 시 `(n)` 인덱스 순차 증가 & 기존 파일 보존
- [ ] Fluid 애니메이션 실행·중복 실행 없음 & FPS 60 유지

### 🚀 성능
- [ ] 메모리 사용량 v0.4 대비 5% 이내 증가
- [ ] CPU 사용률 Fluid 애니 활성화 시 10% 이내 증가

---

## ⚠️ 위험 요소 및 대응

| 위험 | 등급 | 대응 |
|------|------|------|
| 애니메이션 과부하 | 🟠 중 | FPS 모니터링 후 자동 비활성화 |
| 백업 파일 I/O 지연 | 🟠 중 | 비동기 파일 쓰기 & 예외 로깅 |
| CSS 캐시 충돌 | 🟢 낮 | 테마 적용 시 `QApplication.setStyleSheet()` 전체 재적용 |

---

## ✅ 결론

Progress Program **v0.5**는 위 호환성 가이드를 준수함으로써 **기존 사용자 데이터·워크플로우를 100% 보존**하면서도 시각적 완성도와 몰입감을 향상합니다. 모든 신규 기능은 **비파괴적(Non-Breaking)** 방식으로 통합되었으며, 호환성 검증 체크리스트 통과 시 **안전한 배포**가 가능합니다.

> "변화는 새로워야 하지만, 익숙함을 깨뜨려서는 안 된다." – System Architecture 팀 