
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt

from controllers.interfaces import FileControllerProtocol

from views.menu.menu_bar import MenuBar

from views.widgets.filelistwidget import FileListDock
from views.widgets.messagelistwidget import MessageListDock


from views.widgets.T_centeral_widget import CenteralWidget
from views.widgets.signallistwidget import SignalListDock


from views.docks.explorer_dock import ExplorerDock

from viewmodels.explorer_view_model import ExplorerViewModel
from viewmodels.central_view_model import CentralViewModel


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
        self.explorer_vm = ExplorerViewModel(self.model)
        self.central_vm = CentralViewModel(self.model)
        self._init_ui()


    
    def _init_ui(self):
        self.setWindowTitle("DBC Editor Pro")

        # Menu Bar
        menu_bar = MenuBar(self, self.usecase)
        self.setMenuBar(menu_bar)

        self.explorer_dock = ExplorerDock(self.explorer_vm,self.usecase)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.explorer_dock)

        self.central_widget = CenteralWidget(self.central_vm,self.usecase)
        self.setCentralWidget(self.central_widget)





#        ###======ORG code
#
#        # File list widget
#        self.file_list_dock = FileListDock(self.model)
#        self.addDockWidget(Qt.LeftDockWidgetArea, self.file_list_dock)
#
#        # Message list widget
#        self.message_list_dock = MessageListDock(self.model)
#        self.addDockWidget(Qt.LeftDockWidgetArea, self.message_list_dock)
#
#        self.file_list_dock.setAllowedAreas(Qt.LeftDockWidgetArea)
#        self.message_list_dock.setAllowedAreas(Qt.LeftDockWidgetArea)
#
#        self.tabifyDockWidget(self.file_list_dock, self.message_list_dock)
#
#
#        # Center widget ( signal list and layout)
#
#        # Signal list widget
#        self.MainWidget = MainWidget(self.model)
#        self.setCentralWidget(self.MainWidget)
#
#
#
#        self.file_list_dock.raise_()
#        self.setDockOptions(
#            QMainWindow.DockOption.AllowTabbedDocks |
#            QMainWindow.DockOption.AnimatedDocks
#        )