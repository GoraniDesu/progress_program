# Progress Program 호환성 요구사항

**※ 본 문서는 Progress Program 개발 과정의 일환으로 작성된 가상의 전문가 가이드입니다.**

---

**작성자**: 박지훈 (Senior System Architect, 10년 경력)  
**소속**: 시스템 아키텍처 컨설팅 그룹  
**작성일**: 2025년 7월 20일  
**문서 목적**: 기존 코드와의 호환성 요구사항 정의  
**버전**: 1.0 (Progress Program v0.3.0 기준)

---

## 🎯 **호환성 보장 원칙**

### 📋 **핵심 원칙**
1. **하위 호환성 우선**: 기존 기능이 깨지지 않아야 함
2. **점진적 개선**: 급격한 변화보다는 단계적 개선
3. **사용자 경험 일관성**: 기존 워크플로우 유지
4. **데이터 무결성**: 기존 데이터 손실 방지

---

## 🏗️ **시스템 아키텍처 호환성**

### 📁 **1. 폴더 구조 요구사항**
```
✅ MUST MAINTAIN (반드시 유지해야 하는 구조)
progress_program/
├── src/
│   ├── __init__.py
│   ├── main.py                 # 메인 진입점 - 변경 금지
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py      # 메인 UI - 호환성 중요
│   │   ├── project_widget.py   # 프로젝트 위젯
│   │   ├── task_widget.py      # 할 일 위젯
│   │   ├── backup_dialog.py    # 백업 다이얼로그
│   │   └── due_date_dialog.py  # 마감일 다이얼로그
│   ├── database/
│   │   ├── __init__.py
│   │   ├── database.py         # DB 연결 - 스키마 호환성 중요
│   │   └── models.py           # DB 모델 - 변경 시 마이그레이션 필수
│   └── utils/
│       ├── __init__.py
│       ├── backup_manager.py   # 백업 기능
│       ├── helpers.py          # 공통 유틸리티
│       ├── progress.py         # 진척도 계산
│       └── theme_manager.py    # 테마 관리
├── data/                       # 사용자 데이터 - 경로 변경 금지
├── requirements.txt            # 의존성 - 호환성 확인 필수
├── theme_settings.json         # 설정 파일 - 형식 유지 필수
├── run.bat                     # 실행 스크립트 - 변경 금지
└── setup_env.bat              # 환경 설정 - 변경 금지
```

### 🚫 **절대 변경 금지 요소**
```
❌ src/main.py의 진입점 함수명
❌ data/ 폴더 경로 및 구조
❌ run.bat, setup_env.bat 실행 방식
❌ requirements.txt 주요 의존성 버전 (PySide6, SQLite)
❌ 기존 public API 함수 시그니처
```

---

## 🗄️ **데이터베이스 호환성**

### 📊 **2. 스키마 호환성 요구사항**

#### ✅ **기존 테이블 구조 (변경 금지)**
```sql
-- projects 테이블
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- tasks 테이블  
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    completed BOOLEAN DEFAULT 0,
    order_index INTEGER,
    due_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects (id)
);

-- notes 테이블
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects (id)
);
```

#### 🔄 **스키마 변경 시 필수 사항**
```python
# 새 컬럼 추가 시 - 반드시 DEFAULT 값 포함
ALTER TABLE tasks ADD COLUMN priority INTEGER DEFAULT 1;

# 마이그레이션 함수 예시
def migrate_database(db_path):
    """기존 데이터베이스를 새 스키마로 마이그레이션"""
    conn = sqlite3.connect(db_path)
    
    # 백업 생성
    backup_path = f"{db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(db_path, backup_path)
    
    try:
        # 스키마 변경 수행
        cursor = conn.cursor()
        cursor.execute("ALTER TABLE tasks ADD COLUMN priority INTEGER DEFAULT 1")
        conn.commit()
        
        print(f"마이그레이션 완료. 백업: {backup_path}")
    except Exception as e:
        # 실패 시 백업에서 복원
        conn.close()
        shutil.copy2(backup_path, db_path)
        raise e
    finally:
        conn.close()
```

### 🛡️ **데이터 무결성 보장**
```python
# 필수 체크 사항
✅ 기존 데이터 손실 방지
✅ Foreign Key 관계 유지
✅ 인덱스 성능 유지
✅ 백업 생성 후 변경
✅ 롤백 메커니즘 준비
```

---

## 🎨 **UI/UX 호환성**

### 🖼️ **3. UI 컴포넌트 호환성**

#### ✅ **기존 UI 구조 유지**
```python
# MainWindow 클래스 - 주요 메서드 시그니처 유지
class MainWindow(QMainWindow):
    def __init__(self):
        # 기존 초기화 로직 유지
        
    def setup_ui(self):
        # 기존 UI 설정 로직 유지
        
    def create_project(self, name: str) -> int:
        # 반환 타입과 파라미터 유지
        
    def add_task(self, project_id: int, title: str) -> int:
        # 기존 API 유지
        
    def update_progress(self, project_id: int):
        # 진척도 업데이트 로직 유지
```

#### 🎨 **테마 시스템 호환성**
```json
// theme_settings.json - 기존 키 유지 필수
{
    "current_theme": "light",  // 변경 금지
    "themes": {
        "light": {
            "background_color": "#ffffff",
            "text_color": "#000000",
            "progress_color": "#4CAF50"
        },
        "dark": {
            "background_color": "#2b2b2b",
            "text_color": "#ffffff", 
            "progress_color": "#66BB6A"
        }
    }
}
```

#### ⌨️ **키보드 단축키 호환성**
```python
# 기존 단축키 유지 필수 (변경 금지)
EXISTING_SHORTCUTS = {
    "Ctrl+N": "새 할 일 추가",
    "Ctrl+E": "편집 모드",
    "Delete": "선택 항목 삭제",
    "F5": "새로고침",
    "Ctrl+S": "수동 저장"
}

# 새 단축키 추가 시 충돌 방지
NEW_SHORTCUTS = {
    "Ctrl+B": "백업 생성",      # ✅ 충돌 없음
    "Ctrl+R": "복원",           # ✅ 충돌 없음
    "Ctrl+F": "검색",           # ✅ 충돌 없음
    # "Ctrl+N": "새 기능"       # ❌ 기존과 충돌
}
```

---

## 🔧 **API 호환성**

### 🔗 **4. 함수 시그니처 호환성**

#### ✅ **유지해야 하는 핵심 API**
```python
# database/database.py
class DatabaseManager:
    def __init__(self, db_path: str):
        # 파라미터 변경 금지
        
    def create_project(self, name: str) -> int:
        # 반환 타입 변경 금지
        
    def add_task(self, project_id: int, title: str, 
                 due_date: Optional[str] = None) -> int:
        # 기존 파라미터 유지, 새 파라미터는 Optional로

    def get_tasks(self, project_id: int) -> List[Dict]:
        # 반환 구조 유지

# utils/progress.py  
def calculate_progress(tasks: List[Dict]) -> float:
    # 입력/출력 타입 유지

# utils/helpers.py
def format_date(date_str: str) -> str:
    # 기존 포맷 유지
```

#### 🔄 **API 확장 시 권장 패턴**
```python
# ✅ 좋은 예시 - 하위 호환성 유지
def add_task(self, project_id: int, title: str, 
             due_date: Optional[str] = None,
             priority: int = 1) -> int:  # 새 파라미터는 기본값 포함
    
# ❌ 나쁜 예시 - 기존 API 변경
def add_task(self, project_id: int, title: str, 
             priority: int) -> int:  # 기존 호출 코드가 깨짐
```

---

## 📦 **의존성 호환성**

### 📚 **5. 라이브러리 버전 관리**

#### ✅ **핵심 의존성 (버전 고정)**
```txt
# requirements.txt - 주요 버전 변경 금지
PySide6>=6.5.0,<7.0.0       # 메이저 버전 고정
sqlite3                      # 내장 모듈 - 변경 없음
```

#### 🔄 **의존성 추가 시 주의사항**
```python
# 새 의존성 추가 전 체크리스트
✅ 기존 라이브러리와 충돌 없음 확인
✅ 라이선스 호환성 확인  
✅ 최소 버전 요구사항 확인
✅ 크로스 플랫폼 호환성 확인
✅ 패키지 크기 영향 최소화

# 추가 허용 가능한 의존성 예시
requests>=2.25.0      # HTTP 요청 (백업 클라우드 연동용)
cryptography>=3.0.0   # 암호화 (백업 암호화용)
schedule>=1.1.0       # 작업 스케줄링 (자동 백업용)
```

---

## 🔧 **설정 파일 호환성**

### ⚙️ **6. 설정 파일 형식 유지**

#### 📄 **theme_settings.json 호환성**
```python
# 설정 파일 읽기 - 하위 호환성 보장
def load_theme_settings():
    default_settings = {
        "current_theme": "light",
        "themes": {
            "light": {"background_color": "#ffffff", ...},
            "dark": {"background_color": "#2b2b2b", ...}
        }
    }
    
    try:
        with open("theme_settings.json", "r") as f:
            settings = json.load(f)
            
        # 기존 키 유지하면서 새 키 추가
        for key, value in default_settings.items():
            if key not in settings:
                settings[key] = value
                
        return settings
    except (FileNotFoundError, json.JSONDecodeError):
        # 파일이 없거나 손상된 경우 기본값 사용
        return default_settings
```

#### 🔄 **설정 확장 패턴**
```json
// ✅ 좋은 예시 - 기존 구조 유지하며 확장
{
    "current_theme": "light",           // 기존 키 유지
    "themes": { ... },                  // 기존 구조 유지
    "notifications": {                  // 새 기능 추가
        "enabled": true,
        "sound": true,
        "popup": false
    }
}

// ❌ 나쁜 예시 - 기존 구조 변경
{
    "theme": "light",                   // 키 이름 변경 (호환성 깨짐)
    "theme_config": { ... }             // 구조 변경 (호환성 깨짐)
}
```

---

## 🧪 **테스트 호환성**

### 🔍 **7. 호환성 테스트 시나리오**

#### ✅ **필수 테스트 케이스**
```python
def test_backward_compatibility():
    """기존 기능 호환성 테스트"""
    
    # 1. 기존 데이터베이스 파일로 테스트
    old_db_path = "test_data/progress_v0.2.db"
    assert can_open_database(old_db_path)
    
    # 2. 기존 설정 파일로 테스트  
    old_config = "test_data/theme_settings_v0.2.json"
    assert can_load_config(old_config)
    
    # 3. 기존 API 호출 테스트
    db = DatabaseManager("test.db")
    project_id = db.create_project("Test Project")
    task_id = db.add_task(project_id, "Test Task")
    assert isinstance(project_id, int)
    assert isinstance(task_id, int)
    
    # 4. 기존 UI 워크플로우 테스트
    main_window = MainWindow()
    main_window.show()
    assert main_window.isVisible()
```

#### 🔄 **업그레이드 시나리오 테스트**
```python
def test_upgrade_scenarios():
    """버전 업그레이드 시나리오 테스트"""
    
    test_cases = [
        ("v0.1.0", "v0.3.0"),
        ("v0.2.0", "v0.3.0"),
        ("v0.2.5", "v0.3.0")
    ]
    
    for old_version, new_version in test_cases:
        # 이전 버전 데이터로 새 버전 실행
        assert upgrade_test(old_version, new_version)
```

---

## 📋 **호환성 체크리스트**

### ✅ **개발 전 체크리스트**
```
[ ] 기존 폴더 구조 분석 완료
[ ] 기존 API 시그니처 파악 완료
[ ] 기존 데이터베이스 스키마 분석 완료
[ ] 기존 설정 파일 형식 파악 완료
[ ] 기존 의존성 버전 확인 완료
```

### ✅ **개발 중 체크리스트**
```
[ ] 기존 함수 시그니처 유지
[ ] 새 파라미터는 Optional로 추가
[ ] 데이터베이스 변경 시 마이그레이션 포함
[ ] 설정 파일 변경 시 하위 호환성 보장
[ ] 새 의존성 추가 시 충돌 확인
```

### ✅ **개발 후 체크리스트**
```
[ ] 기존 데이터베이스 파일로 테스트 완료
[ ] 기존 설정 파일로 테스트 완료
[ ] 기존 API 호출 테스트 완료
[ ] 업그레이드 시나리오 테스트 완료
[ ] 성능 회귀 테스트 완료
```

---

## 🚨 **호환성 위반 시 대응**

### ⚠️ **경고 신호**
```
🔴 기존 기능이 동작하지 않음
🔴 기존 데이터를 읽을 수 없음
🔴 기존 설정이 적용되지 않음
🔴 API 호출 시 에러 발생
🔴 UI 레이아웃이 깨짐
```

### 🛠️ **대응 방법**
```python
# 1. 즉시 롤백
git revert <commit-hash>

# 2. 호환성 레이어 추가
def legacy_api_wrapper(old_function):
    """기존 API 호환성 유지용 래퍼"""
    def wrapper(*args, **kwargs):
        # 새 API로 변환하여 호출
        return new_function(convert_args(args, kwargs))
    return wrapper

# 3. 마이그레이션 스크립트 제공
def migrate_user_data():
    """사용자 데이터 마이그레이션"""
    backup_data()
    convert_database()
    validate_migration()
```

---

## 🎯 **결론**

### 📊 **호환성 보장 효과**
- ✅ **사용자 경험 일관성** 유지
- ✅ **데이터 손실 방지**
- ✅ **업그레이드 안정성** 보장
- ✅ **개발 생산성** 향상
- ✅ **유지보수 비용** 절감

### 🔑 **핵심 원칙 요약**
1. **기존 API 시그니처 절대 변경 금지**
2. **데이터베이스 변경 시 마이그레이션 필수**
3. **설정 파일 형식 하위 호환성 보장**
4. **새 기능은 점진적 추가**
5. **충분한 테스트로 검증**

**모든 개발 시 이 요구사항을 준수하여 안정적이고 일관된 사용자 경험을 제공하세요.**

---

**※ 본 문서는 Progress Program 개발 과정의 일환으로 작성된 가상의 전문가 가이드입니다.** 