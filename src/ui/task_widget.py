"""
할 일 관리 위젯
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QCheckBox, QInputDialog, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from database.database import Database
from database.models import Project, Task
from utils.helpers import format_datetime, validate_task_title
from datetime import datetime


class TaskWidget(QWidget):
    """할 일 관리 위젯"""
    
    task_updated = Signal()
    
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self.current_project = None
        self.init_ui()

    def init_ui(self):
        """UI 초기화"""
        layout = QVBoxLayout(self)
        
        # 버튼 영역
        button_layout = QHBoxLayout()
        
        self.add_task_btn = QPushButton("+ 할 일 추가")
        self.add_task_btn.clicked.connect(self.add_task)
        button_layout.addWidget(self.add_task_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # 할 일 테이블
        self.task_table = QTableWidget()
        self.task_table.setColumnCount(4)
        self.task_table.setHorizontalHeaderLabels(["완료", "할 일", "생성일", "액션"])
        
        # 컬럼 너비 설정
        header = self.task_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        
        layout.addWidget(self.task_table)

    def set_project(self, project: Project):
        """프로젝트 설정"""
        self.current_project = project
        self.load_tasks()

    def load_tasks(self):
        """할 일 목록 로드"""
        if not self.current_project:
            return
        
        tasks = self.db.get_tasks_by_project(self.current_project.id)
        
        self.task_table.setRowCount(len(tasks))
        
        for row, task in enumerate(tasks):
            # 완료 체크박스
            checkbox = QCheckBox()
            checkbox.setChecked(task.completed)
            checkbox.stateChanged.connect(lambda state, t=task: self.toggle_task_completion(t))
            checkbox_widget = QWidget()
            checkbox_layout = QHBoxLayout(checkbox_widget)
            checkbox_layout.addWidget(checkbox)
            checkbox_layout.setAlignment(Qt.AlignCenter)
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            self.task_table.setCellWidget(row, 0, checkbox_widget)
            
            # 할 일 제목
            title_item = QTableWidgetItem(task.title)
            title_item.setData(Qt.UserRole, task)
            if task.completed:
                title_item.setFlags(title_item.flags() & ~Qt.ItemIsEditable)
                # 완료된 항목 스타일
                title_item.setBackground(Qt.lightGray)
            self.task_table.setItem(row, 1, title_item)
            
            # 생성일
            date_item = QTableWidgetItem(format_datetime(task.created_date, "%m/%d %H:%M"))
            self.task_table.setItem(row, 2, date_item)
            
            # 액션 버튼들
            action_widget = self.create_task_action_widget(task)
            self.task_table.setCellWidget(row, 3, action_widget)

    def create_task_action_widget(self, task: Task) -> QWidget:
        """할 일 액션 위젯 생성"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(4, 4, 4, 4)
        
        # 편집 버튼
        edit_btn = QPushButton("✏️")
        edit_btn.setToolTip("편집")
        edit_btn.setMaximumSize(30, 30)
        edit_btn.clicked.connect(lambda: self.edit_task(task))
        layout.addWidget(edit_btn)
        
        # 삭제 버튼
        delete_btn = QPushButton("🗑️")
        delete_btn.setToolTip("삭제")
        delete_btn.setMaximumSize(30, 30)
        delete_btn.clicked.connect(lambda: self.delete_task(task))
        layout.addWidget(delete_btn)
        
        return widget

    def add_task(self):
        """할 일 추가"""
        if not self.current_project:
            return
        
        title, ok = QInputDialog.getText(
            self, "새 할 일", "할 일을 입력하세요:"
        )
        
        if ok and title:
            # 제목 검증
            is_valid, error_msg = validate_task_title(title)
            if not is_valid:
                QMessageBox.warning(self, "입력 오류", error_msg)
                return
            
            # 할 일 생성
            task = Task(
                project_id=self.current_project.id,
                title=title.strip()
            )
            self.db.create_task(task)
            self.load_tasks()
            self.task_updated.emit()
            QMessageBox.information(self, "성공", "할 일이 추가되었습니다!")

    def edit_task(self, task: Task):
        """할 일 편집"""
        title, ok = QInputDialog.getText(
            self, "할 일 편집", "할 일을 수정하세요:", text=task.title
        )
        
        if ok and title:
            # 제목 검증
            is_valid, error_msg = validate_task_title(title)
            if not is_valid:
                QMessageBox.warning(self, "입력 오류", error_msg)
                return
            
            task.title = title.strip()
            self.db.update_task(task)
            self.load_tasks()
            self.task_updated.emit()
            QMessageBox.information(self, "성공", "할 일이 수정되었습니다!")

    def delete_task(self, task: Task):
        """할 일 삭제"""
        reply = QMessageBox.question(
            self, "삭제 확인", 
            f"정말로 '{task.title}' 할 일을 삭제하시겠습니까?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.db.delete_task(task.id)
            self.load_tasks()
            self.task_updated.emit()
            QMessageBox.information(self, "성공", "할 일이 삭제되었습니다!")

    def toggle_task_completion(self, task: Task):
        """할 일 완료 상태 토글"""
        # 완료 상태 변경
        task.completed = not task.completed
        if task.completed:
            task.completed_date = datetime.now()
        else:
            task.completed_date = None
        
        self.db.update_task(task)
        self.load_tasks()
        self.task_updated.emit() 