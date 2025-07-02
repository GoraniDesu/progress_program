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
            }
            QTableWidget::item {
                padding: 8px;
                border: none;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                color: #333;
                padding: 8px;
                border: 1px solid #ddd;
                font-weight: bold;
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
                gridline-color: #555;
                selection-background-color: #404040;
                background-color: #3c3c3c;
                color: #ffffff;
            }
            QTableWidget::item {
                padding: 8px;
                border: none;
                color: #ffffff;
            }
            QHeaderView::section {
                background-color: #2b2b2b;
                color: #ffffff;
                padding: 8px;
                border: 1px solid #555;
                font-weight: bold;
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
            QDialog, QMessageBox {
                background-color: #3c3c3c;
                color: #ffffff;
            }
            QLineEdit, QTextEdit {
                background-color: #2b2b2b;
                color: #ffffff;
                border: 1px solid #555;
            }
        """
    
    def get_current_theme(self) -> str:
        """현재 테마 반환"""
        return self.current_theme
    
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
                'theme': self.current_theme
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
        except Exception as e:
            print(f"테마 설정 로드 실패: {e}")
            self.current_theme = 'light'


# 전역 테마 매니저 인스턴스
theme_manager = ThemeManager() 