from PySide6.QtCore import QObject, Signal

class CentralViewModel(QObject):

    signals = Signal(object)

    def __init__(self,model):
        super().__init__()
        self._model = model

        # Model -> VM
        self._model.message_selected.connect(self._on_message_select)

    def _on_message_select(self,message):
        
        self.signals.emit(message.signals)