"""
백업/복원 다이얼로그
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, 
    QListWidget, QTableWidget, QTableWidgetItem, QHeaderView,
    QLabel, QMessageBox, QInputDialog,
    QProgressDialog, QApplication
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont


class BackupWorker(QThread):
    """백업 작업을 위한 워커 스레드"""
    finished = Signal(bool, str)
    
    def __init__(self, backup_manager, operation, *args):
        super().__init__()
        self.backup_manager = backup_manager
        self.operation = operation
        self.args = args
    
    def run(self):
        try:
            if self.operation == 'create':
                result = self.backup_manager.create_backup(*self.args)
            elif self.operation == 'restore':
                result = self.backup_manager.restore_backup(*self.args)
            elif self.operation == 'delete':
                result = self.backup_manager.delete_backup(*self.args)
            else:
                result = (False, "알 수 없는 작업입니다.")
            
            self.finished.emit(result[0], result[1])
        except Exception as e:
            self.finished.emit(False, f"작업 중 오류가 발생했습니다: {str(e)}")


class BackupDialog(QDialog):
    """백업/복원 다이얼로그"""
    
    def __init__(self, backup_manager, parent=None):
        super().__init__(parent)
        self.backup_manager = backup_manager
        self.worker = None
        self.init_ui()
        self.refresh_backup_list()
    
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle("백업/복원 관리")
        self.setModal(True)
        self.resize(600, 400)
        
        layout = QVBoxLayout(self)
        
        # 제목
        title = QLabel("데이터 백업/복원 관리")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # 백업 목록
        list_label = QLabel("백업 파일 목록:")
        layout.addWidget(list_label)
        
        # QListWidget → QTableWidget으로 변경 (시인성 개선)
        self.backup_list = QTableWidget()
        self.backup_list.setColumnCount(4)
        self.backup_list.setHorizontalHeaderLabels(["백업 이름", "생성일시", "파일 크기", "작업"])
        
        # 컬럼 크기 설정
        header = self.backup_list.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)          # 백업 이름
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents) # 생성일시
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents) # 파일 크기
        header.setSectionResizeMode(3, QHeaderView.Fixed)            # 작업
        self.backup_list.setColumnWidth(3, 100)
        
        # 행 선택 모드 설정
        self.backup_list.setSelectionBehavior(QTableWidget.SelectRows)
        
        layout.addWidget(self.backup_list)
        
        # 버튼 영역
        button_layout = QHBoxLayout()
        
        # 백업 생성 버튼
        self.create_btn = QPushButton("새 백업 생성")
        self.create_btn.clicked.connect(self.create_backup)
        button_layout.addWidget(self.create_btn)
        
        # 백업 복원 버튼
        self.restore_btn = QPushButton("백업 복원")
        self.restore_btn.clicked.connect(self.restore_backup)
        button_layout.addWidget(self.restore_btn)
        
        # 백업 삭제 버튼
        self.delete_btn = QPushButton("백업 삭제")
        self.delete_btn.clicked.connect(self.delete_backup)
        button_layout.addWidget(self.delete_btn)
        
        # 새로고침 버튼
        self.refresh_btn = QPushButton("새로고침")
        self.refresh_btn.clicked.connect(self.refresh_backup_list)
        button_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(button_layout)
        
        # 닫기 버튼
        close_layout = QHBoxLayout()
        close_layout.addStretch()
        
        self.close_btn = QPushButton("닫기")
        self.close_btn.clicked.connect(self.accept)
        close_layout.addWidget(self.close_btn)
        
        layout.addLayout(close_layout)
    
    def refresh_backup_list(self):
        """백업 목록 새로고침"""
        self.backup_list.setRowCount(0)  # 기존 행 모두 제거
        backups = self.backup_manager.get_backup_list()
        
        if not backups:
            # 빈 목록일 때 안내 메시지 표시
            self.backup_list.setRowCount(1)
            no_backup_item = QTableWidgetItem("생성된 백업이 없습니다.")
            no_backup_item.setFlags(no_backup_item.flags() & ~Qt.ItemIsSelectable)
            self.backup_list.setItem(0, 0, no_backup_item)
            
            # 나머지 컬럼도 빈 아이템으로 채움
            for col in range(1, 4):
                empty_item = QTableWidgetItem("")
                empty_item.setFlags(empty_item.flags() & ~Qt.ItemIsSelectable)
                self.backup_list.setItem(0, col, empty_item)
            
            self.restore_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)
        else:
            self.backup_list.setRowCount(len(backups))
            
            for row, (display_name, created_time, file_size, actual_filename) in enumerate(backups):
                # 백업 이름 (사용자 지정 이름)
                name_item = QTableWidgetItem(display_name)
                name_item.setData(Qt.UserRole, actual_filename)  # 실제 파일명 저장
                name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
                self.backup_list.setItem(row, 0, name_item)
                
                # 생성일시
                time_item = QTableWidgetItem(created_time)
                time_item.setFlags(time_item.flags() & ~Qt.ItemIsEditable)
                self.backup_list.setItem(row, 1, time_item)
                
                # 파일 크기
                size_item = QTableWidgetItem(file_size)
                size_item.setFlags(size_item.flags() & ~Qt.ItemIsEditable)
                self.backup_list.setItem(row, 2, size_item)
                
                # 작업 컬럼 (비워둠 - 버튼은 별도 처리)
                action_item = QTableWidgetItem("")
                action_item.setFlags(action_item.flags() & ~Qt.ItemIsEditable)
                self.backup_list.setItem(row, 3, action_item)
            
            self.restore_btn.setEnabled(True)
            self.delete_btn.setEnabled(True)
    
    def create_backup(self):
        """백업 생성"""
        name, ok = QInputDialog.getText(
            self, "백업 생성", 
            "백업 이름을 입력하세요 (선택사항):"
        )
        
        if not ok:
            return
        
        # 빈 이름인 경우 None으로 처리
        backup_name = name.strip() if name.strip() else None
        
        self.show_progress("백업을 생성하고 있습니다...")
        
        self.worker = BackupWorker(self.backup_manager, 'create', backup_name)
        self.worker.finished.connect(self.on_backup_finished)
        self.worker.start()
    
    def restore_backup(self):
        """백업 복원"""
        current_row = self.backup_list.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "경고", "복원할 백업을 선택해주세요.")
            return
        
        # 첫 번째 컬럼(백업 이름)에서 실제 파일명 가져오기
        name_item = self.backup_list.item(current_row, 0)
        if not name_item:
            QMessageBox.warning(self, "경고", "올바른 백업을 선택해주세요.")
            return
        
        filename = name_item.data(Qt.UserRole)
        if not filename:
            QMessageBox.warning(self, "경고", "올바른 백업을 선택해주세요.")
            return
        
        reply = QMessageBox.question(
            self, "백업 복원 확인",
            f"정말로 '{filename}' 백업으로 복원하시겠습니까?\n\n"
            "현재 데이터는 자동으로 백업된 후 선택한 백업으로 교체됩니다.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.show_progress("백업을 복원하고 있습니다...")
            
            self.worker = BackupWorker(self.backup_manager, 'restore', filename)
            self.worker.finished.connect(self.on_restore_finished)
            self.worker.start()
    
    def delete_backup(self):
        """백업 삭제"""
        current_row = self.backup_list.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "경고", "삭제할 백업을 선택해주세요.")
            return
        
        # 첫 번째 컬럼(백업 이름)에서 실제 파일명 가져오기
        name_item = self.backup_list.item(current_row, 0)
        if not name_item:
            QMessageBox.warning(self, "경고", "올바른 백업을 선택해주세요.")
            return
        
        filename = name_item.data(Qt.UserRole)
        if not filename:
            QMessageBox.warning(self, "경고", "올바른 백업을 선택해주세요.")
            return
        
        reply = QMessageBox.question(
            self, "백업 삭제 확인",
            f"정말로 '{filename}' 백업을 삭제하시겠습니까?\n\n"
            "삭제된 백업은 복구할 수 없습니다.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.show_progress("백업을 삭제하고 있습니다...")
            
            self.worker = BackupWorker(self.backup_manager, 'delete', filename)
            self.worker.finished.connect(self.on_delete_finished)
            self.worker.start()
    
    def show_progress(self, message):
        """진행 상황 표시"""
        self.progress = QProgressDialog(message, None, 0, 0, self)
        self.progress.setWindowModality(Qt.WindowModal)
        self.progress.show()
        QApplication.processEvents()
    
    def hide_progress(self):
        """진행 상황 숨기기"""
        if hasattr(self, 'progress'):
            self.progress.close()
    
    def on_backup_finished(self, success, message):
        """백업 생성 완료"""
        self.hide_progress()
        
        if success:
            QMessageBox.information(self, "성공", message)
            self.refresh_backup_list()
        else:
            QMessageBox.critical(self, "오류", message)
    
    def on_restore_finished(self, success, message):
        """백업 복원 완료"""
        self.hide_progress()
        
        if success:
            QMessageBox.information(self, "성공", 
                f"{message}\n\n프로그램을 다시 시작하여 복원된 데이터를 확인하세요.")
        else:
            QMessageBox.critical(self, "오류", message)
    
    def on_delete_finished(self, success, message):
        """백업 삭제 완료"""
        self.hide_progress()
        
        if success:
            QMessageBox.information(self, "성공", message)
            self.refresh_backup_list()
        else:
            QMessageBox.critical(self, "오류", message) 