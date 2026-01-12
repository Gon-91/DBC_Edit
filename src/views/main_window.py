
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt

from controllers.interfaces import FileControllerProtocol

from views.menu.menu_bar import MenuBar

from views.widgets.filelistwidget import FileListDock
from views.widgets.messagelistwidget import MessageListDock


from views.widgets.main_widget import MainWidget
from views.widgets.signallistwidget import SignalListDock


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

        # Message list widget
        self.message_list_dock = MessageListDock(self.model)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.message_list_dock)

        self.file_list_dock.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.message_list_dock.setAllowedAreas(Qt.LeftDockWidgetArea)

        self.tabifyDockWidget(self.file_list_dock, self.message_list_dock)


        # Center widget ( signal list and layout)

        # Signal list widget
        self.MainWidget = MainWidget(self.model)
        self.setCentralWidget(self.MainWidget)



        self.file_list_dock.raise_()
        self.setDockOptions(
            QMainWindow.DockOption.AllowTabbedDocks |
            QMainWindow.DockOption.AnimatedDocks
        )