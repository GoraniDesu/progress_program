"""
메인 윈도우 UI
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QSplitter, QLabel, QPushButton, QMessageBox,
    QListWidget, QListWidgetItem, QInputDialog,
    QTextEdit, QProgressBar, QTabWidget, QFrame,
    QMenuBar, QMenu, QApplication
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QAction, QShortcut, QKeySequence, QColor
from database.database import Database
from database.models import Project
from utils.progress import ProgressCalculator
from utils.helpers import format_datetime, truncate_text, validate_project_title
from utils.theme_manager import theme_manager
from utils.status_manager import status_manager
from utils.animation_manager import animation_manager
from utils.backup_manager import BackupManager
from ui.project_widget import ProjectWidget
from ui.backup_dialog import BackupDialog


class MainWindow(QMainWindow):
    """메인 윈도우"""
    
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.backup_manager = BackupManager(self.db.db_path)
        self.current_project = None
        self.init_ui()
        self.setup_theme()
        self.load_projects()

    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle("Progress Program v0.5")
        self.setGeometry(100, 100, 1200, 800)
        
        # 메뉴바 설정
        self.setup_menu_bar()
        
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
        
        # 초기 스타일 적용은 setup_theme에서 처리

    def create_project_panel(self) -> QWidget:
        """프로젝트 패널 생성"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.StyledPanel)
        layout = QVBoxLayout(panel)
        
        # 제목
        title = QLabel(" 📂 프로젝트 목록")
        title.setFont(QFont("맑은 고딕", 18, QFont.Bold))
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
        layout = QVBoxLayout(widget)
        
        # 프로젝트 제목
        self.project_title_label = QLabel()
        self.project_title_label.setFont(QFont("맑은 고딕", 22, QFont.Bold))
        self.project_title_label.setStyleSheet("padding-left: 6px; padding-top: 6px; padding-bottom: 6px;")
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

    def setup_menu_bar(self):
        """메뉴바 설정"""
        menubar = self.menuBar()
        
        # 파일 메뉴
        file_menu = menubar.addMenu("파일(&F)")
        
        # 새 프로젝트
        new_project_action = QAction("새 프로젝트(&N)", self)
        new_project_action.setShortcut(QKeySequence("Ctrl+N"))
        new_project_action.triggered.connect(self.create_new_project)
        file_menu.addAction(new_project_action)
        
        file_menu.addSeparator()
        
        # 새로고침
        refresh_action = QAction("새로고침(&R)", self)
        refresh_action.setShortcut(QKeySequence("F5"))
        refresh_action.triggered.connect(self.refresh_data)
        file_menu.addAction(refresh_action)
        
        file_menu.addSeparator()
        
        # 백업/복원
        backup_action = QAction("백업/복원 관리(&B)", self)
        backup_action.setShortcut(QKeySequence("Ctrl+B"))
        backup_action.triggered.connect(self.show_backup_dialog)
        file_menu.addAction(backup_action)
        
        # 보기 메뉴
        view_menu = menubar.addMenu("보기(&V)")
        
        # 테마 서브메뉴
        theme_menu = view_menu.addMenu("테마(&T)")
        
        # 라이트 테마
        light_action = QAction("라이트 모드(&L)", self)
        light_action.setCheckable(True)
        light_action.triggered.connect(lambda: self.change_theme('light'))
        theme_menu.addAction(light_action)
        
        # 다크 테마
        dark_action = QAction("다크 모드(&D)", self)
        dark_action.setCheckable(True)
        dark_action.triggered.connect(lambda: self.change_theme('dark'))
        theme_menu.addAction(dark_action)
        
        # 테마 액션 그룹으로 관리
        self.theme_actions = {'light': light_action, 'dark': dark_action}
        
        # 현재 테마에 체크 표시
        current_theme = theme_manager.get_current_theme()
        if current_theme in self.theme_actions:
            self.theme_actions[current_theme].setChecked(True)
        
        # 애니메이션 설정 서브메뉴
        animation_menu = view_menu.addMenu("애니메이션(&A)")
        
        # 애니메이션 활성화/비활성화
        animation_enabled_action = QAction("애니메이션 활성화(&E)", self)
        animation_enabled_action.setCheckable(True)
        animation_enabled_action.setChecked(theme_manager.get_animation_enabled())
        animation_enabled_action.triggered.connect(self.toggle_animation)
        animation_menu.addAction(animation_enabled_action)
        
        self.animation_enabled_action = animation_enabled_action
            
        # 추가 키보드 단축키 설정
        self.setup_shortcuts()
    
    def setup_shortcuts(self):
        """키보드 단축키 설정"""
        # Ctrl+E: 현재 선택된 항목 편집
        edit_shortcut = QShortcut(QKeySequence("Ctrl+E"), self)
        edit_shortcut.activated.connect(self.edit_current_item)
        
        # Del: 현재 선택된 항목 삭제
        delete_shortcut = QShortcut(QKeySequence("Delete"), self)
        delete_shortcut.activated.connect(self.delete_current_item)
    
    def edit_current_item(self):
        """현재 선택된 항목 편집"""
        if self.current_project and hasattr(self.project_widget, 'edit_selected_task'):
            self.project_widget.edit_selected_task()
    
    def delete_current_item(self):
        """현재 선택된 항목 삭제"""
        if self.current_project and hasattr(self.project_widget, 'delete_selected_task'):
            self.project_widget.delete_selected_task()
    
    def refresh_data(self):
        """데이터 새로고침"""
        self.load_projects()
        if self.current_project:
            self.update_project_info()
            if hasattr(self.project_widget, 'refresh'):
                self.project_widget.refresh()
        
        # 상태바에 새로고침 메시지 표시 (있다면)
        self.statusBar().showMessage("데이터를 새로고침했습니다.", 2000)
    
    def show_backup_dialog(self):
        """백업/복원 다이얼로그 표시"""
        dialog = BackupDialog(self.backup_manager, self)
        dialog.exec()
    
    def setup_theme(self):
        """테마 설정"""
        # 테마 변경 시그널 연결
        theme_manager.theme_changed.connect(self.on_theme_changed)
        
        # 애니메이션 설정 적용
        animation_manager.set_animation_enabled(theme_manager.get_animation_enabled())
        
        # 초기 테마 적용
        self.apply_theme(theme_manager.get_current_theme())
    
    def change_theme(self, theme_name: str):
        """테마 변경"""
        theme_manager.set_theme(theme_name)
    
    def toggle_animation(self):
        """애니메이션 활성화/비활성화 토글"""
        current_state = theme_manager.get_animation_enabled()
        theme_manager.set_animation_enabled(not current_state)
        self.animation_enabled_action.setChecked(not current_state)
    
    def on_theme_changed(self, theme_name: str):
        """테마 변경 이벤트 처리"""
        # 메뉴 체크 상태 업데이트
        for name, action in self.theme_actions.items():
            action.setChecked(name == theme_name)
        
        # 테마 적용
        self.apply_theme(theme_name)
    
    def apply_theme(self, theme_name: str):
        """테마 적용"""
        style_sheet = theme_manager.get_style_sheet(theme_name)
        self.setStyleSheet(style_sheet)
        # 전역 다이얼로그에도 적용
        QApplication.instance().setStyleSheet(style_sheet)
        
        # 자식 위젯들에도 테마 변경 알림
        if hasattr(self, 'project_widget'):
            self.project_widget.apply_theme(theme_name)

    def load_projects(self):
        """프로젝트 목록 로드"""
        self.project_list.clear()
        projects = self.db.get_all_projects()
        
        for project in projects:
            # 진척도 계산
            tasks = self.db.get_tasks_by_project(project.id)
            progress = ProgressCalculator.calculate_progress(tasks)
            stats = ProgressCalculator.get_completion_stats(tasks)
            
            # 프로젝트 상태 계산
            project_status_info = status_manager.get_project_status_summary(project, tasks)
            status_icon = project_status_info['icon']
            
            # 리스트 아이템 생성 - 상태 아이콘 추가
            status_text = f"{status_icon} " if status_icon else ""
            item_text = f"{status_text}{project.title}\n📊 {progress:.0f}% ({stats['completed']}/{stats['total']})"
            
            # 상태별 추가 정보
            if project_status_info['urgent_tasks'] > 0:
                item_text += f" | 🚨 급함: {project_status_info['urgent_tasks']}"
            if project_status_info['overdue_tasks'] > 0:
                item_text += f" | ⚠️ 초과: {project_status_info['overdue_tasks']}"
            
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, project)
            
            # 상태에 따른 색상 적용
            if project_status_info['status'] != 'normal':
                item.setForeground(QColor(project_status_info['color']))
            
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
        # 기존 유동 애니메이션 중지
        animation_manager.stop_all_animations()
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
        self.project_title_label.setText(f"⭐ {self.current_project.title} ⭐")
        
        # 진척도 바 애니메이션
        new_progress = int(stats['progress'])
        update_anim = animation_manager.animate_progress_update(self.progress_bar, new_progress)
        # Fluid 애니메이션 연결
        if update_anim:
            update_anim.finished.connect(lambda: animation_manager.animate_fluid_progress(self.progress_bar, new_progress))
        else:
            animation_manager.animate_fluid_progress(self.progress_bar, new_progress)
        self.progress_label.setText(f"{stats['progress']:.0f}%")
        
        # 진척도에 따른 색상 설정
        progress = stats['progress']
        if progress < 25:
            color = "#f44336"  # 빨강
        elif progress < 50:
            color = "#ff9800"  # 주황
        elif progress < 75:
            color = "#ffeb3b"  # 노랑
        else:
            color = "#4caf50"  # 초록
        
        # 현재 테마에 맞는 진척도 바 색상 설정
        current_theme = theme_manager.get_current_theme()
        if current_theme == 'dark':
            self.progress_bar.setStyleSheet(f"""
                QProgressBar::chunk {{
                    background-color: {color};
                    border-radius: 4px;
                }}
            """)
        else:
            self.progress_bar.setStyleSheet(f"""
                QProgressBar::chunk {{
                    background-color: {color};
                    border-radius: 4px;
                }}
            """)

    def on_project_updated(self):
        """프로젝트 업데이트 이벤트"""
        # 프로젝트 목록 새로고침
        self.load_projects()
        # 현재 프로젝트 정보 업데이트
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
        # 모든 애니메이션 정지
        animation_manager.stop_all_animations()
        self.project_title_label.setText("프로젝트를 선택하거나 새로 만들어보세요! 🚀")
        self.progress_bar.setValue(0)
        self.progress_label.setText("0%")

    def closeEvent(self, event):
        """윈도우 종료 이벤트"""
        try:
            # 데이터베이스 연결 정리
            if hasattr(self, 'db'):
                # Database 클래스에 cleanup 메서드가 있다면 호출
                pass
            event.accept()
        except Exception as e:
            print(f"종료 시 오류: {e}")
            event.accept() 