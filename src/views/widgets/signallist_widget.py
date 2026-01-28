from PySide6.QtWidgets import QTableWidget , QTableView, QAbstractItemView, QHeaderView,QTableWidgetItem,QSizePolicy,QPushButton,QColorDialog,QComboBox,QStyledItemDelegate, QStyle
from PySide6.QtGui import QColor
from PySide6.QtCore import QObject, Signal,QAbstractTableModel,QModelIndex,Qt
from PySide6.QtCore import QEvent 
from PySide6.QtWidgets import QStyledItemDelegate
from PySide6.QtGui import QColor, QPainter 
from PySide6.QtCore import Qt 
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

            color = QColorDialog.getColor(
                current,
                option.widget,
                "Select Signal Color"
            )

            if color.isValid():
                model.setData(index, color, Qt.EditRole)

            return True

        return False
    

    
class SignalListView(QTableView):

    def __init__(self):
        super().__init__()



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

