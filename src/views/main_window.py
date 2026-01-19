
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt

from controllers.interfaces import FileControllerProtocol

from views.menu.menu_bar import MenuBar

from views.widgets.OLDfilelistwidget import FileListDock
from views.widgets.OLDmessagelistwidget import MessageListDock


from views.widgets.centeral_widget import CenteralWidget
from views.widgets.OLDsignallistwidget import SignalListDock


from views.docks.explorer_dock import ExplorerDock


from viewmodels import CentralViewModel,ExplorerViewModel


class MainWindow(QMainWindow):
    def __init__(
            self,
            model,
            usecase 
        ):
        super().__init__()
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
