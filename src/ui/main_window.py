"""
메인 윈도우 UI
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QSplitter, QLabel, QPushButton, QMessageBox,
    QListWidget, QListWidgetItem, QInputDialog,
    QTextEdit, QProgressBar, QTabWidget, QFrame,
    QMenuBar, QMenu, QApplication, QGraphicsOpacityEffect
)
from PySide6.QtCore import Qt, Signal, QTimer, QRect, QEvent, QPropertyAnimation, QEasingCurve, QPoint
from PySide6.QtGui import QFont, QAction, QShortcut, QKeySequence, QColor, QFontMetrics, QPainter, QPen
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
from ui.flow_progress_bar import FlowProgressBar
from utils.celebration_manager import CelebrationManager
import random  # 랜덤 축하 메시지에 사용


class MainWindow(QMainWindow):
    """메인 윈도우"""
    
    # 100% 달성 축하 아이콘/문구 리스트
    CELEBRATION_ICONS = ["| 🤩", "| 🥳", "| 🎉", "| 👍"]
    CELEBRATION_MESSAGES = [
        "완벽 실행‼",
        "성공적 마무리‼",
        "100% 달성‼",
        "최고의 결과‼"
    ]
    
    # 완료 도장 문구 리스트 (공백/개행 동일 규칙 적용)
    STAMP_TEXTS = [
        "대 박 \n 사 건",
        "내 가 \n 해 냄",
        "이 걸 \n 해 냄",
        "이 게 \n 되 네",
        "해 치 \n 웠 다"
    ]
    
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.backup_manager = BackupManager(self.db.db_path)
        self.current_project = None
        # 축하 효과 실행 중 여부는 CelebrationManager 자체에서 관리
        self.init_ui()
        self.setup_theme()
        # 축하 매니저 초기화(테마·애니메이션 매니저 공유)
        self.celebration_manager = CelebrationManager(self, theme_manager, animation_manager)
        self.load_projects()

        # 설명 라벨 테마 변경 시 동기화
        theme_manager.theme_changed.connect(lambda *_: self.apply_theme_to_desc())
        self.apply_theme_to_desc()

        # 100% 도장 지연 표시 타이머 보관용
        self.stamp_timer: QTimer | None = None
        self._stamp_project_id: int | None = None  # 현재 화면에 표시된 도장 대상 프로젝트 id
        self._project_stamp_texts: dict[int, str] = {}  # 프로젝트별 선택된 도장 문구 캐시
        self._previous_project_progress: dict[int, int] = {} # 프로젝트별 이전 진척도 저장

        # 프로젝트별 첫 도장 표시 여부 추적
        self._stamp_first_shown: set[int] = set()
        
        # 도장 페이드 아웃 애니메이션 보관용
        self._stamp_fade_anim: QPropertyAnimation | None = None

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
        self.project_list.currentItemChanged.connect(lambda _new, _old: self.on_project_selected(self.project_list.currentItem()))
        self.project_list.setMinimumWidth(250)  # 최소 너비 설정
        self.project_list.setWordWrap(True)  # 긴 텍스트 자동 줄바꿈
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
        
        # 프로젝트 설명
        self.project_desc_label = QLabel()
        self.project_desc_label.setObjectName("projectDescription")
        self.project_desc_label.setAccessibleName("프로젝트 설명")
        self.project_desc_label.setWordWrap(True)
        self.project_desc_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        # 기본 스타일(컬러는 테마에 따라 apply_theme_to_desc 에서 동적으로 설정)
        self.project_desc_label.setStyleSheet("font-size: 14px; line-height: 1.4em; padding-left: 20px;")
        layout.addWidget(self.project_desc_label)
        # 처음에는 숨김 (환영 화면 대비)
        self.project_desc_label.hide()
        
        # 진척도 바
        progress_layout = QHBoxLayout()
        self.progress_bar = FlowProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_label = QLabel("0%")
        progress_layout.addWidget(self.progress_bar)
        progress_layout.addWidget(self.progress_label)
        layout.addLayout(progress_layout)
        
        # 완료 도장 (우상단 코너, 절대 위치)
        self.completion_stamp = StampWidget("내 가 \n 해 냄 ", self, circle=True, angle=-15)
        self.completion_stamp.hide()
        # 메인 윈도우 리사이즈에 대응해 재배치
        self.installEventFilter(self.completion_stamp)
        
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
            
            # 전체 제목 표시
            item_text = f"{status_icon} {project.title}\n📊 {progress:.0f}% ({stats['completed']}/{stats['total']})"
            
            # 완료(100%) 시 축하 메시지 추가
            if progress >= 100:  # 100% 달성
                random_icon = random.choice(self.CELEBRATION_ICONS)
                random_msg = random.choice(self.CELEBRATION_MESSAGES)
                item_text += f" {random_icon} {random_msg}"
            
            # 상태별 추가 정보
            if project_status_info['urgent_tasks'] > 0:
                item_text += f" | 🚨 급함: {project_status_info['urgent_tasks']}"
            if project_status_info['overdue_tasks'] > 0:
                item_text += f" | ⚠️ 초과: {project_status_info['overdue_tasks']}"
            
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, project)
            
            # 설명을 툴팁으로 제공
            item.setToolTip(project.description or "")
            
            # 상태에 따른 색상 적용
            if project_status_info['status'] != 'normal':
                item.setForeground(QColor(project_status_info['color']))
            
            self.project_list.addItem(item)

        # load_projects 종료

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
        # 다른 프로젝트로 전환 시 모든 애니메이션·축하 효과 중지
        animation_manager.stop_all_animations()
        if hasattr(self, 'celebration_manager'):
            self.celebration_manager.stop()

        # 기존 도장·타이머 정리 (프로젝트 변경 시 반드시 숨김 처리)
        self.hide_completion_stamp()

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
        
        # 설명 라벨 업데이트 (없으면 '(설명 없음)')
        desc_text = (self.current_project.description or "").strip()
        if desc_text:
            self.project_desc_label.setText(desc_text)
            self.project_desc_label.show()
        else:
            self.project_desc_label.hide()
        
        # 진척도 바 애니메이션 (값 동일해도 valueChanged 유도)
        new_progress = int(stats['progress'])
        # 이전 진척도 가져오기 (없으면 0)
        old_progress = self._previous_project_progress.get(self.current_project.id, 0)
        # 현재 진척도 저장
        self._previous_project_progress[self.current_project.id] = new_progress
        
        if self.progress_bar.value() == new_progress:
            # 값이 동일하면 즉시 설정만 하고 애니메이션은 생략
            self.progress_bar.setValue(new_progress)
        else:
            animation_manager.animate_progress_update(self.progress_bar, new_progress)
        self.progress_label.setText(f"{stats['progress']:.0f}%")
        
        # 100 % 달성 시 축하 애니메이션 및 도장 표시(2초 지연)
        if new_progress == 100:
            # CelebrationManager가 이미 실행 중이면 start() 내부에서 무시
            self.celebration_manager.start(self.progress_bar)

            # 같은 프로젝트의 도장이 이미 표시 중이면 아무 것도 하지 않음
            same_stamp_visible = (
                self.completion_stamp.isVisible() and self._stamp_project_id == self.current_project.id
            )

            if not same_stamp_visible:
                # 프로젝트별 첫 표시라면 2초 지연 → 즉시 표시 / 두 번째 이후
                is_first_time = self.current_project.id not in self._stamp_first_shown

                if is_first_time:
                    self.stamp_timer = QTimer(self)
                    self.stamp_timer.setSingleShot(True)

                    current_project_id = self.current_project.id if self.current_project else None

                    def _timeout():
                        # 프로젝트가 변경되지 않았는지 확인
                        if self.current_project and self.current_project.id == current_project_id:
                            self.show_completion_stamp()
                            self._stamp_project_id = self.current_project.id

                    self.stamp_timer.timeout.connect(_timeout)
                    self.stamp_timer.start(2000)
                else:
                    # 즉시 표시
                    self.show_completion_stamp()
                    self._stamp_project_id = self.current_project.id
        else:
            # 100%가 아니면 즉시 도장 숨김
            self.hide_completion_stamp()
            if self.stamp_timer and self.stamp_timer.isActive():
                self.stamp_timer.stop()
            self._stamp_project_id = None
        
        # 레이아웃 변화(설명 라벨 show/hide 등) 후 도장이 이미 표시중이라면 위치 재계산
        if self.completion_stamp.isVisible():
            QTimer.singleShot(0, lambda: self.completion_stamp.reposition(self))
        
        # 진척도에 따른 색상 설정
        progress = stats['progress']
        if new_progress == 100:
            # 축하 모드에서는 골드 스타일이 적용되어 있으므로 색상 설정 건너뜀
            return
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

    def show_completion_stamp(self):
        """완료 도장 표시 및 위치 조정"""
        # 프로젝트별로 한 번 선택된 문구를 기억
        project_id = self.current_project.id if self.current_project else None
        if project_id is None:
            return  # 예외적 상황 - 프로젝트가 없으면 표시하지 않음

        if project_id not in self._project_stamp_texts:
            # 아직 문구가 정해지지 않았다면 랜덤 선택 후 저장
            self._project_stamp_texts[project_id] = random.choice(self.STAMP_TEXTS)

        # 캐시된 문구 적용
        self.completion_stamp.set_text(self._project_stamp_texts[project_id])

        # 먼저 정확한 위치로 이동시킨 후 보이도록 합니다.
        self.completion_stamp.reposition(self, instant=True)
        self.completion_stamp.show()
        self.completion_stamp.raise_()
        self._stamp_project_id = self.current_project.id

        # 첫 표시 여부 기록
        self._stamp_first_shown.add(self._stamp_project_id)

        # 기존 페이드 애니메이션이 진행 중이면 중단 및 초기화
        if self._stamp_fade_anim and self._stamp_fade_anim.state() == QPropertyAnimation.Running:
            self._stamp_fade_anim.stop()
            self.completion_stamp.setGraphicsEffect(None)

        # 6초 뒤 페이드아웃 시작 스케줄링
        QTimer.singleShot(6000, lambda pid=self._stamp_project_id: self._start_stamp_fade_out(pid))

    def hide_completion_stamp(self):
        """완료 도장 숨기기"""
        if self._stamp_fade_anim and self._stamp_fade_anim.state() == QPropertyAnimation.Running:
            self._stamp_fade_anim.stop()
            self._stamp_fade_anim = None
            self.completion_stamp.setGraphicsEffect(None)
        # 예약된 타이머가 있으면 취소
        if self.stamp_timer and self.stamp_timer.isActive():
            self.stamp_timer.stop()
        # 내부 상태 초기화
        self._stamp_project_id = None
        self.completion_stamp.hide()

    def on_project_updated(self):
        """프로젝트 업데이트 이벤트"""
        if self.current_project:
            current_project_id = self.current_project.id
            # 프로젝트 목록 새로고침
            self.load_projects()
            # 현재 프로젝트 선택 상태 복원
            self.select_project_by_id(current_project_id)
        else:
            # 선택된 프로젝트가 없는 경우 단순 새로고침
            self.load_projects()

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
        self.project_desc_label.clear()
        self.project_desc_label.hide()
        # 완료 도장도 숨김
        self.completion_stamp.hide()

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

    # ------------------------------------------------------------------
    # 프로젝트 설명 라벨 테마 적용
    # ------------------------------------------------------------------

    def apply_theme_to_desc(self):
        """테마 변경에 따라 설명 라벨 색상 조정"""
        current_theme = theme_manager.get_current_theme()
        if current_theme == 'dark':
            color = "#B0B0B0"
        else:
            color = "#636363"
        # 왼쪽 패딩 포함 스타일 업데이트
        self.project_desc_label.setStyleSheet(
            f"color: {color}; font-size: 14px; line-height: 1.4em; padding-left: 20px;"
        ) 

    # ------------------------------------------------------------------
    # 도장 페이드 아웃 애니메이션
    # ------------------------------------------------------------------
    def _start_stamp_fade_out(self, project_id: int | None):
        """현재 도장이 여전히 같은 프로젝트에 대해 표시된 경우 투명도 애니메이션으로 서서히 사라지게 한다."""
        if project_id is None or project_id != self._stamp_project_id:
            return  # 다른 프로젝트로 변경되었음
        if not self.completion_stamp.isVisible():
            return

        # 투명도 효과 준비
        effect = QGraphicsOpacityEffect(self.completion_stamp)
        effect.setOpacity(1.0)
        self.completion_stamp.setGraphicsEffect(effect)

        self._stamp_fade_anim = QPropertyAnimation(effect, b"opacity", self)
        self._stamp_fade_anim.setDuration(3000)  # 3초 동안 서서히 사라짐
        self._stamp_fade_anim.setStartValue(1.0)
        self._stamp_fade_anim.setEndValue(0.0)
        self._stamp_fade_anim.setEasingCurve(QEasingCurve.OutCubic)

        def _on_finished():
            self.completion_stamp.hide()
            self.completion_stamp.setGraphicsEffect(None)
            self._stamp_fade_anim = None

        self._stamp_fade_anim.finished.connect(_on_finished)
        self._stamp_fade_anim.start()

class StampWidget(QWidget):
    """회전/사각·원형 도장 위젯"""
    def __init__(self, text: str = "내가해냄", parent: QWidget | None = None, *, circle: bool = False, angle: int = -45):
        super().__init__(parent)
        self.text = text
        self.circle = circle  # True -> 원형, False -> 사각형
        self.angle = angle    # 회전 각도
        self.font = QFont("영양군 음식디미방", 35, QFont.Bold)
        # 투명 배경 설정
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        # 마우스 이벤트 투명화(클릭 통과)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.update_size()
        self._move_anim: QPropertyAnimation | None = None  # 위치 애니메이션

    def update_size(self):
        """텍스트 기반으로 위젯 크기 갱신"""
        fm = QFontMetrics(self.font)
        lines = self.text.splitlines()
        text_w = max(fm.horizontalAdvance(line) for line in lines)
        text_h = fm.height() * len(lines)
        margin = 14  # 내부 여백
        self.base_w = text_w + margin * 2
        self.base_h = text_h + margin * 2

        # 원형은 정사각형 기준으로 강제 (정확한 원을 위해)
        if self.circle:
            longest = max(self.base_w, self.base_h)
            self.base_w = self.base_h = longest  # 정사각형 내부 영역 확보
            size = longest + 10  # 추가 버퍼 포함 위젯 전체 크기
        else:
            # 사각형(회전) 도장은 대각선 길이를 고려하여 위젯 크기 결정
            size = int((self.base_w ** 2 + self.base_h ** 2) ** 0.5) + 2
        # 위젯은 정사각형으로 고정(가로=세로)
        self.setFixedSize(size, size)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 중심으로 이동 후 회전
        painter.translate(self.width() / 2, self.height() / 2)
        if self.angle:
            painter.rotate(self.angle)
        painter.translate(-self.base_w / 2, -self.base_h / 2)

        # 붉은 펜 설정(도장 테두리)
        pen = QPen(QColor("#CC0000"))
        pen.setWidth(3)
        painter.setPen(pen)
        painter.setBrush(Qt.transparent)

        if self.circle:
            painter.drawEllipse(0, 0, self.base_w, self.base_h)
        else:
            painter.drawRect(0, 0, self.base_w, self.base_h)

        # 텍스트(여러 줄 가능) 그리기
        painter.setFont(self.font)
        text_rect = QRect(0, 0, self.base_w, self.base_h)
        painter.drawText(text_rect, Qt.AlignCenter | Qt.TextWordWrap, self.text)
        painter.end()

    # ---------------------------------------------
    # 위치 재계산 및 이벤트 필터
    # ---------------------------------------------
    def reposition(self, main_window: 'MainWindow', *, instant: bool = False):
        """도장 위치 계산
        - X: '생성일'(4)과 '액션'(5) 컬럼 중앙
        - Y: '완료된 할 일 숨기기' 버튼 Y
        instant=True 일 때 애니메이션 없이 바로 이동"""
        try:
            task_widget = main_window.project_widget.task_widget
            btn = task_widget.toggle_completed_btn
            header = task_widget.task_table.horizontalHeader()
            from PySide6.QtCore import QPoint
            # 컬럼 중앙 계산
            center4 = header.sectionPosition(4) + header.sectionSize(4)//2
            center5 = header.sectionPosition(5) + header.sectionSize(5)//2
            mid_x = (center4 + center5)//2

            header_global = header.mapToGlobal(QPoint(mid_x, 0))
            btn_global = btn.mapToGlobal(QPoint(0, 0))

            # 설명 라벨 가시성에 따른 오프셋 결정
            if main_window.project_desc_label.isVisible():
                offset_x = -30  # 설명이 있을 때 약간 왼쪽으로
                offset_y = -60 # 더 위로 올림(설명 공간 만큼)
            else:
                offset_x = -30  # 동일 X 오프셋 유지
                offset_y = -60  # 설명이 없으므로 덜 올림

            # 도장 좌표 (글로벌)
            x_global = header_global.x() - self.width()//2 + offset_x
            y_global = btn_global.y() + offset_y

            # 부모(MainWindow) 좌표계로 변환 후 이동
            self._apply_move(main_window.mapFromGlobal(QPoint(x_global, y_global)), instant)
        except Exception:
            # fallback: 우상단
            self.move(main_window.width() - self.width() - 10, 10)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Resize:
            from PySide6.QtCore import QTimer
            # 지연 호출로 레이아웃 완료 후 재배치
            QTimer.singleShot(0, lambda: self.reposition(obj if isinstance(obj, MainWindow) else self.parentWidget(), instant=True))
        return False  # 계속 전파 

    # 공통 이동 처리 (애니메이션/즉시)
    def _apply_move(self, target: QPoint, instant: bool):
        if instant:
            self.move(target)
            return
        if self._move_anim is None:
            self._move_anim = QPropertyAnimation(self, b"pos", self)
            self._move_anim.setDuration(200)
            self._move_anim.setEasingCurve(QEasingCurve.OutCubic)
        else:
            if self._move_anim.state() == QPropertyAnimation.Running:
                self._move_anim.stop()
        self._move_anim.setStartValue(self.pos())
        self._move_anim.setEndValue(target)
        self._move_anim.start() 

    # 문구 변경 후 크기 갱신
    def set_text(self, new_text: str):
        if self.text == new_text:
            return
        self.text = new_text
        self.update_size()
        self.update() 