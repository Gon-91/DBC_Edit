from PySide6.QtWidgets import QDockWidget, QTabWidget
from views.tabs.T_filetab import FileTab
from views.tabs.T_messagetab import MessageTab


class ExplorerDock(QDockWidget):
    def __init__(self,vm):
        super().__init__("Explorer")

        vm.files.connect(self._update_filelist)

        self.filetab = FileTab()
        self.messagetab = MessageTab()



        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.North)

        tabs.addTab(self.filetab, "Files")
        tabs.addTab(self.messagetab, "Messages")

        self.setWidget(tabs)

    def _update_filelist(self,filelist):

        self.filetab.update(filelist)