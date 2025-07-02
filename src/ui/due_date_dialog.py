"""
마감일 설정 다이얼로그
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QDateTimeEdit, QCheckBox, QFrame
)
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtGui import QFont
from datetime import datetime, timedelta


class DueDateDialog(QDialog):
    """마감일 설정 다이얼로그"""
    
    def __init__(self, current_due_date=None, parent=None):
        super().__init__(parent)
        self.current_due_date = current_due_date
        self.selected_due_date = None
        self.init_ui()
    
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle("마감일 설정")
        self.setModal(True)
        self.resize(350, 200)
        
        layout = QVBoxLayout(self)
        
        # 제목
        title_label = QLabel("📅 마감일 설정")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 구분선
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
        
        # 마감일 없음 체크박스
        self.no_due_date_checkbox = QCheckBox("마감일 없음")
        self.no_due_date_checkbox.toggled.connect(self.on_no_due_date_toggled)
        layout.addWidget(self.no_due_date_checkbox)
        
        # 마감일 입력
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("마감일:"))
        
        self.due_date_edit = QDateTimeEdit()
        self.due_date_edit.setCalendarPopup(True)
        self.due_date_edit.setDisplayFormat("yyyy-MM-dd hh:mm")
        
        # 기본값 설정
        if self.current_due_date:
            qt_datetime = QDateTime.fromSecsSinceEpoch(int(self.current_due_date.timestamp()))
            self.due_date_edit.setDateTime(qt_datetime)
            self.no_due_date_checkbox.setChecked(False)
        else:
            # 현재 시간 + 1일을 기본값으로 설정
            default_date = datetime.now() + timedelta(days=1)
            qt_datetime = QDateTime.fromSecsSinceEpoch(int(default_date.timestamp()))
            self.due_date_edit.setDateTime(qt_datetime)
            self.no_due_date_checkbox.setChecked(True)
        
        date_layout.addWidget(self.due_date_edit)
        layout.addLayout(date_layout)
        
        # 빠른 설정 버튼들
        quick_layout = QHBoxLayout()
        quick_layout.addWidget(QLabel("빠른 설정:"))
        
        today_btn = QPushButton("오늘")
        today_btn.clicked.connect(lambda: self.set_quick_date(0))
        quick_layout.addWidget(today_btn)
        
        tomorrow_btn = QPushButton("내일")
        tomorrow_btn.clicked.connect(lambda: self.set_quick_date(1))
        quick_layout.addWidget(tomorrow_btn)
        
        week_btn = QPushButton("1주일 후")
        week_btn.clicked.connect(lambda: self.set_quick_date(7))
        quick_layout.addWidget(week_btn)
        
        layout.addLayout(quick_layout)
        
        # 버튼 영역
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        cancel_btn = QPushButton("취소")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        ok_btn = QPushButton("확인")
        ok_btn.clicked.connect(self.accept_date)
        ok_btn.setDefault(True)
        button_layout.addWidget(ok_btn)
        
        layout.addLayout(button_layout)
        
        # 초기 상태 설정
        self.on_no_due_date_toggled(self.no_due_date_checkbox.isChecked())
        
        # 스타일 적용
        self.apply_styles()
    
    def apply_styles(self):
        """스타일 적용"""
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QLabel {
                color: #333;
                margin: 5px 0;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 60px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QDateTimeEdit {
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 4px;
                background-color: white;
            }
            QCheckBox {
                color: #333;
                font-weight: bold;
            }
        """)
    
    def on_no_due_date_toggled(self, checked):
        """마감일 없음 체크박스 토글 이벤트"""
        self.due_date_edit.setEnabled(not checked)
        # 빠른 설정 버튼들도 비활성화
        for button in self.findChildren(QPushButton):
            if button.text() in ["오늘", "내일", "1주일 후"]:
                button.setEnabled(not checked)
    
    def set_quick_date(self, days_offset):
        """빠른 날짜 설정"""
        target_date = datetime.now() + timedelta(days=days_offset)
        # 시간을 오후 6시로 설정
        target_date = target_date.replace(hour=18, minute=0, second=0, microsecond=0)
        
        qt_datetime = QDateTime.fromSecsSinceEpoch(int(target_date.timestamp()))
        self.due_date_edit.setDateTime(qt_datetime)
        
        # 마감일 없음 체크 해제
        self.no_due_date_checkbox.setChecked(False)
    
    def accept_date(self):
        """날짜 확인"""
        if self.no_due_date_checkbox.isChecked():
            self.selected_due_date = None
        else:
            qt_datetime = self.due_date_edit.dateTime()
            self.selected_due_date = datetime.fromtimestamp(qt_datetime.toSecsSinceEpoch())
        
        self.accept()
    
    def get_due_date(self):
        """선택된 마감일 반환"""
        return self.selected_due_date 