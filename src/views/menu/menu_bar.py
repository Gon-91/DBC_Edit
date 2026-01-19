from PySide6.QtWidgets import QMenuBar

from views.actions import UsecaseAction

class MenuBar(QMenuBar):
    def __init__(self, parent, usecase):
        super().__init__(parent)

        # 1. File
        file_menu = self.addMenu("File")

        #open_usecase = usecase.open_file()
        open_action = UsecaseAction("Open File", parent, usecase.get("file.open"))
        print("MenuBar init")
        file_menu.addAction(open_action)