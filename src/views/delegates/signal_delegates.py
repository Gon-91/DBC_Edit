"""src.views.delegates.signal_delegates

View 계층에서 사용하는 Signal 관련 Delegate 모음.

- Delegate는 Qt(View) 레이어의 책임이므로 `src/views/` 아래에 둔다.
- 다만 위젯 파일(`signallist_widget.py`)이 커지는 것을 막기 위해 별도 모듈로 분리한다.
- 표시 문자열("Unsigned"/"Signed", "Motorola"/"Intel")은 UI 라벨이며,
  저장/도메인 값은 Enum(`ValueType`, `ByteOrder`)을 single source of truth로 사용한다.

주의:
- 이 모듈은 도메인 Enum import에 실패하면 에러가 발생한다(요구사항: 조용히 폴백하지 않음).
"""

from __future__ import annotations

from PySide6.QtWidgets import QColorDialog, QComboBox, QStyledItemDelegate, QStyle
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt, QEvent

from models.domainmodels.enums import ByteOrder, ValueType


class TypeDelegate(QStyledItemDelegate):
    """시그널 ValueType(부호) 선택용 콤보박스 델리게이트."""

    _ITEMS: list[tuple[str, ValueType]] = [
        ("Unsigned", ValueType.UNSIGNED),
        ("Signed", ValueType.SIGNED),
    ]

    def createEditor(self, parent, option, index):
        cb = QComboBox(parent)
        for label, enum_value in self._ITEMS:
            cb.addItem(label, enum_value)
        return cb

    def setEditorData(self, editor, index):
        current = index.data(Qt.EditRole)

        # current는 ValueType 또는 '+/-' 문자열(레거시)을 허용
        if isinstance(current, ValueType):
            enum_value = current
        else:
            enum_value = ValueType(str(current) if current is not None else ValueType.UNSIGNED.value)

        i = editor.findData(enum_value)
        editor.setCurrentIndex(i if i >= 0 else 0)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentData(), Qt.EditRole)


class OrderDelegate(QStyledItemDelegate):
    """시그널 바이트 오더(Endian) 선택용 콤보박스 델리게이트."""

    _ITEMS: list[tuple[str, ByteOrder]] = [
        ("Motorola", ByteOrder.BIG),
        ("Intel", ByteOrder.LITTLE),
    ]

    def createEditor(self, parent, option, index):
        cb = QComboBox(parent)
        for label, enum_value in self._ITEMS:
            cb.addItem(label, enum_value)
        return cb

    def setEditorData(self, editor, index):
        current = index.data(Qt.EditRole)

        # current는 ByteOrder 또는 'BIG_ENDIAN/LITTLE_ENDIAN' 문자열(레거시)을 허용
        if isinstance(current, ByteOrder):
            enum_value = current
        else:
            enum_value = ByteOrder(str(current) if current is not None else ByteOrder.BIG.value)

        i = editor.findData(enum_value)
        editor.setCurrentIndex(i if i >= 0 else 0)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentData(), Qt.EditRole)


class ColorDelegate(QStyledItemDelegate):
    """시그널 컬러 선택용 델리게이트 (컬러 셀 렌더링 및 클릭 시 컬러 다이얼로그)."""

    def paint(self, painter, option, index):
        if index.column() != 0:
            super().paint(painter, option, index)
            return

        color = index.model().data(index, Qt.BackgroundRole)
        if not isinstance(color, QColor):
            color = QColor(Qt.white)

        painter.save()

        if option.state & QStyle.State_Selected:
            painter.setPen(option.palette.highlight().color())
        else:
            painter.setPen(Qt.NoPen)

        rect = option.rect.adjusted(4, 4, -4, -4)
        painter.setBrush(color)
        painter.drawRect(rect)

        painter.restore()

    def editorEvent(self, event, model, option, index):
        if index.column() != 0:
            return False

        if event.type() == QEvent.MouseButtonRelease:
            current = model.data(index, Qt.BackgroundRole)
            if not isinstance(current, QColor):
                current = QColor(Qt.white)

            color = QColorDialog.getColor(current, option.widget, "Select Signal Color")
            if color.isValid():
                model.setData(index, color, Qt.EditRole)
            return True

        return False
