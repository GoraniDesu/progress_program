"""
간단한 테마 관리 모듈
"""
import json
import os
from PySide6.QtCore import QObject, Signal


class ThemeManager(QObject):
    """간단한 테마 관리 클래스"""
    
    theme_changed = Signal(str)  # 테마 변경 시그널
    
    def __init__(self):
        super().__init__()
        # 프로젝트 루트 기준으로 config 폴더의 설정 파일 경로
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.settings_file = os.path.join(project_root, "config", "theme_settings.json")
        self.current_theme = "light"
        self.animation_enabled = True
        self.animation_speed = "normal"
        self.load_settings()
    
    def get_light_theme(self) -> str:
        """라이트 테마 스타일 반환"""
        return """
            QMainWindow {
                background-color: #f5f5f5;
                color: #333;
            }
            QFrame {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin: 2px;
                color: #333;
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
                color: #333;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #eee;
                color: #333;
            }
            QListWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QProgressBar {
                border: 1px solid #ddd;
                border-radius: 5px;
                text-align: center;
                background-color: #f0f0f0;
                color: #333;
                min-height: 30px;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 4px;
            }
            QLabel {
                color: #333;
                background-color: transparent;
            }
            QTableWidget {
                gridline-color: #ddd;
                selection-background-color: #e3f2fd;
                background-color: white;
                color: #333;
                font-size: 15px;
            }
            QTableWidget::item {
                padding: 8px;
                border: none;
                font-size: 15px;
                background-color: white;
                color: #333;
            }
            QTableWidget::item:selected {
                background-color: #0078d4;
                color: #ffffff;
            }
            QTableWidget::item:hover {
                background-color: #e5f3ff;
                color: #333;
            }
            QTableWidget::item:selected:focus {
                background-color: #106ebe;
                color: #ffffff;
            }
            QTableWidget::item:selected:!focus {
                background-color: #cce8ff;
                color: #333;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                color: #333;
                padding: 8px;
                border: 1px solid #ddd;
                font-weight: bold;
            }
            QHeaderView::section:hover {
                background-color: #e8e8e8;
            }
            QTabWidget::pane {
                border: 1px solid #ddd;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #f0f0f0;
                color: #333;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #4CAF50;
                color: #333;
            }
            QTabBar::tab:hover {
                background-color: #e8f5e8;
            }
            QTextEdit {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px;
                background-color: white;
                color: #333;
            }
            QMenuBar {
                background-color: #f5f5f5;
                color: #333;
                border-bottom: 1px solid #ddd;
            }
            QMenuBar::item {
                background-color: transparent;
                color: #333;
                padding: 8px 12px;
            }
            QMenuBar::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QMenu {
                background-color: white;
                color: #333;
                border: 1px solid #ddd;
            }
            QMenu::item {
                background-color: transparent;
                color: #333;
                padding: 6px 20px;
            }
            QMenu::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QDialog, QMessageBox {
                background-color: white;
                color: #333;
            }
            QLineEdit, QTextEdit {
                background-color: white;
                color: #333;
                border: 1px solid #ddd;
            }
            QSplitter::handle {
                background-color: #e0e0e0;
                width: 4px;
            }
            QSplitter::handle:hover {
                background-color: #4CAF50;
            }
        """
    
    def get_dark_theme(self) -> str:
        """다크 테마 스타일 반환"""
        return """
            QMainWindow {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QFrame {
                background-color: #3c3c3c;
                border: 1px solid #555;
                border-radius: 5px;
                margin: 2px;
                color: #ffffff;
            }
            QPushButton {
                background-color: #45a049;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4CAF50;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QListWidget {
                border: 1px solid #555;
                border-radius: 4px;
                background-color: #3c3c3c;
                selection-background-color: #404040;
                color: #ffffff;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #555;
                color: #ffffff;
            }
            QListWidget::item:selected {
                background-color: #404040;
                color: #4CAF50;
            }
            QProgressBar {
                border: 1px solid #555;
                border-radius: 5px;
                text-align: center;
                background-color: #2b2b2b;
                color: #ffffff;
                min-height: 30px;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 4px;
            }
            QLabel {
                color: #ffffff;
                background-color: transparent;
            }
            QTableWidget {
                gridline-color: #555555;
                selection-background-color: #404040;
                background-color: #2b2b2b;
                color: #ffffff;
                font-size: 15px;
            }
            QTableWidget::item {
                background-color: #2b2b2b;
                color: #ffffff;
                padding: 8px;
                border: none;
                font-size: 15px;
            }
            QTableWidget::item:selected {
                background-color: #404040;
                color: #ffffff;
            }
            QTableWidget::item:hover {
                background-color: #353535;
            }
            QTableCornerButton::section {
                background-color: #2b2b2b;
                border: 1px solid #555555;
            }
            QHeaderView::section {
                background-color: #404040;
                color: #ffffff;
                padding: 8px;
                border: 1px solid #555555;
                font-weight: bold;
            }
            QHeaderView::section:hover {
                background-color: #4a4a4a;
            }
            QTabWidget::pane {
                border: 1px solid #555;
                background-color: #3c3c3c;
            }
            QTabBar::tab {
                background-color: #2b2b2b;
                color: #ffffff;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #3c3c3c;
                border-bottom: 2px solid #4CAF50;
                color: #ffffff;
            }
            QTabBar::tab:hover {
                background-color: #404040;
            }
            QTextEdit {
                border: 1px solid #555;
                border-radius: 4px;
                padding: 8px;
                background-color: #3c3c3c;
                color: #ffffff;
            }
            QMenuBar {
                background-color: #2b2b2b;
                color: #ffffff;
                border-bottom: 1px solid #555;
            }
            QMenuBar::item {
                background-color: transparent;
                color: #ffffff;
                padding: 8px 12px;
            }
            QMenuBar::item:selected {
                background-color: #404040;
                color: #4CAF50;
            }
            QMenu {
                background-color: #3c3c3c;
                color: #ffffff;
                border: 1px solid #555;
            }
            QMenu::item {
                background-color: transparent;
                color: #ffffff;
                padding: 6px 20px;
            }
            QMenu::item:selected {
                background-color: #404040;
                color: #4CAF50;
            }
            QDialog, QMessageBox {
                background-color: #3c3c3c;
                color: #ffffff;
            }
            QLineEdit, QTextEdit {
                background-color: #2b2b2b;
                color: #ffffff;
                border: 1px solid #555;
            }
            QSplitter::handle {
                background-color: #555555;
                width: 4px;
            }
            QSplitter::handle:hover {
                background-color: #4CAF50;
            }
        """
    
    def get_current_theme(self) -> str:
        """현재 테마 반환"""
        return self.current_theme
    
    def get_animation_enabled(self) -> bool:
        """애니메이션 활성화 상태 반환"""
        return self.animation_enabled
    
    def set_animation_enabled(self, enabled: bool):
        """애니메이션 활성화/비활성화 설정"""
        self.animation_enabled = enabled
        self.save_settings()
        # 애니메이션 관리자에 설정 적용
        from utils.animation_manager import animation_manager
        animation_manager.set_animation_enabled(enabled)
    
    def get_animation_speed(self) -> str:
        """애니메이션 속도 반환"""
        return self.animation_speed
    
    def set_animation_speed(self, speed: str):
        """애니메이션 속도 설정 (slow, normal, fast)"""
        if speed in ['slow', 'normal', 'fast']:
            self.animation_speed = speed
            self.save_settings()
    
    def set_theme(self, theme_name: str):
        """테마 설정"""
        if theme_name in ['light', 'dark']:
            self.current_theme = theme_name
            self.save_settings()
            self.theme_changed.emit(theme_name)
    
    def get_style_sheet(self, theme_name: str = None) -> str:
        """스타일시트 반환"""
        if theme_name is None:
            theme_name = self.current_theme
        
        if theme_name == 'dark':
            return self.get_dark_theme()
        else:
            return self.get_light_theme()
    
    def save_settings(self):
        """설정 저장"""
        try:
            settings = {
                'theme': self.current_theme,
                'animation_enabled': self.animation_enabled,
                'animation_speed': self.animation_speed
            }
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"테마 설정 저장 실패: {e}")
    
    def load_settings(self):
        """설정 로드"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.current_theme = settings.get('theme', 'light')
                    self.animation_enabled = settings.get('animation_enabled', True)
                    self.animation_speed = settings.get('animation_speed', 'normal')
        except Exception as e:
            print(f"테마 설정 로드 실패: {e}")
            self.current_theme = 'light'
            self.animation_enabled = True
            self.animation_speed = 'normal'


# 전역 테마 매니저 인스턴스
theme_manager = ThemeManager() 