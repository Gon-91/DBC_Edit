from PySide6.QtWidgets import QTableWidget , QTableView, QAbstractItemView, QHeaderView,QTableWidgetItem,QSizePolicy,QPushButton,QColorDialog,QComboBox,QStyledItemDelegate
from PySide6.QtGui import QColor
from PySide6.QtCore import QObject, Signal,QAbstractTableModel,QModelIndex,Qt

from models import MessageSignalModel

class SignalListModel(QAbstractTableModel):
    """
    SignalListModel
    ---------------
    - MessageSignalModel의 signal_updated 시그널을 구독하여 row별 데이터 변경을 감지.
    - QAbstractTableModel을 상속하여 리스트 뷰에 데이터 제공.
    - list_changed: 전체 모델 교체 시 외부에 알림.
    """
    list_changed = Signal()
    HEADERS = [
        " ", "Name", "Start", "Length", "Factor",
        "Offset", "Unit", "Min", "Max", "Order"
    ]

    def __init__(self):
        """
        SignalListModel 생성자
        - 내부적으로 MessageSignalModel을 참조
        """
        super().__init__()
        self._model: MessageSignalModel | None = None

    def set_model(self, model: MessageSignalModel):
        """
        MessageSignalModel을 교체하고, signal_updated 연결/해제 관리
        - 이전 모델이 있으면 signal_updated 연결 해제
        - 새 모델의 signal_updated를 _row_updated에 연결
        - begin/endResetModel로 전체 뷰 갱신
        - list_changed 시그널 emit
        """
        if self._model:
            try:
                self._model.signal_updated.disconnect(self._row_updated)
            except TypeError:
                pass
        self.beginResetModel()
        self._model = model
        self._model.signal_updated.connect(self._row_updated)
        self.endResetModel()
        self.list_changed.emit()

    def rowCount(self, parent=QModelIndex()) -> int:
        """
        현재 모델의 시그널 개수 반환
        """
        if not self._model:
            return 0
        return len(self._model.signals())

    def columnCount(self, parent=QModelIndex()) -> int:
        """
        컬럼 개수 반환
        """
        return len(self.HEADERS)

    def headerData(self, section, orientation, role):
        """
        헤더 텍스트 반환
        """
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.HEADERS[section]

    def flags(self, index):
        """
        각 셀의 플래그(편집 가능 등) 반환
        """
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def data(self, index, role=Qt.DisplayRole):
        """
        셀 데이터 반환
        """
        row, col = index.row(), index.column()
        sig = self._model.signals()[row]
        if col == 0 and role == Qt.BackgroundRole:
            return self._model.color(row)
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
                "Motorola" if sig.byte_order == "BIG_ENDIAN" else "Intel"
            ][col]

    def setData(self, index, value, role=Qt.EditRole):
        """
        셀 데이터 편집 처리
        """
        if role != Qt.EditRole:
            return False
        row, col = index.row(), index.column()
        if col == 0:
            self._model.set_color(row, value)
            self.dataChanged.emit(index, index, [Qt.BackgroundRole])
            return True
        field_map = {
            1: "name",
            2: "start_bit",
            3: "length",
            4: "factor",
            5: "offset",
            6: "unit",
            7: "min",
            8: "max",
            9: "byte_order",
        }
        if col == 9:
            value = "BIG_ENDIAN" if value == "Motorola" else "LITTLE_ENDIAN"
        if col in field_map:
            self._model.update_signal_field(row, field_map[col], value)
            return True
        return False

    def _row_updated(self, row: int):
        """
        MessageSignalModel에서 row 데이터가 변경될 때 호출되어 dataChanged 시그널 emit
        """
        self.dataChanged.emit(
            self.index(row, 0),
            self.index(row, self.columnCount() - 1),
            [Qt.BackgroundRole]
        )