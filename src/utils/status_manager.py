"""
상태 표시 관리 모듈
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from database.models import Task, Project


class StatusManager:
    """할 일 및 프로젝트 상태 관리 클래스"""
    
    def __init__(self):
        self.status_icons = {
            'urgent': '🚨',
            'overdue': '⚠️',
            'completed': '✅',
            'high_progress': '🏆',
            'normal': ''
        }
        
        self.status_colors = {
            'urgent': '#ff6b6b',
            'overdue': '#ff4757',
            'completed': '#2ed573',
            'high_progress': '#ffa502',
            'normal': '#ddd'
        }
        
        # 상태 우선순위 (낮은 번호 = 높은 우선순위)
        self.status_priority = {
            'overdue': 0,
            'urgent': 1,
            'completed': 2,
            'high_progress': 3,
            'normal': 4
        }
    
    def get_task_status(self, task: Task) -> str:
        """할 일 상태 계산"""
        if task.completed:
            return 'completed'
        
        if task.due_date:
            if task.due_date < datetime.now():
                return 'overdue'
            elif task.due_date < datetime.now() + timedelta(hours=24):
                return 'urgent'
        
        return 'normal'
    
    def get_project_status(self, project: Project, tasks: List[Task]) -> str:
        """프로젝트 상태 계산"""
        if not tasks:
            return 'normal'
        
        completed_tasks = [t for t in tasks if t.completed]
        completion_rate = len(completed_tasks) / len(tasks)
        
        # 완료율 80% 이상
        if completion_rate >= 0.8:
            return 'high_progress'
        
        # 마감일 임박한 할 일이 있는지 확인
        urgent_tasks = [t for t in tasks if self.get_task_status(t) == 'urgent']
        if urgent_tasks:
            return 'urgent'
        
        # 마감일 초과한 할 일이 있는지 확인
        overdue_tasks = [t for t in tasks if self.get_task_status(t) == 'overdue']
        if overdue_tasks:
            return 'overdue'
        
        return 'normal'
    
    def get_status_icon(self, status: str) -> str:
        """상태 아이콘 반환"""
        return self.status_icons.get(status, '')
    
    def get_status_color(self, status: str) -> str:
        """상태 색상 반환"""
        return self.status_colors.get(status, '#ddd')
    
    def get_status_description(self, status: str) -> str:
        """상태 설명 반환"""
        descriptions = {
            'urgent': '마감일 임박',
            'overdue': '마감일 초과',
            'completed': '완료',
            'high_progress': '진행률 우수',
            'normal': '일반'
        }
        return descriptions.get(status, '일반')
    
    def get_priority_status(self, statuses: List[str]) -> str:
        """여러 상태 중 우선순위가 높은 상태 반환"""
        if not statuses:
            return 'normal'
        
        # 우선순위에 따라 정렬
        sorted_statuses = sorted(statuses, key=lambda x: self.status_priority.get(x, 99))
        return sorted_statuses[0]
    
    def get_task_status_summary(self, task: Task) -> Dict:
        """할 일 상태 요약 정보 반환"""
        status = self.get_task_status(task)
        
        return {
            'status': status,
            'icon': self.get_status_icon(status),
            'color': self.get_status_color(status),
            'description': self.get_status_description(status),
            'priority': self.status_priority.get(status, 99)
        }
    
    def get_project_status_summary(self, project: Project, tasks: List[Task]) -> Dict:
        """프로젝트 상태 요약 정보 반환"""
        status = self.get_project_status(project, tasks)
        
        # 각 할 일의 상태 통계
        task_statuses = [self.get_task_status(task) for task in tasks]
        status_counts = {}
        for s in ['urgent', 'overdue', 'completed', 'high_progress', 'normal']:
            status_counts[s] = task_statuses.count(s)
        
        return {
            'status': status,
            'icon': self.get_status_icon(status),
            'color': self.get_status_color(status),
            'description': self.get_status_description(status),
            'priority': self.status_priority.get(status, 99),
            'task_counts': status_counts,
            'total_tasks': len(tasks),
            'completed_tasks': status_counts['completed'],
            'urgent_tasks': status_counts['urgent'],
            'overdue_tasks': status_counts['overdue']
        }
    
    def is_due_soon(self, task: Task, hours: int = 24) -> bool:
        """마감일이 임박한지 확인"""
        if not task.due_date:
            return False
        
        return datetime.now() <= task.due_date < datetime.now() + timedelta(hours=hours)
    
    def is_overdue(self, task: Task) -> bool:
        """마감일이 초과했는지 확인"""
        if not task.due_date:
            return False
        
        return task.due_date < datetime.now()
    
    def get_completion_rate(self, tasks: List[Task]) -> float:
        """완료율 계산"""
        if not tasks:
            return 0.0
        
        completed_tasks = [t for t in tasks if t.completed]
        return len(completed_tasks) / len(tasks)


# 전역 상태 관리자 인스턴스
status_manager = StatusManager() 