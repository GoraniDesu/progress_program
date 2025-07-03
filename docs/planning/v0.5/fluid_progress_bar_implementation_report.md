# 진척도 바 유동 애니메이션 구현 보고서 (v0.4.2 계획)

## 📝 **개요**

이 문서는 Progress Program v0.4.2에서 계획하고 있는 진척도 바의 유동적(Fluid) 애니메이션 구현 방안에 대해 상세히 설명합니다. 현재 진척도 값이 채워진 상태에서 물이 흐르거나 잔잔하게 숨쉬는 듯한 시각적 효과를 추가하여, 사용자에게 더욱 역동적이고 몰입감 있는 피드백을 제공하는 것을 목표로 합니다.

## 💡 **구현 목표**

- 진척도 바가 고정된 값에 머무르지 않고, 현재 진척도 값 주변에서 미세하게 움직이는 효과 구현.
- 기존의 진척도 값 변화(0% → 40%) 애니메이션과 조화롭게 동작.
- 성능에 미치는 영향을 최소화하고, 사용자 설정으로 활성화/비활성화 가능성 고려.

## 🛠️ **기술 스택 및 주요 컴포넌트**

- **PyQt5/PySide6**: UI 프레임워크
- **QPropertyAnimation**: 위젯 속성(value)을 애니메이션하는 데 사용.
- **QEasingCurve**: 애니메이션의 속도 곡선을 정의하여 자연스러운 움직임 구현.
- `src/utils/animation_manager.py`: 애니메이션 로직을 중앙 관리하는 모듈.
- `src/ui/main_window.py`: 진척도 바를 표시하고 업데이트하는 메인 UI 모듈.

## ⚙️ **구현 상세 계획**

### 1. `src/utils/animation_manager.py` 수정

`AnimationManager` 클래스에 새로운 메서드 `animate_fluid_progress`를 추가하여 유동 애니메이션의 핵심 로직을 캡슐화합니다.

- **메서드명**: `animate_fluid_progress(self, progress_bar: QProgressBar, static_value: int)`
- **동작 방식**:
    - `QPropertyAnimation`을 사용하여 `progress_bar`의 `value` 속성을 애니메이션합니다.
    - 애니메이션의 시작 값은 `static_value - epsilon` (예: `static_value - 1`), 끝 값은 `static_value + epsilon` (예: `static_value + 1`)으로 설정하여 현재 진척도 값 주변에서 미세하게 움직이도록 합니다.
    - `setLoopCount(-1)`를 사용하여 애니메이션이 무한 반복되도록 설정합니다.
    - `setDuration()`으로 애니메이션의 한 사이클(왕복) 시간을 조절합니다. (예: 1500ms = 1.5초)
    - `setEasingCurve(QEasingCurve.InOutSine)`와 같은 이징 커브를 적용하여 시작과 끝에서 부드럽게 가속/감속하여 물결치는 듯한 자연스러운 느낌을 줍니다.
    - **중요**: 이전에 실행 중이던 동일한 `QProgressBar`에 대한 `animate_fluid_progress` 애니메이션이 있다면, 새로 시작하기 전에 해당 애니메이션을 중지하여 충돌을 방지합니다.

```python
# src/utils/animation_manager.py 에 추가될 코드 예시
class AnimationManager:
    // ... existing code ...

    def animate_fluid_progress(self, progress_bar: QProgressBar, static_value: int) -> Optional[QPropertyAnimation]:
        if not self.animation_enabled:
            return None

        # 기존 유동 애니메이션 중지 로직
        for anim in self.active_animations[:]:
            if isinstance(anim, QPropertyAnimation) and anim.targetObject() == progress_bar and anim.propertyName() == b"value" and anim.loopCount() == -1:
                anim.stop()
                self.active_animations.remove(anim)

        epsilon = 1 # 미세 움직임 범위 (예: ±1%)
        start_val = max(0, static_value - epsilon)
        end_val = min(100, static_value + epsilon)

        fluid_animation = QPropertyAnimation(progress_bar, b"value")
        fluid_animation.setDuration(1500) # 1.5초 동안 왕복
        fluid_animation.setLoopCount(-1)  # 무한 반복
        fluid_animation.setEasingCurve(QEasingCurve.InOutSine) # 물결치는 듯한 효과

        fluid_animation.setStartValue(start_val)
        fluid_animation.setKeyValueAt(0.5, end_val) # 중간에서 최고점
        fluid_animation.setEndValue(start_val) # 다시 시작점으로

        self.active_animations.append(fluid_animation)
        fluid_animation.start()

        return fluid_animation
```

### 2. `src/ui/main_window.py` 수정

`MainWindow` 클래스 내에서 `animate_fluid_progress` 메서드를 적절한 시점에 호출하고 관리합니다.

- **`update_project_info` 함수 내 호출**: 
    - 프로젝트의 진척도 바가 업데이트된 후 (즉, `animation_manager.animate_progress_update`가 완료된 후), 새로운 진척도 값(`new_progress`)을 기반으로 `animation_manager.animate_fluid_progress`를 호출하여 유동 애니메이션을 시작합니다.
    - `animation_manager.animate_progress_update`의 `finished` 시그널에 유동 애니메이션 시작 로직을 연결할 수 있습니다.

- **`on_project_selected` 함수 내 관리**: 
    - 새로운 프로젝트가 선택될 때, 기존 프로젝트의 유동 애니메이션이 중지되고 새 프로젝트의 유동 애니메이션이 시작되도록 로직을 추가합니다.

- **`show_welcome_message` 또는 `closeEvent` 함수 내 중지**: 
    - 초기 화면(`show_welcome_message`)으로 돌아갈 때나, 프로그램이 종료될 때(`closeEvent`) 진행 중인 유동 애니메이션을 명시적으로 중지하여 리소스 누수를 방지합니다.

```python
# src/ui/main_window.py 에 수정될 코드 예시
class MainWindow(QMainWindow):
    // ... existing code ...

    def update_project_info(self):
        // ... existing code ...

        new_progress = int(stats['progress'])
        # 기존 업데이트 애니메이션
        update_anim = animation_manager.animate_progress_update(self.progress_bar, new_progress)

        # 유동 애니메이션 시작 (업데이트 애니메이션 완료 후)
        if update_anim:
            update_anim.finished.connect(lambda: 
                animation_manager.animate_fluid_progress(self.progress_bar, new_progress)
            )
        else: # 애니메이션 비활성화 시 즉시 유동 애니메이션 시작
            animation_manager.animate_fluid_progress(self.progress_bar, new_progress)

        // ... existing code ...

    def on_project_selected(self, item: QListWidgetItem):
        // ... existing code ...
        if project:
            # 기존 유동 애니메이션 중지 (선택된 프로젝트의 애니메이션만 남기기)
            animation_manager.stop_all_animations() # 또는 특정 progress_bar 애니메이션만 중지하는 로직 구현

            self.current_project = project
            self.update_project_info()
            self.project_widget.set_project(project)

    def show_welcome_message(self):
        // ... existing code ...
        animation_manager.stop_all_animations() # 환영 메시지 시 애니메이션 중지
        self.progress_bar.setValue(0)
        self.progress_label.setText("0%")

    def closeEvent(self, event):
        // ... existing code ...
        animation_manager.stop_all_animations() # 종료 시 애니메이션 중지
        event.accept()
```

## 🧪 **테스트 계획**

1.  **애니메이션 활성화/비활성화**: 설정에 따라 유동 애니메이션이 켜지고 꺼지는지 확인.
2.  **진척도 값 변화**: 진척도 값이 변경될 때, 부드럽게 목표 값에 도달한 후 유동 애니메이션이 시작되는지 확인.
3.  **유동성 확인**: 애니메이션이 실행되는 동안 진척도 바가 미세하게 자연스럽게 움직이는지 확인.
4.  **프로젝트 전환**: 다른 프로젝트를 선택했을 때, 이전 프로젝트의 애니메이션은 멈추고 새 프로젝트의 애니메이션이 올바르게 시작되는지 확인.
5.  **성능 영향**: 애니메이션 실행 중 CPU/메모리 사용량이 과도하게 증가하지 않는지 모니터링.

## ⚠️ **고려사항 및 잠재적 문제점**

-   **성능**: `QPropertyAnimation`이 백그라운드에서 계속 실행되므로, 너무 많은 위젯에 동시에 적용하거나 애니메이션 지속 시간을 너무 짧게 설정하면 성능 저하가 발생할 수 있습니다.
-   **리소스 관리**: 애니메이션이 종료되거나 더 이상 필요 없을 때 명시적으로 중지하고 `active_animations` 리스트에서 제거하여 메모리 누수를 방지해야 합니다.
-   **미세 조정**: `epsilon` 값, `setDuration`, `QEasingCurve` 종류에 따라 애니메이션의 '물 흐르는' 정도와 자연스러움이 달라지므로, 여러 번 테스트하여 최적의 값을 찾아야 합니다.

## 📈 **기대 효과**

-   사용자에게 더욱 동적이고 생동감 있는 UI 경험 제공.
-   진척도 바가 단순히 정적인 숫자가 아닌, '진행 중'인 느낌을 시각적으로 강화.
-   프로그램의 시각적 완성도 및 고급스러운 느낌 증대. 