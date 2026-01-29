"""
signal_layout_model.py
뷰모델 계층: 시그널 레이아웃 뷰모델
"""
from PySide6.QtWidgets import QTableWidget, QTableView, QAbstractItemView, QHeaderView, QTableWidgetItem, QSizePolicy, QPushButton, QColorDialog, QComboBox, QStyledItemDelegate
from PySide6.QtGui import QColor
from PySide6.QtCore import QObject, Signal, QAbstractTableModel, QModelIndex, Qt, QRect
from models import MessageSignalModel

class SignalLayoutModel(QObject):
    """
    시그널 레이아웃 뷰모델. MessageSignalModel의 signal_updated, signal_changed 시그널을 구독하여
    데이터 변경 시 layout_changed 시그널을 emit하여 View(UI) 갱신을 유도합니다.
    """
    layout_changed = Signal()
    CELL_W = 80
    CELL_H = 60

    def __init__(self):
        """
        SignalLayoutModel 생성자: 내부적으로 MessageSignalModel 참조
        """
        super().__init__()
        self._model: MessageSignalModel | None = None

    def set_model(self, model: MessageSignalModel) -> None:
        """
        MessageSignalModel을 교체하고, signal_updated/signal_changed 연결/해제 관리
        Args:
            model (MessageSignalModel): 새로운 메시지/시그널 모델
        """
        if self._model:
            try:
                self._model.signal_updated.disconnect(self._on_model_changed)
                self._model.signal_changed.disconnect(self._on_model_changed)
            except TypeError:
                pass
        self._model = model
        self._model.signal_updated.connect(self._on_model_changed)
        self._model.signal_changed.connect(self._on_model_changed)
        self.layout_changed.emit()

    def _on_model_changed(self, *args, **kwargs) -> None:
        """
        MessageSignalModel에서 데이터가 변경될 때 호출되어 layout_changed 시그널을 emit합니다.
        """
        self.layout_changed.emit()

    def get_signal_rects(self) -> list[tuple[QRect, QColor, object]]:
        """
        현재 메시지의 시그널 정보를 바탕으로 시각화용 rect, color, sig 튜플 리스트 반환
        Returns:
            list[tuple[QRect, QColor, object]]: 시각화용 rect, color, sig 튜플 리스트
        """
        if not self._model:
            return []
        items = []
        message = self._model._message
        if not message:
            return items
        for row, sig in enumerate(message.signals):
            start = sig.start_bit
            length = sig.length
            color = self._get_signal_color(row)
            while length > 0:
                byte_row = start // 8
                bit_col = start % 8
                remain_in_byte = 8 - bit_col
                draw_bits = min(remain_in_byte, length)
                rect = QRect(
                    bit_col * self.CELL_W,
                    byte_row * self.CELL_H,
                    draw_bits * self.CELL_W,
                    self.CELL_H
                )
                items.append((rect, color, sig))
                start += draw_bits
                length -= draw_bits
        return items

    def _get_signal_color(self, row: int) -> QColor:
        """
        해당 row(시그널)의 색상 반환, 없으면 기본 색상 반환
        Args:
            row (int): 시그널의 row 인덱스
        Returns:
            QColor: 시그널의 색상
        """
        color = self._model.color(row)
        return color if color else QColor("#CCCCCC")


