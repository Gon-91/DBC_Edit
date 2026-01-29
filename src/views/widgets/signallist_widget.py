"""
signallist_widget.py
View 계층: 시그널 리스트/테이블 위젯 및 델리게이트
"""
from PySide6.QtWidgets import QTableWidget, QTableView, QAbstractItemView, QHeaderView, QTableWidgetItem, QSizePolicy, QPushButton, QColorDialog, QComboBox, QStyledItemDelegate, QStyle
from PySide6.QtGui import QColor, QPainter
from PySide6.QtCore import QObject, Signal, QAbstractTableModel, QModelIndex, Qt, QEvent

# 도메인 Enum을 단일 소스로 사용 (import 실패 시 조용히 동작하지 않도록 그대로 예외 발생)
from models.domainmodels.enums import ValueType, ByteOrder

# Delegate는 별도 모듈로 분리
from views.delegates.signal_delegates import ColorDelegate, OrderDelegate, TypeDelegate


class SignalListView(QTableView):
    """
    시그널 리스트/테이블 뷰
    """
    def __init__(self):
        super().__init__()

    def _setmodel(self, model):
        """
        모델 설정 및 뷰 초기화
        """
        self.setModel(model)

        # Delegate 설정은 View에서!
        self.setItemDelegateForColumn(0, ColorDelegate(self))
        self.setItemDelegateForColumn(9, OrderDelegate(self))
        self.setItemDelegateForColumn(10, TypeDelegate(self))

        header = self.horizontalHeader()
        # Resize 정책 먼저
        header.setSectionResizeMode(0, QHeaderView.Fixed)
        header.setSectionResizeMode(1, QHeaderView.Stretch)

        for col in range(2, 9):
            header.setSectionResizeMode(col, QHeaderView.Fixed)

        header.setSectionResizeMode(9, QHeaderView.Fixed)
        header.setSectionResizeMode(10, QHeaderView.Fixed)

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
        self.setColumnWidth(10, 80)

        # 전체 위젯 최소 크기
        self.setMinimumSize(600, 200)
        self.setMaximumSize(1000, 20000)

