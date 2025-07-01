"""
진척도 계산 유틸리티
"""
from typing import List
from database.models import Task


class ProgressCalculator:
    """진척도 계산기"""
    
    @staticmethod
    def calculate_progress(tasks: List[Task]) -> float:
        """
        할 일 목록에서 진척도 계산
        
        Args:
            tasks: 할 일 목록
            
        Returns:
            진척도 퍼센트 (0.0 ~ 100.0)
        """
        if not tasks:
            return 0.0
        
        completed_count = sum(1 for task in tasks if task.completed)
        total_count = len(tasks)
        
        return (completed_count / total_count) * 100.0

    @staticmethod
    def get_progress_color(progress: float) -> str:
        """
        진척도에 따른 색상 반환
        
        Args:
            progress: 진척도 퍼센트
            
        Returns:
            색상 문자열
        """
        if progress >= 75:
            return "#4CAF50"  # 초록색
        elif progress >= 50:
            return "#FFC107"  # 노란색
        elif progress >= 25:
            return "#FF9800"  # 주황색
        else:
            return "#F44336"  # 빨간색

    @staticmethod
    def get_progress_text(progress: float) -> str:
        """
        진척도 텍스트 반환
        
        Args:
            progress: 진척도 퍼센트
            
        Returns:
            진척도 텍스트
        """
        if progress == 100:
            return "완료! 🎉"
        elif progress >= 75:
            return "거의 다 됐어요! 💪"
        elif progress >= 50:
            return "절반 완료! 👍"
        elif progress >= 25:
            return "순조롭게 진행 중! 🚀"
        elif progress > 0:
            return "시작했어요! 😊"
        else:
            return "시작해보세요! 💡"

    @staticmethod
    def get_completion_stats(tasks: List[Task]) -> dict:
        """
        완료 통계 반환
        
        Args:
            tasks: 할 일 목록
            
        Returns:
            통계 딕셔너리
        """
        total = len(tasks)
        completed = sum(1 for task in tasks if task.completed)
        remaining = total - completed
        progress = ProgressCalculator.calculate_progress(tasks)
        
        return {
            'total': total,
            'completed': completed,
            'remaining': remaining,
            'progress': progress,
            'progress_text': ProgressCalculator.get_progress_text(progress),
            'progress_color': ProgressCalculator.get_progress_color(progress)
        } 