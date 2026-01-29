"""
message_signal_model.py
----------------------
메시지-시그널 데이터 모델. 시그널 값 변경, 추가/삭제 시 시그널을 emit하여 ViewModel에 알린다.
"""
from models.domainmodels import Message, Signal as DomainSignal
from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QColor
from models.color_palette import pick_color

class MessageSignalModel(QObject):
    """
    MessageSignalModel
    ------------------
    - 메시지 및 시그널 데이터 관리
    - 값 변경, 추가/삭제 시 signal_updated, signal_changed 시그널 emit
    """
    signal_updated = Signal(int)  # 특정 row(시그널) 값 변경 시 emit
    signal_changed = Signal()     # 시그널 추가/삭제 등 전체 구조 변경 시 emit

    def __init__(self, message: Message):
        """
        MessageSignalModel 생성자
        :param message: 메시지 객체
        """
        super().__init__()
        self._message = message
        self._signals: list[DomainSignal] = message.signals

    def signals(self):
        """
        현재 메시지의 시그널 리스트 반환
        """
        return self._signals
    
    def color(self, row):
        """
        해당 row(시그널)의 색상(QColor)을 반환.
        """
        c = getattr(self._signals[row], "color", "")
        if not c:
            c = pick_color(row)
        return c if isinstance(c, QColor) else QColor(str(c))
    
    def set_color(self, row, color):
        """
        해당 row(시그널)의 색상 설정 및 signal_updated emit.
        """
        # Table의 BackgroundRole은 QColor를 주는 케이스가 많으니 hex로 normalize
        if isinstance(color, QColor):
            color_value = color.name()
        else:
            color_value = str(color)

        self._signals[row].color = color_value
        self.signal_updated.emit(row)

    def update_signal_field(self, row, field, value):
        """
        해당 row(시그널)의 특정 필드 값 변경 및 signal_updated emit
        """
        setattr(self._signals[row], field, value)
        self.signal_updated.emit(row)

    def add_signal(self, signal):
        """
        시그널 추가 및 signal_changed emit
        """
        # 새 시그널에 color가 없으면 팔레트 기반 기본 색상 부여
        if not getattr(signal, "color", None):
            try:
                signal.color = pick_color(len(self._signals))
            except Exception:
                pass
        self._signals.append(signal)
        self.signal_changed.emit()

    def remove_signal(self, row):
        """
        시그널 삭제 및 signal_changed emit
        """
        del self._signals[row]
        self.signal_changed.emit()