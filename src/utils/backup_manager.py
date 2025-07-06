"""
백업/복원 관리자
"""
import os
import shutil
import sqlite3
from datetime import datetime
from typing import Tuple, Optional
from pathlib import Path
from utils.helpers import format_datetime
import re


class BackupManager:
    """백업/복원 관리자"""
    
    def __init__(self, db_path: str):
        """
        초기화
        
        Args:
            db_path: 데이터베이스 파일 경로
        """
        self.db_path = db_path
        self.backup_dir = os.path.join(os.path.dirname(db_path), "backups")
        
        # 백업 디렉토리 생성
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def create_backup(self, custom_name: Optional[str] = None) -> Tuple[bool, str]:
        """
        백업 생성
        
        Args:
            custom_name: 사용자 지정 백업 이름 (선택사항)
            
        Returns:
            (성공 여부, 메시지)
        """
        try:
            # 데이터베이스 파일 존재 확인
            if not os.path.exists(self.db_path):
                return False, "데이터베이스 파일을 찾을 수 없습니다."
            
            # 백업 파일명 생성
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if custom_name:
                # 사용자 지정 이름에서 특수문자 제거
                safe_name = "".join(c for c in custom_name if c.isalnum() or c in (' ', '-', '_')).strip()
                prefix = safe_name or "temporary"
            else:
                prefix = "temporary"

            backup_filename = f"{prefix}_{timestamp}.db"
            backup_path = os.path.join(self.backup_dir, backup_filename)

            # 중복 파일명 존재 시 넘버링 (temporary_20240101_120000 (1).db ...)
            counter = 1
            while os.path.exists(backup_path):
                backup_filename = f"{prefix}_{timestamp} ({counter}).db"
                backup_path = os.path.join(self.backup_dir, backup_filename)
                counter += 1
            
            # 데이터베이스 무결성 검사
            if not self._verify_database_integrity(self.db_path):
                return False, "데이터베이스 파일이 손상되어 백업할 수 없습니다."
            
            # 파일 복사
            shutil.copy2(self.db_path, backup_path)
            
            # 백업 파일 검증
            if not self._verify_database_integrity(backup_path):
                os.remove(backup_path)
                return False, "백업 파일 생성 중 오류가 발생했습니다."
            
            return True, f"백업이 성공적으로 생성되었습니다.\n파일: {backup_filename}"
            
        except Exception as e:
            return False, f"백업 생성 중 오류가 발생했습니다: {str(e)}"
    
    def restore_backup(self, backup_filename: str, should_backup: bool = True) -> Tuple[bool, str]:
        """
        백업 복원
        
        Args:
            backup_filename: 복원할 백업 파일 이름
            should_backup: 현재 데이터 자동 백업 여부 (기본값: True)
            
        Returns:
            (성공 여부, 메시지)
        """
        try:
            backup_path = os.path.join(self.backup_dir, backup_filename)
            
            # 백업 파일 존재 확인
            if not os.path.exists(backup_path):
                return False, "백업 파일을 찾을 수 없습니다."
            
            # 백업 파일 무결성 검사
            if not self._verify_database_integrity(backup_path):
                return False, "백업 파일이 손상되어 복원할 수 없습니다."
            
            # 현재 데이터베이스 백업 (사용자 선택에 따라)
            if should_backup:
                current_backup_result = self.create_backup("before_restore")
                if not current_backup_result[0]:
                    return False, f"복원 전 현재 데이터 백업 실패: {current_backup_result[1]}"
            
            # 데이터베이스 복원
            shutil.copy2(backup_path, self.db_path)
            
            # 복원된 파일 검증
            if not self._verify_database_integrity(self.db_path):
                return False, "복원된 데이터베이스 파일이 손상되었습니다."
            
            return True, f"백업이 성공적으로 복원되었습니다.\n파일: {backup_filename}"
            
        except Exception as e:
            return False, f"백업 복원 중 오류가 발생했습니다: {str(e)}"
    
    def get_backup_list(self) -> list:
        """
        백업 파일 목록 조회
        
        Returns:
            백업 파일 정보 리스트 [(표시명, 생성일시, 크기, 실제 파일명), ...]
        """
        raw_backup_files = []
        
        try:
            for filename in os.listdir(self.backup_dir):
                if filename.endswith('.db'):
                    file_path = os.path.join(self.backup_dir, filename)
                    stat = os.stat(file_path)
                    
                    created_time_dt = datetime.fromtimestamp(stat.st_ctime) # datetime 객체로 저장
                    file_size = stat.st_size
                    
                    # (실제 파일명, datetime 객체, 파일 크기)
                    raw_backup_files.append((filename, created_time_dt, file_size))
            
            # Step 1: 모든 백업을 생성 시간 오름차순 (오래된 순)으로 정렬
            raw_backup_files.sort(key=lambda x: x[1])
            
            name_groups = {}

            # Step 2: 기본 표시 이름 추출 및 그룹화
            for filename, created_time_dt, file_size in raw_backup_files:
                # 실제 파일명에서 타임스탬프와 (N) 접미사를 제거한 '기본' 표시 이름 추출
                # 예: 'MyProject_20250501_123456 (1).db' -> 'MyProject'
                #     'before_restore_20250501_123456.db' -> 'before_restore'
                base_name_without_timestamp = re.sub(r'_\d{8}_\d{6}', '', filename.rsplit('.', 1)[0])
                base_display_name = re.sub(r'\s\((\d+)\)$', '', base_name_without_timestamp).strip()
                
                if base_display_name not in name_groups:
                    name_groups[base_display_name] = []
                
                name_groups[base_display_name].append({
                    'filename': filename,
                    'created_time_dt': created_time_dt,
                    'file_size': file_size,
                })
            
            # Step 3: 각 그룹 내에서 고유한 표시 이름 부여
            final_backup_list = []
            for base_name, backups_in_group in name_groups.items():
                for i, backup_info in enumerate(backups_in_group):
                    display_name_to_use = base_name
                    if len(backups_in_group) > 1 and i > 0: # 그룹 내에 2개 이상이고, 첫 번째(가장 오래된)가 아닐 경우
                        display_name_to_use = f"{base_name} ({i})"
                    
                    final_backup_list.append((
                        display_name_to_use,
                        format_datetime(backup_info['created_time_dt']),
                        self._format_file_size(backup_info['file_size']),
                        backup_info['filename']
                    ))
            
            # Step 4: 최종 결과는 UI 표시를 위해 생성일시 역순으로 다시 정렬 (최신이 위로)
            final_backup_list.sort(key=lambda x: x[1], reverse=True)
            return final_backup_list
            
        except Exception as e:
            print(f"백업 목록 조회 중 오류: {e}")
        
        return [] # 오류 발생 시 빈 리스트 반환
    
    def delete_backup(self, backup_filename: str) -> Tuple[bool, str]:
        """
        백업 파일 삭제
        
        Args:
            backup_filename: 삭제할 백업 파일 이름
            
        Returns:
            (성공 여부, 메시지)
        """
        try:
            backup_path = os.path.join(self.backup_dir, backup_filename)
            
            if not os.path.exists(backup_path):
                return False, "백업 파일을 찾을 수 없습니다."
            
            os.remove(backup_path)
            return True, f"백업 파일이 삭제되었습니다: {backup_filename}"
            
        except Exception as e:
            return False, f"백업 파일 삭제 중 오류가 발생했습니다: {str(e)}"
    
    def _verify_database_integrity(self, db_path: str) -> bool:
        """
        데이터베이스 무결성 검사
        
        Args:
            db_path: 검사할 데이터베이스 파일 경로
            
        Returns:
            무결성 검사 통과 여부
        """
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # PRAGMA integrity_check 실행
            cursor.execute("PRAGMA integrity_check")
            result = cursor.fetchone()
            
            conn.close()
            
            # 'ok'가 반환되면 무결성 검사 통과
            return result and result[0] == 'ok'
            
        except Exception:
            return False
    
    def _format_file_size(self, size_bytes: int) -> str:
        """
        파일 크기를 읽기 쉬운 형태로 변환
        
        Args:
            size_bytes: 바이트 단위 파일 크기
            
        Returns:
            포맷된 파일 크기 문자열
        """
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB" 