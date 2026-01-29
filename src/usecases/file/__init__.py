"""
file/__init__.py
유스케이스 계층: 파일 관련 Open/Close/Select 유스케이스 정의
"""
from PySide6.QtWidgets import QFileDialog
from usecases.base import Usecase

class Open(Usecase):
    """
    파일 오픈 유스케이스. 파일 다이얼로그를 통해 파일을 선택하고 컨트롤러에 전달합니다.
    """
    def __init__(self, file_controller):
        self._file_controller = file_controller

    def execute(self, parent) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            parent,
            "Open DBC File",
            "",
            "DBC Files (*.dbc);;All Files (*)"
        )
        if not file_path:
            return
        self._file_controller.open_file(file_path)
        # 로그 출력
        print("File Usecase : Open")

class Close(Usecase):
    """
    파일 닫기 유스케이스. 파일명을 받아 컨트롤러에 닫기 요청을 전달합니다.
    """
    def __init__(self, file_controller):
        self._file_controller = file_controller

    def execute(self, file_name: str) -> None:
        self._file_controller.close_file(file_name)
        # 로그 출력
        print("File Usecase : Close")

class Select(Usecase):
    """
    파일 선택 유스케이스. 파일명을 받아 컨트롤러에 선택 요청을 전달합니다.
    """
    def __init__(self, file_controller):
        self._file_controller = file_controller

    def execute(self, file_name: str) -> None:
        self._file_controller.select_file(file_name)
        # 로그 출력
        print("File Usecase : Select")

class Save(Usecase):
    """현재 선택된 파일을 저장하는 유스케이스."""

    def __init__(self, file_controller):
        self._file_controller = file_controller

    def execute(self) -> None:
        self._file_controller.save_file()
        print("File Usecase : Save")