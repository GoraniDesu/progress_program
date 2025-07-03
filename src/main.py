"""
Progress Program 메인 애플리케이션
"""
import sys
import os
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

# 프로젝트 루트를 Python 경로에 추가
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 테마 매니저 (현재 모듈에서는 직접 사용하지 않지만, 초기화가 필요한 경우 import)
from utils.theme_manager import theme_manager

try:
    # 현재 디렉토리를 모듈 경로에 추가
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    from ui.main_window import MainWindow
except ImportError as e:
    print(f"Import Error: {e}")
    print("PySide6가 설치되어 있는지 확인하세요: pip install PySide6")
    print("현재 경로:", os.getcwd())
    print("Python 경로:", sys.path[:3])
    sys.exit(1)


def main():
    """메인 함수"""
    # 애플리케이션 생성
    app = QApplication(sys.argv)
    
    # 애플리케이션 정보 설정
    app.setApplicationName("Progress Program")
    app.setApplicationVersion("0.3.2")
    app.setOrganizationName("Progress Team")
    
    # High DPI 지원
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    try:
        # 메인 윈도우 생성 및 표시
        window = MainWindow()
        window.show()
        
        # 애플리케이션 실행
        sys.exit(app.exec())
        
    except Exception as e:
        # 예외 발생 시 에러 메시지 표시
        error_msg = f"애플리케이션 실행 중 오류가 발생했습니다:\n\n{str(e)}"
        
        # QApplication이 존재하면 메시지 박스 사용, 아니면 콘솔 출력
        if QApplication.instance():
            QMessageBox.critical(None, "오류", error_msg)
        else:
            print(error_msg)
        
        sys.exit(1)


if __name__ == "__main__":
    main() 