"""
signal_list_model.py
뷰모델 계층: 시그널 리스트 뷰모델
"""
from PySide6.QtWidgets import QTableWidget, QTableView, QAbstractItemView, QHeaderView, QTableWidgetItem, QSizePolicy, QPushButton, QColorDialog, QComboBox, QStyledItemDelegate
from PySide6.QtGui import QColor
from PySide6.QtCore import QObject, Signal, QAbstractTableModel, QModelIndex, Qt
from models import MessageSignalModel
from models.domainmodels.enums import ByteOrder, ValueType

class SignalListModel(QAbstractTableModel):
    """
    시그널 리스트 뷰모델. MessageSignalModel의 signal_updated 시그널을 구독하여 row별 데이터 변경을 감지하고,
    QAbstractTableModel을 상속하여 리스트 뷰에 데이터 제공. list_changed 시그널로 전체 모델 교체 시 알림.
    """
    list_changed = Signal()
    HEADERS = [
        " ", "Name", "Start", "Length", "Factor",
        "Offset", "Unit", "Min", "Max", "Order", "Type"
    ]

    def __init__(self):
        """
        SignalListModel 생성자: 내부적으로 MessageSignalModel 참조
        """
        super().__init__()
        self._model: MessageSignalModel | None = None

    def set_model(self, model: MessageSignalModel) -> None:
        """
        MessageSignalModel을 교체하고, signal_updated 연결/해제 관리 및 전체 뷰 갱신
        Args:
            model (MessageSignalModel): 새로운 메시지/시그널 모델
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

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """
        현재 모델의 시그널 개수 반환
        Returns:
            int: 시그널 개수
        """
        if not self._model:
            return 0
        return len(self._model.signals())

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """
        컬럼 개수 반환
        Returns:
            int: 컬럼 개수
        """
        return len(self.HEADERS)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        """
        헤더 텍스트 반환
        Args:
            section (int): 섹션 인덱스
            orientation (Qt.Orientation): 헤더 방향
            role (int): 역할
        Returns:
            Any: 헤더 텍스트
        """
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.HEADERS[section]

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        """
        각 셀의 플래그(편집 가능 등) 반환
        Args:
            index (QModelIndex): 셀 인덱스
        Returns:
            Qt.ItemFlags: 셀 플래그
        """
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        """
        셀 데이터 반환
        Args:
            index (QModelIndex): 셀 인덱스
            role (int): 역할
        Returns:
            Any: 셀 데이터
        """
        row, col = index.row(), index.column()
        sig = self._model.signals()[row]

        if col == 0 and role == Qt.BackgroundRole:
            return self._model.color(row)

        # 편집 시 delegate가 Enum을 잘 선택할 수 있도록 EditRole에 Enum(가능하면)을 제공
        if role == Qt.EditRole:
            if col == 9:
                v = getattr(sig, "byte_order", ByteOrder.BIG.value)
                return v if isinstance(v, ByteOrder) else ByteOrder(str(v))
            if col == 10:
                v = getattr(sig, "value_type", ValueType.UNSIGNED.value)
                return v if isinstance(v, ValueType) else ValueType(str(v))

        if role == Qt.DisplayRole:
            byte_order = getattr(sig, "byte_order", ByteOrder.BIG.value)
            value_type = getattr(sig, "value_type", ValueType.UNSIGNED.value)

            byte_order_token = byte_order.value if isinstance(byte_order, ByteOrder) else str(byte_order)
            value_type_token = value_type.value if isinstance(value_type, ValueType) else str(value_type)

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
                "Motorola" if byte_order_token == ByteOrder.BIG.value else "Intel",
                "Unsigned" if value_type_token == ValueType.UNSIGNED.value else "Signed",
            ][col]

    def setData(self, index: QModelIndex, value, role: int = Qt.EditRole) -> bool:
        """
        셀 데이터 편집 처리
        Args:
            index (QModelIndex): 셀 인덱스
            value (Any): 새로운 값
            role (int): 역할
        Returns:
            bool: 성공 여부
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
            10: "value_type",
        }

        # --- type normalization (Qt editor -> domain type) ---
        try:
            if col in (2, 3):
                # start_bit, length
                value = int(value)
            elif col in (4, 5, 7, 8):
                # factor, offset, min, max
                value = float(value)
            elif col == 6:
                # unit
                value = "" if value is None else str(value)
            elif col == 1:
                # name
                value = "" if value is None else str(value)
        except (TypeError, ValueError):
            return False

        if col == 9:
            # Delegate는 ByteOrder를 전달(권장). 레거시 문자열도 허용.
            try:
                if isinstance(value, ByteOrder):
                    value = value
                elif value in ("Motorola", "Intel"):
                    value = ByteOrder.BIG if value == "Motorola" else ByteOrder.LITTLE
                else:
                    value = ByteOrder(str(value))
            except Exception:
                return False

        if col == 10:
            # Delegate는 ValueType을 전달(권장). 레거시 문자열도 허용.
            try:
                if isinstance(value, ValueType):
                    value = value
                elif value in ("Unsigned", "+"):
                    value = ValueType.UNSIGNED
                elif value in ("Signed", "-"):
                    value = ValueType.SIGNED
                else:
                    value = ValueType(str(value))
            except Exception:
                return False

        if col in field_map:
            self._model.update_signal_field(row, field_map[col], value)
            return True
        return False

    def _row_updated(self, row: int) -> None:
        """
        MessageSignalModel에서 row 데이터가 변경될 때 호출되어 dataChanged 시그널 emit
        Args:
            row (int): 변경된 row 인덱스
        """
        self.dataChanged.emit(
            self.index(row, 0),
            self.index(row, self.columnCount() - 1),
            [Qt.BackgroundRole]
        )