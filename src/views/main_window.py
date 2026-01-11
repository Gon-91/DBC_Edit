
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt

from controllers.interfaces import FileControllerProtocol

from views.menu.menu_bar import MenuBar
from views.widgets.filelistwidget.dock import FileListDock
class MainWindow(QMainWindow):
    def __init__(
            self,
            model,
            usecase 
        ):
        super().__init__()

        #self.file_controller = file_controller
        self.model = model
        self.usecase = usecase
        self._init_ui()


    
    def _init_ui(self):
        self.setWindowTitle("DBC Editor Pro")

        # Menu Bar
        menu_bar = MenuBar(self, self.usecase)
        self.setMenuBar(menu_bar)

        # File list widget
        self.file_list_dock = FileListDock(self.model)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.file_list_dock)
