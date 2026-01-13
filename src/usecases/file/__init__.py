from PySide6.QtWidgets import QFileDialog
from usecases.base import Usecase

class Open(Usecase):

    def __init__(self,  file_controller):
        self._file_controller = file_controller

    def execute(self,parent):
        file_path, _ = QFileDialog.getOpenFileName(
            parent,
            "Open DBC File",
            "",
            "DBC Files (*.dbc);;All Files (*)"
        )

        if not file_path:
            return
        
        self._file_controller.open_file(file_path)

        #log 
        print("File Usecase : Open")


class Close(Usecase):

    def __init__(self,  file_controller):
        self._file_controller = file_controller

    def execute(self,parent):
        file_path, _ = QFileDialog.getOpenFileName(
            parent,
            "Open DBC File",
            "",
            "DBC Files (*.dbc);;All Files (*)"
        )

        if not file_path:
            return
        
        self._file_controller.open_file(file_path)

        #log 
        print("File Usecase : Close")