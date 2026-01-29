"""
central_view_model.py
뷰모델 계층: 앱의 메인 뷰모델 및 하위 뷰모델 관리
"""
from PySide6.QtCore import QObject, Signal
from .signal_list_model import SignalListModel
from .signal_layout_model import SignalLayoutModel

class CentralViewModel(QObject):
    """
    앱의 메인 뷰모델로, 하위 뷰모델(SignalList/SignalLayout 등)을 관리하고
    메시지 선택 이벤트를 받아 하위 뷰모델에 데이터 전달 및 갱신을 담당합니다.
    """
    signals = Signal(object)

    def __init__(self, model):
        """
        Args:
            model: 메시지/시그널 모델 (MessageSignalModel 등)
        """
        super().__init__()
        self._model = model
        self._signallistmodel = SignalListModel()
        self._signallayoutmodel = SignalLayoutModel()
        # 메시지 선택 시 하위 뷰모델에 데이터 전달
        self._model.message_selected.connect(self._on_message_select)

    def _on_message_select(self, message_signal_model):
        """
        메시지 선택 이벤트 핸들러: 하위 뷰모델에 데이터 전달 및 갱신
        Args:
            message_signal_model: 선택된 메시지/시그널 모델
        """
        self._signallistmodel.set_model(message_signal_model)
        self._signallayoutmodel.set_model(message_signal_model)
