from PySide6.QtWidgets import QTableWidget ,  QAbstractItemView, QHeaderView

class MessageTableWidget(QTableWidget):
    def __init__(self): 
        super().__init__()
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["ID", "Name", "DLC"])
        self.setColumnWidth(0, 80)   # ID
        self.setColumnWidth(2, 60)   # DLC

        header = self.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)