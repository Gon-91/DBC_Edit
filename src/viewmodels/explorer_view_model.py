from PySide6.QtCore import QObject, Signal

class ExplorerViewModel(object):

    files = Signal(list)


    def __init__(self,model):
        super().__init__()
        self._model = model

        # Model -> VM
        self._model.files_changed.connect(self._on_files_changed)

    def _on_files_changed(self,files):
        self.files.emit(files)