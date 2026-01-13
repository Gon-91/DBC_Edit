from PySide6.QtWidgets import QWidget, QVBoxLayout
from views.widgets.T_filelist_widget import FileListWidget

class FileTab(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        self.filelistwidget = FileListWidget
        layout.addWidget(self.filelist)
    
    def update(self,filelist):
        self.filelistwidget.update(filelist)