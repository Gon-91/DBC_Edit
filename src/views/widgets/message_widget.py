from PySide6.QtWidgets import QTableWidget ,  QAbstractItemView, QHeaderView,QTableWidgetItem
from PySide6.QtCore import QObject, Signal
from PySide6.QtCore import Qt


from viewmodels.rows.messageviewdata import MessageViewData

class MessageTableWidget(QTableWidget):

    selectedmessage = Signal(object) #message id,name,dlc


    def __init__(self): 
        super().__init__()


        self._ui()
        self._connect()


    def _ui(self):
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["ID", "Name", "DLC"])
        self.setColumnWidth(0, 80)   # ID
        self.setColumnWidth(2, 60)   # DLC

        header = self.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        # ✔ Selection behavior
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)

        # ✔ Read only
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # ✔ Cursor / Focus 제거
        self.setFocusPolicy(Qt.NoFocus)

        # ✔ 깔끔한 강조 스타일
        self.setStyleSheet("""
        QTableWidget::item:selected {
            background-color: #3a7afe;
            color: white;
        }
        QTableWidget::item:selected:!active {
            background-color: #3a7afe;
            color: white;
        }
        """)

    def _connect(self):

        self.itemSelectionChanged.connect(self._currentitem)


    def _currentitem(self):
        row = self.currentRow()
        if row < 0:
            return

        id_item = self.item(row, 0).text()
        name_item = self.item(row, 1).text()
        dlc_item = int(self.item(row, 2).text())

        if not all([id_item, name_item, dlc_item]):
            return

        self.selectedmessage.emit(MessageViewData(id_item,name_item,dlc_item))

#        tablerow = self.selectedItems()
#
#        id = tablerow[0].text()
#        name = tablerow[1].text()
#        dlc = tablerow[2].text()
#
#        self.selectedmessage.emit(id,name,dlc)            

        #self.selectedfile.emit(self.currentItem().text())






    def update_messagelist(self,messagelist) :
        
        self.setRowCount(0)
        self.setRowCount(len(messagelist))

        for row, msg in enumerate(messagelist):
            self.setItem(row, 0, QTableWidgetItem(msg.id))
            self.setItem(row, 1, QTableWidgetItem(msg.name))
            self.setItem(row, 2, QTableWidgetItem(str(msg.length)))