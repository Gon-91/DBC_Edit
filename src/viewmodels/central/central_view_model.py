from PySide6.QtCore import QObject, Signal

from .signal_table_model import SignalTableModel

from .signal_list_model import SignalListModel
from .signal_layout_model import SignalLayoutModel



class CentralViewModel(QObject):
    """
    CentralViewModel
    ----------------
    - 앱의 메인 모델과 하위 ViewModel(리스트/레이아웃 등)을 관리하는 중앙 ViewModel.
    - 메시지 선택 등 주요 이벤트를 받아 하위 ViewModel에 MessageSignalModel을 전달.
    - 하위 ViewModel의 시그널을 통해 View(UI) 갱신을 트리거.
    """
    signals = Signal(object)

    def __init__(self, model):
        """
        CentralViewModel 생성자
        - 메인 모델과 하위 ViewModel을 초기화
        - 메인 모델의 message_selected 시그널을 _on_message_select에 연결
        """
        super().__init__()
        self._model = model
        self._signallistmodel = SignalListModel()
        self._signallayoutmodel = SignalLayoutModel()
        # 메인 모델에서 메시지 선택 시 하위 ViewModel에 데이터 전달
        self._model.message_selected.connect(self._on_message_select)

    def _on_message_select(self, message_signal_model):
        """
        메시지 선택 이벤트 핸들러
        - 하위 ViewModel에 MessageSignalModel을 전달하여 데이터/시그널 연결을 갱신
        """
        self._signallistmodel.set_model(message_signal_model)
        self._signallayoutmodel.set_model(message_signal_model)
