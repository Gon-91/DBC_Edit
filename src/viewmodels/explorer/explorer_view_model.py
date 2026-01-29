"""
explorer_view_model.py
뷰모델 계층: 파일/메시지 탐색 뷰모델
"""
from PySide6.QtCore import QObject, Signal

class ExplorerViewModel(QObject):
    """
    파일/메시지 탐색 뷰모델. 파일/메시지 리스트 변경 시 시그널을 emit하여 View(UI) 갱신을 유도합니다.
    """
    files = Signal(list)  # 파일 리스트 변경 시그널
    messages = Signal(list)  # 메시지 리스트 변경 시그널

    def __init__(self, model):
        """
        Args:
            model: 파일/메시지 모델
        """
        super().__init__()
        self._model = model
        # 모델의 시그널을 뷰모델 핸들러에 연결
        self._model.files_changed.connect(self._on_files_changed)
        self._model.file_selected.connect(self._on_file_select)

    def _on_files_changed(self, files) -> None:
        """
        파일 리스트 변경 시 호출되어 files 시그널 emit
        Args:
            files (list): 변경된 파일 리스트
        """
        self.files.emit(files)

    def _on_file_select(self, messages) -> None:
        """
        파일 선택 시 호출되어 messages 시그널 emit
        Args:
            messages (list): 선택된 파일의 메시지 리스트
        """
        self.messages.emit(messages)
