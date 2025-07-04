"""
Completion celebration manager providing visual & audio feedback when progress reaches 100 %.

약식 구현 – 디자인 문서(v0.5.1_추가개선사항.md)의 전체 효과 중 핵심(골드 프로그래스바 Morph·마이크로 콘페티·사운드·ESC 스킵)을 간단히 충족해 호환성을 유지한다.

참고:
- Qt 5/6 기본 모듈만 사용해 외부 의존성 추가 0
- ThemeManager 연동: 골드·다크 팔레트 색상 선택
- AnimationManager를 사용해 프로그래스바 Morph
"""

from __future__ import annotations

import random
from typing import List

from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, QPoint, QParallelAnimationGroup, QSequentialAnimationGroup, QPauseAnimation
from PySide6.QtMultimedia import QSoundEffect  # PySide6 >= 6.2
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QApplication,
    QGraphicsOpacityEffect,
)
from PySide6.QtGui import QColor
from shiboken6 import isValid


class ConfettiParticle(QLabel):
    """간단한 콘페티 입자(QLabel 사각형)."""

    COLORS_LIGHT = ["#FFB3BA", "#FFDFBA", "#FFFFBA", "#BAFFC9", "#BAE1FF"]
    COLORS_DARK = [
        "#FF9AA2",
        "#FFB7B2",
        "#FFDAC1",
        "#E2F0CB",
        "#B5EAD7",
    ]

    def __init__(self, parent: QWidget, dark_mode: bool):
        super().__init__(parent)
        size = random.randint(12, 18)  # 이전 6~10 → 가독성 ↑
        self.resize(size, size)
        self.setStyleSheet(
            f"background-color: {random.choice(self.COLORS_DARK if dark_mode else self.COLORS_LIGHT)};"
            "border-radius: 3px;"
            "border:1px solid rgba(0,0,0,0.15);"
        )


class CelebrationManager(QWidget):
    """전체 화면 오버레이 위젯으로 100 % 완료 축하 효과를 표시한다."""

    def __init__(self, parent_window: QWidget, theme_manager, animation_manager):
        super().__init__(parent_window)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.parent_window = parent_window
        self.theme_manager = theme_manager
        self.animation_manager = animation_manager
        self.sound: QSoundEffect | None = None
        self.particles: List[ConfettiParticle] = []
        self.active = False
        self.resize(parent_window.size())
        parent_window.installEventFilter(self)  # 부모 리사이즈 감지

        # ESC/E 키 스킵용
        self.setFocusPolicy(Qt.StrongFocus)

    # ---------------------------------------------------
    # Public API
    # ---------------------------------------------------
    def start(self, progress_bar):
        """축하 애니메이션 시작. 이미 실행 중이면 무시."""
        if self.active:
            return
        self.active = True
        self.target_progress_bar = progress_bar  # 복원용 레퍼런스 보관
        # ProgressBar 축하 모드 ON (FlowProgressBar 확장 메서드 체크)
        if hasattr(progress_bar, "set_celebration_mode"):
            progress_bar.set_celebration_mode(True)
        self.raise_()
        self.show()
        self._play_sound()
        self._spawn_confetti()

        # 애니메이션 총 길이 ≈ 1.8 s + 여유 0.2 s -> 2.0 s 후 자동 종료
        QTimer.singleShot(2000, self.stop)

    def stop(self):
        """모든 애니메이션·사운드 종료 및 정리."""
        if not self.active:
            return
        # 애니메이션 정리 – AnimationManager가 개별 애니메이션을 관리하므로 종료 요청
        self.animation_manager.stop_all_animations()

        # 파티클 제거 (이미 deleteLater 된 객체는 skip)
        for p in self.particles[:]:
            if isValid(p):
                p.deleteLater()
        self.particles.clear()

        # ProgressBar 축하 모드 해제
        if hasattr(self, "target_progress_bar") and hasattr(self.target_progress_bar, "set_celebration_mode"):
            self.target_progress_bar.set_celebration_mode(False)

        # 사운드 중지
        if self.sound:
            self.sound.stop()
        self.hide()
        self.active = False

    # ---------------------------------------------------
    # 내부 구현
    # ---------------------------------------------------
    def _play_sound(self):
        try:
            self.sound = QSoundEffect(self)
            self.sound.setSource(
                "qrc:/qt-project.org/Resources/qtlogo.wav"  # Qt 내장 데모 음원(짧음)
            )
            self.sound.setLoopCount(1)
            self.sound.setVolume(0.35)
            self.sound.play()
        except Exception:
            # 사운드 장치 문제 시 무음
            pass

    def _spawn_confetti(self):
        dark = self.theme_manager.get_current_theme() == "dark"
        # 폭죽처럼 아래에서 위로 퍼지는 효과: 중앙 하단에서 시작
        origin_x = self.width() // 2
        origin_y = self.height() - 10

        for i in range(50):  # particle count↑ (±10 런타임 조정 가능)
            particle = ConfettiParticle(self, dark)
            particle.move(origin_x, origin_y)
            particle.show()
            self.particles.append(particle)

            # --------------------------------------------
            # 위치 애니메이션: 상승 0.4 s + 낙하 1.1 s
            # --------------------------------------------
            angle_deg = random.uniform(-85, 85)
            distance = random.randint(int(self.height() * 0.6), int(self.height() * 0.9))

            # Apex 좌표
            apex_x = origin_x + int(distance * 0.8 * (angle_deg / 100))  # 더 넓게 퍼짐
            apex_y = origin_y - distance

            # Landing 좌표 – apex에서 80 % 만큼 낙하
            land_x = apex_x + int((angle_deg / 100) * distance * 0.25)  # 더 퍼짐
            land_y = apex_y + int(distance * 0.8)

            # 상승 애니메이션
            up = QPropertyAnimation(particle, b"pos", self)
            up.setDuration(400)  # 0.4 s (더 느린 상승)
            up.setStartValue(QPoint(origin_x, origin_y))
            up.setEndValue(QPoint(apex_x, apex_y))
            up.setEasingCurve(QEasingCurve.OutCubic)

            # 낙하 애니메이션
            down = QPropertyAnimation(particle, b"pos", self)
            down.setDuration(1100)  # 1.1 s (총 1.5)
            down.setStartValue(QPoint(apex_x, apex_y))
            down.setEndValue(QPoint(land_x, land_y))
            down.setEasingCurve(QEasingCurve.InQuad)

            # 위치 시퀀스 그룹
            seq_pos = QSequentialAnimationGroup(self)
            seq_pos.addAnimation(up)
            seq_pos.addAnimation(down)

            # --------------------------------------------
            # 투명도 애니메이션: 0.4 s 대기 후 1.1 s fade
            # --------------------------------------------
            opacity_effect = QGraphicsOpacityEffect()
            particle.setGraphicsEffect(opacity_effect)

            pause = QPauseAnimation(400, self)
            fade = QPropertyAnimation(opacity_effect, b"opacity", self)
            fade.setDuration(1100)
            fade.setStartValue(1.0)
            fade.setEndValue(0.0)

            seq_opacity = QSequentialAnimationGroup(self)
            seq_opacity.addAnimation(pause)
            seq_opacity.addAnimation(fade)

            # --------------------------------------------
            # 병렬 실행 그룹 (pos + opacity)
            # --------------------------------------------
            group = QParallelAnimationGroup(self)
            group.addAnimation(seq_pos)
            group.addAnimation(seq_opacity)

            # 종료 처리
            def _on_group_finished(p=particle, g=group):
                if isValid(p):
                    p.hide()
                    p.deleteLater()
                if p in self.particles:
                    self.particles.remove(p)
                if g in self.animation_manager.active_animations:
                    self.animation_manager.active_animations.remove(g)

            group.finished.connect(_on_group_finished)

            self.animation_manager.active_animations.append(group)
            group.start()

    def _morph_progress_bar(self, progress_bar):
        # 컬러 변경 – 골드 그라디언트 단순화(고정 색으로 대체)
        gold_color = "#FFD700" if self.theme_manager.get_current_theme() == "light" else "#FFA000"
        progress_bar.setStyleSheet(
            f"QProgressBar::chunk {{ background-color: {gold_color}; border-radius: 4px; }}"
        )

        # 살짝 팽창 애니메이션(높이 +4px)
        original_geo = progress_bar.geometry()
        expanded_geo = original_geo.adjusted(0, -2, 0, 2)
        anim = QPropertyAnimation(progress_bar, b"geometry", self)
        anim.setDuration(300)
        anim.setStartValue(original_geo)
        anim.setKeyValueAt(0.5, expanded_geo)
        anim.setEndValue(original_geo)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        self.animation_manager.active_animations.append(anim)
        anim.start()

    # ---------------------------------------------------
    # Event filter & key handling
    # ---------------------------------------------------
    def eventFilter(self, obj, event):
        # 부모 윈도 리사이즈 시 오버레이 크기 동기화
        from PySide6.QtCore import QEvent

        if obj == self.parent_window and event.type() == QEvent.Resize:
            self.resize(self.parent_window.size())
        return super().eventFilter(obj, event)

    def keyPressEvent(self, event):
        if event.key() in (Qt.Key_Escape, Qt.Key_E):
            self.stop()
            event.accept()
        else:
            super().keyPressEvent(event) 