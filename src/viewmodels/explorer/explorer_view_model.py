from PySide6.QtCore import QObject, Signal

class ExplorerViewModel(QObject):

    files = Signal(list) # 파일 관련 
    messages = Signal(list) # 메세지 관련


    def __init__(self,model):
        super().__init__()
        self._model = model

        # Model -> VM
        self._model.files_changed.connect(self._on_files_changed)
        self._model.file_selected.connect(self._on_file_select)

    # 파일리스트 변화가 있을 때
    def _on_files_changed(self,files):
        self.files.emit(files)

    # 파일을 선택 했을 때
    def _on_file_select(self,messages):

        self.messages.emit(messages)
