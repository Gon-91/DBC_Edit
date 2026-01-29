"""
signal_table_model.py
뷰모델 계층: 시그널 테이블 뷰모델
"""
from PySide6.QtWidgets import QTableWidget, QTableView, QAbstractItemView, QHeaderView, QTableWidgetItem, QSizePolicy, QPushButton, QColorDialog, QComboBox, QStyledItemDelegate
from PySide6.QtGui import QColor
from PySide6.QtCore import QObject, Signal, QAbstractTableModel, QModelIndex, Qt

class SignalTableModel(QAbstractTableModel):
    """
    시그널 테이블 뷰모델. 시그널 리스트를 테이블 형태로 제공하며, 컬러 등 부가 정보도 관리합니다.
    """
    HEADERS = [
        " ", "Name", "Start", "Length", "Factor",
        "Offset", "Unit", "Min", "Max", "Order"
    ]

    def __init__(self):
        """
        SignalTableModel 생성자: 시그널 및 컬러 리스트 초기화
        """
        super().__init__()
        self._signals = []
        self._colors = []

    def set_signals(self, signals) -> None:
        """
        시그널 리스트를 교체하고, 컬러 리스트도 재설정하며 전체 뷰 갱신
        Args:
            signals (list): 새로운 시그널 리스트
        """
        self.beginResetModel()
        self._signals = signals
        self._colors = [QColor("white") for _ in signals]
        self.endResetModel()
        return

    def rowCount(self, parent=QModelIndex()) -> int:
        """
        테이블의 행 수 반환
        """
        return len(self._signals)

    def columnCount(self, parent=QModelIndex()) -> int:
        """
        테이블의 열 수 반환
        """
        return len(self.HEADERS)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        """
        테이블 헤더 데이터 반환
        """
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.HEADERS[section]

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        """
        셀의 플래그 설정
        """
        if not index.isValid():
            return Qt.NoItemFlags

        flags = Qt.ItemIsSelectable | Qt.ItemIsEnabled
        if index.column() in range(len(self.HEADERS)):
            flags |= Qt.ItemIsEditable
        return flags

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        """
        셀 데이터 반환
        """
        row, col = index.row(), index.column()
        sig = self._signals[row]

        if col == 0:
            if role == Qt.BackgroundRole:
                return self._colors[row]
            return None

        if role in (Qt.DisplayRole, Qt.EditRole):
            return [
                None,
                sig.name,
                sig.start_bit,
                sig.length,
                sig.factor,
                sig.offset,
                sig.unit,
                sig.min,
                sig.max,
                "Motorola" if sig.byte_order == "BIG_ENDIAN" else "Intel",
            ][col]

        return None

    def setData(self, index: QModelIndex, value, role: int = Qt.EditRole) -> bool:
        """
        셀 데이터 설정
        """
        if role != Qt.EditRole:
            return False

        row, col = index.row(), index.column()
        sig = self._signals[row]

        try:
            if col == 0 and isinstance(value, QColor):
                self._colors[row] = value
                self.dataChanged.emit(index, index, [Qt.BackgroundRole])
                return True

            elif col == 1: sig.name = value
            elif col == 2: sig.start_bit = int(value)
            elif col == 3: sig.length = int(value)
            elif col == 4: sig.factor = float(value)
            elif col == 5: sig.offset = float(value)
            elif col == 6: sig.unit = value
            elif col == 7: sig.min = float(value)
            elif col == 8: sig.max = float(value)
            elif col == 9:
                sig.byte_order = "BIG_ENDIAN" if value == "Motorola" else "LITTLE_ENDIAN"

            self.dataChanged.emit(index, index)
            return True

        except ValueError:
            return False

class TypeDelegate(QStyledItemDelegate):
    """
    Value Type 선택을 위한 Delegate
    """

    def createEditor(self, parent, option, index) -> QComboBox:
        """
        에디터 생성
        """
        cb = QComboBox(parent)
        cb.addItems(["Unsigned", "Signed"])
        return cb

    def setEditorData(self, editor: QComboBox, index: QModelIndex) -> None:
        """
        에디터 데이터 설정
        """
        editor.setCurrentText(index.data())

    def setModelData(self, editor: QComboBox, model: QAbstractTableModel, index: QModelIndex) -> None:
        """
        모델 데이터 설정
        """
        model.setData(index, editor.currentText())




class OrderDelegate(QStyledItemDelegate):
    """
    Byte Order 선택을 위한 Delegate
    """

    def createEditor(self, parent, option, index) -> QComboBox:
        """
        에디터 생성
        """
        cb = QComboBox(parent)
        cb.addItems(["Motorola", "Intel"])
        return cb

    def setEditorData(self, editor: QComboBox, index: QModelIndex) -> None:
        """
        에디터 데이터 설정
        """
        editor.setCurrentText(index.data())

    def setModelData(self, editor: QComboBox, model: QAbstractTableModel, index: QModelIndex) -> None:
        """
        모델 데이터 설정
        """
        model.setData(index, editor.currentText())

class ColorDelegate(QStyledItemDelegate):
    """
    색상 선택을 위한 Delegate
    """

    def createEditor(self, parent, option, index) -> QColorDialog:
        """
        에디터 생성
        """
        current = index.model().data(index, Qt.BackgroundRole)
        dlg = QColorDialog(current, parent)
        dlg.setOption(QColorDialog.DontUseNativeDialog)
        dlg.colorSelected.connect(
            lambda c, i=index: index.model().setData(i, c)
        )
        return dlg