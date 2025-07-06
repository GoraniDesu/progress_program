# Progress Program LLM 개발 가이드

## 0. 문서의 목적

이 문서는 LLM(거대 언어 모델)이 `Progress Program`의 소스 코드를 이해하고, **기존 기능과의 호환성을 유지**하며 **안전하게 코드를 수정**할 수 있도록 돕는 것을 목표로 합니다. 코드 수정 요청 시, LLM은 반드시 이 문서를 정독하고 모든 가이드라인을 준수해야 합니다.

---

## 1. 프로젝트 개요

`Progress Program`은 사용자가 프로젝트와 하위 할 일(Task)을 관리하며 진행 상황을 시각적으로 추적할 수 있도록 돕는 데스크톱 애플리케이션입니다.

- **핵심 기능**: 프로젝트 생성/수정/삭제, 할 일 관리, 진행률 시각화, 데이터 백업/복원
- **기술 스택**: Python, PySide6 (Qt for Python), SQLite
- **플랫폼**: Windows 10/11

---

## 2. 개발 환경 설정 및 실행

LLM이 코드를 수정하고 테스트하기 위한 표준 개발 환경 설정 절차입니다.

### 2.1. 요구사항

- **Python**: 3.9+
- **OS**: Windows 10/11
- **기타**: Git

### 2.2. 설정 절차

1.  **저장소 복제**:
    ```bash
    git clone <repository_url>
    cd progress_program
    ```

2.  **환경 설정 스크립트 실행**:
    - 프로젝트 루트에서 다음 스크립트를 실행하여 Python 가상 환경을 설정하고 모든 의존성을 설치합니다.
    ```bash
    .\scripts\setup_env.bat
    ```
    - 이 스크립트는 다음 작업을 자동으로 수행합니다:
        - `progress_env` 이름의 가상 환경 생성
        - `requirements.txt` 기반으로 패키지 설치

3.  **가상 환경 활성화** (선택 사항, IDE에서 보통 자동 인식):
    ```bash
    .\progress_env\Scripts\activate
    ```

### 2.3. 프로그램 실행

- 개발 환경에서 프로그램을 실행하려면 **반드시** 다음 스크립트를 사용해야 합니다.
  ```bash
  .\run.bat
  ```
- 또는 PowerShell 환경인 경우:
  ```bash
  .\run.ps1
  ```
- **직접 `src/main.py`를 실행하지 마십시오.** 실행 스크립트는 프로그램에 필요한 환경 변수와 경로를 설정하는 중요한 역할을 합니다.

---

## 3. 프로젝트 아키텍처

### 3.1. 디렉토리 구조
```
progress_program/
├── .git/
├── config/
│   └── theme_settings.json   # 테마 설정 (색상, 폰트 등)
├── data/
│   └── progress.db           # (자동 생성) 애플리케이션 데이터베이스
├── docs/                     # 프로젝트 문서
├── resources/
│   └── fonts/                # 사용자 정의 폰트
├── scripts/                  # 빌드, 실행 등 자동화 스크립트
├── src/                      # 애플리케이션 소스 코드
│   ├── database/             # 데이터베이스 관리
│   ├── ui/                   # UI 컴포넌트
│   ├── utils/                # 유틸리티 모듈
│   └── main.py               # 애플리케이션 진입점
├── tests/                    # (향후 추가 예정) 테스트 코드
├── .gitignore
├── README.md
└── requirements.txt          # Python 의존성 목록
```

### 3.2. 실행 흐름

1.  `run.bat` 또는 `run.ps1` 스크립트가 실행됩니다.
2.  스크립트는 `progress_env` 가상환경의 Python 인터프리터를 사용하여 `src/main.py`를 실행합니다.
3.  `src/main.py`:
    - `QApplication` 인스턴스를 생성하고 기본 설정을 적용합니다.
    - `ui.main_window.MainWindow` 클래스의 인스턴스를 생성하고 화면에 표시합니다.
4.  `MainWindow`는 `ProjectWidget`, `TaskWidget` 등 다른 UI 컴포넌트를 초기화하고 전체 레이아웃을 구성합니다.
5.  사용자 상호작용은 각 UI 위젯의 이벤트 핸들러(슬롯)를 통해 처리되며, 데이터 변경이 필요할 경우 `database` 모듈을 통해 데이터베이스와 통신합니다.

### 3.3. 핵심 컴포넌트 역할

- **`src/main.py`**: 애플리케이션의 **유일한 진입점**. QApplication 생성, 메인 윈도우 초기화 및 실행을 담당합니다.
- **`src/database/`**: 데이터베이스 관련 모든 로직을 캡슐화합니다.
    - `database.py`: DB 연결, CRUD(생성, 읽기, 갱신, 삭제) 작업을 위한 `Database` 클래스를 제공합니다. **모든 DB 접근은 이 클래스를 통해서만 이루어져야 합니다.**
    - `models.py`: `Project`, `Task` 등 데이터베이스 테이블과 매핑되는 `dataclass` 모델을 정의합니다.
- **`src/ui/`**: 사용자 인터페이스를 구성하는 모든 PySide6 위젯이 위치합니다.
    - `main_window.py`: 애플리케이션의 메인 프레임. 다른 모든 UI 위젯을 포함하고 배치합니다.
    - `project_widget.py`, `task_widget.py`: 각 기능(프로젝트 관리, 할 일 관리)에 해당하는 UI와 로직을 담당합니다.
- **`src/utils/`**: 애플리케이션 전반에서 사용되는 유틸리티 모듈입니다.
    - `theme_manager.py`: UI 테마(색상, 폰트)를 관리합니다. `config/theme_settings.json` 파일을 읽어 적용합니다.
    - `status_manager.py`: 애플리케이션의 현재 상태(예: 현재 선택된 프로젝트)를 관리하고 위젯 간 상태 공유를 돕습니다.
    - `backup_manager.py`: 데이터베이스 백업 및 복원 기능을 담당합니다.
    - `helpers.py`: 날짜 포매팅, 텍스트 자르기 등 범용 도우미 함수를 제공합니다.

---

## 4. 데이터베이스 가이드

### 4.1. 스키마
```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    order_index INTEGER DEFAULT 0,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_date TIMESTAMP,
    due_date TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
);

CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
);
```

### 4.2. 데이터 모델 (`src/database/models.py`)
- 데이터베이스의 각 테이블은 아래의 `dataclass`와 1:1로 대응됩니다.
```python
@dataclass
class Project:
    id: Optional[int] = None
    title: str = ""
    description: str = ""
    created_date: Optional[datetime] = None
    updated_date: Optional[datetime] = None

@dataclass
class Task:
    id: Optional[int] = None
    project_id: int = 0
    title: str = ""
    description: str = ""
    completed: bool = False
    order_index: int = 0
    created_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    due_date: Optional[datetime] = None

@dataclass
class Note:
    id: Optional[int] = None
    project_id: int = 0
    content: str = ""
    created_date: Optional[datetime] = None
```

### 4.3. 데이터베이스 인터페이스 (`src/database/database.py`)
- **원칙**: 어떠한 경우에도 UI 코드나 다른 유틸리티에서 직접 SQL 쿼리를 실행해서는 안 됩니다. 모든 데이터베이스 상호작용은 반드시 `Database` 클래스의 메서드를 통해 수행해야 합니다.
- **주요 메서드**:
  ```python
  class Database:
      # Project-related methods
      def create_project(self, project: Project) -> int
      def get_all_projects(self) -> List[Project]
      def update_project(self, project: Project) -> None
      def delete_project(self, project_id: int) -> None
      
      # Task-related methods
      def create_task(self, task: Task) -> int
      def get_tasks_by_project(self, project_id: int) -> List[Task]
      def update_task(self, task: Task) -> None
      def delete_task(self, task_id: int) -> None
      # ... 등등
  ```

---

## 5. UI 가이드

### 5.1. 위젯 간 통신: 시그널과 슬롯

- 위젯 간의 결합도를 낮추기 위해 Qt의 시그널-슬롯 메커니즘을 적극적으로 사용합니다.
- 한 위젯에서 발생한 이벤트(예: "프로젝트 선택됨")는 시그널을 발생(emit)시키고, 이 시그널에 연결된 다른 위젯의 슬롯(메서드)이 실행됩니다.
- **주요 사용자 정의 시그널**:
    - `MainWindow`: `project_selected(Project)`, `project_updated()`
    - `ProjectWidget`: `task_updated()`, `note_updated()`
    - `TaskWidget`: `task_completed(Task)`, `task_reordered()`

### 5.2. 테마와 스타일링
- UI의 색상, 폰트 등은 `config/theme_settings.json` 파일에 정의되어 있습니다.
- `utils.theme_manager.ThemeManager`가 이 파일을 로드하여 애플리케이션 전역에 스타일을 적용합니다.
- UI 스타일 변경이 필요할 경우, 가급적 PySide6 위젯의 `setStyleSheet`을 직접 수정하기보다 `theme_settings.json`과 `ThemeManager`를 수정하는 것을 권장합니다.

---

## 6. 개발 가이드라인

### 6.1. 코딩 스타일
- **PEP 8**을 준수합니다.
- **Docstring**: 클래스, 메서드, 함수에는 반드시 Google 스타일 Docstring을 작성하여 역할, 인자, 반환 값을 명시해야 합니다.
- **Type Hinting**: 모든 변수, 함수 인자, 반환 값에 대해 타입 힌트를 사용하는 것을 강력히 권장합니다.

### 6.2. 의존성 관리
- 새로운 외부 라이브러리를 추가할 경우, `requirements.txt` 파일에 해당 라이브러리와 버전을 명시해야 합니다.
- 그 후, `scripts/setup_env.bat`를 다시 실행하여 모든 팀원이 동일한 환경을 유지할 수 있도록 합니다.

### 6.3. 에러 핸들링
- 사용자에게 보여져야 하는 오류는 `QMessageBox`를 사용하여 명확한 메시지를 전달합니다.
- 개발 중 확인이 필요한 로그는 `print()` 대신 Python의 `logging` 모듈을 사용하는 것을 권장합니다.

### 6.4. 커밋 및 브랜치 전략
- **커밋 메시지**: `feat: 로그인 기능 추가`, `fix: 메인 화면 렌더링 오류 수정`과 같이 [Conventional Commits](https://www.conventionalcommits.org/) 형식을 따릅니다.
- **브랜치**: `main` 브랜치에 직접 커밋하는 것을 금지합니다. 기능 개발은 `feat/`, 버그 수정은 `fix/` 접두사를 사용하여 새로운 브랜치를 생성한 후 작업하고, Pull Request를 통해 리뷰를 거칩니다.

---

## 7. 빌드 및 배포
- 최종 실행 파일 생성은 `scripts/build_release.ps1` (PowerShell) 또는 `build_release.bat` (CMD) 스크립트를 사용합니다.
- 이 스크립트는 `PyInstaller`를 사용하여 `dist/` 폴더에 실행 파일을 생성합니다.
- 빌드 과정 수정이 필요할 경우, 이 스크립트들을 수정해야 합니다.
