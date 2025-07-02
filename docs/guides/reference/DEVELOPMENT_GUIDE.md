# 개발 가이드

## 🚀 빠른 시작

### 1. 환경 설정
```bash
# 필요한 패키지 설치
pip install PySide6 matplotlib

# 프로젝트 실행
python src/main.py
```

### 2. 개발 순서
1. **데이터베이스 설계** → `src/database/` 
2. **기본 UI 구조** → `src/ui/`
3. **비즈니스 로직** → `src/utils/`
4. **테스트 및 배포** → `tests/`, `dist/`

## 💻 AI 활용 팁

### 코드 생성 요청 예시
```
"PySide6로 다음 기능의 메인 윈도우를 만들어줘:
- 왼쪽: 프로젝트 목록 (QListWidget)
- 오른쪽 상단: 할 일 목록 (QTableWidget) 
- 오른쪽 하단: 진척도 바 (QProgressBar)
- 하단: 메모 영역 (QTextEdit)"
```

```
"SQLite로 다음 테이블을 만들고 CRUD 함수를 작성해줘:
- projects: id, title, description, created_date
- tasks: id, project_id, title, completed, created_date
- notes: id, content, timestamp"
```

### 문제 해결 요청
```
"이 에러를 수정해줘: [에러 메시지 복사]"
"이 코드를 최적화해줘: [코드 복사]"
"이 기능의 테스트 코드를 작성해줘: [함수 복사]"
```

## 🎯 핵심 기능 체크리스트

### MVP (2주차까지)
- [ ] 프로젝트 생성/수정/삭제
- [ ] 할 일 추가/완료 체크
- [ ] 진척도 자동 계산 및 표시
- [ ] 데이터 저장/불러오기

### 추가 기능 (3-4주차)
- [ ] 메모/노트 기능
- [ ] 날짜/시간 자동 기록
- [ ] 간단한 통계 (완료율, 소요시간)
- [ ] 데이터 백업/복원

## 🔧 유용한 명령어

### 테스트 실행
```bash
python -m pytest tests/
```

### EXE 빌드
```bash
pip install pyinstaller
pyinstaller --onefile --windowed src/main.py
```

### 코드 정리
```bash
pip install black
black src/
```

## 📂 파일 구조

```
src/
├── main.py              # 앱 진입점
├── ui/
│   ├── main_window.py   # 메인 윈도우
│   ├── project_widget.py # 프로젝트 관리 위젯
│   └── task_widget.py   # 할 일 관리 위젯
├── database/
│   ├── models.py        # 데이터 모델
│   └── database.py      # DB 연결 및 CRUD
└── utils/
    ├── progress.py      # 진척도 계산
    └── helpers.py       # 기타 유틸리티
```

## ⚡ 개발 속도 향상 팁

1. **작은 단위로 개발**: 한 번에 하나의 기능만 구현
2. **AI 적극 활용**: 반복적인 코드는 AI에게 맡기기
3. **빠른 테스트**: 기능 완성 즉시 직접 사용해보기
4. **문서는 최소한**: 코드가 문서가 되도록 명확하게 작성 