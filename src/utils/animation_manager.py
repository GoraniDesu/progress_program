"""
애니메이션 관리 모듈
"""
from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QSequentialAnimationGroup, QParallelAnimationGroup, QTimer
from PySide6.QtWidgets import QWidget, QGraphicsOpacityEffect, QTableWidget, QProgressBar
from PySide6.QtGui import QColor
from typing import List, Optional
import time


class AnimationManager:
    """마이크로 애니메이션 관리 클래스"""
    
    def __init__(self, parent=None):
        self.parent = parent
        self.active_animations: List[QPropertyAnimation] = []
        self.animation_queue: List[tuple] = []
        self.max_concurrent_animations = 3  # 동시 실행 제한
        self.animation_enabled = True  # 애니메이션 활성화/비활성화
        
        # 성능 모니터링
        self.performance_monitor = {
            'last_frame_time': time.time(),
            'frame_count': 0,
            'fps': 60
        }
    
    def is_animation_enabled(self) -> bool:
        """애니메이션 활성화 상태 확인"""
        return self.animation_enabled
    
    def set_animation_enabled(self, enabled: bool):
        """애니메이션 활성화/비활성화 설정"""
        self.animation_enabled = enabled
        if not enabled:
            self.stop_all_animations()
    
    def can_start_animation(self) -> bool:
        """새 애니메이션 시작 가능 여부 확인"""
        return len(self.active_animations) < self.max_concurrent_animations
    
    def add_animation(self, animation_func, *args, **kwargs):
        """애니메이션 추가 (큐 관리)"""
        if not self.animation_enabled:
            return None
        
        if self.can_start_animation():
            return animation_func(*args, **kwargs)
        else:
            # 큐에 추가
            self.animation_queue.append((animation_func, args, kwargs))
            return None
    
    def animation_finished(self, animation: QPropertyAnimation):
        """애니메이션 완료 시 콜백"""
        if animation in self.active_animations:
            self.active_animations.remove(animation)
        
        # 큐에서 대기 중인 애니메이션 시작
        self.start_queued_animation()
    
    def start_queued_animation(self):
        """큐에서 대기 중인 애니메이션 시작"""
        if self.animation_queue and self.can_start_animation():
            animation_func, args, kwargs = self.animation_queue.pop(0)
            animation_func(*args, **kwargs)
    
    def stop_all_animations(self):
        """모든 애니메이션 중지"""
        for animation in self.active_animations[:]:
            animation.stop()
        self.active_animations.clear()
        self.animation_queue.clear()
    
    def animate_task_completion(self, checkbox_widget: QWidget) -> Optional[QPropertyAnimation]:
        """할 일 완료 체크 애니메이션"""
        if not self.animation_enabled:
            return None
        
        # 체크박스 확대/축소 애니메이션
        animation = QPropertyAnimation(checkbox_widget, b"geometry")
        animation.setDuration(200)
        
        original_geometry = checkbox_widget.geometry()
        expanded_geometry = original_geometry.adjusted(-2, -2, 2, 2)
        
        animation.setStartValue(original_geometry)
        animation.setKeyValueAt(0.5, expanded_geometry)
        animation.setEndValue(original_geometry)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # 애니메이션 완료 시 콜백 연결
        animation.finished.connect(lambda: self.animation_finished(animation))
        
        self.active_animations.append(animation)
        animation.start()
        
        return animation
    
    def animate_progress_update(self, progress_bar: QProgressBar, new_value: int) -> Optional[QPropertyAnimation]:
        """진척도 바 업데이트 애니메이션"""
        if not self.animation_enabled:
            progress_bar.setValue(new_value)
            return None
        
        animation = QPropertyAnimation(progress_bar, b"value")
        animation.setDuration(800)
        animation.setStartValue(progress_bar.value())
        animation.setEndValue(new_value)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # 애니메이션 완료 시 콜백 연결
        animation.finished.connect(lambda: self.animation_finished(animation))
        
        self.active_animations.append(animation)
        animation.start()
        
        return animation
    
    def animate_new_item_appearance(self, item_widget: QWidget) -> Optional[QPropertyAnimation]:
        """새 항목 추가 애니메이션 (페이드인)"""
        if not self.animation_enabled:
            return None
        
        # 투명도 효과 생성
        opacity_effect = QGraphicsOpacityEffect()
        item_widget.setGraphicsEffect(opacity_effect)
        
        # 페이드인 애니메이션
        animation = QPropertyAnimation(opacity_effect, b"opacity")
        animation.setDuration(300)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # 애니메이션 완료 시 콜백 연결
        animation.finished.connect(lambda: self.animation_finished(animation))
        
        self.active_animations.append(animation)
        animation.start()
        
        return animation
    
    def animate_status_change(self, widget: QWidget, color: QColor) -> Optional[QPropertyAnimation]:
        """상태 변경 애니메이션 (색상 변화)"""
        if not self.animation_enabled:
            return None
        
        # 간단한 하이라이트 효과
        animation = QPropertyAnimation(widget, b"geometry")
        animation.setDuration(150)
        
        original_geometry = widget.geometry()
        highlighted_geometry = original_geometry.adjusted(-1, -1, 1, 1)
        
        animation.setStartValue(original_geometry)
        animation.setKeyValueAt(0.5, highlighted_geometry)
        animation.setEndValue(original_geometry)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # 애니메이션 완료 시 콜백 연결
        animation.finished.connect(lambda: self.animation_finished(animation))
        
        self.active_animations.append(animation)
        animation.start()
        
        return animation
    
    def animate_table_row_insert(self, table: QTableWidget, row_index: int) -> Optional[QSequentialAnimationGroup]:
        """테이블 행 삽입 애니메이션"""
        if not self.animation_enabled:
            return None
        
        # 행 높이 애니메이션 (0에서 정상 높이로)
        animation_group = QSequentialAnimationGroup()
        
        # 첫 번째: 행 높이를 0으로 설정
        table.setRowHeight(row_index, 0)
        
        # 두 번째: 행 높이를 점진적으로 증가
        row_height_animation = QPropertyAnimation()
        row_height_animation.setDuration(200)
        row_height_animation.setStartValue(0)
        row_height_animation.setEndValue(42)  # 기본 행 높이
        row_height_animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # 행 높이 업데이트 함수
        def update_row_height(value):
            table.setRowHeight(row_index, int(value))
        
        row_height_animation.valueChanged.connect(update_row_height)
        animation_group.addAnimation(row_height_animation)
        
        # 애니메이션 완료 시 콜백 연결
        animation_group.finished.connect(lambda: self.animation_finished(animation_group))
        
        self.active_animations.append(animation_group)
        animation_group.start()
        
        return animation_group
    
    def animate_fluid_progress(self, progress_bar: QProgressBar, static_value: int) -> Optional[QPropertyAnimation]:
        """
        진척도 바가 현재 값 주변에서 유동적으로 움직이는 애니메이션
        (예: 40%에서 39%~41% 사이를 반복)
        """
        if not self.animation_enabled:
            return None

        # 기존에 진행 중인 유동 애니메이션이 있다면 중지
        for anim in self.active_animations[:]:
            if isinstance(anim, QPropertyAnimation) and anim.targetObject() == progress_bar and anim.propertyName() == b"value" and anim.loopCount() == -1:
                anim.stop()
                self.active_animations.remove(anim)

        # 미세하게 움직일 범위 설정 (예: ±1%)
        epsilon = 1
        start_value = max(0, static_value - epsilon)
        end_value = min(100, static_value + epsilon)

        fluid_animation = QPropertyAnimation(progress_bar, b"value")
        fluid_animation.setDuration(1500) # 한 번 왕복하는 시간 (밀리초)
        fluid_animation.setLoopCount(-1)  # 무한 반복
        fluid_animation.setEasingCurve(QEasingCurve.InOutSine) # 부드러운 흐름

        fluid_animation.setStartValue(start_value)
        fluid_animation.setKeyValueAt(0.5, end_value) # 중간 지점에서 최대값
        fluid_animation.setEndValue(start_value) # 다시 시작 값으로 돌아옴

        self.active_animations.append(fluid_animation)
        fluid_animation.start()

        return fluid_animation
    
    def get_performance_info(self) -> dict:
        """성능 정보 반환"""
        current_time = time.time()
        frame_time = current_time - self.performance_monitor['last_frame_time']
        self.performance_monitor['last_frame_time'] = current_time
        self.performance_monitor['frame_count'] += 1
        
        if frame_time > 0:
            self.performance_monitor['fps'] = 1.0 / frame_time
        
        return {
            'active_animations': len(self.active_animations),
            'queued_animations': len(self.animation_queue),
            'fps': self.performance_monitor['fps'],
            'animation_enabled': self.animation_enabled
        }


# 전역 애니메이션 관리자 인스턴스
animation_manager = AnimationManager() 