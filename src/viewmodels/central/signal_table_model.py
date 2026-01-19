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
    
    def __init__(self):
        super().__init__()
        self._signals = []
#
        self._colors = [] 

    def set_signals(self, signals):
        self.beginResetModel()

        self._signals = signals
        self._colors = [QColor("white") for _ in signals]

        self.endResetModel()

        return 
    
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