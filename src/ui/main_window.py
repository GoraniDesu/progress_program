"""
메인 윈도우 UI
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QSplitter, QLabel, QPushButton, QMessageBox,
    QListWidget, QListWidgetItem, QInputDialog,
    QTextEdit, QProgressBar, QTabWidget, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont
from database.database import Database
from database.models import Project
from utils.progress import ProgressCalculator
from utils.helpers import format_datetime, truncate_text, validate_project_title
from ui.project_widget import ProjectWidget


class MainWindow(QMainWindow):
    """메인 윈도우"""
    
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.current_project = None
        self.init_ui()
        self.load_projects()

    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle("Progress Program v1.0")
        self.setGeometry(100, 100, 1200, 800)
        
        # 중앙 위젯
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 메인 레이아웃
        main_layout = QHBoxLayout(central_widget)
        
        # 스플리터로 좌우 분할
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # 왼쪽 프로젝트 패널
        left_panel = self.create_project_panel()
        splitter.addWidget(left_panel)
        
        # 오른쪽 콘텐츠 패널
        self.right_panel = self.create_content_panel()
        splitter.addWidget(self.right_panel)
        
        # 스플리터 비율 설정 (30:70)
        splitter.setSizes([350, 850])
        
        # 스타일 적용
        self.apply_styles()

    def create_project_panel(self) -> QWidget:
        """프로젝트 패널 생성"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.StyledPanel)
        layout = QVBoxLayout(panel)
        
        # 제목
        title = QLabel("📋 프로젝트 목록")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(title)
        
        # 새 프로젝트 버튼
        self.new_project_btn = QPushButton("+ 새 프로젝트")
        self.new_project_btn.clicked.connect(self.create_new_project)
        layout.addWidget(self.new_project_btn)
        
        # 프로젝트 목록
        self.project_list = QListWidget()
        self.project_list.itemClicked.connect(self.on_project_selected)
        layout.addWidget(self.project_list)
        
        return panel

    def create_content_panel(self) -> QWidget:
        """콘텐츠 패널 생성"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.StyledPanel)
        layout = QVBoxLayout(panel)
        
        # 프로젝트 정보 영역
        self.project_info_widget = self.create_project_info_widget()
        layout.addWidget(self.project_info_widget)
        
        # 프로젝트 상세 위젯
        self.project_widget = ProjectWidget(self.db)
        self.project_widget.project_updated.connect(self.on_project_updated)
        layout.addWidget(self.project_widget)
        
        # 초기 상태 설정
        self.show_welcome_message()
        
        return panel

    def create_project_info_widget(self) -> QWidget:
        """프로젝트 정보 위젯 생성"""
        widget = QFrame()
        widget.setFrameStyle(QFrame.StyledPanel)
        widget.setMaximumHeight(100)
        layout = QVBoxLayout(widget)
        
        # 프로젝트 제목
        self.project_title_label = QLabel()
        self.project_title_label.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(self.project_title_label)
        
        # 진척도 바
        progress_layout = QHBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_label = QLabel("0%")
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.progress_label)
        layout.addLayout(progress_layout)
        
        return widget

    def apply_styles(self):
        """스타일 적용"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QFrame {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin: 2px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
                selection-background-color: #e3f2fd;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QProgressBar {
                border: 1px solid #ddd;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 4px;
            }
            QLabel {
                color: #333;
            }
        """)

    def load_projects(self):
        """프로젝트 목록 로드"""
        self.project_list.clear()
        projects = self.db.get_all_projects()
        
        for project in projects:
            # 진척도 계산
            tasks = self.db.get_tasks_by_project(project.id)
            progress = ProgressCalculator.calculate_progress(tasks)
            stats = ProgressCalculator.get_completion_stats(tasks)
            
            # 리스트 아이템 생성
            item_text = f"{project.title}\n📊 {progress:.0f}% ({stats['completed']}/{stats['total']})"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, project)
            self.project_list.addItem(item)

    def create_new_project(self):
        """새 프로젝트 생성"""
        title, ok = QInputDialog.getText(
            self, "새 프로젝트", "프로젝트 제목을 입력하세요:"
        )
        
        if ok and title:
            # 제목 검증
            is_valid, error_msg = validate_project_title(title)
            if not is_valid:
                QMessageBox.warning(self, "입력 오류", error_msg)
                return
            
            # 설명 입력
            description, ok = QInputDialog.getText(
                self, "새 프로젝트", "프로젝트 설명을 입력하세요 (선택사항):"
            )
            
            if not ok:
                description = ""
            
            # 프로젝트 생성
            project = Project(title=title.strip(), description=description.strip())
            project_id = self.db.create_project(project)
            project.id = project_id
            
            # 목록 새로고침 및 선택
            self.load_projects()
            self.select_project_by_id(project_id)
            
            QMessageBox.information(self, "성공", f"프로젝트 '{title}'가 생성되었습니다!")

    def on_project_selected(self, item: QListWidgetItem):
        """프로젝트 선택 이벤트"""
        project = item.data(Qt.UserRole)
        if project:
            self.current_project = project
            self.update_project_info()
            self.project_widget.set_project(project)

    def update_project_info(self):
        """프로젝트 정보 업데이트"""
        if not self.current_project:
            return
        
        # 최신 데이터 가져오기
        tasks = self.db.get_tasks_by_project(self.current_project.id)
        stats = ProgressCalculator.get_completion_stats(tasks)
        
        # UI 업데이트
        self.project_title_label.setText(f"📋 {self.current_project.title}")
        self.progress_bar.setValue(int(stats['progress']))
        self.progress_label.setText(f"{stats['progress']:.0f}%")
        
        # 진척도에 따른 색상 변경
        color = stats['progress_color']
        self.progress_bar.setStyleSheet(f"""
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 4px;
            }}
        """)

    def on_project_updated(self):
        """프로젝트 업데이트 이벤트"""
        self.load_projects()
        if self.current_project:
            self.update_project_info()

    def select_project_by_id(self, project_id: int):
        """ID로 프로젝트 선택"""
        for i in range(self.project_list.count()):
            item = self.project_list.item(i)
            project = item.data(Qt.UserRole)
            if project and project.id == project_id:
                self.project_list.setCurrentItem(item)
                self.on_project_selected(item)
                break

    def show_welcome_message(self):
        """환영 메시지 표시"""
        self.project_title_label.setText("Progress Program에 오신 것을 환영합니다! 🚀")
        self.progress_bar.setValue(0)
        self.progress_label.setText("프로젝트를 선택하거나 새로 만들어보세요!")
        self.project_widget.hide()

    def closeEvent(self, event):
        """프로그램 종료 시"""
        reply = QMessageBox.question(
            self, '확인', '프로그램을 종료하시겠습니까?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore() 