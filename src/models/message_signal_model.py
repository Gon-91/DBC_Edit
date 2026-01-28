from models.domainmodels import Message,Signal as DomainSignal
from PySide6.QtCore import QObject,Signal
from PySide6.QtGui import QColor

class MessageSignalModel(QObject):
    """
    MessageSignalModel
    ------------------
    - 도메인 메시지 및 시그널 데이터를 관리하는 모델.
    - 시그널 값 변경, 추가/삭제 시 signal_updated, signal_changed 시그널을 emit.
    - ViewModel에서 이 시그널을 구독하여 UI 갱신에 활용.
    """
    signal_updated = Signal(int)  # 특정 row(시그널) 값 변경 시 emit
    signal_changed = Signal()     # 시그널 추가/삭제 등 전체 구조 변경 시 emit

    def __init__(self, message: Message):
        """
        MessageSignalModel 생성자
        :param message: 도메인 메시지 객체
        """
        super().__init__()
        self._message: Message = message
        self._signals: list[DomainSignal] = message.signals
        self._colors: list[QColor|None] = [None for _ in self._signals]

    def signals(self) -> list[DomainSignal]:
        """
        현재 메시지의 시그널 리스트 반환
        """
        return self._signals
    
    def color(self, row: int) -> QColor|None:
        """
        해당 row(시그널)의 색상 반환
        """
        return self._colors[row]
    
    def set_color(self, row: int, color: QColor):
        """
        해당 row(시그널)의 색상 설정 및 signal_updated emit
        """
        self._colors[row] = color
        self.signal_updated.emit(row)

    def update_signal_field(self, row: int, field: str, value):
        """
        해당 row(시그널)의 특정 필드 값 변경 및 signal_updated emit
        """
        setattr(self._signals[row], field, value)
        self.signal_updated.emit(row)

    def add_signal(self, signal: DomainSignal):
        """
        시그널 추가 및 signal_changed emit
        """
        self._signals.append(signal)
        self._colors.append(None)
        self.signal_changed.emit()

    def remove_signal(self, row: int):
        """
        시그널 삭제 및 signal_changed emit
        """
        del self._signals[row]
        del self._colors[row]
        self.signal_changed.emit()