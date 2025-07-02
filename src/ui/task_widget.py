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
from database.database import Database
from database.models import Project, Task
from utils.helpers import format_datetime, validate_task_title
from datetime import datetime, timedelta
from utils.theme_manager import theme_manager
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
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # 액션
        
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
            checkbox.stateChanged.connect(lambda state, t=task: self.toggle_task_completion(t))
            checkbox_widget = QWidget()
            checkbox_layout = QHBoxLayout(checkbox_widget)
            checkbox_layout.addWidget(checkbox)
            checkbox_layout.setAlignment(Qt.AlignCenter)
            checkbox_layout.setContentsMargins(0, 0, 0, 0)
            self.task_table.setCellWidget(row, 1, checkbox_widget)
            
            # 할 일 제목
            title_item = QTableWidgetItem(task.title)
            title_item.setData(Qt.UserRole, task)
            if task.completed:
                title_item.setFlags(title_item.flags() & ~Qt.ItemIsEditable)
                title_item.setBackground(Qt.lightGray)
            self.task_table.setItem(row, 2, title_item)
            
            # 마감일
            due_date_text = ""
            if task.due_date:
                due_date_text = format_datetime(task.due_date, "%m/%d %H:%M")
                # 마감일이 지났는지 확인
                if task.due_date < datetime.now() and not task.completed:
                    due_date_text = f"⚠️ {due_date_text}"
                elif task.due_date < datetime.now() + timedelta(days=1) and not task.completed:
                    due_date_text = f"🔥 {due_date_text}"
            else:
                due_date_text = "-"
            
            due_date_item = QTableWidgetItem(due_date_text)
            due_date_item.setFlags(due_date_item.flags() & ~Qt.ItemIsEditable)
            if task.due_date and task.due_date < datetime.now() and not task.completed:
                # 마감일이 지난 경우 빨간색 배경
                due_date_item.setBackground(Qt.red)
                due_date_item.setForeground(Qt.white)
            elif task.due_date and task.due_date < datetime.now() + timedelta(days=1) and not task.completed:
                # 마감일이 임박한 경우 노란색 배경
                due_date_item.setBackground(Qt.yellow)
            self.task_table.setItem(row, 3, due_date_item)
            
            # 생성일
            date_item = QTableWidgetItem(format_datetime(task.created_date, "%m/%d %H:%M"))
            self.task_table.setItem(row, 4, date_item)
            
            # 액션 버튼들
            action_widget = self.create_task_action_widget(task)
            self.task_table.setCellWidget(row, 5, action_widget)

    def create_task_action_widget(self, task: Task) -> QWidget:
        """할 일 액션 위젯 생성"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(4, 4, 4, 4)
        
        # 마감일 설정 버튼
        due_date_btn = QPushButton("📅")
        due_date_btn.setToolTip("마감일 설정")
        due_date_btn.setMaximumSize(30, 30)
        due_date_btn.clicked.connect(lambda: self.set_due_date(task))
        layout.addWidget(due_date_btn)
        
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
            self.toggle_completed_btn.setText("👁️ 완료된 할 일 보이기")
        
        self.load_tasks()
    
    def start_inline_editing(self, item: QTableWidgetItem):
        """인라인 편집 시작"""
        # 할 일 제목 컬럼(인덱스 2)에서만 편집 허용
        if item.column() != 2:  # '할 일' 컬럼 인덱스
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

    def apply_theme(self, theme_name: str):
        """테마 적용"""
        style_sheet = theme_manager.get_style_sheet(theme_name)
        self.setStyleSheet(style_sheet)
    
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