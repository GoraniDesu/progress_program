from PySide6.QtWidgets import QProgressBar
from PySide6.QtCore import QTimer, QRect, Qt
from PySide6.QtGui import QPainter, QLinearGradient, QColor, QPalette, QPen, QGradient, QFont

# Utils import is placed inside to avoid heavy dependency if not used in other contexts
from utils.theme_manager import theme_manager

class FlowProgressBar(QProgressBar):
    """Apple Music iOS-style flowing pastel gradient progress bar."""

    # Segment definitions for light & dark mode per new color psychology guideline
    _segments_light = [
        (0, 20, QColor("#F0F0F0"), QColor("#BF360C")),      # light grey → deep orange
        (20, 40, QColor("#BF360C"), QColor("#E65100")),      # deep orange → orange darken
        (40, 60, QColor("#E65100"), QColor("#FF8F00")),      # orange darken → amber accent
        (60, 80, QColor("#FF8F00"), QColor("#2E7D32")),      # amber accent → green darken
        (80, 100, QColor("#2E7D32"), QColor("#1B5E20"))      # green darken → deep green
    ]

    @staticmethod
    def _rgba(hex_str: str, alpha_f: float) -> QColor:
        c = QColor(hex_str)
        c.setAlphaF(alpha_f)
        return c

    _segments_dark = [
        (0, 20, QColor("#616161"), _rgba.__func__("#42A5F5", 0.60)),
        (20, 40, _rgba.__func__("#42A5F5", 0.60), _rgba.__func__("#26C6DA", 0.65)),
        (40, 60, _rgba.__func__("#26C6DA", 0.65), _rgba.__func__("#00ACC1", 0.70)),
        (60, 80, _rgba.__func__("#00ACC1", 0.70), _rgba.__func__("#4CAF50", 0.80)),
        (80, 100, _rgba.__func__("#4CAF50", 0.80), _rgba.__func__("#43A047", 0.85))
    ]

    @staticmethod
    def _lerp_channel(a: int, b: int, t: float) -> int:
        return int(a + (b - a) * t)

    @classmethod
    def _interpolate_color(cls, c1: QColor, c2: QColor, t: float) -> QColor:
        """Linear interpolate two QColor objects (including alpha)."""
        r = cls._lerp_channel(c1.red(), c2.red(), t)
        g = cls._lerp_channel(c1.green(), c2.green(), t)
        b = cls._lerp_channel(c1.blue(), c2.blue(), t)
        a = cls._lerp_channel(c1.alpha(), c2.alpha(), t)
        return QColor(r, g, b, a)

    def _color_for_progress(self, progress: float) -> QColor:
        """Return blended QColor based on progress (0-100)."""
        segments = self._segments_dark if theme_manager.get_current_theme() == "dark" else self._segments_light
        for start, end, c_start, c_end in segments:
            if progress <= end:
                t = (progress - start) / (end - start) if end != start else 0
                return self._interpolate_color(c_start, c_end, t)
        return segments[-1][3]

    def _current_palette(self):
        """Generate three colors for gradient based on current progress with slight brightness variation."""
        base_color = self._color_for_progress(self.value())
        lighter = base_color.lighter(120)
        return [lighter, base_color, lighter]

    # Smaller value => faster flow. 0.2 ≈ 5 s cycle for full loop when timer is 16 ms.
    gradient_speed = 0.2

    show_text: bool = True

    def __init__(self, parent=None):
        super().__init__(parent)
        self._offset = 0.0  # value between 0 and 1 indicating current gradient shift
        self._celebration = False  # 100% 완료 축하 모드 여부
        # The default text is shown separately by MainWindow, so hide internal text.
        self.setTextVisible(False)

        # Timer drives continuous offset updates (approx 60 FPS)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_offset)
        self._timer.start(16)

        # Repaint when theme changes to adjust color palette automatically
        theme_manager.theme_changed.connect(lambda *_: self.update())

    # ---------------------------------------------------------------------
    # Painting Logic
    # ---------------------------------------------------------------------
    def paintEvent(self, event):  # noqa: N802 (Qt naming conventions)
        painter = QPainter(self)
        rect = self.rect()

        # Background: use the base color from current palette so that widget
        # integrates with the active theme.
        painter.fillRect(rect, self.palette().color(QPalette.Base))

        # Calculate filled portion of the bar
        if self.maximum() == self.minimum():
            progress_ratio = 0.0
        else:
            progress_ratio = (self.value() - self.minimum()) / (self.maximum() - self.minimum())
        filled_width = int(rect.width() * progress_ratio)
        filled_rect = QRect(rect.x(), rect.y(), filled_width, rect.height())

        # 축하 모드: 골드 그라디언트로 덮어쓰기 ------------------------------------------------
        if self._celebration:
            gold_start = QColor("#FFD700") if theme_manager.get_current_theme() == "light" else QColor("#FFA000")
            gold_end = QColor("#FFB400") if theme_manager.get_current_theme() == "light" else QColor("#FFCC00")
            grad = QLinearGradient(0, 0, 1, 0)
            grad.setCoordinateMode(QGradient.ObjectBoundingMode)
            grad.setColorAt(0.0, gold_start)
            grad.setColorAt(1.0, gold_end)
            painter.fillRect(filled_rect, grad)
            # 텍스트
            if self.show_text:
                pct_text = f"{self.value():.0f}%"
                painter.setFont(QFont("Segoe UI", 10, QFont.Bold))
                painter.setPen(QColor("#333") if theme_manager.get_current_theme() == "light" else QColor("#fff"))
                painter.drawText(rect, Qt.AlignCenter, pct_text)
            painter.end()
            return

        # Select color set depending on theme
        colors = self._current_palette()

        # Build flowing linear gradient using RepeatSpread for seamless wrap
        grad = QLinearGradient(self._offset, 0, 1 + self._offset, 0)
        grad.setCoordinateMode(QGradient.ObjectBoundingMode)
        grad.setSpread(QGradient.RepeatSpread)

        # Static color stops – pattern itself repeats, so offset is handled by start/stop shift
        for pos, color in zip([0.0, 0.5, 1.0], colors):
            grad.setColorAt(pos, color)

        painter.fillRect(filled_rect, grad)

        # Draw percentage text
        if self.show_text:
            pct_text = f"{self.value():.0f}%"
            painter.setFont(QFont("Segoe UI", 10, QFont.Bold))
            base_color = self._color_for_progress(self.value())
            if theme_manager.get_current_theme() == "light" and self.value() < 60:
                text_color = QColor("#424242")  # fixed dark gray for early progress
            else:
                luminance = 0.299 * base_color.redF() + 0.587 * base_color.greenF() + 0.114 * base_color.blueF()
                text_color = QColor("#000") if luminance > 0.6 else QColor("#fff")
            painter.setPen(text_color)
            painter.drawText(rect, Qt.AlignCenter, pct_text)

        # Optional: draw border (disabled pen draws nothing)
        painter.setPen(QPen(Qt.NoPen))
        painter.end()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _update_offset(self):
        """Shift gradient offset and schedule repaint."""
        # accumulate offset; modulo 1.0 keeps value in reasonable range w/o visual jump
        delta = self.gradient_speed * (16 / 1000)
        self._offset = (self._offset + delta) % 1.0  # 방향 유지 (start 좌표 변경으로 반전)
        self.update()

    def set_celebration_mode(self, enabled: bool):
        """골드 Morph 축하 모드 켜고 끄기"""
        if self._celebration == enabled:
            return
        self._celebration = enabled
        if enabled:
            self._timer.stop()  # 흐르는 그라디언트 정지
        else:
            self._offset = 0.0
            self._timer.start(16)
        self.update() 