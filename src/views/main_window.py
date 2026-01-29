"""
main_window.py
View 계층: 메인 윈도우 및 전체 UI 구성
"""
from PySide6.QtWidgets import QMainWindow
from PySide6.QtCore import Qt
from controllers.interfaces import FileControllerProtocol
from views.menu.menu_bar import MenuBar
from views.widgets.centeral_widget import CenteralWidget
from views.docks.explorer_dock import ExplorerDock
from viewmodels import CentralViewModel, ExplorerViewModel
from logger import get_logger
log = get_logger(__name__)

class MainWindow(QMainWindow):
    """
    애플리케이션의 메인 윈도우. 메뉴, 도킹, 중앙 위젯 등 전체 UI를 초기화하고 관리합니다.
    """
    def __init__(self, model, usecase):
        """
        Args:
            model: 전체 데이터 모델
            usecase: 유스케이스(업무 로직) 객체
        """
        super().__init__()
        self.model = model
        self.usecase = usecase
        self.explorer_vm = ExplorerViewModel(self.model)
        self.central_vm = CentralViewModel(self.model)
        self._init_ui()

    def _init_ui(self) -> None:
        """
        UI 구성: 메뉴바, 도킹, 중앙 위젯 등 배치
        """
        self.setWindowTitle("DBC Editor Pro")
        # 메뉴 바
        menu_bar = MenuBar(self, self.usecase)
        self.setMenuBar(menu_bar)
        # 좌측 Dock (파일 및 메시지 탐색)
        self.explorer_dock = ExplorerDock(self.explorer_vm, self.usecase)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.explorer_dock)
        # 중앙 메인 Widget (시그널 List 및 Layout View)
        self.central_widget = CenteralWidget(self.central_vm, self.usecase)
        self.setCentralWidget(self.central_widget)
