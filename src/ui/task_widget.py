"""
할 일 관리 위젯
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QCheckBox, QInputDialog, QMessageBox, QLineEdit,
    QAbstractItemView, QDialog
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from database.database import Database
from database.models import Project, Task
from utils.helpers import format_datetime, validate_task_title
from datetime import datetime, timedelta
from utils.theme_manager import theme_manager
from utils.status_manager import status_manager
from utils.animation_manager import animation_manager
from ui.due_date_dialog import DueDateDialog


class TaskWidget(QWidget):
    """할 일 관리 위젯"""
    
    task_updated = Signal()
    
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self.current_project = None
        self.show_completed = True  # 완료된 할 일 표시 여부
        self.editing_item = None    # 현재 편집 중인 아이템
        self.init_ui()

    def init_ui(self):
        """UI 초기화"""
        layout = QVBoxLayout(self)
        
        # 버튼 영역
        button_layout = QHBoxLayout()
        
        self.add_task_btn = QPushButton("+ 할 일 추가")
        self.add_task_btn.clicked.connect(self.add_task)
        button_layout.addWidget(self.add_task_btn)
        
        # 완료된 할 일 표시/숨김 토글 버튼
        self.toggle_completed_btn = QPushButton("✅ 완료된 할 일 숨기기")
        self.toggle_completed_btn.clicked.connect(self.toggle_completed_tasks)
        button_layout.addWidget(self.toggle_completed_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # 할 일 테이블
        self.task_table = TaskTableWidget(self)
        
        # 컬럼 설정
        self.task_table.setColumnCount(6)
        self.task_table.setHorizontalHeaderLabels(["순서", "완료", "할 일", "마감일", "생성일", "액션"])
        
        # 드래그앤드롭 설정 (행 이동)
        self.task_table.setDragDropMode(QTableWidget.InternalMove)
        self.task_table.setDefaultDropAction(Qt.MoveAction)
        self.task_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.task_table.setDragEnabled(True)
        self.task_table.setAcceptDrops(True)
        self.task_table.setDropIndicatorShown(True)
        
        # 더블클릭 편집 설정
        self.task_table.itemDoubleClicked.connect(self.start_inline_editing)
        
        # 컬럼 너비 설정
        header = self.task_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # 순서
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # 완료
        header.setSectionResizeMode(2, QHeaderView.Stretch)          # 할 일
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # 마감일
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # 생성일
        header.setSectionResizeMode(5, QHeaderView.Fixed)            # 액션
        
        # 액션 컬럼 너비 (아이콘 + 텍스트 표시를 위해 확대)
        self.task_table.setColumnWidth(5, 200)
        
        # 테이블 행 높이 설정 (반응형 위젯에 맞춤)
        vertical_header = self.task_table.verticalHeader()
        vertical_header.setDefaultSectionSize(42)  # 반응형 위젯 높이에 맞춤
        vertical_header.setMinimumSectionSize(30)  # 최소 행 높이
        
        layout.addWidget(self.task_table)

    def set_project(self, project: Project):
        """프로젝트 설정"""
        self.current_project = project
        self.load_tasks()

    def load_tasks(self):
        """할 일 목록 로드"""
        if not self.current_project:
            return
        
        all_tasks = self.db.get_tasks_by_project(self.current_project.id)
        
        # 완료된 할 일 필터링
        tasks = all_tasks if self.show_completed else [t for t in all_tasks if not t.completed]
        
        # 데이터베이스에서 이미 order_index로 정렬되어 있음
        
        self.task_table.setRowCount(len(tasks))
        
        for row, task in enumerate(tasks):
            # 순서 표시
            order_item = QTableWidgetItem(str(task.order_index))
            order_item.setData(Qt.UserRole, task)
            order_item.setFlags(order_item.flags() & ~Qt.ItemIsEditable)
            self.task_table.setItem(row, 0, order_item)
            
            # 완료 체크박스
            checkbox = QCheckBox()
            checkbox.setChecked(task.completed)
            checkbox.stateChanged.connect(lambda state, t=task, cb=checkbox: self.toggle_task_completion(t, cb))
            checkbox_widget = QWidget()
            checkbox_layout = QHBoxLayout(checkbox_widget)
            checkbox_layout.addWidget(checkbox)
            checkbox_layout.setAlignment(Qt.AlignCenter)
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            self.task_table.setCellWidget(row, 1, checkbox_widget)
            
            # 할 일 제목 - 상태 표시 추가
            task_status_info = status_manager.get_task_status_summary(task)
            status_icon = task_status_info['icon']
            title_text = f"{status_icon} {task.title}" if status_icon else task.title
            
            title_item = QTableWidgetItem(title_text)
            title_item.setData(Qt.UserRole, task)
            
            # 상태에 따른 색상 적용
            if task_status_info['status'] != 'normal':
                title_item.setForeground(QColor(task_status_info['color']))
            
            if task.completed:
                title_item.setFlags(title_item.flags() & ~Qt.ItemIsEditable)
                title_item.setBackground(Qt.lightGray)
            self.task_table.setItem(row, 2, title_item)
            
            # 마감일 - 상태 기반 표시
            due_date_text = ""
            if task.due_date:
                due_date_text = format_datetime(task.due_date, "%m/%d %H:%M")
                
                # 상태에 따른 아이콘 추가
                if task_status_info['status'] == 'overdue':
                    due_date_text = f"⚠️ {due_date_text}"
                elif task_status_info['status'] == 'urgent':
                    due_date_text = f"🔥 {due_date_text}"
            else:
                due_date_text = "-"
            
            due_date_item = QTableWidgetItem(due_date_text)
            due_date_item.setFlags(due_date_item.flags() & ~Qt.ItemIsEditable)
            
            # 상태에 따른 배경색 적용
            if task_status_info['status'] == 'overdue':
                due_date_item.setBackground(QColor("#ff4757"))
                due_date_item.setForeground(QColor("#ffffff"))
            elif task_status_info['status'] == 'urgent':
                due_date_item.setBackground(QColor("#ff6b6b"))
                due_date_item.setForeground(QColor("#ffffff"))
            elif task_status_info['status'] == 'completed':
                due_date_item.setBackground(QColor("#2ed573"))
                due_date_item.setForeground(QColor("#ffffff"))
            
            self.task_table.setItem(row, 3, due_date_item)
            
            # 생성일
            date_item = QTableWidgetItem(format_datetime(task.created_date, "%m/%d %H:%M"))
            self.task_table.setItem(row, 4, date_item)
            
            # 액션 버튼들 (완벽한 수직 중앙 정렬을 위한 wrapper 적용)
            action_widget = self.create_task_action_widget(task)
            
            # 수직 중앙 정렬을 강제하는 wrapper 위젯
            wrapper = QWidget()
            wrapper_layout = QVBoxLayout(wrapper)
            wrapper_layout.setContentsMargins(0, 0, 0, 0)
            wrapper_layout.setSpacing(0)
            wrapper_layout.addStretch()  # 위쪽 여백
            wrapper_layout.addWidget(action_widget)
            wrapper_layout.addStretch()  # 아래쪽 여백
            
            self.task_table.setCellWidget(row, 5, wrapper)

    def create_task_action_widget(self, task: Task) -> QWidget:
        """할 일 액션 위젯 생성 (wrapper와 함께 완벽한 중앙 정렬)"""
        from PySide6.QtWidgets import QSizePolicy
        
        # 액션 버튼들을 담는 위젯 (wrapper에 의해 중앙 정렬됨)
        widget = QWidget()
        widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        widget.setFixedHeight(20)  # 적절한 버튼 높이
        
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 1, 5, 1)  # 좌우 여백, 최소 상하 여백
        layout.setSpacing(3)  # 버튼 간격
        layout.setAlignment(Qt.AlignCenter)
        
        # 현재 테마 확인
        current_theme = theme_manager.get_current_theme()
        
        # 반응형 버튼 스타일 (전문가 권장: 호버 효과 개선)
        if current_theme == 'dark':
            button_style = """
                QPushButton {
                    font-family: 'Segoe UI', '맑은 고딕';
                    font-size: 12px;
                    font-weight: normal;
                    border: 1px solid #666;
                    border-radius: 3px;
                    background-color: #4a4a4a;
                    color: #ffffff;
                    text-align: center;
                    padding: 2px 4px;
                }
                QPushButton:hover {
                    background-color: #5a5a5a;
                    border-color: #777;
                }
                QPushButton:pressed {
                    background-color: #3a3a3a;
                }
            """
            delete_button_style = """
                QPushButton {
                    font-family: 'Segoe UI', '맑은 고딕';
                    font-size: 12px;
                    font-weight: normal;
                    border: 1px solid #666;
                    border-radius: 3px;
                    background-color: #4a4a4a;
                    color: #ffffff;
                    text-align: center;
                    padding: 2px 4px;
                }
                QPushButton:hover {
                    background-color: #664444;
                    border-color: #777;
                }
                QPushButton:pressed {
                    background-color: #553333;
                }
            """
        else:
            # 라이트 테마: 밝은 색상으로 일관성 유지
            button_style = """
                QPushButton {
                    font-family: 'Segoe UI', '맑은 고딕';
                    font-size: 12px;
                    font-weight: normal;
                    border: 1px solid #d0d0d0;
                    border-radius: 3px;
                    background-color: #ffffff;
                    color: #333333;
                    text-align: center;
                    padding: 2px 4px;
                }
                QPushButton:hover {
                    background-color: #f0f8ff;
                    border-color: #0078d4;
                    color: #0078d4;
                }
                QPushButton:pressed {
                    background-color: #e6f3ff;
                    border-color: #106ebe;
                    color: #106ebe;
                }
            """
            delete_button_style = """
                QPushButton {
                    font-family: 'Segoe UI', '맑은 고딕';
                    font-size: 12px;
                    font-weight: normal;
                    border: 1px solid #d0d0d0;
                    border-radius: 3px;
                    background-color: #ffffff;
                    color: #333333;
                    text-align: center;
                    padding: 2px 4px;
                }
                QPushButton:hover {
                    background-color: #fff5f5;
                    border-color: #dc3545;
                    color: #dc3545;
                }
                QPushButton:pressed {
                    background-color: #ffe6e6;
                    border-color: #c82333;
                    color: #c82333;
                }
            """
        
        # 버튼 생성 (전문가 권장: 아이콘 + 텍스트 조합으로 직관성 향상)
        buttons_data = [
            ("📅 날짜", lambda: self.set_due_date(task), button_style, "마감일 설정/수정"),
            ("✏️ 편집", lambda: self.edit_task(task), button_style, "할 일 편집"),
            ("🗑️ 삭제", lambda: self.delete_task(task), delete_button_style, "할 일 삭제")
        ]
        
        for text, handler, style, tooltip in buttons_data:
            btn = QPushButton(text)
            btn.setToolTip(tooltip)
            
            # 🔥 핵심 수정: 반응형 크기 정책 적용
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setMaximumHeight(18)  # wrapper 높이에 맞춤
            btn.setMinimumHeight(16)
            btn.setMinimumWidth(28)  # 최소 너비
            
            btn.setStyleSheet(style)
            btn.clicked.connect(handler)
            layout.addWidget(btn)
        
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
    
    def set_due_date(self, task: Task):
        """마감일 설정"""
        dialog = DueDateDialog(task.due_date, self)
        if dialog.exec() == QDialog.Accepted:
            task.due_date = dialog.get_due_date()
            self.db.update_task(task)
            self.load_tasks()
            self.task_updated.emit()
            
            if task.due_date:
                due_date_str = format_datetime(task.due_date, "%Y-%m-%d %H:%M")
                QMessageBox.information(self, "성공", f"마감일이 설정되었습니다.\n{due_date_str}")
            else:
                QMessageBox.information(self, "성공", "마감일이 제거되었습니다.")
    
    def toggle_completed_tasks(self):
        """완료된 할 일 표시/숨김 토글"""
        self.show_completed = not self.show_completed
        
        if self.show_completed:
            self.toggle_completed_btn.setText("✅ 완료된 할 일 숨기기")
        else:
            self.toggle_completed_btn.setText("🔍 완료된 할 일 보이기")
        
        self.load_tasks()
    
    def start_inline_editing(self, item: QTableWidgetItem):
        """인라인 편집 시작"""
        column = item.column()
        
        # 마감일 컬럼(인덱스 3) 더블클릭 시 마감일 다이얼로그 호출
        if column == 3:  # '마감일' 컬럼 인덱스
            # Task 객체 찾기 (순서 컬럼에서 가져오기)
            row = item.row()
            order_item = self.task_table.item(row, 0)
            if order_item:
                task = order_item.data(Qt.UserRole)
                if task:
                    self.set_due_date(task)
            return
        
        # 할 일 제목 컬럼(인덱스 2)에서만 텍스트 편집 허용
        if column != 2:  # '할 일' 컬럼 인덱스
            return
        
        # 완료된 할 일은 편집 불가
        task = item.data(Qt.UserRole)
        if task and task.completed:
            return
        
        # 이미 편집 중인 경우 무시
        if self.editing_item is not None:
            return
        
        self.editing_item = item
        row = item.row()
        
        # 라인 에디트 생성
        line_edit = QLineEdit()
        line_edit.setText(item.text())
        line_edit.selectAll()
        
        # 이벤트 연결
        line_edit.editingFinished.connect(lambda: self.finish_inline_editing(line_edit, item))
        line_edit.returnPressed.connect(lambda: self.finish_inline_editing(line_edit, item))
        
        # 테이블에 위젯 설정
        self.task_table.setCellWidget(row, 2, line_edit)
        line_edit.setFocus()
    
    def finish_inline_editing(self, line_edit: QLineEdit, item: QTableWidgetItem):
        """인라인 편집 완료"""
        if self.editing_item is None:
            return
        
        new_title = line_edit.text().strip()
        task = item.data(Qt.UserRole)
        
        if new_title and task:
            # 제목 검증
            is_valid, error_msg = validate_task_title(new_title)
            if is_valid:
                # 할 일 업데이트
                task.title = new_title
                self.db.update_task(task)
                item.setText(new_title)
                self.task_updated.emit()
            else:
                QMessageBox.warning(self, "입력 오류", error_msg)
        
        # 위젯 제거 및 편집 상태 초기화
        row = item.row()
        self.task_table.removeCellWidget(row, 2)
        self.editing_item = None
        
        # 목록 새로고침
        self.load_tasks()
    
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

    def toggle_task_completion(self, task: Task, checkbox: QCheckBox):
        """할 일 완료 상태 토글"""
        # 체크박스 애니메이션 실행
        animation_manager.animate_task_completion(checkbox)
        
        # 완료 상태 변경
        task.completed = not task.completed
        if task.completed:
            task.completed_date = datetime.now()
        else:
            task.completed_date = None
        
        self.db.update_task(task)
        self.load_tasks()
        self.task_updated.emit()

    def apply_theme(self, theme_name: str):
        """테마 적용"""
        style_sheet = theme_manager.get_style_sheet(theme_name)
        self.setStyleSheet(style_sheet)
        # 테마 변경 시 액션 버튼들도 새로 적용되도록 할 일 목록 재로드
        if self.current_project:
            self.load_tasks()
    
    def edit_selected_task(self):
        """선택된 할 일 편집 (키보드 단축키용)"""
        current_row = self.task_table.currentRow()
        if current_row >= 0:
            # 순서 컬럼(0)에서 Task 객체 가져오기
            order_item = self.task_table.item(current_row, 0)
            if order_item:
                task = order_item.data(Qt.UserRole)
                if task:
                    self.edit_task(task)
    
    def delete_selected_task(self):
        """선택된 할 일 삭제 (키보드 단축키용)"""
        current_row = self.task_table.currentRow()
        if current_row >= 0:
            # 순서 컬럼(0)에서 Task 객체 가져오기
            order_item = self.task_table.item(current_row, 0)
            if order_item:
                task = order_item.data(Qt.UserRole)
                if task:
                    self.delete_task(task)

    # ------------------------------------------------------------------
    # Drag & Drop 행 이동 처리 (TaskTableWidget에서 호출)
    # ------------------------------------------------------------------

    def reorder_tasks(self, source_row: int, target_row: int):
        """source_row 를 target_row 위치로 이동하고 DB/테이블 동기화"""

        if not self.current_project:
            return

        # 현재 화면에 표시된 Task 객체 순서를 확보
        tasks_on_screen: list[Task] = []
        for r in range(self.task_table.rowCount()):
            item = self.task_table.item(r, 0)
            if item:
                tasks_on_screen.append(item.data(Qt.UserRole))

        # pop & insert
        moved_task = tasks_on_screen.pop(source_row)
        tasks_on_screen.insert(target_row, moved_task)

        # order_index 재계산 및 DB 업데이트 목록 작성
        updated_orders: list[tuple[int, int]] = []
        for idx, task in enumerate(tasks_on_screen):
            new_order = idx + 1  # 1부터 시작
            if task.order_index != new_order:
                task.order_index = new_order
                updated_orders.append((task.id, new_order))

        if updated_orders:
            self.db.update_task_orders(self.current_project.id, updated_orders)

        # 캐시된 셀 위젯 제거 후 재로드 (행 사라짐 방지)
        self.task_table.clearContents()

        # 테이블 재로드 (UI 위젯/시그널 일관성 보장)
        self.load_tasks()
        self.task_updated.emit()

# 내부 테이블 위젯 서브클래스 (드래그 앤드 드롭 순서를 처리하기 위함)
class TaskTableWidget(QTableWidget):
    def __init__(self, parent_widget):
        super().__init__(parent_widget)
        self.parent_widget = parent_widget

    def dropEvent(self, event):
        """행 단위 드래그 이동 처리

        Qt 기본 drop 처리는 셀 단위로 위젯까지 이동시키므로
        체크박스 / 버튼 등이 엇갈리는 문제가 발생한다.
        따라서 기본 처리(super().dropEvent)를 **막고**,
        대상 행 인덱스만 계산한 뒤 부모(TaskWidget)에
        '행 이동' 정보를 전달해 테이블을 **완전 재생성**하도록 한다.
        """

        if not self.parent_widget or not self.parent_widget.current_project:
            event.ignore()
            return

        source_row = self.currentRow()
        # Qt 6: QDropEvent.position() → QPointF
        target_row = self.rowAt(int(event.position().y()))

        # 행 아래 빈 공간에 드롭한 경우 → 마지막 행으로 간주
        if target_row < 0:
            target_row = self.rowCount() - 1

        if source_row == target_row or source_row < 0:
            event.ignore()
            return

        # 부모 위젯에 순서 변경 요청 (DB 갱신 + 테이블 재로드)
        self.parent_widget.reorder_tasks(source_row, target_row)

        event.acceptProposedAction() 