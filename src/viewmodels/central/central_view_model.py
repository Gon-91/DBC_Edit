from PySide6.QtCore import QObject, Signal

from viewmodels.central.signal_table_model import SignalTableModel

class CentralViewModel(QObject):

    signals = Signal(object)

    def __init__(self,model):
        super().__init__()
        self._model = model

        self._signallist_table_model = SignalTableModel()
        # Model -> VM
        self._model.message_selected.connect(self._on_message_select)

    def _on_message_select(self,message):
        self._signallist_table_model.set_signals(message.signals)
        
        
        #self.signals.emit(message.message)