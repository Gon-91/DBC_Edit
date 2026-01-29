"""
file.py
유스케이스 계층: 파일 오픈 커맨드 정의
"""
from PySide6.QtWidgets import QFileDialog
from usecases.base import Usecase

class OpenFileCommand(Usecase):
    """
    DBC 파일을 오픈하는 유스케이스 커맨드 클래스입니다.
    """
    def __init__(self, file_controller):
        """
        Args:
            file_controller: 파일 관련 컨트롤러 인스턴스
        """
        self._file_controller = file_controller

    def execute(self, parent) -> None:
        """
        파일 오픈 다이얼로그를 띄워 사용자가 선택한 DBC 파일을 컨트롤러에 전달합니다.
        Args:
            parent: 다이얼로그 부모 위젯
        """
        file_path, _ = QFileDialog.getOpenFileName(
            parent,
            "Open DBC File",
            "",
            "DBC Files (*.dbc);;All Files (*)"
        )
        if not file_path:
            return
        self._file_controller.open_file(file_path)