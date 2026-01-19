from PySide6.QtWidgets import QTableWidget , QTableView, QAbstractItemView, QHeaderView,QTableWidgetItem,QSizePolicy,QPushButton,QColorDialog,QComboBox,QStyledItemDelegate
from PySide6.QtGui import QColor
from PySide6.QtCore import QObject, Signal,QAbstractTableModel,QModelIndex,Qt


class SignalTableModel(QAbstractTableModel):

    HEADERS =   [
                    " ",
                    "Name",
                    "Start",
                    "Length",
                    "Factor",
                    "Offset",
                    "Unit",
                    "Min",
                    "Max",
                    "Order"
                ]
    
    def __init__(self, App_model_signals):
        super().__init__()
        self._signals = App_model_signals

        # 🔴 UI 전용 상태
        self._colors: list[QColor] = [QColor("white") for _ in App_model_signals]


    
    def rowCount(self, parent=QModelIndex()):
        return len(self._signals)

    def columnCount(self, parent=QModelIndex()):
        return 10
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.HEADERS[section]

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        flags = Qt.ItemIsSelectable | Qt.ItemIsEnabled
        if index.column() in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9):
            flags |= Qt.ItemIsEditable
        return flags

    def data(self, index, role=Qt.DisplayRole):
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

    def setData(self, index, value, role=Qt.EditRole):
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

class OrderDelegate(QStyledItemDelegate):

    def createEditor(self, parent, option, index):
        cb = QComboBox(parent)
        cb.addItems(["Motorola", "Intel"])
        return cb

    def setEditorData(self, editor, index):
        editor.setCurrentText(index.data())

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentText())


class ColorDelegate(QStyledItemDelegate):

    def createEditor(self, parent, option, index):
        current = index.model().data(index, Qt.BackgroundRole)
        dlg = QColorDialog(current, parent)
        dlg.setOption(QColorDialog.DontUseNativeDialog)
        dlg.colorSelected.connect(
            lambda c, i=index: index.model().setData(i, c)
        )
        return dlg
class SignalListView(QTableView):

    def __init__(self):
        super().__init__()
        #self.setModel(model)



    def _setmodel(self,model):
        self.setModel(model)

        # Delegate 설정은 View에서!
        self.setItemDelegateForColumn(0, ColorDelegate(self))
        self.setItemDelegateForColumn(9, OrderDelegate(self))

        header = self.horizontalHeader()
        # Resize 정책 먼저
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        for col in range(2, 9):
            header.setSectionResizeMode(col, QHeaderView.Fixed)

        header.setSectionResizeMode(9, QHeaderView.Fixed)

        # 그 다음 폭 설정
        self.setColumnWidth(0, 20)
        self.setColumnWidth(1, 120)  # Stretch지만 최소 기준
        self.setColumnWidth(2, 50)
        self.setColumnWidth(3, 50)
        self.setColumnWidth(4, 50)
        self.setColumnWidth(5, 50)
        self.setColumnWidth(6, 50)
        self.setColumnWidth(7, 50)
        self.setColumnWidth(8, 50)
        self.setColumnWidth(9, 80)

#        # 전체 위젯 최소 크기
        self.setMinimumSize(600, 200)
        self.setMaximumSize(1000, 20000)

#
#class SignalListWidget(QTableWidget):
#
#    changed = Signal(object)
#
#
#
#    def __init__(self):
#        super().__init__()
#
#        self._ui()
#        self._connect()
#    def _connect(self):
#
#        self.itemChanged.connect(self._datachanged)
#        #model = self.model()
#        #m
#    def _datachanged(self,item: QTableWidgetItem):
#
#        # 전체 데이터 생성 및 전달
#        # 규칙에 맞게 table 빈 셀 있으면 걸르던지 패스 등등 
#        Signals = []  #dummy
#
#        self.changed.emit(Signals)
#
#
#    def _ui(self):
#
#        self.setColumnCount(10)
#        self.setHorizontalHeaderLabels(
#                [
#                    " ",
#                    "Name",
#                    "Start",
#                    "Length",
#                    "Factor",
#                    "Offset",
#                    "Unit",
#                    "Min",
#                    "Max",
#                    "Order"])
#        
#        header = self.horizontalHeader()
#        # 컬럼별 기본 폭
#        self.setColumnWidth(0, 20)
#        self.setColumnWidth(1, 120)
#        self.setColumnWidth(2, 50)
#        self.setColumnWidth(3, 50)
#        self.setColumnWidth(4, 50)
#        self.setColumnWidth(5, 50)
#        self.setColumnWidth(6, 50)
#        self.setColumnWidth(7, 50)
#        self.setColumnWidth(8, 50)
#        self.setColumnWidth(9, 80)
#
#        # Name 컬럼만 Stretch
#        header.setSectionResizeMode(0, QHeaderView.Fixed)
#        header.setSectionResizeMode(1, QHeaderView.Stretch)
#        #header.setSectionResizeMode(2, QHeaderView.Stretch)
#        #header.setSectionResizeMode(3, QHeaderView.Stretch)
#        #header.setSectionResizeMode(4, QHeaderView.Stretch)
#        #header.setSectionResizeMode(5, QHeaderView.Stretch)
#        #header.setSectionResizeMode(6, QHeaderView.Stretch)
#        #header.setSectionResizeMode(6, QHeaderView.Stretch)
#        #header.setSectionResizeMode(7, QHeaderView.Stretch)
#        #header.setSectionResizeMode(8, QHeaderView.Stretch)
#        #header.setSectionResizeMode(9, QHeaderView.Stretch)
#
#        # 전체 위젯 최소 크기
#        self.setMinimumSize(600, 200)
#
#        # Dock 대응
#        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#
#
#    def update_signallist(self,signallist):
#        self.setRowCount(len(signallist))
#
#        for row, sig in enumerate(signallist):
#
#
#            # Color selector
#            color_item = QPushButton()
#            color_item.setStyleSheet("background-color: white;")
#            color_item.setProperty("bg_color", QColor("white"))
#
#            color_item.clicked.connect(lambda checked, b=color_item: self.choose_color(b))
#
#
#            self.setCellWidget(row, 0, color_item)
#            self.setItem(row, 1, QTableWidgetItem(sig.name))
#            self.setItem(row, 2, QTableWidgetItem(str(sig.start_bit)))
#            self.setItem(row, 3, QTableWidgetItem(str(sig.length)))
#            self.setItem(row, 4, QTableWidgetItem(str(sig.factor)))
#            self.setItem(row, 5, QTableWidgetItem(str(sig.offset)))
#            self.setItem(row, 6, QTableWidgetItem(str(sig.unit)))
#            self.setItem(row, 7, QTableWidgetItem(str(sig.min)))
#            self.setItem(row, 8, QTableWidgetItem(str(sig.max)))
#
#
#            cb_order = QComboBox()
#            cb_order.addItems(["Motorola", "Intel"])  # Motorola / Intel
#            if sig.byte_order == "BIG_ENDIAN" :
#                order = "Motorola"
#            else :
#                order = "Intel"
#            cb_order.setCurrentText(order)
#            self.setCellWidget(row, 9, cb_order)
#
#
#            #self.setItem(row, 9, QTableWidgetItem(sig.byte_order))
#
#    def choose_color(self, color_item: QPushButton):
#        color = QColorDialog.getColor(color_item.property("bg_color"),self)
#        if color.isValid():
#            color_item.setStyleSheet(f"background-color: {color.name()};")
#            color_item.setProperty("bg_color", color)