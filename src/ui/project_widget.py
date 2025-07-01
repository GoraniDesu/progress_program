"""
프로젝트 상세 위젯
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QPushButton, QTableWidget, QTableWidgetItem, 
    QTextEdit, QInputDialog, QMessageBox, QHeaderView,
    QCheckBox, QLabel, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from database.database import Database
from database.models import Project, Task, Note
from utils.helpers import format_datetime, validate_task_title, validate_project_title
from ui.task_widget import TaskWidget


class ProjectWidget(QWidget):
    """프로젝트 상세 위젯"""
    
    project_updated = Signal()
    
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self.current_project = None
        self.init_ui()

    def init_ui(self):
        """UI 초기화"""
        layout = QVBoxLayout(self)
        
        # 프로젝트 액션 버튼들
        button_layout = QHBoxLayout()
        
        self.edit_project_btn = QPushButton("📝 프로젝트 편집")
        self.edit_project_btn.clicked.connect(self.edit_project)
        button_layout.addWidget(self.edit_project_btn)
        
        self.delete_project_btn = QPushButton("🗑️ 프로젝트 삭제")
        self.delete_project_btn.clicked.connect(self.delete_project)
        button_layout.addWidget(self.delete_project_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # 탭 위젯
        self.tab_widget = QTabWidget()
        
        # 할 일 탭
        self.task_widget = TaskWidget(self.db)
        self.task_widget.task_updated.connect(self.on_task_updated)
        self.tab_widget.addTab(self.task_widget, "📋 할 일")
        
        # 노트 탭
        self.note_widget = self.create_note_widget()
        self.tab_widget.addTab(self.note_widget, "📝 노트")
        
        layout.addWidget(self.tab_widget)
        
        # 스타일 적용
        self.apply_styles()

    def create_note_widget(self) -> QWidget:
        """노트 위젯 생성"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 노트 버튼
        button_layout = QHBoxLayout()
        self.add_note_btn = QPushButton("+ 노트 추가")
        self.add_note_btn.clicked.connect(self.add_note)
        button_layout.addWidget(self.add_note_btn)
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # 노트 내용
        self.note_text = QTextEdit()
        self.note_text.setPlaceholderText("여기에 프로젝트 관련 메모를 작성하세요...")
        layout.addWidget(self.note_text)
        
        return widget

    def apply_styles(self):
        """스타일 적용"""
        self.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #ddd;
                background-color: white;
            }
            QTabWidget::tab-bar {
                alignment: left;
            }
            QTabBar::tab {
                background-color: #f0f0f0;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #4CAF50;
            }
            QTabBar::tab:hover {
                background-color: #e8f5e8;
            }
            QTableWidget {
                gridline-color: #ddd;
                selection-background-color: #e3f2fd;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px;
            }
        """)

    def apply_theme(self, theme_name: str):
        """테마 적용"""
        # 테마 매니저를 통해 스타일시트 적용
        from utils.theme_manager import theme_manager
        style_sheet = theme_manager.get_style_sheet(theme_name)
        self.setStyleSheet(style_sheet)
        
        # 자식 위젯들에도 테마 적용
        if hasattr(self, 'task_widget'):
            self.task_widget.apply_theme(theme_name)

    def set_project(self, project: Project):
        """프로젝트 설정"""
        self.current_project = project
        self.show()
        self.load_project_data()

    def load_project_data(self):
        """프로젝트 데이터 로드"""
        if not self.current_project:
            return
        
        # 할 일 위젯에 프로젝트 설정
        self.task_widget.set_project(self.current_project)
        
        # 노트 로드
        self.load_notes()

    def load_notes(self):
        """노트 로드"""
        if not self.current_project:
            return
        
        notes = self.db.get_notes_by_project(self.current_project.id)
        
        self.note_text.setPlainText("")
        for note in notes:
            timestamp = format_datetime(note.created_date, "%Y-%m-%d %H:%M")
            self.note_text.append(f"[{timestamp}]\n{note.content}\n\n")

    def add_note(self):
        """노트 추가"""
        if not self.current_project:
            return
        
        text, ok = QInputDialog.getMultiLineText(
            self, "새 노트", "노트 내용을 입력하세요:"
        )
        
        if ok and text.strip():
            # 노트 생성
            from database.models import Note
            note = Note(
                project_id=self.current_project.id,
                content=text.strip()
            )
            self.db.create_note(note)
            
            # 노트 다시 로드
            self.load_notes()
            QMessageBox.information(self, "성공", "노트가 추가되었습니다!")

    def edit_project(self):
        """프로젝트 편집"""
        if not self.current_project:
            return
        
        title, ok = QInputDialog.getText(
            self, "프로젝트 편집", "프로젝트 제목을 수정하세요:",
            text=self.current_project.title
        )
        
        if ok and title:
            # 제목 검증
            is_valid, error_msg = validate_project_title(title)
            if not is_valid:
                QMessageBox.warning(self, "입력 오류", error_msg)
                return
            
            # 설명 입력
            description, ok = QInputDialog.getText(
                self, "프로젝트 편집", "프로젝트 설명을 수정하세요:",
                text=self.current_project.description or ""
            )
            
            if not ok:
                description = self.current_project.description
            
            # 프로젝트 업데이트
            self.current_project.title = title.strip()
            self.current_project.description = description.strip() if description else ""
            self.db.update_project(self.current_project)
            
            # 업데이트 시그널 발생
            self.project_updated.emit()
            QMessageBox.information(self, "성공", "프로젝트가 수정되었습니다!")

    def delete_project(self):
        """프로젝트 삭제"""
        if not self.current_project:
            return
        
        reply = QMessageBox.question(
            self, "삭제 확인", 
            f"정말로 '{self.current_project.title}' 프로젝트를 삭제하시겠습니까?\n"
            "모든 할 일과 노트가 함께 삭제됩니다.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.db.delete_project(self.current_project.id)
            self.current_project = None
            
            # 화면 숨김
            self.hide()
            
            # 업데이트 시그널 발생
            self.project_updated.emit()
            QMessageBox.information(self, "성공", "프로젝트가 삭제되었습니다!")

    def on_task_updated(self):
        """할 일 업데이트 이벤트"""
        self.project_updated.emit() 