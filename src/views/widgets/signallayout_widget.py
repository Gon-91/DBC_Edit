from PySide6.QtWidgets import QTableView,QWidget
from PySide6.QtCore import QRect,Qt
from PySide6.QtGui import QPainter
from models import MessageSignalModel

class SignalLayoutView(QWidget):
    """
    SignalLayoutView
    ----------------
    - SignalLayoutModel(ViewModel)의 layout_changed 시그널을 구독하여 UI를 갱신합니다.
    - paintEvent에서 메시지의 바이트/비트 그리드와 시그널 배치를 시각화합니다.
    - MVVM 패턴에서 View 역할을 담당합니다.
    """
    def __init__(self, viewmodel, parent=None):
        """
        SignalLayoutView 생성자
        - ViewModel(viewmodel)의 layout_changed 시그널을 self.update에 연결하여 데이터 변경 시 UI가 자동 갱신되도록 함
        """
        super().__init__(parent)
        self._vm = viewmodel
        if hasattr(self._vm, "layout_changed"):
            self._vm.layout_changed.connect(self.update)
        # 셀 크기 설정
        self.CELL_W = 80
        self.CELL_H = 60

    def paintEvent(self, event):
        """
        paintEvent
        - 그리드와 시그널을 화면에 그림
        - layout_changed 시그널이 emit될 때마다 호출되어 최신 데이터를 반영
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self._draw_grid(painter)
        self._draw_signals(painter)
        painter.end()

    def _draw_grid(self, painter):
        """
        _draw_grid
        - 메시지의 길이만큼 바이트/비트 그리드를 그림
        """
        model = getattr(self._vm, '_model', None)
        if not model or not hasattr(model, '_message'):
            return
        message = model._message
        if not message or not hasattr(message, 'length'):
            return
        rows = message.length
        for row in range(rows):
            for col in range(8):
                rect = QRect(
                    col * self.CELL_W,
                    row * self.CELL_H,
                    self.CELL_W,
                    self.CELL_H
                )
                painter.setPen(Qt.gray)
                painter.drawRect(rect)

    def _draw_signals(self, painter):
        """
        _draw_signals
        - ViewModel에서 시그널 정보를 받아 각 시그널을 그리드 위에 시각화
        """
        rects = self._vm.get_signal_rects()
        if not rects:
            return
        for rect, color, sig in rects:
            painter.setPen(Qt.black)
            painter.setBrush(color)
            painter.drawRect(rect)
            painter.drawText(
                rect.adjusted(4, 4, -4, -4),
                Qt.AlignCenter,
                sig.name
            )

    def _setmodel(self, viewmodel):
        """
        (선택적) 외부에서 ViewModel을 교체할 때 호출할 수 있는 메서드
        - 필요시 강제로 paintEvent를 호출하여 UI를 갱신할 수 있음
        """
        self._vm = viewmodel
        self.update()