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
from utils.helpers import format_datetime, validate_task_title
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
        
        # 버튼 영역
        button_layout = QHBoxLayout()
        
        self.add_note_btn = QPushButton("+ 노트 추가")
        self.add_note_btn.clicked.connect(self.add_note)
        button_layout.addWidget(self.add_note_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # 노트 목록
        self.note_table = QTableWidget()
        self.note_table.setColumnCount(3)
        self.note_table.setHorizontalHeaderLabels(["내용", "작성 시간", "액션"])
        
        # 컬럼 너비 설정
        header = self.note_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        
        layout.addWidget(self.note_table)
        
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
        
        self.note_table.setRowCount(len(notes))
        
        for row, note in enumerate(notes):
            # 내용 (최대 100자)
            content = note.content[:100] + "..." if len(note.content) > 100 else note.content
            content_item = QTableWidgetItem(content)
            content_item.setData(Qt.UserRole, note)
            self.note_table.setItem(row, 0, content_item)
            
            # 작성 시간
            time_item = QTableWidgetItem(format_datetime(note.created_date))
            self.note_table.setItem(row, 1, time_item)
            
            # 액션 버튼들
            action_widget = self.create_note_action_widget(note)
            self.note_table.setCellWidget(row, 2, action_widget)

    def create_note_action_widget(self, note: Note) -> QWidget:
        """노트 액션 위젯 생성"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(4, 4, 4, 4)
        
        # 편집 버튼
        edit_btn = QPushButton("✏️")
        edit_btn.setToolTip("편집")
        edit_btn.setMaximumSize(30, 30)
        edit_btn.clicked.connect(lambda: self.edit_note(note))
        layout.addWidget(edit_btn)
        
        # 삭제 버튼
        delete_btn = QPushButton("🗑️")
        delete_btn.setToolTip("삭제")
        delete_btn.setMaximumSize(30, 30)
        delete_btn.clicked.connect(lambda: self.delete_note(note))
        layout.addWidget(delete_btn)
        
        return widget

    def add_note(self):
        """노트 추가"""
        if not self.current_project:
            return
        
        # 다이얼로그로 노트 내용 입력
        dialog = QInputDialog()
        dialog.setInputMode(QInputDialog.TextInput)
        dialog.setWindowTitle("새 노트")
        dialog.setLabelText("노트 내용을 입력하세요:")
        dialog.setTextValue("")
        dialog.resize(400, 200)
        
        if dialog.exec() == QInputDialog.Accepted:
            content = dialog.textValue().strip()
            if content:
                note = Note(
                    project_id=self.current_project.id,
                    content=content
                )
                self.db.create_note(note)
                self.load_notes()
                QMessageBox.information(self, "성공", "노트가 추가되었습니다!")

    def edit_note(self, note: Note):
        """노트 편집"""
        dialog = QInputDialog()
        dialog.setInputMode(QInputDialog.TextInput)
        dialog.setWindowTitle("노트 편집")
        dialog.setLabelText("노트 내용을 수정하세요:")
        dialog.setTextValue(note.content)
        dialog.resize(400, 200)
        
        if dialog.exec() == QInputDialog.Accepted:
            new_content = dialog.textValue().strip()
            if new_content:
                note.content = new_content
                self.db.update_note(note)
                self.load_notes()
                QMessageBox.information(self, "성공", "노트가 수정되었습니다!")

    def delete_note(self, note: Note):
        """노트 삭제"""
        reply = QMessageBox.question(
            self, "삭제 확인", 
            f"정말로 이 노트를 삭제하시겠습니까?\n\n내용: {note.content[:50]}...",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.db.delete_note(note.id)
            self.load_notes()
            QMessageBox.information(self, "성공", "노트가 삭제되었습니다!")

    def on_task_updated(self):
        """할 일 업데이트 이벤트"""
        self.project_updated.emit() 