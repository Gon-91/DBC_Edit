"""
centeral_widget.py
View 계층: 중앙 메인 위젯 (시그널 리스트/레이아웃)
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter
from PySide6.QtCore import Qt
from .signallist_widget import SignalListView
from .signallayout_widget import SignalLayoutView

class CenteralWidget(QWidget):
    """
    중앙 메인 위젯. 시그널 리스트/레이아웃 뷰를 수평 분할로 배치하고, ViewModel/Usecase와 연결합니다.
    """
    def __init__(self, vm, usecase):
        """
        Args:
            vm: 중앙 뷰모델
            usecase: 유스케이스(업무 로직) 객체
        """
        super().__init__()
        self._viewmodel = vm
        self._uc = usecase
        self._ui()
        self._connect()

    def _ui(self) -> None:
        """
        시그널 리스트/레이아웃 뷰를 수평 분할로 배치
        """
        self.signallist_widget = SignalListView()
        self.signallayout_widget = SignalLayoutView(self._viewmodel._signallayoutmodel)
        layout = QVBoxLayout(self)
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.signallist_widget)
        splitter.addWidget(self.signallayout_widget)
        layout.addWidget(splitter)

    def _connect(self) -> None:
        """
        ViewModel과 View 연결: 모델을 각 뷰에 설정
        """
        self.signallist_widget._setmodel(self._viewmodel._signallistmodel)
        self.signallayout_widget._setmodel(self._viewmodel._signallayoutmodel)
