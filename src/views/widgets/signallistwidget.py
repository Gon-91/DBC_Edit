from PySide6.QtWidgets import (
    QWidget , QDockWidget , QListWidget,QPushButton , QVBoxLayout , QTableWidget , QTableWidgetItem , QAbstractItemView,QHeaderView)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
class SignalListDock(QDockWidget):
    def __init__(self, model):
        super().__init__("Signal List")
    
    
        self.model = model

        self._init_ui()
        self._connect_model()

    def _init_ui(self):

        # 기본 DockWidget 옵션 설정
        # 닫기 버튼 비활성화
        self.setFeatures(
            QDockWidget.NoDockWidgetFeatures
        )

        # UI 구성
        container = QWidget(self)
        self.setWidget(container)
        main_layout = QVBoxLayout(container)

        #Table Widget에 메세지 리스트 표시
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels(["Name","ByteOrder","Start_Bit","Length","Factor","Offset","Unit","Min","Max","Color"])

        main_layout.addWidget(self.table)

    def _connect_model(self):

        self.model.current_message_changed.connect(self._on_signalslist)

    def _on_signalslist(self,signals):
        self.table.setRowCount(len(signals))
        self.table.setColumnCount(10)
        #self.table.setHorizontalHeaderLabels(["Name","ByteOrder","Start_Bit","Length","Factor","Offset","Unit","Min","Max","Color"])

        for row, sig in enumerate(signals):
            self.table.setItem(row, 0, QTableWidgetItem(sig.name))
            self.table.setItem(row, 1, QTableWidgetItem(sig.byte_order))
            self.table.setItem(row, 2, QTableWidgetItem(str(sig.start_bit)))
            self.table.setItem(row, 3, QTableWidgetItem(str(sig.length)))
            self.table.setItem(row, 4, QTableWidgetItem(str(sig.factor)))
            self.table.setItem(row, 5, QTableWidgetItem(str(sig.offset)))
            self.table.setItem(row, 6, QTableWidgetItem(str(sig.unit)))
            self.table.setItem(row, 7, QTableWidgetItem(str(sig.min)))
            self.table.setItem(row, 8, QTableWidgetItem(str(sig.max)))
            # Color 컬럼 (셀 색상으로 표현)
            color_item = QTableWidgetItem()
            color_item.setBackground(QColor("lightblue"))  # 예시
            self.table.setItem(row, 9, color_item)