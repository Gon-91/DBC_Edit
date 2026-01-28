
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt

from controllers.interfaces import FileControllerProtocol

from views.menu.menu_bar import MenuBar



from views.widgets.centeral_widget import CenteralWidget


from views.docks.explorer_dock import ExplorerDock


from viewmodels import CentralViewModel,ExplorerViewModel

from logger import get_logger
log = get_logger(__name__)

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

        # 좌측 Dock (파일 및 메시지 셀렉터)
        self.explorer_dock = ExplorerDock(self.explorer_vm,self.usecase)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.explorer_dock)

        # 중앙 메인 Widget ( 시그널 List 및 Layout View)
        self.central_widget = CenteralWidget(self.central_vm,self.usecase)
        self.setCentralWidget(self.central_widget)
