"""
message_widget.py
View 계층: 메시지 테이블 위젯
"""
from PySide6.QtWidgets import QTableWidget, QAbstractItemView, QHeaderView, QTableWidgetItem
from PySide6.QtCore import QObject, Signal, Qt
from viewmodels.rows.messageviewdata import MessageViewData

class MessageTableWidget(QTableWidget):
    """
    메시지 리스트를 테이블로 표시하는 QTableWidget 기반 위젯. 메시지 선택 시 selectedmessage 시그널 emit.
    """
    selectedmessage = Signal(object)  # message id, name, dlc

    def __init__(self):
        super().__init__()
        self._ui()
        self._connect()

    def _ui(self) -> None:
        """
        테이블 UI 구성: 컬럼, 헤더, 스타일 등 설정
        """
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(["ID", "Name", "DLC"])
        self.setColumnWidth(0, 80)   # ID
        self.setColumnWidth(2, 60)   # DLC
        header = self.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        # 행 선택, 단일 선택, 읽기 전용, 포커스 제거 등 스타일 적용
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)
        self.setStyleSheet("""
        ExplorerDock QTableWidget::item:selected {
            background-color: #3a7afe;
            color: white;
        }
        ExplorerDock QTableWidget::item:selected:!active {
            background-color: #3a7afe;
            color: white;
        }
        """)

    def _connect(self) -> None:
        """
        시그널-슬롯 연결
        """
        self.itemSelectionChanged.connect(self._currentitem)

    def _currentitem(self) -> None:
        """
        현재 선택된 메시지 정보를 selectedmessage 시그널로 emit
        """
        row = self.currentRow()
        if row < 0:
            return

        id_item = self.item(row, 0).text()
        name_item = self.item(row, 1).text()
        dlc_item = int(self.item(row, 2).text())

        if not all([id_item, name_item, dlc_item]):
            return

        self.selectedmessage.emit(MessageViewData(id_item, name_item, dlc_item))

    def update_messagelist(self, messagelist: list[MessageViewData]) -> None:
        """
        메시지 리스트를 테이블에 업데이트
        """
        self.setRowCount(0)
        self.setRowCount(len(messagelist))

        for row, msg in enumerate(messagelist):
            self.setItem(row, 0, QTableWidgetItem(msg.id))
            self.setItem(row, 1, QTableWidgetItem(msg.name))
            self.setItem(row, 2, QTableWidgetItem(str(msg.length)))