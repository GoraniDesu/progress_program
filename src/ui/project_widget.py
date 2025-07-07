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
from datetime import datetime


class ProjectWidget(QWidget):
    """프로젝트 상세 위젯"""
    
    project_updated = Signal()
    
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self.current_project = None
        self.last_saved_note_content = ""  # 마지막으로 저장된 노트 내용
        self.last_note_time = None  # 마지막 노트 저장 시간
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
        layout = QVBoxLayout()
        widget.setLayout(layout)

        button_layout = QHBoxLayout()
        
        self.add_note_btn = QPushButton("+ 노트 추가")
        self.add_note_btn.clicked.connect(self.add_note)
        button_layout.addWidget(self.add_note_btn)
        
        self.save_note_btn = QPushButton("💾 저장")
        self.save_note_btn.clicked.connect(self.save_note)
        button_layout.addWidget(self.save_note_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)

        self.note_text = QTextEdit()
        self.note_text.setPlaceholderText("""여기에 프로젝트 관련 메모를 작성하세요 ...

예시)
• 갑자기 떠오른 생각
• 기억해야 할 일
• 느낀점 등등""")
        layout.addWidget(self.note_text)
        self.note_text.setStyleSheet("font-size: 15px;")

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
        # 저장되지 않은 노트 내용이 있는지 확인
        if self.current_project and self.has_unsaved_notes():
            reply = QMessageBox.question(
                self,
                "저장되지 않은 노트",
                "저장되지 않은 노트 내용이 있습니다. 저장하시겠습니까?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
            )
            
            if reply == QMessageBox.Yes:
                self.save_note()
            elif reply == QMessageBox.Cancel:
                return
        
        self.current_project = project
        self.show()
        self.load_project_data()

    def has_unsaved_notes(self) -> bool:
        """저장되지 않은 노트가 있는지 확인"""
        current_content = self.note_text.toPlainText().strip()
        return current_content != self.last_saved_note_content

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
            # 타임스탬프가 포함된 노트인 경우에만 타임스탬프 표시
            if note.content.startswith("["):
                self.note_text.append(note.content + "\n")
            else:
                self.note_text.append(note.content + "\n")
        
        # 현재 표시된 내용을 마지막 저장 내용으로 설정
        self.last_saved_note_content = self.note_text.toPlainText().strip()

    def add_note(self):
        """노트 추가 (타임스탬프 포함)"""
        if not self.current_project:
            return
        
        text, ok = QInputDialog.getMultiLineText(
            self, "새 노트", "노트 내용을 입력하세요:"
        )
        
        if ok and text.strip():
            # 타임스탬프와 함께 노트 내용 생성
            timestamp = format_datetime(datetime.now(), "%Y-%m-%d %H:%M")
            content = f"[{timestamp}]\n{text.strip()}"
            
            # 노트 생성
            note = Note(
                project_id=self.current_project.id,
                content=content
            )
            self.db.create_note(note)
            
            # 노트 다시 로드
            self.load_notes()
            QMessageBox.information(self, "성공", "노트가 추가되었습니다!")

    def save_note(self):
        """일반 저장 (타임스탬프 없음)"""
        if not hasattr(self, 'current_project') or not self.current_project:
            QMessageBox.warning(self, "알림", "프로젝트를 먼저 선택해주세요.")
            return
        
        current_content = self.note_text.toPlainText().strip()
        if not current_content:
            # 내용이 비어있는 경우, 기존 노트들을 모두 삭제
            try:
                notes = self.db.get_notes_by_project(self.current_project.id)
                for note in notes:
                    self.db.delete_note(note.id)
                self.last_saved_note_content = ""
                QMessageBox.information(self, "성공", "모든 노트가 삭제되었습니다.")
                self.load_notes()
                return
            except Exception as e:
                QMessageBox.critical(self, "오류", f"노트 삭제 중 오류가 발생했습니다: {str(e)}")
                return
            
        # 마지막 저장 내용과 동일하면 저장하지 않음
        if current_content == self.last_saved_note_content:
            QMessageBox.information(self, "알림", "변경된 내용이 없습니다.")
            return
        
        try:
            # 기존 노트들을 모두 삭제
            notes = self.db.get_notes_by_project(self.current_project.id)
            for note in notes:
                self.db.delete_note(note.id)
            
            # 현재 내용을 새로운 노트로 저장
            note = Note(
                project_id=self.current_project.id,
                content=current_content,
                created_date=datetime.now()
            )
            self.db.create_note(note)
            
            self.last_saved_note_content = current_content
            QMessageBox.information(self, "성공", "노트가 저장되었습니다.")
            self.load_notes()
        except Exception as e:
            QMessageBox.critical(self, "오류", f"노트 저장 중 오류가 발생했습니다: {str(e)}")

    def extract_new_content(self, current_content: str) -> str:
        """현재 내용에서 새로운 내용만 추출"""
        return current_content  # 이제 이 메서드는 사용하지 않지만, 호환성을 위해 유지

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
        """할 일 업데이트 시그널 전달"""
        self.project_updated.emit()
    
    def edit_selected_task(self):
        """선택된 할 일 편집 (키보드 단축키용)"""
        if hasattr(self.task_widget, 'edit_selected_task'):
            self.task_widget.edit_selected_task()
    
    def delete_selected_task(self):
        """선택된 할 일 삭제 (키보드 단축키용)"""
        if hasattr(self.task_widget, 'delete_selected_task'):
            self.task_widget.delete_selected_task()
    
    def refresh(self):
        """데이터 새로고침 (키보드 단축키용)"""
        if self.current_project:
            self.load_project_data() 