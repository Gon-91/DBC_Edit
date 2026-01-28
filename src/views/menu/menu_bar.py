from PySide6.QtWidgets import QMenuBar

from views.actions import UsecaseAction

class MenuBar(QMenuBar):
    def __init__(self, parent, usecase):
        super().__init__(parent)

        # 1. File
        file_menu = self.addMenu("File")

        open_action = UsecaseAction("Open File", parent, usecase.get("file.open"))
        file_menu.addAction(open_action)